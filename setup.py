# blowfish
# Copyright (C) 2015 Jashandeep Sohi <jashandeep.s.sohi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from blowfish import __version__
from distutils.core import setup

if __name__ == "__main__":
  try:
    long_desc = open("./README.rst", "r").read()
  except:
    long_desc = ""
  setup(
    name = "blowfish",
    version = __version__,
    description = "Fast, efficient Blowfish cipher implementation in pure "
                  "Python (3.4+).",
    long_description  = long_desc,
    author = "Jashandeep Sohi",
    author_email = "jashandeep.s.sohi@gmail.com",
    url = "https://github.com/jashandeep-sohi/python-blowfish",
    license = "GPLv3",
    py_modules = ["blowfish"],
    classifiers = [
     "Development Status :: 5 - Production/Stable",
     "Intended Audience :: Developers",
     "Intended Audience :: Education",
     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
     "Programming Language :: Python :: 3.4",
     "Programming Language :: Python :: 3 :: Only",
     "Topic :: Security :: Cryptography",
     "Topic :: Software Development :: Libraries :: Python Modules",  
    ],
  )
