#version 460
in vec3 rayDirection;
out vec4 fragColor;

uniform sampler2D Texture;
uniform vec3 cameraPosition;
uniform int numSpheres;

vec3 getBackColor(vec3 rayDirection) {
    return vec3(0.0, 0.2 + (rayDirection.y / 3.0), 0.0);
}

void main() {
    vec3 color;
    //vec3 rayDirectionNorm = normalize(rayDirection);
    vec3 rayDirectionNorm = rayDirection;
    color = getBackColor(rayDirectionNorm);

    for(int i = 0; i < numSpheres; i++)
    {
        vec3 spherePosition = vec3(texelFetch(Texture, ivec2(0, i), 0));
        float sphereRadius = texelFetch(Texture, ivec2(1, i), 0).x;
        vec3 oc = cameraPosition - spherePosition;
        float a = dot(rayDirectionNorm, rayDirectionNorm);
        float halfb = dot(oc, rayDirectionNorm);
        float c = dot(oc, oc) - sphereRadius*sphereRadius;
        float discriminant = halfb*halfb - a*c;

        if (discriminant > 0.0) color = vec3(texelFetch(Texture, ivec2(2, i), 0));
    }

    fragColor = vec4(color, 1.0);
}