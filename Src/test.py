import utility as ut


def encryption(plaintext, key):
    k0, k1, k2 = ut.key_extend(key)
    text = ut.XOR(plaintext, k0)
    text = ut.half_byte_substitution(text, 0)
    text = ut.row_shift(text)
    text = ut.column_confuse(text, 0)
    text = ut.key_XOR(text, k1)
    temp = ""
    for column in range(len(text[0])):
        for row in range(len(text)):
            temp += str(text[row][column])
    text = ut.half_byte_substitution(temp, 0)
    text = ut.row_shift(text)
    text = ut.key_XOR(text, k2)
    ciphertext = ''
    for column in range(len(text[0])):
        for row in range(len(text)):
            ciphertext += str(text[row][column])
    return ciphertext


if __name__ == '__main__':
    cipher_text = encryption("0110111101101011", "1010011100111011")
    print(cipher_text)
