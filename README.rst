blowfish
========
This module implements the Blowfish cipher using only Python (3.4+).

Blowfish is a block cipher that can be used for symmetric-key encryption. It
has a 8-byte block size and supports a variable-length key, from 4 to 56 bytes.
It's fast, free and has been analyzed considerably. It was designed by Bruce
Schneier and more details about it can be found at
<https://www.schneier.com/blowfish.html>.

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
- Cipher-Block Chaining with Ciphertext Stealing (CBC-CTS) mode
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

Tests
-----
Tests are written using the Python `unittest` framework. All tests are in the
``test.py`` file and can be run using::
  
  $ python -m unittest test.py


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
the big-endian byte order. Should the need arrise to use the little-endian byte
order, provide ``"little"`` as the second argument.

.. code:: python3

    cipher_little = blowfish.Cipher(b"my key", byte_order = "little")
    
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

    data = urandom(10 * 8) # data to encrypt
    
    data_encrypted = b"".join(cipher.encrypt_ecb(data))
    data_decrypted = b"".join(cipher.decrypt_ecb(data_encrypted)
    
    assert data == data_decrypted
    
Electronic Codebook Mode with Cipher Text Stealing (ECB-CTS)
############################################################
To encrypt or decrypt data in ECB-CTS mode, use `encrypt_ecb_cts` or 
`decrypt_ebc_cts` methods of the `Cipher` object. ECB-CTS mode can operate
on data of any length greater than 8 bytes.

.. code:: python3

    data = urandom(10 * 8 + 5) # data to encrypt
    
    data_encrypted = b"".join(cipher.encrypt_ecb_cts(data))
    data_decrypted = b"".join(cipher.decrypt_ecb_cts(data_encrypted))
    
    assert data == data_decrypted
    
Cipher-Block Chaining Mode (CBC)
################################
To encrypt or decrypt data in CBC mode, use `encrypt_cbc` or `decrypt_cbc`
methods of the `Cipher` object. CBC mode can only operate on data that is a
multiple of the block-size in length.

.. code:: python3

    data = urandom(10 * 8) # data to encrypt
    iv = urandom(8) # initialization vector
    
    data_encrypted = b"".join(cipher.encrypt_cbc(data, iv))
    data_decrypted = b"".join(cipher.decrypt_cbc(data_encrypted, iv))
    
    assert data == data_decrypted
    
Cipher-Block Chaining with Ciphertext Stealing (CBC-CTS)
########################################################
To encrypt or decrypt data in CBC-CTS mode, use `encrypt_cbc_cts` or
`decrypt_cbc_cts` methods of the `Cipher` object. CBC-CTS mode can operate
on data of any length greater than 8 bytes.

.. code:: python3

    data = urandom(10 * 8 + 6) # data to encrypt
    iv = urandom(8) # initialization vector
    
    data_encrypted = b"".join(cipher.encrypt_cbc_cts(data, iv))
    data_decrypted = b"".join(cipher.decrypt_cbc_cts(data_encrypted, iv))
    
    assert data == data_decrypted

Propagating Cipher-Block Chaining Mode (PCBC)
#############################################
To encrypt or decrypt data in PCBC mode, use `encrypt_pcbc` or `decrypt_pcbc`
methods of the `Cipher` object. PCBC mode can only operate on data that is a
multiple of the block-size in length.

.. code:: python3

    data = urandom(10 * 8) # data to encrypt
    iv = urandom(8) # initialization vector
    
    data_encrypted = b"".join(cipher.encrypt_pcbc(data, iv))
    data_decrypted = b"".join(cipher.decrypt_pcbc(data_encrypted, iv))
    
    assert data == data_decrypted

Cipher Feedback Mode (CFB)
##########################
To encrypt or decrypt data in CFB mode, use `encrypt_cfb` or `decrypt_cfb`
methods of the `Cipher` object. CFB mode can operate on data of any length.

.. code:: python3

    data = urandom(10 * 8 + 7) # data to encrypt
    iv = urandom(8) # initialization vector
    
    data_encrypted = b"".join(cipher.encrypt_cfb(data, iv))
    data_decrypted = b"".join(cipher.decrypt_cfb(data_encrypted, iv))
    
    assert data == data_decrypted

Output Feedback Mode (OFB)
##########################
To encrypt or decrypt data in OFB mode, use `encrypt_ofb` or `decrypt_ofb`
methods of the `Cipher` object. OFB mode can operate on data of any length.

.. code:: python3
    
    data = urandom(10 * 8 + 1) # data to encrypt
    iv = urandom(8) # initialization vector
    
    data_encrypted = b"".join(cipher.encrypt_ofb(data, iv))
    data_decrypted = b"".join(cipher.decrypt_ofb(data_encrypted, iv))
    
    assert data == data_decrypted

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
    
    data = urandom(10 * 8 + 2) # data to encrypt
    
    # increment by one counters
    nonce = int.from_bytes(urandom(8), "big")
    enc_counter = blowfish.ctr_counter(nonce, f = xor)
    dec_counter = blowfish.ctr_counter(nonce, f = xor)
    
    data_encrypted = b"".join(cipher.encrypt_ctr(data, enc_counter))
    data_decrypted = b"".join(cipher.decrypt_ctr(data_encrypted, dec_counter))
    
    assert data == data_decrypted

.. vim: tabstop=2 expandtab
