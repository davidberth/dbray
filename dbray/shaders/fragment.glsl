#version 460
in vec3 rayDestination;
out vec4 fragColor;

uniform sampler2D Texture;
uniform vec3 cameraPosition;
uniform vec3 lightPosition;
uniform int numObjects;
uniform vec3 cameraRight;
uniform vec3 cameraUp;
uniform vec2 samples[4];

//const int depth = 2;

vec3 getBackColor(vec3 rayDirection) {
    float t = (-rayDirection.y + 0.5);
    return mix( vec3(0.0, 0.0, 1.0), vec3(1.0, 1.0, 1.0), t);
}

float intersectPlane(int i, vec3 rayOrigin, vec3 rayDirection, out vec3 planeOrigin, out vec3 planeNormal)
{
    planeOrigin = vec3(texelFetch(Texture, ivec2(1, i), 0));
    planeNormal = vec3(texelFetch(Texture, ivec2(2, i), 0));
    float t = dot(planeOrigin - rayOrigin, planeNormal) / dot(rayDirection, planeNormal);
    return t;
}

float intersectSphere(int i, vec3 rayOrigin, vec3 rayDirection, out vec3 spherePosition, out vec3 sphereRadius)
{
    spherePosition = vec3(texelFetch(Texture, ivec2(1, i), 0));
    float sphereRadiusFloat = texelFetch(Texture, ivec2(2, i), 0).x;
    sphereRadius = vec3(sphereRadiusFloat, 0.0, 0.0);
    vec3 oc = rayOrigin - spherePosition;
    float a = dot(rayDirection, rayDirection);
    float halfb = dot(oc, rayDirection);
    float c = dot(oc, oc) - sphereRadiusFloat*sphereRadiusFloat;
    float disc =  halfb*halfb - a*c;
    float t = -999.0;
    if (disc > 0.0) t =  (-halfb - sqrt(disc) ) / a;
    return t;
}

float intersectTriangle(int i, vec3 rayOrigin, vec3 rayDirection, out vec3 v0, out vec3 v1, out vec3 v2)
{
    v0 = vec3(texelFetch(Texture, ivec2(1, i), 0));
    v1 = vec3(texelFetch(Texture, ivec2(2, i), 0));
    v2 = vec3(texelFetch(Texture, ivec2(3, i), 0));
    vec3 v0v1 = v1 - v0;
    vec3 v0v2 = v2 - v0;

    vec3 pvec = cross(rayDirection, v0v2);
    float det = dot(v0v1, pvec);

    // ray and triangle are parallel if det is close to 0
    if (abs(det) < 0.000001) return -1.0;

    float invDet = 1 / det;
    vec3 tvec = rayOrigin - v0;
    float u = dot(tvec, pvec) * invDet;
    if (u < 0 || u > 1) return -1;

    vec3 qvec = cross(tvec, v0v1);
    float v = dot(rayDirection, qvec) * invDet;
    if (v < 0 || u + v > 1) return -1.0;
    float t = dot(v0v2, qvec) * invDet;

    return t;
}

vec3 getPlaneNormal(vec3 hitPos, vec3 d0, vec3 d1)
{
    return d1;
}

vec3 getSphereNormal(vec3 hitPos, vec3 d0, vec3 d1)
{
    vec3 outVec = hitPos - d0;
    return normalize(outVec);
}

vec3 getTriangleNormal(vec3 hitPos, vec3 d0, vec3 d1, vec3 d2)
{
    return normalize(cross(d2-d0, d1-d0));
}

void castRay(in vec3 rayOrigin, in vec3 rayDirection, in bool earlyStop, out float minDistance, out int objectHitIndex,
             out int closestGeometryType, out vec3 closestd0, out vec3 closestd1, out vec3 closestd2)
{
    minDistance = 99999999.0;
    objectHitIndex = -1;
    closestGeometryType = -1;

    vec3 d0;
    vec3 d1;
    vec3 d2;
    for(int i = 0; i < numObjects; i++)
    {
        int geomType = int(texelFetch(Texture, ivec2(0, i), 0).x);
        float distance = -1.0;
        if (geomType == 1) distance = intersectPlane(i, rayOrigin, rayDirection, d0, d1);
        if (geomType == 2) distance = intersectSphere(i, rayOrigin, rayDirection, d0, d1);
        if (geomType == 3) distance = intersectTriangle(i, rayOrigin, rayDirection, d0, d1, d2);

        if (distance > 0.0001 && distance < minDistance)
        {
            objectHitIndex = i;
            minDistance = distance;
            closestGeometryType = geomType;
            closestd0 = d0;
            closestd1 = d1;
            closestd2 = d2;
            if (earlyStop) i = numObjects;
        }
    }

}

