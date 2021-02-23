import os
import glob

from distutils.core import setup
#from distutils.extension import Extension
from setuptools.extension import Extension
from setuptools import find_packages

from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np

subdirs = [
        "phd/utils/",
        "phd/containers/",
        "phd/domain/",
        "phd/hilbert/",
        "phd/equation_state/",
        "phd/load_balance/",
        "phd/gravity",
        "phd/riemann/",
        "phd/mesh/",
        "phd/reconstruction/",
        "phd/source_term/",
        #"phd/integrate/",
]

#cpp = ("mesh", "boundary", "reconstruction", "riemann", "integrate", "gravity")
cpp = ("mesh", "domain", "reconstruction", "riemann", "gravity", "load_balance", "source_term")

extensions = []
for subdir in subdirs:
    sources = [os.path.join(subdir, "*.pyx")]
    if "mesh" in subdir:
        sources += ["phd/mesh/tess.cpp", "phd/mesh/tess3.cpp"]
    if "domain" in subdir:
        sources += ["phd/domain/particle.cpp"]
    extensions.append(
            Extension(subdir.replace("/", ".") + ".*",
                sources, include_dirs = [np.get_include()] + subdirs + ["/opt/homebrew/Cellar/cgal/5.2/include"] + \
                                            ["/opt/homebrew/Cellar/boost/1.75.0_1/include"],
                library_dirs = ["/opt/homebrew/Cellar/cgal/5.2/lib"], 
                libraries=["gmp", "m"],
                define_macros=[("CGAL_NDEBUG",1)],
            )
    )
    if any(_ in subdir for _ in cpp):
        extensions[-1].language = "c++"
setup(
        name="phd",
        version="0.1",
        author="Ricardo Fernandez",
        license="MIT",
        cmdclass={'build_ext':build_ext},
        ext_modules=cythonize(extensions),
        packages=find_packages(),
        package_data={'':['*.pxd']},
)
