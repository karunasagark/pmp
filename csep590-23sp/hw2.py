# Warning: This will only work with Python 3 (in case you need to worry about this)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import sys

def check_enc(text):
    nl = len(text)
    val = int(text[-1])
    if val == 0 or val > 16:
        return False

    for i in range(1,val+1):
        if (int(text[nl-i]) != val):
            return False
    return True

def PadOracle(ciphertext):
    if len(ciphertext) % 16 != 0:
        return False

    # Do not cheat - of course you an decrypt ciphertexts directly,
    # but this is not the goal. Ok? :)
    
    key = b"Sixteen byte key"
    backend = default_backend()
    
    ivd = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(ivd), backend=backend)
    decryptor = cipher.decryptor()
    ptext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    
    return check_enc(ptext)

def PaddingOracleAttack(ctext):
    originalCipherText = bytearray(ctext)
    blockCount = len(ctext) // 16
    plainText = bytearray(len(ctext))

    for block in range(blockCount-1, 0, -1):
        cipherText = bytearray(ctext)
        for byte in range(15, -1, -1):
            expectedPadding = 16 - byte
            for guess in range(0, 256):
                cipherText[(block-1)*16 + byte] = guess
                if PadOracle(cipherText[0:(block+1)*16]):
                    cipherText[(block-1)*16 + (byte-1)] = (guess+1) % 256
                    if PadOracle(cipherText[0:(block+1)*16]):
                        plainText[block*16 + byte] = guess ^ expectedPadding ^ originalCipherText[(block-1)*16 + byte]
                        for i in range(byte, 16):
                            cipherText[(block-1)*16 + i] = plainText[block*16 + i] ^ originalCipherText[(block-1)*16 + i] ^ (expectedPadding+1)
                        break
    return plainText[16:]

if len(sys.argv) > 1:
    myfile = open(sys.argv[1], "rb")
    ctext=myfile.read()
    myfile.close()

    # Padding-oracle attack comes here
    # ctext contains the ciphertext now
    plainText = PaddingOracleAttack(ctext)
    print(plainText.decode("utf-8"))

else:
    print("You need to specify a file!")
    
