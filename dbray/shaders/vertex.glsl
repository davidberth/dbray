#version 460
in vec3 in_position;
in vec2 in_texcoord_0;
out vec3 rayDestination;

uniform vec3 cameraPosition;
uniform vec3 cameraForward;
uniform vec3 cameraRight;
uniform vec3 cameraUp;

uniform float projScale;


void main() {
    gl_Position = vec4(in_position, 1.0);
    vec2 uv = vec2(projScale * (in_texcoord_0 - 0.5));
    rayDestination = cameraPosition + cameraForward + uv.x * cameraRight + uv.y * cameraUp;
}