#!/usr/bin/python3

import os
from setuptools import setup, find_packages, Command

def readme():
    os.system("pandoc --from=markdown --to=rst --output=README.rst README.md")
    with open('README.rst') as f:   # has to be in .rst format
        return f.read()

class CleanCommand(Command):
    """Custom clean command to tidy up the project root"""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        if os.name == "posix":
            os.system(
                'rm -vrf ./build ./dist ./*.pyc ./*tgz ./*.egg-info *.rst *.db *~'
            )

setup(name = 'remarkable-tweak',
      version = '0.1.0',
      description = 'Tweak tool for the reMarkable paper tablet.',
      long_description = readme(),
      classifiers = [
          'Development Status :: 1 - Planning',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities'
      ],
      url = 'https://github.com/morngrar/remarkable-tweak',
      author = 'Svein-Kåre Bjørnsen',
      author_email = 'sveinkare@gmail.com',
      license = 'GPL',
      include_package_data = True,
      packages = find_packages(),
      install_requires = [
          "paramiko>=2.4.0",
          "Pillow>=5.0.0",
      ],
      entry_points = {
          'gui_scripts': [
              'remarkable-tweak = remarkable_tweak.__main__:main'
          ]
      },
      cmdclass = {
          'clean': CleanCommand,
      },
      zip_safe = False
)
