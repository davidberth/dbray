import pytest
import buffer
import raytracer
import scene
import sphere
import material

@pytest.fixture(scope='module')
def testBuffer():
    return buffer.Buffer(100, 100)

@pytest.fixture(scope='module')
def testRaytracer(testBuffer):
    return raytracer.RayTracer()

@pytest.fixture(scope='module')
def testScene():
    tscene = scene.Scene()
    tscene.addObject(sphere.Sphere([0.0, 0.0, 0.0], 1.0), material.Material(1.0, 0.0, 0.0))
    tscene.addObject(sphere.Sphere([1.0, 2.0, 3.0], 4.0), material.Material(0.0, 0.0, 1.0))
    return tscene


