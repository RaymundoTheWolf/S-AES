"""
参数设置
"""
# 便于处理简便将十六进制转为了十进制
S_Box = [(9, 4, 10, 11), (13, 1, 8, 5), (6, 2, 0, 3), (12, 14, 15, 7)]
S_Box_Verse = [(10, 5, 9, 11), (1, 7, 8, 15), (6, 0, 2, 3), (12, 4, 13, 14)]
RCON = ["10000000", "00110000"]
# 便于计算处理为10进制
GF_Plus_Matrix = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                  [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14],
                  [2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13],
                  [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12],
                  [4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11],
                  [5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10],
                  [6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10, 11, 8, 9],
                  [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8],
                  [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
                  [9, 8, 11, 10, 13, 12, 15, 14, 1, 0, 3, 2, 5, 4, 7, 6],
                  [10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5],
                  [11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4],
                  [12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3],
                  [13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 7, 6, 1, 0, 3, 2],
                  [14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1],
                  [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]

GF_Multi_Matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                   [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
                   [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
                   [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
                   [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
                   [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
                   [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
                   [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
                   [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
                   [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
                   [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
                   [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 9, 5, 2, 14],
                   [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
                   [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 10, 4, 5, 11],
                   [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 11, 4]]


# x^4+x+1模的GF(2^4)加法
def GF_Plus(x, y):
    return GF_Plus_Matrix[x][y]


# x^4+x+1模的GF(2^4)乘法
def GF_Multiply(x, y):
    return GF_Multi_Matrix[x][y]


# 传入类型为字符串类型
def XOR(x, y):
    res = ""
    for i in range(len(x)):
        if x[i] == y[i]:
            res += "0"
        else:
            res += "1"
    return res


# 传入w为字符串类型,round{0:k1生成，1:k2生成}
def function_g(w, round):
    left = w[:4]
    right = w[4:]
    temp = left
    left = right
    right = temp
    left_x = int(left[:2], 2)
    left_y = int(left[2:], 2)
    right_x = int(right[:2], 2)
    right_y = int(right[2:], 2)
    left = bin(S_Box[left_x][left_y])[2:].zfill(4)
    right = bin(S_Box[right_x][right_y])[2:].zfill(4)
    res = left + right
    if round == 1:
        res = XOR(res, RCON[0])
    elif round == 2:
        res = XOR(res, RCON[1])
    return res


# key为字符串类型，返回三把密钥
def key_extend(key):
    k0 = key
    w2 = XOR(key[:8], function_g(key[8:], 1))
    w3 = XOR(w2, key[8:])
    k1 = w2 + w3
    w4 = XOR(w2, function_g(w3, 2))
    w5 = XOR(w4, w3)
    k2 = w4 + w5
    return k0, k1, k2


# text类型为字符串，mode解释{0:加密，1:解密}
def half_byte_substitution(text, mode):
    bits_array = [[text[0:4], text[8:12]],
                  [text[4:8], text[12:16]]]
    if mode == 0:
        for i in range(2):
            for j in range(2):
                temp = bits_array[i][j]
                x = int(temp[:2], 2)
                y = int(temp[2:], 2)
                bits_array[i][j] = bin(S_Box[x][y])[2:].zfill(4)
    elif mode == 1:
        for i in range(2):
            for j in range(2):
                temp = bits_array[i][j]
                x = int(temp[:2], 2)
                y = int(temp[2:], 2)
                bits_array[i][j] = bin(S_Box_Verse[x][y])[2:].zfill(4)
    return bits_array


# 行位移输入为矩阵形式的内容，加解密相同
def row_shift(array):
    temp = array[1][0]
    array[1][0] = array[1][1]
    array[1][1] = temp
    return array


# 列混淆，输入为矩阵形式，mode解释{0:加密，1:解密}
def column_confuse(array, mode):
    if mode == 0:
        s00 = GF_Plus(int(array[0][0], 2), GF_Multiply(4, int(array[1][0], 2)))
        s10 = GF_Plus(GF_Multiply(4, int(array[0][0], 2)), int(array[1][0], 2))
        s01 = GF_Plus(int(array[0][1], 2), GF_Multiply(4, int(array[1][1], 2)))
        s11 = GF_Plus(GF_Multiply(4, int(array[0][1], 2)), int(array[1][1], 2))
    elif mode == 1:
        s00 = GF_Plus(GF_Multiply(9, int(array[0][0], 2)), GF_Multiply(2, int(array[1][0], 2)))
        s10 = GF_Plus(GF_Multiply(2, int(array[0][0], 2)), GF_Multiply(9, int(array[1][0], 2)))
        s01 = GF_Plus(GF_Multiply(9, int(array[0][1], 2)), GF_Multiply(2, int(array[1][1], 2)))
        s11 = GF_Plus(GF_Multiply(2, int(array[0][1], 2)), GF_Multiply(9, int(array[1][1], 2)))
    array = [[bin(s00)[2:].zfill(4), bin(s01)[2:].zfill(4)],
             [bin(s10)[2:].zfill(4), bin(s11)[2:].zfill(4)]]
    return array


# 轮密钥加，输入为矩阵形式
def key_XOR(bits_array, key):
    for i in range(2):
        for j in range(2):
            bits_array[j][i] = XOR(bits_array[j][i], key[4 * (i * 2 + j):4 * (i * 2 + j + 1)])
    return bits_array

