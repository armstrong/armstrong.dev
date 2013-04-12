"""
setup.py file for building armstrong components.

Nothing in this file should need to be edited, please see accompanying
package.json file if you need to adjust metadata about this package.
"""

import json
from setuptools import setup, find_packages


info = json.load(open("./package.json"))
NAMESPACE_PACKAGES = []


def convert_to_str(d):
    """
    Recursively convert all values in a dictionary to strings

    This is required because setup() does not like unicode in
    the values it is supplied.
    """
    d2 = {}
    for k, v in d.items():
        k = str(k)
        if type(v) in [list, tuple]:
            d2[k] = [str(a) for a in v]
        elif type(v) is dict:
            d2[k] = convert_to_str(v)
        else:
            d2[k] = str(v)
    return d2

info = convert_to_str(info)


# TODO: simplify this process
def generate_namespaces(package):
    new_package = ".".join(package.split(".")[0:-1])
    if new_package.count(".") > 0:
        generate_namespaces(new_package)
    NAMESPACE_PACKAGES.append(new_package)
generate_namespaces(info["name"])


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
