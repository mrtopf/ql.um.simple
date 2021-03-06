from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='ql.um.simple',
      version=version,
      description="Simple account based user manager for QuantumLounge",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ql','ql.um'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'logbook',
          'ql.backend',
      ],
      entry_points={
        'paste.app_factory': [
            'main=ql.um.simple.main:app_factory',
        ],
      }
      )
