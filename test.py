# vim: filetype=python3 tabstop=2 expandtab

import unittest
import blowfish
import operator
from os import urandom

class CipherMixin(object):
  """
  Test core functionality, i.e. encrypting & decrypting blocks.
  """
  
  byte_order = None
  
  test_vectors = ()
  
  @classmethod
  def setUpClass(cls):
    """
    Setup the test vectors and cipher objects.
    """
    cls.test_vectors = [
      (
        blowfish.Cipher(bytes.fromhex(key), cls.byte_order),
        key, clear_text, cipher_text
      )
      for key, clear_text, cipher_text in cls.test_vectors
    ]
    
  def test_encrypt_block(self):
    """
    Test encryption of blocks.
    """
    for cipher, key, clear_text, cipher_text in self.test_vectors:
      with self.subTest(key = key, clear_text = clear_text):
        self.assertEqual(
          cipher.encrypt_block(bytes.fromhex(clear_text)),
          bytes.fromhex(cipher_text)
        )
  
  def test_decrypt_block(self):
    """
    Test decryption of blocks.
    """
    for cipher, key, clear_text, cipher_text in self.test_vectors:
      with self.subTest(key = key, cipher_text = cipher_text):
        self.assertEqual(
          cipher.decrypt_block(bytes.fromhex(cipher_text)),
          bytes.fromhex(clear_text)
        )

class CipherBigEndian(CipherMixin, unittest.TestCase):
  """
  Test core functionality with big-endian byte order input data.
  """
  byte_order = "big"
  
  # Big-endian test vectors from <https://www.schneier.com/code/vectors.txt>
  test_vectors = (
    # key                 clear text          cipher text
    ("0000000000000000", "0000000000000000", "4EF997456198DD78"),
    ("FFFFFFFFFFFFFFFF", "FFFFFFFFFFFFFFFF", "51866FD5B85ECB8A"),
    ("3000000000000000", "1000000000000001", "7D856F9A613063F2"),
    ("1111111111111111", "1111111111111111", "2466DD878B963C9D"),
    ("0123456789ABCDEF", "1111111111111111", "61F9C3802281B096"),
    ("1111111111111111", "0123456789ABCDEF", "7D0CC630AFDA1EC7"),
    ("0000000000000000", "0000000000000000", "4EF997456198DD78"),
    ("FEDCBA9876543210", "0123456789ABCDEF", "0ACEAB0FC6A0A28D"),
    ("7CA110454A1A6E57", "01A1D6D039776742", "59C68245EB05282B"),
    ("0131D9619DC1376E", "5CD54CA83DEF57DA", "B1B8CC0B250F09A0"),
    ("07A1133E4A0B2686", "0248D43806F67172", "1730E5778BEA1DA4"),
    ("3849674C2602319E", "51454B582DDF440A", "A25E7856CF2651EB"),
    ("04B915BA43FEB5B6", "42FD443059577FA2", "353882B109CE8F1A"),
    ("0113B970FD34F2CE", "059B5E0851CF143A", "48F4D0884C379918"),
    ("0170F175468FB5E6", "0756D8E0774761D2", "432193B78951FC98"),
    ("43297FAD38E373FE", "762514B829BF486A", "13F04154D69D1AE5"),
    ("07A7137045DA2A16", "3BDD119049372802", "2EEDDA93FFD39C79"),
    ("04689104C2FD3B2F", "26955F6835AF609A", "D887E0393C2DA6E3"),
    ("37D06BB516CB7546", "164D5E404F275232", "5F99D04F5B163969"),
    ("1F08260D1AC2465E", "6B056E18759F5CCA", "4A057A3B24D3977B"),
    ("584023641ABA6176", "004BD6EF09176062", "452031C1E4FADA8E"),
    ("025816164629B007", "480D39006EE762F2", "7555AE39F59B87BD"),
    ("49793EBC79B3258F", "437540C8698F3CFA", "53C55F9CB49FC019"),
    ("4FB05E1515AB73A7", "072D43A077075292", "7A8E7BFA937E89A3"),
    ("49E95D6D4CA229BF", "02FE55778117F12A", "CF9C5D7A4986ADB5"),
    ("018310DC409B26D6", "1D9D5C5018F728C2", "D1ABB290658BC778"),
    ("1C587F1C13924FEF", "305532286D6F295A", "55CB3774D13EF201"),
    ("0101010101010101", "0123456789ABCDEF", "FA34EC4847B268B2"),
    ("1F1F1F1F0E0E0E0E", "0123456789ABCDEF", "A790795108EA3CAE"),
    ("E0FEE0FEF1FEF1FE", "0123456789ABCDEF", "C39E072D9FAC631D"),
    ("0000000000000000", "FFFFFFFFFFFFFFFF", "014933E0CDAFF6E4"),
    ("FFFFFFFFFFFFFFFF", "0000000000000000", "F21E9A77B71C49BC"),
    ("0123456789ABCDEF", "0000000000000000", "245946885754369A"),
    ("FEDCBA9876543210", "FFFFFFFFFFFFFFFF", "6B5C5A9C5D9E0A5A"),
  )
  
