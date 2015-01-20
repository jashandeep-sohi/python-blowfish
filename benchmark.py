import blowfish
from time import perf_counter
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
  test_cipher = blowfish.Cipher(b"this ist a key")
  
  times = 6
  num_bytes = 10000 * 8
  
  rand_bytes = urandom(num_bytes)
  iv = urandom(8)
  nonce = int.from_bytes(urandom(8), "big")
    
  print("Benchmarking 'encrypt_block'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    for i, j in zip(
      range(0, num_bytes, 8),
      range(8, num_bytes, 8)
    ):
      rand_block = rand_bytes[i:j]
      with timer:
        test_cipher.encrypt_block(rand_block)
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_block'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    for i, j in zip(
      range(0, num_bytes, 8),
      range(8, num_bytes, 8)
    ):
      rand_block = rand_bytes[i:j]
      with timer:
        test_cipher.decrypt_block(rand_block)
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_ecb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ecb(rand_bytes))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_ecb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ecb(rand_bytes))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_ecb_cts'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ecb_cts(rand_bytes))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_ecb_cts'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ecb_cts(rand_bytes))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_cbc'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_cbc(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_cbc'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_cbc(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_cbc_cts'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_cbc_cts(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_cbc_cts'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_cbc_cts(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_pcbc'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_pcbc(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_pcbc'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_pcbc(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_cfb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_cfb(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_cfb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_cfb(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_ofb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.encrypt_ofb(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_ofb'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    with timer:
      b"".join(test_cipher.decrypt_ofb(rand_bytes, iv))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'encrypt_ctr'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    counter = blowfish.ctr_counter(nonce, operator.xor)
    with timer:
      b"".join(test_cipher.encrypt_ctr(rand_bytes, counter))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
  
  print("\nBenchmarking 'decrypt_ctr'...")
  total = 0
  for n in range(1, times):
    timer = Timer(perf_counter)
    counter = blowfish.ctr_counter(nonce, operator.xor)
    with timer:
      b"".join(test_cipher.decrypt_ctr(rand_bytes, counter))
    print("{} random bytes in {:.5f} sec".format(num_bytes, timer.elapsed))
    total += timer.elapsed
  print("{} random bytes in {:.5f} sec (average)".format(num_bytes, total / n))
      
# vim: tabstop=2 expandtab
