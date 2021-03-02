import sphere
import numpy as np


def test_set_center():
    testSphere = sphere.Sphere([0.0,0.0,0.0], 1)
    newCenter = [1.0,1.0,1.0]
    testSphere.setCenter(newCenter)
    assert np.allclose(testSphere.center, newCenter)

def test_set_radius():
    testSphere = sphere.Sphere([0.0,0.0,0.0], 1)
    testSphere.setRadius(10.0)
    assert np.allclose(testSphere.radius, 10.0)

def test_to_vector():
    testSphere = sphere.Sphere([1.0,2.0,3.0],4.0)
    assert np.allclose(testSphere.toVector(), np.array([1.0,2.0,3.0,4.0]))

