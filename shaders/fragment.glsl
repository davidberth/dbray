#version 460
in vec3 rayDirection;
out vec4 fragColor;

uniform vec3 cameraPosition;
uniform vec3 spherePosition;
uniform float sphereRadius;
uniform vec3 sphereColor;

vec3 getBackColor(vec3 rayDirection) {
    return vec3(0.0, 0.2 + (rayDirection.y / 3.0), (rayDirection.y + 1.0) / 4.0 + 0.2);
}

void main() {
    vec3 color;
    vec3 oc = cameraPosition - spherePosition;
    float a = dot(rayDirection, rayDirection);
    float b = 2.0 * dot(oc, rayDirection);
    float c = dot(oc, oc) - sphereRadius*sphereRadius;
    float discriminant = b*b - 4*a*c;

    if (discriminant > 0.0)
        color = vec3(1.0, 0.0, 0.0);
    else
        color = getBackColor(rayDirection);
    fragColor = vec4(color, 1.0);
}