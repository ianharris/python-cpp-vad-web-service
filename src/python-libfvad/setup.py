from distutils.core import setup, Extension

c_ext = Extension("iharrisvad", 
    ["vadmodule.cc", "libfvad_module.cc"],
    include_dirs=['/Users/i.a.harris/work/learning/install/include'],
    library_dirs=['/Users/i.a.harris/work/learning/install/lib'],
    runtime_library_dirs=['/Users/i.a.harris/work/learning/install/lib'],
    libraries=['fvad']
    )

setup(
   ext_modules=[c_ext],
)
