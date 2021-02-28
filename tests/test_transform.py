import transform
import numpy as np


def test_add_vec():
    a = np.array([1,2,3])
    b = np.array([4,5,6])
    c = transform.addVec(a,b)
    assert np.allclose(c, np.array([5,7,9]))
