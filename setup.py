#!/usr/bin/env python

import os
import imp
from setuptools import setup, find_packages

dirname = os.path.dirname(__file__)
path_version = os.path.join(dirname, "glue_vaex/_version.py")
version = imp.load_source('version', path_version)


name = 'glue-vaex'
author = 'Maarten A. Breddels'
author_email = 'maartenbreddels@gmail.com'
license = 'BSD'
version = version.__version__
url = 'https://github.com/glue-viz/glue-vaex'
install_requires = ['vaex-core', 'vaex-hdf5', 'glue-core>=0.12']

with open('README.rst') as infile:
    long_description = infile.read()

entry_points = """
[glue.plugins]
glue_vaex=glue_vaex:setup
"""

setup(name=name,
      version=version,
      description='A glue plugin to use Vaex to access local and remote data',
      url=url,
      long_description=long_description,
      author=author,
      author_email=author_email,
      install_requires=install_requires,
      license=license,
      packages=find_packages(),
      zip_safe=False,
      entry_points=entry_points
      )