class CipherLittleEndian(CipherMixin, unittest.TestCase):
  """
  Test core functionality with little-endian byte order input data.
  """
  
  byte_order = "little"
  
  # Little-endian test vectors derived from
  # <https://www.schneier.com/code/vectors.txt>
  # I've simply changed the clear text and cipher text to little-endian byte
  # order hex.
  test_vectors = (
    # key                 clear text          cipher text
    ("0000000000000000", "0000000000000000", "4597F94E78DD9861"),
    ("FFFFFFFFFFFFFFFF", "FFFFFFFFFFFFFFFF", "D56F86518ACB5EB8"),
    ("3000000000000000", "0000001001000000", "9A6F857DF2633061"),
    ("1111111111111111", "1111111111111111", "87DD66249D3C968B"),
    ("0123456789ABCDEF", "1111111111111111", "80C3F96196B08122"),
    ("1111111111111111", "67452301EFCDAB89", "30C60C7DC71EDAAF"),
    ("0000000000000000", "0000000000000000", "4597F94E78DD9861"),
    ("FEDCBA9876543210", "67452301EFCDAB89", "0FABCE0A8DA2A0C6"),
    ("7CA110454A1A6E57", "D0D6A10142677739", "4582C6592B2805EB"),
    ("0131D9619DC1376E", "A84CD55CDA57EF3D", "0BCCB8B1A0090F25"),
    ("07A1133E4A0B2686", "38D448027271F606", "77E53017A41DEA8B"),
    ("3849674C2602319E", "584B45510A44DF2D", "56785EA2EB5126CF"),
    ("04B915BA43FEB5B6", "3044FD42A27F5759", "B18238351A8FCE09"),
    ("0113B970FD34F2CE", "085E9B053A14CF51", "88D0F4481899374C"),
    ("0170F175468FB5E6", "E0D85607D2614777", "B793214398FC5189"),
    ("43297FAD38E373FE", "B81425766A48BF29", "5441F013E51A9DD6"),
    ("07A7137045DA2A16", "9011DD3B02283749", "93DAED2E799CD3FF"),
    ("04689104C2FD3B2F", "685F95269A60AF35", "39E087D8E3A62D3C"),
    ("37D06BB516CB7546", "405E4D163252274F", "4FD0995F6939165B"),
    ("1F08260D1AC2465E", "186E056BCA5C9F75", "3B7A054A7B97D324"),
    ("584023641ABA6176", "EFD64B0062601709", "C13120458EDAFAE4"),
    ("025816164629B007", "00390D48F262E76E", "39AE5575BD879BF5"),
    ("49793EBC79B3258F", "C8407543FA3C8F69", "9C5FC55319C09FB4"),
    ("4FB05E1515AB73A7", "A0432D0792520777", "FA7B8E7AA3897E93"),
    ("49E95D6D4CA229BF", "7755FE022AF11781", "7A5D9CCFB5AD8649"),
    ("018310DC409B26D6", "505C9D1DC228F718", "90B2ABD178C78B65"),
    ("1C587F1C13924FEF", "283255305A296F6D", "7437CB5501F23ED1"),
    ("0101010101010101", "67452301EFCDAB89", "48EC34FAB268B247"),
    ("1F1F1F1F0E0E0E0E", "67452301EFCDAB89", "517990A7AE3CEA08"),
    ("E0FEE0FEF1FEF1FE", "67452301EFCDAB89", "2D079EC31D63AC9F"),
    ("0000000000000000", "FFFFFFFFFFFFFFFF", "E0334901E4F6AFCD"),
    ("FFFFFFFFFFFFFFFF", "0000000000000000", "779A1EF2BC491CB7"),
    ("0123456789ABCDEF", "0000000000000000", "884659249A365457"),
    ("FEDCBA9876543210", "FFFFFFFFFFFFFFFF", "9C5A5C6B5A0A9E5D"),
  )
        
