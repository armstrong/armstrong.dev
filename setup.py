"""
setup.py file for building armstrong components.

Nothing in this file should need to be edited, please see accompanying
package.json file if you need to adjust metadata about this package.

"""
import os
import json
from setuptools import setup, find_packages


info = json.load(open("./package.json"))


def generate_namespaces(package):
    i = package.count(".")
    while i:
        yield package.rsplit(".", i)[0]
        i -= 1
NAMESPACE_PACKAGES = list(generate_namespaces(info['name']))

if os.path.exists("MANIFEST"):
    os.unlink("MANIFEST")

setup_kwargs = {
    "author": "Bay Citizen & Texas Tribune",
    "author_email": "dev@armstrongcms.org",
    "url": "http://github.com/armstrong/%s/" % info["name"],
    "packages": find_packages(exclude=["*.tests", "*.tests.*"]),
    "namespace_packages": NAMESPACE_PACKAGES,
    "include_package_data": True,
    "zip_safe": False,
    "classifiers": [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
}

setup_kwargs.update(info)
setup(**setup_kwargs)
