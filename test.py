import blowfish
import codecs
import time
from os import urandom
import operator

class Timer(object):
  def __init__(self, clock):
    self.clock = clock
    self.elapsed = 0
    
  def __enter__(self):
    self._enter_time = self.clock()
    
  def __exit__(self, exc_type, exc_value, traceback):
    t = self.clock()
    self.elapsed += t - self._enter_time

if __name__ == "__main__":
    
  print("Testing 'encrypt_block' and 'decrypt_block'...", end="", flush=True)
  # Test vectors from <https://www.schneier.com/code/vectors.txt>
  test_blocks = (
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
  
  for test_block in test_blocks:
    test_key, test_clear_text, test_cipher_text = [
      x.lower() for x in test_block
    ]
    
    cipher = blowfish.Cipher(bytes.fromhex(test_key))
    
    cipher_text = codecs.encode(
      cipher.encrypt_block(bytes.fromhex(test_clear_text)),
      "hex"
    ).lower().decode("utf-8")
    assert cipher_text == test_cipher_text, \
      "expected cipher text {!r}; computed {!r}".format(
        test_cipher_text,
        cipher_text
      )
    
    clear_text = codecs.encode(
      cipher.decrypt_block(bytes.fromhex(test_cipher_text)),
      "hex"
    ).lower().decode("utf-8")
    assert clear_text == test_clear_text, \
      "expected clear text {!r}; computed {!r}".format(
        test_clear_text,
        clear_text
      )
  print("Success!")
  
  test_cipher = blowfish.Cipher(b"this ist a key")  
    
  num_blocks = 10000
  rand_blocks = urandom(8 * num_blocks)
  
  print("\nBenchmarking 'encrypt_block'...")
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    for i in range(0, 8 * num_blocks, 8):
      rand_block = rand_blocks[i:i+8]
      with timer:
        test_cipher.encrypt_block(rand_block)
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_block'...")
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    for i in range(0, 8 * num_blocks, 8):
      rand_block = rand_blocks[i:i+8]
      with timer:
        test_cipher.decrypt_block(rand_block)
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
  
  print("\nTesting 'encrypt_ecb' and 'decrypt_ecb'...", end="", flush=True)
  assert rand_blocks == b"".join(
    test_cipher.decrypt_ecb(
      b"".join(test_cipher.encrypt_ecb(rand_blocks))
    )
  )
  print("Success!")
  
  print("\nBenchmarking 'encrypt_ecb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ecb(rand_blocks))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_ecb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ecb(rand_blocks))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nTesting 'encrypt_cbc' and 'decrypt_cbc'...", end="", flush=True)
  assert rand_blocks == b"".join(
    test_cipher.decrypt_cbc(
      b"".join(test_cipher.encrypt_cbc(rand_blocks, b"12345678")),
      b"12345678"
    )
  )
  print("Success!")
  
  print("\nBenchmarking 'encrypt_cbc'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_cbc(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_cbc'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_cbc(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nTesting 'encrypt_pcbc' and 'decrypt_pcbc'...", end="", flush=True)
  assert rand_blocks == b"".join(
    test_cipher.decrypt_pcbc(
      b"".join(test_cipher.encrypt_pcbc(rand_blocks, b"12345678")),
      b"12345678"
    )
  )
  print("Success!")
    
  print("\nBenchmarking 'encrypt_pcbc'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_pcbc(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_pcbc'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_pcbc(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nTesting 'encrypt_cfb' and 'decrypt_cfb'...", end="", flush=True)
  assert rand_blocks == b"".join(
    test_cipher.decrypt_cfb(
      b"".join(test_cipher.encrypt_cfb(rand_blocks, b"12345678")),
      b"12345678"
    )
  )
  print("Success!")
  
  print("\nBenchmarking 'encrypt_cfb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_cfb(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_cfb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_cfb(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
  
  print("\nTesting 'encrypt_ofb' and 'decrypt_ofb'...", end="", flush=True)
  assert rand_blocks == b"".join(
    test_cipher.decrypt_ofb(
      b"".join(test_cipher.encrypt_ofb(rand_blocks, b"12345678")),
      b"12345678"
    )
  )
  print("Success!")
  
  print("\nBenchmarking 'encrypt_ofb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ofb(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  print("\nBenchmarking 'decrypt_ofb'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ofb(rand_blocks, b"12345678"))
    print("{} random blocks in {:.5f} sec".format(num_blocks, timer.elapsed))
    
  
  ctr_rand_bytes = urandom(8 * num_blocks + 7)
  
  print("\nTesting 'encrypt_ctr' and 'decrypt_ctr'...", end="", flush=True)
  assert ctr_rand_bytes == b"".join(
    test_cipher.decrypt_ctr(
      b"".join(test_cipher.encrypt_ctr(
        ctr_rand_bytes,
        blowfish.ctr_counter(412232, operator.xor)
      )),
      blowfish.ctr_counter(412232, operator.xor)
    )
  )
  print("Success!")
  
  print("\nBenchmarking 'encrypt_ctr'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ctr(
          ctr_rand_bytes,
          blowfish.ctr_counter(412232, operator.xor)
        )
      )
    print("{} random bytes in {:.5f} sec".format(len(ctr_rand_bytes), timer.elapsed))
    
  print("\nBenchmarking 'decrypt_ctr'...")  
  for _ in range(0, 5):
    timer = Timer(time.perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ctr(
          ctr_rand_bytes,
          blowfish.ctr_counter(412232, operator.xor)
        )
      )
    print("{} random bytes in {:.5f} sec".format(len(ctr_rand_bytes), timer.elapsed))
