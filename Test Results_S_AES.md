# 测试结果

## 第一关：基本测试

- 根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文

### 1.1 加密

- 密钥使用：***0010111101101011***

 ![encryption_binary](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/encryption_binary.png)

### 1.2 解密

- 使用相同密钥：***0010111101101011***

 ![decryption_binary](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/decryption_binary.png)



## 第二关：交叉测试

- 考虑到是"**算法标准"**，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行
- 设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P

**A组**

- 明文：1010101010101010
- 密钥：0101010101010101

 ![cross_test_A](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/cross_test_A.png)



**B组**

- 明文：1010101010101010
- 密钥：0101010101010101

 ![cross_test_B](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/cross_test_B.png)

## 第三关：扩展功能

- 考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)

### 3.1 加密（ASCII风格）

 ![encryption_ascii](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/encryption_ascii.png)

### 3.2 解密（ASCII风格）

 ![decryption_ascii](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/decryption_ascii.png)



## 第四关：多重加密

### 4.1 双重加密

- 将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits
- 密钥使用：***00101111011010111101010110101011***

#### 4.1.1 加密

 ![double_encrypt](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/double_encrypt.png)



#### 4.1.2解密

 ![double_encryption_decrypt](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/double_encryption_decrypt.png)

### 4.2 中间相遇攻击

- 假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥***Key(K1+K2)***

 ![crack](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/crack.gif)



### 4.3 三重加密

- 采用***48bits(K1+K2+K3)***的模式进行三重加解密
- 密钥使用：***001011110110101111010101101010111100100011101000***

#### 4.3.1 加密

 ![triple_encryption](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/triple_encryption.png)



#### 4.3.2 解密

 ![triple_encryption_decrypt](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/triple_encryption_decrypt.png)



## 第五关：工作模式

- 基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。

### 5.1 CBC工作模式加密

 ![CBC_encryption](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/CBC_encryption.png)



### 5.2 CBC工作模式解密

 ![CBC_decryption](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/CBC_decryption.png)



### 5.3 额外测试

- 在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果

- 将***101011100111==000111==00001000001010***修改为***101011100111==010100==00001000001010***

 ![CBC_test](https://github.com/RaymundoTheWolf/S-AES/blob/main/References/CBC_test.png)

## 总结

- S-AES通过一系列可逆的异或，移位，混淆操作进行加解密，很好地提高了安全性
- 同时与DES不同的是，其中的替换盒都经过严密的数学计算显性解释，为其商用提供了安全性保障
