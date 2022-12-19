from setuptools import setup, Extension

functions_module = Extension(
    name='scheduler',
    sources=['scheduler.cpp'],
    extra_compile_args=["-O3","-fPIC"],
    include_dirs=['/home/zhou/.local/lib/python3.7/site-packages/pybind11/include'],
)

setup(ext_modules=[functions_module])
