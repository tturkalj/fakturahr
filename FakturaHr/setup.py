from setuptools import setup, find_packages
from FakturaHr import __version__

setup(name='FakturaHr',
      version=__version__,
      packages=find_packages(),
      include_package_data=True,
      )

