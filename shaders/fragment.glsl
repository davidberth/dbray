#version 460
in vec3 rayDirection;
out vec4 fragColor;

uniform sampler2D Texture;

uniform vec3 cameraPosition;
uniform vec3 sphereColor;

vec3 getBackColor(vec3 rayDirection) {
    return vec3(0.0, 0.2 + (rayDirection.y / 3.0), (rayDirection.y + 1.0) / 4.0 + 0.2);
}

void main() {
    vec3 color;
    color = getBackColor(rayDirection);

    for(int i = 0; i < 3; i++)
    {
        vec3 spherePosition = vec3(texelFetch(Texture, ivec2(0, i), 0).x, texelFetch(Texture, ivec2(1, i), 0).x, texelFetch(Texture, ivec2(2, i), 0).x);
        float sphereRadius = texelFetch(Texture, ivec2(3, i), 0).x;
        vec3 oc = cameraPosition - spherePosition;
        float a = dot(rayDirection, rayDirection);
        float b = 2.0 * dot(oc, rayDirection);
        float c = dot(oc, oc) - sphereRadius*sphereRadius;
        float discriminant = b*b - 4*a*c;

        if (discriminant > 0.0) color = vec3(1.0, 0.0, 0.0);
    }

    fragColor = vec4(color, 1.0);
}