blowfish
========
A Python module implementing Blowfish, a symmetric-key block cipher designed
by Bruce Schneier. Implemented entirely in Python.

Dependencies
------------
- Python 3.4+

Installation
------------
If you just need a Blowfish cipher in your Python project, feel free to
manually copy the ``blowfish.py`` file to your package directory.

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

TODO
----
- Implement common modes of operation (ECB, CBC, etc.)

.. vim: tabstop=2 expandtab
