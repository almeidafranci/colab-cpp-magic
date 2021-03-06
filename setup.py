from distutils.core import setup

setup(
    name='ColabCPPMagic',
    version='0.0.2',
    author='Francinaldo Almeida',
    author_email='falmeida@dca.ufrn.br',
    py_modules=['colab_cpp_magic'],
    url='htpps://github.com/almeidafranci/colab-cpp-magic',
    license='MIT',
    description='IPython extension to run C++ code in Google Colab',
    long_description=open('README.md').read(),
)
