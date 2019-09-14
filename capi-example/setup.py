from distutils.core import setup, Extension

hello_module = Extension('hello', sources = ['hello.c'])

setup(name='hello',
      version='0.1.0',
      description='Hello world module written in C',
      ext_modules=[hello_module])
