#version 460
in vec3 in_position;
in vec2 in_texcoord_0;
out vec3 rayDirection;

uniform vec3 cameraPosition;

void main() {
    gl_Position = vec4(in_position, 1.0);
    rayDirection = vec3(in_texcoord_0 - 0.5, -1.0);
}