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

.. code:: python3

    import blowfish
    cipher = blowfish.Cipher(
      b"This is the key. It must be between 8 and 56 bytes long."
    )
    
.. code:: python3

    ciphertext = cipher.encrypt_block(b"12345678")
    plaintext = cipher.decrypt_block(ciphertext)
    
    assert b"12345678" == plaintext
    
Electronic Codebook Mode (ECB)
##############################

.. code:: python3

    from os import urandom
    
    block_multiple_data = urandom(10 * 8) # data to encrypt
    
    ecb_ciphertext_iter = cipher.encrypt_ecb(block_multiple_data)
    ecb_plaintext_iter = cipher.decrypt_ecb(b"".join(ecb_ciphertext_iter))
    
    assert block_multiple_data == b"".join(ecb_plaintext_iter)
    
Cipher-Block Chaining (CBC)
###########################

.. code:: python3

    iv = urandom(8) # initialization vector
    cbc_ciphertext_iter = cipher.encrypt_cbc(block_multiple_data, iv)
    cbc_plaintext_iter = cipher.decrypt_cbc(b"".join(cbc_ciphertext_iter), iv)
    
    assert block_multiple_data == b"".join(cbc_plaintext_iter)
    
Propagating Cipher-Block Chaining Mode (PCBC)
#############################################

.. code:: python3

    pcbc_ciphertext_iter = cipher.encrypt_pcbc(block_multiple_data, iv)
    pcbc_plaintext_iter = cipher.decrypt_pcbc(
      b"".join(pcbc_ciphertext_iter),
      iv
    )
    
    assert block_multiple_data == b"".join(pcbc_plaintext_iter)

Cipher Feedback Mode (CFB)
##########################

.. code:: python3

    cfb_ciphertext_iter = cipher.encrypt_cfb(block_multiple_data, iv)
    cfb_plaintext_iter = cipher.decrypt_cfb(b"".join(cfb_ciphertext_iter), iv)
    
    assert block_multiple_data == b"".join(cfb_plaintext_iter)

Output Feedback Mode (OFB)
##########################

.. code:: python3

    ofb_ciphertext_iter = cipher.encrypt_ofb(block_multiple_data, iv)
    ofb_plaintext_iter = cipher.decrypt_ofb(b"".join(ofb_ciphertext_iter), iv)
    
    assert block_multiple_data == b"".join(ofb_plaintext_iter)

Counter Mode (CTR)
##################

.. code:: python3

    from operator import xor
    
    non_block_multiple_data = urandom(10 * 8 + 5) # data to encrypt
    
    encrypt_counter = blowfish.ctr_counter(nonce = 0xfaff1fffffffffff, f = xor)
    decrypt_counter = blowfish.ctr_counter(nonce = 0xfaff1fffffffffff, f = xor)
    
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
