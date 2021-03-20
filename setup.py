from setuptools import find_packages, setup
setup(
    name='dbray',
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where="dbray"),
    package_dir={"": "dbray"},
)