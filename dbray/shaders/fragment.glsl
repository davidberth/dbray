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

const int depth = 1;
const int pad = 10;

vec3 getBackColor(vec3 rayDirection) {
    float t = (-rayDirection.y + 0.5);
    return mix( vec3(0.0, 0.0, 1.0), vec3(1.0, 1.0, 1.0), t);
}

float intersectPlane(int ty, int tx, vec3 rayOrigin, vec3 rayDirection, out vec3 planeOrigin, out vec3 planeNormal)
{
    planeOrigin = vec3(texelFetch(Texture, ivec2(ty + 1, tx), 0));
    planeNormal = vec3(texelFetch(Texture, ivec2(ty + 2, tx), 0));
    float t = dot(planeOrigin - rayOrigin, planeNormal) / dot(rayDirection, planeNormal);
    return t;
}

float intersectSphere(int ty, int tx, vec3 rayOrigin, vec3 rayDirection, out vec3 spherePosition, out vec3 sphereRadius)
{
    spherePosition = vec3(texelFetch(Texture, ivec2(ty + 1, tx), 0));
    float sphereRadiusFloat = texelFetch(Texture, ivec2(ty + 2, tx), 0).x;
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

float intersectTriangle(int ty, int tx, vec3 rayOrigin, vec3 rayDirection, out vec3 v0, out vec3 v1, out vec3 v2)
{

    v0 = vec3(texelFetch(Texture, ivec2(ty + 1, tx), 0));
    v1 = vec3(texelFetch(Texture, ivec2(ty + 2, tx), 0));
    v2 = vec3(texelFetch(Texture, ivec2(ty + 3, tx), 0));
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

int intersectAABB(int ty, int tx, vec3 rayOrigin, vec3 rayDirection, out vec3 vmin, out vec3 vmax) {
    float tmin = -999999999.0, tmax = 999999999.0;

    vmin = vec3(texelFetch(Texture, ivec2(ty + 1, tx), 0));
    vmax = vec3(texelFetch(Texture, ivec2(ty + 2, tx), 0));

    if (rayDirection.x != 0.0) {
        float tx1 = (vmin.x - rayOrigin.x)/rayDirection.x;
        float tx2 = (vmax.x - rayOrigin.x)/rayDirection.x;

        tmin = max(tmin, min(tx1, tx2));
        tmax = min(tmax, max(tx1, tx2));
    }

    if (rayDirection.y != 0.0) {
        float tx1 = (vmin.y - rayOrigin.y)/rayDirection.y;
        float tx2 = (vmax.y - rayOrigin.y)/rayDirection.y;

        tmin = max(tmin, min(tx1, tx2));
        tmax = min(tmax, max(tx1, tx2));
    }

    if (rayDirection.z != 0.0) {
        float tx1 = (vmin.z - rayOrigin.z)/rayDirection.z;
        float tx2 = (vmax.z - rayOrigin.z)/rayDirection.z;

        tmin = max(tmin, min(tx1, tx2));
        tmax = min(tmax, max(tx1, tx2));
    }

    if ((tmax >= tmin) && (max(tmin, tmax) > 0.0))
    {
        return 1;
    }
    else
    {
        return 0;
    }

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

vec3 getTriangleNormal(vec3 hitPos, int tx, int ty, vec3 d0, vec3 d1, vec3 d2)
{
    vec3 n0 = vec3(texelFetch(Texture, ivec2(ty + 4, tx), 0));
    vec3 n1 = vec3(texelFetch(Texture, ivec2(ty + 5, tx), 0));
    vec3 n2 = vec3(texelFetch(Texture, ivec2(ty + 6, tx), 0));

    vec3 v0 = d1 - d0;
    vec3 v1 = d2 - d0;
    vec3 v2 = hitPos - d0;
    float d00 = dot(v0, v0);
    float d01 = dot(v0, v1);
    float d11 = dot(v1, v1);
    float d20 = dot(v2, v0);
    float d21 = dot(v2, v1);
    float denom = d00 * d11 - d01 * d01;
    float b = (d11 * d20 - d01 * d21) / denom;
    float c = (d00 * d21 - d01 * d20) / denom;
    float a = 1.0f - b - c;

    // Interpolate the normals using barycentric coordinates.
    return a * n0 + b * n1 + c * n2;
    //return vec3(a,b,c);
}



void castRay(in vec3 rayOrigin, in vec3 rayDirection, in bool earlyStop, in float minDistanceMax, out float minDistance, out int objectHitIndex,
             out int closestGeometryType, out vec3 closestd0, out vec3 closestd1, out vec3 closestd2, out vec3 closestd3)
{
    minDistance = minDistanceMax;
    objectHitIndex = -1;
    closestGeometryType = -1;
    int bound = 0;
    vec3 d0;
    vec3 d1;
    vec3 d2;
    vec3 d3;
    int tx;
    int ty;
    for(int i = 0; i < numObjects; i++)
    {
        tx = i % 2048;
        ty = int(i / 2048) * pad;
        vec4 geomInfo = texelFetch(Texture, ivec2(ty, tx), 0);
        int level = int(geomInfo.y);
        int geomType = int(geomInfo.x);
        float distance = -1.0;
        if (geomType == 1) distance = intersectPlane(ty, tx, rayOrigin, rayDirection, d0, d1);
        if (geomType == 2) distance = intersectSphere(ty, tx, rayOrigin, rayDirection, d0, d1);
        if (geomType == 3) distance = intersectTriangle(ty, tx, rayOrigin, rayDirection, d0, d1, d2);
        if (geomType == 4) bound = intersectAABB(ty, tx, rayOrigin, rayDirection, d0, d1);

        if (bound == 0 && geomType == 4)
        {
            i+=level;
        }

        if (geomType < 4 && distance > 0.0001 && distance < minDistance)
        {
            objectHitIndex = i;
            minDistance = distance;
            closestGeometryType = geomType;
            closestd0 = d0;
            closestd1 = d1;
            closestd2 = d2;
            closestd3 = d3;
            if (earlyStop) i = numObjects;
        }
    }


}

vec3 getNormal(in int closestGeometryType, in int tx, in int ty, in vec3 location, in vec3 d0, in vec3 d1, in vec3 d2,
                in vec3 d3)
{
    vec3 normal;
    if (closestGeometryType == 1) normal = getPlaneNormal(location, d0, d1);
    if (closestGeometryType == 2) normal = getSphereNormal(location, d0, d1);
    if (closestGeometryType == 3) normal = getTriangleNormal(location, tx, ty, d0, d1, d2);

    return normal;
}

vec3 getColor(in int objectHitIndex, in int objectType, in vec3 rayHit, in vec3 rayDirection, in vec3 d0, in vec3 d1,
    in vec3 d2, in vec3 d3, out vec3 normal)
{

    // get the normal of the surface
    int tx = objectHitIndex % 2048;
    int ty = int(objectHitIndex / 2048) * pad;
    normal = getNormal(objectType, tx, ty, rayHit, d0, d1, d2, d3);
    vec3 lightDir = normalize(lightPosition - rayHit);
    vec3 lightReflect = reflect(lightDir, normal);
    float reflectDotEye = dot(lightReflect, rayDirection);
    int sourceObjectIndex = objectHitIndex;
    rayHit+=lightDir * 0.01;
    // Now we cast a ray to determine if the point is in shadow
    bool inShadow = false;
    float minDistance;
    int objectHitIndexShadow;
    int closestGeometryTypeShadow;
    float minDistanceMax = distance(rayHit, lightPosition);
    castRay(rayHit, lightDir, true, minDistanceMax, minDistance, objectHitIndexShadow, closestGeometryTypeShadow,
            d0, d1, d2, d3);

    if (objectHitIndexShadow >= 0)
        inShadow = true;


    vec3 surfaceColor = vec3(texelFetch(Texture, ivec2(ty + 7, tx), 0));

    if (objectType==1)
    {
        if (mod(int(rayHit.x / 3.0 + 1000) + int(rayHit.z / 3.0 + 1000), 2) == 0)
        {
            surfaceColor = vec3(0.1, 0.4, 0.0);
        }
    }

    vec3 surfLighting = vec3(texelFetch(Texture, ivec2(ty + 8, tx), 0));
    float shininess = vec3(texelFetch(Texture, ivec2(ty + 9, tx), 0)).x;
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
    vec3 clcolor;
    vec3 color;


    float minDistance;
    int objectHitIndex;
    int closestGeometryType;
    vec3 closestd0;
    vec3 closestd1;
    vec3 closestd2;
    vec3 closestd3;
    int numSamples = samples.length();

    color = vec3(0.0, 0.0, 0.0);
    for (int samp = 0; samp < numSamples; ++samp)
    {
        // cast the main ray
        vec3 rayDestinationSamp = rayDestination + samples[samp][0] * cameraRight + samples[samp][1] * cameraUp;
        vec3 rayDirection = normalize(rayDestinationSamp - cameraPosition);
        vec3 rayOrigin = cameraPosition;

        for (int d = 0; d < depth; ++d)
        {

            castRay(rayOrigin, rayDirection,
            false, 999999999.0, minDistance, objectHitIndex, closestGeometryType,
            closestd0, closestd1, closestd2, closestd3);

            if (objectHitIndex >= 0)
            {
                vec3 rayHit = rayOrigin + minDistance * rayDirection;
                vec3 normal;
                clcolor = getColor(objectHitIndex, closestGeometryType, rayHit, rayDirection,
                closestd0, closestd1, closestd2, closestd3, normal);

                if (d < depth - 1)
                {
                    rayDirection = reflect(rayDirection, normal);
                    rayOrigin = rayHit + rayDirection * 0.01;
                }

                if (d > 0)
                {
                    lcolor = lcolor * .85 + clcolor * .15;
                }
                else
                {
                    lcolor = clcolor;
                }

            }
            else
            {
                if (d==0)
                {
                    lcolor = getBackColor(rayDirection);
                }
                else
                {
                    lcolor = lcolor * .85 + getBackColor(rayDirection) * .15;
                    d = depth;// exit the loop
                }
            }
        }

        color+=lcolor;
    }

    color/=(float(numSamples));
    fragColor = vec4(color, 1.0);
}