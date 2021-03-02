import numpy as np

def test_get_num_spheres(testScene):
    assert testScene.getNumSpheres() == 2


def test_get_objects_matrix(testScene):
    assert np.allclose(testScene.getObjectsMatrix(),
                       np.array( [[0.0,0.0,0.0,1.0],[1.0,2.0,3.0,4.0]]))

def test_get_material_matrix(testScene):
    assert np.allclose(testScene.getMaterialsMatrix(),
                       np.array( [[1.0,0.0,0.0],[0.0,0.0,1.0]]))
