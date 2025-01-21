def task1a():
    cipher_text = "tnspnvpotegpcjeszczfrswjdltoespnzxafepclyoeslebftepopqtytepwjtdesplydhpctestyvespaczmwpxezmpbftepszypdehtesjzftdeslejzfgpypgpclneflwwjvyzhyhsleespbfpdetzytd"
    print("Shift = {}, Ciphr text = {}".format('NA', cipher_text))
    for k in range(26):
        plain_text = ""
        for c in cipher_text:
            plain_text += chr(((ord(c) - ord('a') + k) % 26) + ord('a'))
        print("Shift = {}, Plain text = {}".format(k, plain_text))

def task1b_frequency():
    cipher_text = "GRGZQEGKXJPRQERQEWXJXLDQPHQORRNQRRNGEIZQPTEJRQDVQYZVNQRRNTYZTTKHJPGEZRQEOTJERNTXDQETRTQPRNKQENQWQDVQYZQZZLKTWRNQRNTVQZKJPTGERTDDGITERRNQEWJDXNGEZUTOQLZTNTNQWQONGTFTWZJKLONRNTVNTTDETVYJPSVQPZQEWZJJEVNGDZRQDDRNTWJDXNGEZNQWTFTPWJETVQZKLOSQUJLRGERNTVQRTPNQFGEIQIJJWRGKTULROJEFTPZTDYRNTWJDXNGEZNQWQDVQYZUTDGTFTWRNQRRNTYVTPTHQPKJPTGERTDDGITERRNQEKQEHJPXPTOGZTDYRNTZQKTPTQZJEZOLPGJLZDYTEJLINRNTWJDXNGEZNQWDJEISEJVEJHRNTGKXTEWGEIWTZRPLORGJEJHRNTXDQETRTQPRNQEWNQWKQWTKQEYQRRTKXRZRJQDTPRKQESGEWJHRNTWQEITPULRKJZRJHRNTGPOJKKLEGOQRGJEZVTPTKGZGERTPXPTRTWQZQKLZGEIQRRTKXRZRJXLEONHJJRUQDDZJPVNGZRDTHJPRGWUGRZZJRNTYTFTERLQDDYIQFTLXQEWDTHRRNTTQPRNUYRNTGPJVEKTQEZZNJPRDYUTHJPTRNTFJIJEZQPPGFTWRNTDQZRTFTPWJDXNGEKTZZQITVQZKGZGERTPXPTRTWQZQZLPXPGZGEIDYZJXNGZRGOQRTWQRRTKXRRJWJQWJLUDTUQOSVQPWZZJKTPZQLDRRNPJLINQNJJXVNGDZRVNGZRDGEIRNTZRQPZXQEIDTWUQEETPULRGEHQORRNTKTZZQITVQZRNGZZJDJEIQEWRNQESZHJPQDDRNTHGZNGEHQORRNTPTVQZJEDYJETZXTOGTZJERNTXDQETRKJPTGERTDDGITERRNQEWJDXNGEZQEWRNTYZXTERQDJRJHRNTGPRGKTGEUTNQFGJLPQDPTZTQPONDQUJPQRJPGTZPLEEGEIPJLEWGEZGWTVNTTDZQEWOJEWLORGEIHPGINRTEGEIDYTDTIQERQEWZLURDTTBXTPGKTERZJEKQERNTHQORRNQRJEOTQIQGEKQEOJKXDTRTDYKGZGERTPXPTRTWRNGZPTDQRGJEZNGXVQZTERGPTDYQOOJPWGEIRJRNTZTOPTQRLPTZXDQEZ"

    freq = {}
    for c in cipher_text:
        if c not in freq:
            freq[c] = 0
        freq[c] += 1

    difreq = {}
    for i in range(0, len(cipher_text)):
        if i + 1 >= len(cipher_text):
            break
        di = cipher_text[i] + cipher_text[i + 1]
        if di not in difreq:
            difreq[di] = 0
        difreq[di] += 1

    trifreq = {}
    for i in range(0, len(cipher_text)):
        if i + 2 >= len(cipher_text):
            break
        tri = cipher_text[i] + cipher_text[i + 1] + cipher_text[i + 2]
        if tri not in trifreq:
            trifreq[tri] = 0
        trifreq[tri] += 1

    quadfreq = {}
    for i in range(0, len(cipher_text)):
        if i + 3 >= len(cipher_text):
            break
        quad = cipher_text[i] + cipher_text[i + 1] + cipher_text[i + 2] + cipher_text[i + 3]
        if quad not in quadfreq:
            quadfreq[quad] = 0
        quadfreq[quad] += 1

    print("Frequency: {}".format(sorted(freq.items(), key=lambda x: x[1], reverse=True)))
    print("Di-frequency: {}".format(sorted(difreq.items(), key=lambda x: x[1], reverse=True)))
    print("Tri-frequency: {}".format(sorted(trifreq.items(), key=lambda x: x[1], reverse=True)))
    print("Quad-frequency: {}".format(sorted(quadfreq.items(), key=lambda x: x[1], reverse=True)))

def task1b_decrypt():
    subst = {
        'T': 'e', 
        'R': 't', 
        'Q': 'a', 
        'N': 'h', 
        'E': 'n', 
        'W': 'd', 
        'G': 'i', 
        'I': 'g', 
        'Z': 's', 
        'P': 'r', 
        'J': 'o',
        'O': 'c',
        'K': 'm',
        'X': 'p',
        'D': 'l',
        'L': 'u',
        'H': 'f',
        'V': 'w',
        'Y': 'y',
        'U': 'b',
        'F': 'v',
        'S': 'k',
        'B': 'x'
        }
    plain_text = ""
    for c in cipher_text:
        if c in subst:
            plain_text += subst[c]
        else:
            plain_text += '?'

    print(plain_text)

def task2_aes(key, mesg):
    import os
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(mesg) + encryptor.finalize()
    return ct

def task2_aes_d(key, ct):
    import os
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct) + decryptor.finalize()
    print(pt.hex())

X = bytes.fromhex('10 04 20 18 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ', ''))

def task2a():
    task2_aes(X, X)

def task2b():
    task2_aes(X, bytes.fromhex('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ', '')))
    task2_aes(X, bytes.fromhex('11 11 11 11 11 11 11 11 11 11 11 11 11 11 11 11'.replace(' ', '')))

def task2c():
    k = bytes.fromhex('00000000000000000000000000000000')
    c = task2_aes(k, X)
    while not c.endswith(b'\x00'):
        k = (int(k.hex(), 16) + 1).to_bytes(16, 'big')
        print("inner {}".format(k.hex()))
        c = task2_aes(k, X)
    print(k.hex())