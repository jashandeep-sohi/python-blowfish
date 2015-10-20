# vim: filetype=python3 tabstop=2 expandtab

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

import unittest
import sys
from pathlib import Path
from distutils.command.build_ext import build_ext as org_build_ext
from distutils.cmd import Command
from distutils.extension import Extension
from distutils.errors import DistutilsOptionError, DistutilsFileError

try:
  from Cython.Compiler.Main import compile_single, CompilationOptions
except ImportError:
  HAVE_CYTHON = False
else:
  HAVE_CYTHON = True


class CythonExtension(Extension):

  def __init__(
    self,
    name,
    cython_source,
    sources = None,
    output_dir = None,
    language_level = None,
    cplus = None,
    annotate = None,
    **kwargs
  ):
    self.cython_source = Path(cython_source)
    self.output_dir = Path(output_dir or "cythonized")
    self.language_level = language_level or 3
    self.cplus = cplus or False
    self.annotate = annotate or False
    
    self.output_file = self.output_dir.joinpath(
      self.cython_source.with_suffix(".cpp" if self.cplus else ".c")
    )
    
    sources = sources or []
    sources.append(str(self.output_file))
    super().__init__(name, sources, **kwargs)
    

class build_ext(org_build_ext):
  
  def check_newer(self, source, target):
    if not target.is_file():
      return True
    
    if source.stat().st_mtime > target.stat().st_mtime:
      return True
    
    return False
  
  def build_extensions(self):
    for ext in self.extensions:
      if not isinstance(ext, CythonExtension):
        continue
      self.cythonize_extension(ext)
    
    super().build_extensions()
  
  def cythonize_extension(self, ext):
    if not HAVE_CYTHON:
      if not ext.output_file.is_file():
        raise DistutilsFileError(
          "expected cythonized file %r not found" % str(ext.output_file)
        )
      else:
        return
    
    is_newer = self.check_newer(ext.cython_source, ext.output_file)
    if not self.force and not is_newer:
      return
    
    self.announce("cythonizing %r extension" % ext.name, 2)
    
    try:
      ext.output_dir.mkdir(parents=True)
    except FileExistsError:
      pass
    
    options = CompilationOptions(
      defaults = None,
      output_file = str(ext.output_file),
      language_level = ext.language_level,
      cplus = ext.cplus,
      annotate = ext.annotate,
    )
    source = str(ext.cython_source)
    output_file = str(ext.output_file)
    
    self.announce("cythonizing %r -> %r" % (source, output_file), 2)
    result = compile_single(source, options, ext.name)
  

class test(Command):
  
  command_name = "test"
  description = "run unittests using built modules/packages"
  user_options = [
    ("start-dir=", "s", "directory to start discovery"),
    ("pattern=", "p", "pattern to match test files"),
    ("test-name=", "t", "load specific tests using a Python dotted name "
                  "(e.g. pkg.module.Class.function)"),
    ("buffer", "b", "buffer stdout and stderr during tests"),
    ("catch", "c", "catch ctrl-C and display results so far"),
    ("failfast", "f", "stop on first fail or error"),
    ("exit", "e", "exit if any tests fail")
  ]
  boolean_options = ["buffer", "catch", "failfast", "exit"]
  
  def initialize_options(self):
    self.start_dir = None
    self.pattern = None
    self.test_name = None
    self.buffer = False
    self.catch = False
    self.failfast = False
    self.exit = True
  
  def finalize_options(self):    
    if self.test_name and (self.start_dir or self.pattern):
      raise DistutilsOptionError(
        "must supply either --start-dir/--pattern or --test-name, not both"
      )
    
    if self.start_dir is None:
      self.start_dir = "."
    
    if self.pattern is None:
      self.pattern = "test*.py"
  
  def run(self):    
    build = self.get_finalized_command("build")
    build.run()
    
    if self.catch:
      unittest.installHandler()
    
    sys.path.insert(0, str(Path(build.build_lib).resolve()))
    
    test_loader = unittest.defaultTestLoader
    
    if self.test_name:
      tests = test_loader.loadTestsFromName(self.test_name, None)
    else:
      tests = test_loader.discover(self.start_dir, self.pattern)
    
    test_runner = unittest.TextTestRunner(
      verbosity = self.verbose,
      failfast = self.failfast,
      buffer = self.buffer
    )
    
    test_results = test_runner.run(tests)
      
    del sys.path[0]
    
    if self.exit and not test_results.wasSuccessful():
      raise SystemExit()
  
