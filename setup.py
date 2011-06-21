from distutils.core import setup
import os

# Borrowed and modified from django-registration
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

def build_package(dirpath, dirnames, filenames):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    pkg = dirpath.replace(os.path.sep, '.')
    if os.path.altsep:
        pkg = pkg.replace(os.path.altsep, '.')
    packages.append(pkg)

[build_package(dirpath, dirnames, filenames) for dirpath, dirnames, filenames
        in os.walk('armstrong/dev')]

setup(
    name='armstrong.dev',
    version='1.1.0.alpha.0',
    description='Tools needed for development and testing of Armstrong',
    author='Bay Citizen and Texas Tribune',
    author_email='dev@armstrongcms.org',
    url='http://github.com/armstrong/armstrong.dev/',
    # TODO: generate this dynamically
    packages=packages,
    namespace_packages=["armstrong", "armstrong.dev", ],
    install_requires=[
        # TODO: add this as a concrete dependency once 1.1 is out
        #'fabric',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