vec3 getNormal(in int closestGeometryType, in vec3 location, in vec3 d0, in vec3 d1, in vec3 d2)
{
    vec3 normal;
    if (closestGeometryType == 1) normal = getPlaneNormal(location, d0, d1);
    if (closestGeometryType == 2) normal = getSphereNormal(location, d0, d1);
    if (closestGeometryType == 3) normal = getTriangleNormal(location, d0, d1, d2);
    return normal;
}

vec3 getColor(in int objectHitIndex, in int objectType, in vec3 rayHit, in vec3 rayDirection, in vec3 d0, in vec3 d1, in vec3 d2,
            out vec3 normal)
{

    // get the normal of the surface
    normal = getNormal(objectType, rayHit, d0, d1, d2);
    vec3 lightDir = normalize(lightPosition - rayHit);
    vec3 lightReflect = reflect(lightDir, normal);
    float reflectDotEye = dot(lightReflect, rayDirection);
    int sourceObjectIndex = objectHitIndex;
    rayHit+=lightDir * 0.0001;
    // Now we cast a ray to determine if the point is in shadow
    bool inShadow = false;
    float minDistance;
    //int objectHitIndexShadow;
    //int closestGeometryTypeShadow;
    //castRay(rayHit, lightDir, true, minDistance, objectHitIndexShadow, closestGeometryTypeShadow,
    //        d0, d1, d2);

    //if (objectHitIndexShadow >= 0)
    //    inShadow = true;

    vec3 surfaceColor = vec3(texelFetch(Texture, ivec2(5, objectHitIndex), 0));
    vec3 surfLighting = vec3(texelFetch(Texture, ivec2(6, objectHitIndex), 0));
    float shininess = vec3(texelFetch(Texture, ivec2(7, objectHitIndex), 0)).x;
    vec3 specular = vec3(0.0, 0.0, 0.0);
    vec3 diffuse = vec3(0.0, 0.0, 0.0);
    vec3 ambient = surfaceColor * surfLighting.x;
    float lightDotNormal = dot(lightDir, normal);
    if (lightDotNormal > 0 && !inShadow)
    {
        diffuse = surfaceColor * surfLighting.y * lightDotNormal;
    }
    if (reflectDotEye > 0 && !inShadow)
    {
        float factor = pow(reflectDotEye, shininess);
        specular = vec3(1.0, 1.0, 1.0) * surfLighting.z * factor;
    }
    return ambient + diffuse + specular;
}

void main() {
    vec3 lcolor;
    vec3 color;


    float minDistance;
    int objectHitIndex;
    int closestGeometryType;
    vec3 closestd0;
    vec3 closestd1;
    vec3 closestd2;
    int numSamples = samples.length();

    color = vec3(0.0, 0.0, 0.0);
    for (int samp = 0; samp < numSamples; ++samp)
    {
        // cast the main ray
        vec3 rayDestinationSamp = rayDestination + samples[samp][0] * cameraRight + samples[samp][1] * cameraUp;
        vec3 rayDirectionSamp = normalize(rayDestinationSamp - cameraPosition);

        castRay(cameraPosition, rayDirectionSamp,
                false, minDistance, objectHitIndex, closestGeometryType,
        closestd0, closestd1, closestd2);

        if (objectHitIndex >= 0)
        {
            vec3 rayHit = cameraPosition + minDistance * rayDirectionSamp;
            vec3 normal;
            lcolor = getColor(objectHitIndex, closestGeometryType, rayHit, rayDirectionSamp,
                            closestd0, closestd1, closestd2, normal);
            // Cast the reflection ray

            vec3 reflectionDirection = reflect(rayDirectionSamp, normal);
            //lcolor = reflectionDirection;

            rayHit+= reflectionDirection * 0.001;

            castRay(rayHit, reflectionDirection, false, minDistance, objectHitIndex, closestGeometryType,
                    closestd0, closestd1, closestd2);
            if (objectHitIndex > 0)
            {
                vec3 rayHitRef = rayHit + minDistance * reflectionDirection;
                lcolor = lcolor + getColor(objectHitIndex, closestGeometryType, rayHitRef, reflectionDirection,
                closestd0, closestd1, closestd2, normal) / 2.0;
            }
            else
            {
                lcolor = lcolor + getBackColor(reflectionDirection);
            }

        }
        else
        {
            lcolor = getBackColor(rayDirectionSamp);
        }

        color+=lcolor;



    }

    color/=(float(numSamples));
    fragColor = vec4(color, 1.0);
}