blowfish
========
Fast, efficient Blowfish block cipher implementation in pure Python (3.4+).

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

However, if you'd like to install the module to your Python distribution, use
the included `distutils` script::

  $ python setup.py install

Usage
-----
.. code:: python3

    import blowfish
    
    cipher = blowfish.Cipher(b"This ist ein Key")
    
    ciphertext = cipher.encrypt_block(b"12345678")
    plaintext = cipher.decrypt_block(ciphertext)
    assert plaintext == b"12345678"


.. vim: tabstop=2 expandtab
