from setuptools import setup, find_packages

from meross_discovery.version import VERSION

setup(name='meross_discovery',
      version=VERSION,
      description='Tools for discovering meross local devices',
      url='http://server/',
      author='Katia Shatkin',
      author_email='email addy',
      license='',
      packages=find_packages(),
      install_requires=[
          'argcomplete'
      ],
      scripts=["meross"],
      classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: ?',
        'License :: ???',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
      ],
      zip_safe=False)
