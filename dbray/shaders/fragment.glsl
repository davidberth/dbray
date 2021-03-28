#version 460
in vec3 rayDestination;
out vec4 fragColor;

uniform sampler2D Texture;
uniform vec3 cameraPosition;
uniform vec3 lightPosition;
uniform int numObjects;
uniform vec2 numSamples;

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

        if (distance > 0.5 && distance < minDistance)
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

void main() {
    vec3 color;
    vec3 rayDirectionNorm = normalize(rayDestination - cameraPosition);

    float minDistance;
    int objectHitIndex;
    int closestGeometryType;
    vec3 closestd0;
    vec3 closestd1;
    vec3 closestd2;
    castRay(cameraPosition, rayDirectionNorm, false, minDistance, objectHitIndex, closestGeometryType,
            closestd0, closestd1, closestd2);

    if (objectHitIndex >= 0)
    {
        vec3 rayHit = cameraPosition + minDistance * rayDirectionNorm;
        color = vec3(texelFetch(Texture, ivec2(5, objectHitIndex), 0));
        // get the normal of the surface
        vec3 normal;

        if (closestGeometryType == 1) normal = getPlaneNormal(rayHit, closestd0, closestd1);
        if (closestGeometryType == 2) normal = getSphereNormal(rayHit, closestd0, closestd1);
        if (closestGeometryType == 3) normal = getTriangleNormal(rayHit, closestd0, closestd1, closestd2);

        vec3 lightDir = normalize(lightPosition - rayHit);

        rayHit+=lightDir * 0.01;
        // Now we cast a ray to determine if the point is in shadow
        castRay(rayHit, lightDir, true, minDistance, objectHitIndex, closestGeometryType,
                closestd0, closestd1, closestd2);

        if (objectHitIndex < 0)
        {
            color = color * max(dot(normal, lightDir), 0.05);
        }
        else
        {
            color = vec3(0.05, 0.05, 0.05);
        }
    }
    else
    {
        color = getBackColor(rayDirectionNorm);
    }
    fragColor = vec4(color, 1.0);
}