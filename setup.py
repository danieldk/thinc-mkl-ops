#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import numpy

from pathlib import Path
from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize


PACKAGES = find_packages()
MOD_NAMES = ["thinc_mkl_ops.blas"]


def clean(path):
    for name in MOD_NAMES:
        name = name.replace(".", "/")
        for ext in [".so", ".html", ".cpp", ".c"]:
            file_path = os.path.join(path, name + ext)
            if os.path.exists(file_path):
                os.unlink(file_path)

try:
    mkl_root=Path(os.environ["MKLROOT"])
except KeyError:
    print("MKL should be installed and MKLROOT set")
    sys.exit(1)

mkl_lib=mkl_root / "lib" / "intel64"

def setup_package():
    extensions = [
        Extension(
            "thinc_mkl_ops.blas",
            ["thinc_mkl_ops/blas.pyx"],
            include_dirs=[mkl_root / "include", numpy.get_include()],
            extra_objects=[str(mkl_lib / "libmkl_intel_lp64.a"),
                str(mkl_lib / "libmkl_sequential.a"),
                str(mkl_lib / "libmkl_core.a")]
        ),
    ]

    setup(
        name="thinc_mkl_ops",
        zip_safe=True,
        packages=PACKAGES,
        package_data={"": ["*.pyx", "*.pxd"]},
        ext_modules=cythonize(extensions),
    )


if __name__ == "__main__":
    setup_package()
