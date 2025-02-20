import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from time import sleep
from timeit import default_timer as timer

def EtMEncrypt(key_enc,key_mac, pt):
    backend = default_backend()
    iv = os.urandom(16)
    algorithm = algorithms.ChaCha20(key_enc, iv)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt) + encryptor.finalize()
    h = hmac.HMAC(key_mac, hashes.SHA256(), backend=default_backend())
    h.update(iv+ct)
    tag = h.finalize()
    final = iv + ct + tag[:8]
    return final

def EtMDecrypt(key_enc,key_mac, ct):
    backend = default_backend()
    h = hmac.HMAC(key_mac, hashes.SHA256(), backend=default_backend())
    h.update(ct[:-8])
    tag = h.finalize()[:8]
    if CheckEq(tag,ct[-8:]):
        iv = ct[:16]
        algorithm = algorithms.ChaCha20(key_enc, iv)
        cipher = Cipher(algorithm, mode=None, backend=default_backend())
        decryptor = cipher.decryptor()
        pt = decryptor.update(ct[16:-8]) + decryptor.finalize()
        return pt
    raise Exception('authentication failure')

def CheckEq(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        sleep(0.005)
        if a[i] != b[i]:
            return False
    sleep(0.005)
    return True

def EtMOracle(ct):
    backend = default_backend()
    h = hmac.HMAC(key_mac, hashes.SHA256(), backend=default_backend())
    h.update(ct[:-8])
    tag = h.finalize()[:8]
    if CheckEq(tag,ct[-8:]):
        return True
    return False

key_enc = os.urandom(32)
key_mac = os.urandom(16)


cipher = EtMEncrypt(key_enc, key_mac, b"Hello world!")

# =======================
# Insert your attack below this line.
# Do not modify above this line.

cipher_array = bytearray(cipher)
cipher_array[22] = ord('f') ^ cipher_array[22] ^ ord('w')
cipher_array[24] = ord('l') ^ cipher_array[24] ^ ord('r')
cipher_array[25] = ord('k') ^ cipher_array[25] ^ ord('l')
cipher_array[26] = ord('s') ^ cipher_array[26] ^ ord('d')

prevRoundMax = 0
tagStartIndex = len(cipher) - 8
for byteIndex in range(0, 8):
    currentRoundMax = 0
    for byteGuess in range(0, 256):
        cipher_array[tagStartIndex + byteIndex] = byteGuess
        testCipherText = bytes(cipher_array)
        start = timer()
        EtMOracle(testCipherText)
        end = timer()
        delta = end - start
        if delta > currentRoundMax:
            currentRoundMax = delta
            currentByteValue = byteGuess
    cipher_array[tagStartIndex + byteIndex] = currentByteValue
    prevRoundMax = currentRoundMax

cipher_forged = bytes(cipher_array)

# Insert the attack above this line.
# Do not mofidy below this line.
# =======================

pt = EtMDecrypt(key_enc, key_mac, cipher_forged)
print(pt)