from setuptools import setup, find_packages
import sys, os

version = '0.1.04'

setup(name='angemilner',
      version=version,
      description="Manages a library of API keys using MongoDB to prevent rate limiting",
      long_description="""\
The Ghost of Ange Milner sets up a library of your API keys using MongoDB.  Then everytime you need to make an API call, she checks out the key that has been resting the longest/ has the most remaining calls before it hits the daily rate limit.""",
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: Apache Software License'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Trevor Grant',
      author_email='trevor.d.grant@gmail.com',
      url='https://github.com/rawkintrevo/API-Key-Librarian',
      license='Apache License v2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "pymongo>=2.7.2"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
