from distutils.core import setup, Extension


# cmd python3 setup.py build_ext --inplace
# cmd python setup.py build_ext --inplace




c_ext = Extension("_target_module", ["_target_module.cpp","Attacker.cpp","Attribution.cpp","Attributor.cpp","Checks.cpp","Target.cpp","Geometry.cpp"], 
				extra_compile_args=['-std=c++11'], language = 'c++')

setup(
    ext_modules=[c_ext]
)
