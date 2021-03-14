#version 460
in vec3 rayDestination;
out vec4 fragColor;

uniform sampler2D Texture;
uniform vec3 cameraPosition;
uniform int numObjects;

vec3 getBackColor(vec3 rayDirection) {
    float t = (-rayDirection.y + 0.5);
    return mix( vec3(0.0, 0.0, 1.0), vec3(1.0, 1.0, 1.0), t);
}

float intersectPlane(int i, vec3 rayOrigin, vec3 rayDirection)
{
    vec3 planeOrigin = vec3(texelFetch(Texture, ivec2(1, i), 0));
    vec3 planeNormal = vec3(texelFetch(Texture, ivec2(2, i), 0));
    float t = dot(planeOrigin - cameraPosition, planeNormal) / dot(rayDirection, planeNormal);
    return t;
}

float intersectSphere(int i, vec3 rayOrigin, vec3 rayDirection)
{
    vec3 spherePosition = vec3(texelFetch(Texture, ivec2(1, i), 0));
    float sphereRadius = texelFetch(Texture, ivec2(2, i), 0).x;
    vec3 oc = cameraPosition - spherePosition;
    float a = dot(rayDirection, rayDirection);
    float halfb = dot(oc, rayDirection);
    float c = dot(oc, oc) - sphereRadius*sphereRadius;
    float disc =  halfb*halfb - a*c;
    float t = -999.0;
    if (disc > 0) t =  (-halfb - sqrt(disc) ) / a;
    return t;
}

void main() {
    vec3 color;
    vec3 rayDirectionNorm = normalize(rayDestination - cameraPosition);

    float minDistance = 99999999.0;
    int objectHitIndex = -1;
    int closestGeometryType = -1;
    for(int i = 0; i < numObjects; i++)
    {
        int geomType = int(texelFetch(Texture, ivec2(0, i), 0).x);
        float distance = -1.0;
        if (geomType == 1) distance = intersectPlane(i, cameraPosition, rayDirectionNorm);
        if (geomType == 2) distance = intersectSphere(i, cameraPosition, rayDirectionNorm);

        if (distance > 1.0 && distance < minDistance)
        {
            objectHitIndex = i;
            minDistance = distance;
            closestGeometryType = geomType;
        }
    }

    if (objectHitIndex >= 0)
    {
        color = vec3(texelFetch(Texture, ivec2(5, objectHitIndex), 0));
        if (closestGeometryType == 1)
        {
            // create a checkered pattern
            vec3 hitPoint = cameraPosition + minDistance * rayDirectionNorm;
            int xysum = int(hitPoint.x) + int(hitPoint.z);
            if (xysum % 2 == 0) color = vec3(0.0, 0.0, 0.0);
        }
    }
    else
    {
        color = getBackColor(rayDirectionNorm);
    }
    fragColor = vec4(color, 1.0);
}