blowfish
========
Fast, efficient Blowfish cipher implementation in pure Python (3.4+).

.. contents:: Contents
    :local:
    :backlinks: top

Dependencies
------------
- Python 3.4+

Features
--------
- Fast (well, as fast you can possibly go using only Python 3.4+)
- Efficient; generators/iterators are used liberally to reduce memory usage
- Electronic Codebook (ECB) mode
- Cipher-Block Chaining (CBC) mode
- Propagating Cipher-Block Chaining (PCBC) mode
- Cipher Feedback (CFB) mode
- Output Feedback (OFB) mode
- Counter (CTR) mode

Installation
------------
If you just need a Blowfish cipher in your Python project, feel free to
manually copy ``blowfish.py`` to your package directory (license permitting).

distutils
#########
To install the module to your Python distribution, use the included
`distutils` script::

  $ python setup.py install
  
pip
####
Stable versions can be installed from `pypi`_ using `pip`::
  
  $ pip install blowfish
  
`pip` can also install the latest development version directly from `git`::
  
  $ pip install 'git+https://github.com/jashandeep-sohi/python-blowfish.git'
  
.. _pypi: https://pypi.python.org/pypi/blowfish

Development
-----------
Want to add a mode of operation? Speed up encryption?

Make your changes to a clone of the repository at
https://github.com/jashandeep-sohi/python-blowfish
and send me a pull request.

Bugs
----
Are you having problems? Please let me know at:
https://github.com/jashandeep-sohi/python-blowfish/issues

Usage
-----
.. warning::

    Crypto is hard and this module is young, so please don't use it in anything
    critical without understanding what you are doing and checking the source
    to make sure it is doing what you want it to.
    

ECB, CBC, PCBC, CFB & OFB
#########################

CTR
###
    
.. vim: tabstop=2 expandtab