class ModesOfOperationMixin(object):
  """
  Test the modes of operation.
  """
  byte_order = None
  
  @classmethod
  def setUpClass(cls):
    """
    Setup the Cipher object and dummy test data.
    """
    cls.cipher = blowfish.Cipher(
      b"this ist ein key",
      byte_order = cls.byte_order
    )
    cls.block_multiple_data = urandom(500 * 8)
  
  def test_ecb_mode(self):
    """
    Test ECB mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    
    encrypted_data = b"".join(cipher.encrypt_ecb(block_multiple_data))
    decrypted_data = b"".join(cipher.decrypt_ecb(encrypted_data))
    
    self.assertEqual(block_multiple_data, decrypted_data)
    
  def test_ecb_cts_mode(self):
    """
    Test ECB-CTS mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    
    for i in range(0, 8):
      with self.subTest(extra_bytes = i):
        data = block_multiple_data + urandom(i)
        
        encrypted_data = b"".join(cipher.encrypt_ecb_cts(data))
        decrypted_data = b"".join(cipher.decrypt_ecb_cts(encrypted_data))
        
        self.assertEqual(data, decrypted_data)
    
  def test_cbc_mode(self):
    """
    Test CBC mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    init_vector = urandom(8)
    
    encrypted_data = b"".join(
      cipher.encrypt_cbc(block_multiple_data, init_vector)
    )
    decrypted_data = b"".join(
      cipher.decrypt_cbc(encrypted_data, init_vector)
    )

    self.assertEqual(block_multiple_data, decrypted_data)
  
  def test_cbc_cts_mode(self):
    """
    Test CBC-CTS mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    init_vector = urandom(8)
    
    for i in range(0, 8):
      with self.subTest(extra_bytes = i):
        data = block_multiple_data + urandom(i)
        
        encrypted_data = b"".join(
          cipher.encrypt_cbc_cts(data, init_vector)
        )
        decrypted_data = b"".join(
          cipher.decrypt_cbc_cts(encrypted_data, init_vector)
        )
        self.assertEqual(data, decrypted_data)
  
  def test_pcbc_mode(self):
    """
    Test PCBC mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    init_vector = urandom(8)
    
    encrypted_data = b"".join(
      cipher.encrypt_pcbc(block_multiple_data, init_vector)
    )
    decrypted_data = b"".join(
      cipher.decrypt_pcbc(encrypted_data, init_vector)
    )

    self.assertEqual(block_multiple_data, decrypted_data)
  
  def test_cfb_mode(self):
    """
    Test CFB mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    init_vector = urandom(8)
    
    for i in range(0, 8):
      with self.subTest(extra_bytes = i):
        data = block_multiple_data + urandom(i)
        
        encrypted_data = b"".join(
          cipher.encrypt_cfb(data, init_vector)
        )
        decrypted_data = b"".join(
          cipher.decrypt_cfb(encrypted_data, init_vector)
        )
        self.assertEqual(data, decrypted_data)
  
  def test_ofb_mode(self):
    """
    Test OFB mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    init_vector = urandom(8)
    
    for i in range(0, 8):
      with self.subTest(extra_bytes = i):
        data = block_multiple_data + urandom(i)
        
        encrypted_data = b"".join(
          cipher.encrypt_ofb(data, init_vector)
        )
        decrypted_data = b"".join(
          cipher.decrypt_ofb(encrypted_data, init_vector)
        )
        self.assertEqual(data, decrypted_data)
  
  def test_ctr_mode(self):
    """
    Test CTR mode.
    """
    cipher = self.cipher
    block_multiple_data = self.block_multiple_data
    nonce = int.from_bytes(urandom(8), "big")
    
    for i in range(0, 8):
      with self.subTest(extra_bytes = i):
        data = block_multiple_data + urandom(i)
        
        encrypted_data = b"".join(
          cipher.encrypt_ctr(
            data,
            blowfish.ctr_counter(nonce, operator.xor)
          )
        )
        decrypted_data = b"".join(
          cipher.decrypt_ctr(
            encrypted_data,
            blowfish.ctr_counter(nonce, operator.xor)
          )
        )
        self.assertEqual(data, decrypted_data)

class ModesOfOperationBigEndian(ModesOfOperationMixin, unittest.TestCase):
  """
  Test the modes of operation using big-endian byte order input.
  """
  
  byte_order = "big"
  
class ModesOfOperationLittleEndian(ModesOfOperationMixin, unittest.TestCase):
  """
  Test the modes of operation using little-endian byte order input.
  """
  
  byte_order = "little"

