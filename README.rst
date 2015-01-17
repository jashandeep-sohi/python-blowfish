blowfish
========
Fast, efficient Blowfish cipher implementation in pure Python (3.4+).

.. contents::
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
- Electronic Codebook with Ciphertext Stealing (ECB-CTS) mode
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
Are you having problems? Please let me know at
https://github.com/jashandeep-sohi/python-blowfish/issues

Usage
-----
.. warning::

    Cryptography is complex, so please don't use this module in anything
    *critical* without understanding what you are doing and checking the source
    code to make sure it is doing what you want it to.
    
.. note::

    This is just a quick overview on how to use the module. For detailed
    documentation please see the `docstrings` in the module.

First create a `Cipher` object with a `key`.

.. code:: python3

    import blowfish
    
    cipher = blowfish.Cipher(b"Key must be between 4 and 56 bytes long.")
    
By default this initializes a Blowfish cipher that will interpret bytes using
big-endian byte order. This should not be a problem since most implementations
use big-endian byte order as well. However, should the need arrise to use
little-endian byte order, provide ``"little"`` as the second argument.
    
Block
#####
To encrypt or decrypt a block of data (8 bytes), use the `encrypt_block` or
`decrypt_block` methods of the `Cipher` object.

.. code:: python3

    from os import urandom
    
    block = urandom(8)
    
    ciphertext = cipher.encrypt_block(block)
    plaintext = cipher.decrypt_block(ciphertext)
    
    assert block == plaintext
    
As these methods can only operate on 8 bytes of data, they're of little
practical use. Instead, use one of the implemented modes of operation.
    
Electronic Codebook Mode (ECB)
##############################
To encrypt or decrypt data in ECB mode, use `encrypt_ecb` or `decrypt_ecb`
methods of the `Cipher` object. ECB mode can only operate on data that is a
multiple of the block-size in length.

.. code:: python3

    block_multiple_data = urandom(10 * 8) # data to encrypt
    
    ecb_ciphertext_iter = cipher.encrypt_ecb(block_multiple_data)
    ecb_plaintext_iter = cipher.decrypt_ecb(b"".join(ecb_ciphertext_iter))
    
    assert block_multiple_data == b"".join(ecb_plaintext_iter)
    
Electronic Codebook Mode with Cipher Text Stealing (ECB-CTS)
############################################################
To encrypt or decrypt data in ECB-CTS mode, use `encrypt_ecb_cts` or 
`decrypt_ecb_cts` methods of the `Cipher` object. ECB-CTS mode can operate
on data of any length as long as it is at least 8 bytes long.

.. code:: python3

    non_block_multiple_data = urandom(10 * 8 + 5) # data to encrypt
    
    ecb_cts_ciphertext_iter = cipher.encrypt_ecb_cts(non_block_multiple_data)
    ecb_cts_plaintext_iter = cipher.decrypt_ecb_cts(
      b"".join(ecb_cts_ciphertext_iter)
    )
    
    assert non_block_multiple_data == b"".join(ecb_cts_plaintext_iter)
    
Cipher-Block Chaining Mode (CBC)
################################
To encrypt or decrypt data in CBC mode, use `encrypt_cbc` or `decrypt_cbc`
methods of the `Cipher` object. CBC mode can only operate on data that is a
multiple of the block-size in length.

.. code:: python3

    iv = urandom(8) # initialization vector
    cbc_ciphertext_iter = cipher.encrypt_cbc(block_multiple_data, iv)
    cbc_plaintext_iter = cipher.decrypt_cbc(b"".join(cbc_ciphertext_iter), iv)
    
    assert block_multiple_data == b"".join(cbc_plaintext_iter)
    
Propagating Cipher-Block Chaining Mode (PCBC)
#############################################
To encrypt or decrypt data in PCBC mode, use `encrypt_pcbc` or `decrypt_pcbc`
methods of the `Cipher` object. PCBC mode can only operate on data that is a
multiple of the block-size in length.

.. code:: python3

    pcbc_ciphertext_iter = cipher.encrypt_pcbc(block_multiple_data, iv)
    pcbc_plaintext_iter = cipher.decrypt_pcbc(
      b"".join(pcbc_ciphertext_iter),
      iv
    )
    
    assert block_multiple_data == b"".join(pcbc_plaintext_iter)

Cipher Feedback Mode (CFB)
##########################
To encrypt or decrypt data in CFB mode, use `encrypt_cfb` or `decrypt_cfb`
methods of the `Cipher` object. CFB mode can operate on data of any length.

.. code:: python3

    non_block_multiple_data = urandom(10 * 8 + 5) # data to encrypt
    
    cfb_ciphertext_iter = cipher.encrypt_cfb(non_block_multiple_data, iv)
    cfb_plaintext_iter = cipher.decrypt_cfb(b"".join(cfb_ciphertext_iter), iv)
    
    assert non_block_multiple_data == b"".join(cfb_plaintext_iter)

Output Feedback Mode (OFB)
##########################
To encrypt or decrypt data in OFB mode, use `encrypt_ofb` or `decrypt_ofb`
methods of the `Cipher` object. OFB mode can operate on data of any length.

.. code:: python3
    
    ofb_ciphertext_iter = cipher.encrypt_ofb(non_block_multiple_data, iv)
    ofb_plaintext_iter = cipher.decrypt_ofb(b"".join(ofb_ciphertext_iter), iv)
    
    assert non_block_multiple_data == b"".join(ofb_plaintext_iter)

Counter Mode (CTR)
##################
To encrypt or decrypt data in CTR mode, use `encrypt_ctr` or `decrypt_ctr`
methods of the `Cipher` object. CTR mode can operate on data of any length.
Although you can use any `counter` you want, a simple increment by one counter
is secure and the most popular. So for convenience sake a simple increment by
one counter is implemented by the `blowfish.ctr_counter` function. However,
you should implement your own for optimization purposes.

.. code:: python3

    from operator import xor
    
    nonce = int.from_bytes(urandom(8), "big")
    
    encrypt_counter = blowfish.ctr_counter(nonce, f = xor)
    decrypt_counter = blowfish.ctr_counter(nonce, f = xor)
    
    ctr_ciphertext_iter = cipher.encrypt_ctr(
      non_block_multiple_data,
      encrypt_counter
    )
    ctr_plaintext_iter = cipher.decrypt_ctr(
      b"".join(ctr_ciphertext_iter),
      decrypt_counter
    )
    
    assert block_multiple_data == b"".join(ctr_plaintext_iter)

    
.. vim: tabstop=2 expandtab
