import raytracer
import buffer
import numpy as np

def test_render(testBuffer, testRaytracer, testScene):
    testRaytracer.render(testBuffer, testScene)
    assert np.min(testBuffer.buffer[0, 0, 0]) == 0


