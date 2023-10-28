# S-AES
Repository for cryptography homework, teamed up with Yuyang Hu @[Gracivio](https://github.com/Gracivio), a S-AES instance.

# Procedure
1. **Encryption**
    - According to S-AES tutorial, the encryption procedure follows **first XOR, nibblebyte substitution, shift rows, confuse columns, second XOR, nibblebyte substitution, shift rows and third XOR**. For each XOR, a different key is used so that we need three keys. To generate three keys from the original one, a **key extend function** is used.
    -  The key extend function first divide the key into two 8-bits parts, the right of which goes into a function that follows a bunch of steps for better performance, which is also called as the g-function. The g-function *first swaps the two parts, then do a substitution, after that do a XOR process with initial vector(settled)*.


      ```
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
      ```


    - The nibblebyte substituion divides the plain text into four 4-bits and turn into a *state matrix*. And for each part, we do a substituion.
    - The row shift only swaps the second row
    - The column confusion goes a GF(2^4) with mod x^4+x+1 calculation.

2. **Decryption**
    - According to S-AES tutorial, the decryption procedure is alike encryption but reversed. Following **first XOR(use Key-2), reversed shift rows, reversed nibblebyte substitution, second XOR(use Key-1), reversed column confusion, reversed shift rows, reversed nibblebyte substitution, third XOR(use Key-0)**. For nibblebyte substituion, row shifts and column confusion, a reversed S-Box and matrix is used, which under the calculation of math.


    ```
    S_Box = [(9, 4, 10, 11), (13, 1, 8, 5), (6, 2, 0, 3), (12, 14, 15, 7)]
    S_Box_Verse = [(10, 5, 9, 11), (1, 7, 8, 15), (6, 0, 2, 3), (12, 4, 13, 14)]
    ```

# Feature
1. 2-AES
    - 2-AES has 16-bit plain text or cipher text input, and 32-bit key. In 2-AES, we use two S-AES to encrypt the plaintext via two keys, and each key is seperated of 16-bit from the 32-bit key.
    - Also, we add a crack feature in 2-AES, given plain text and corresponding cipher text, we use a key to encrypt the plaintext and use the other to decrypt the cipher text, and compare the middle text to perform the attack.
2. 3-AES
    - Like 2-AES, we use three S-AES to encrypt the plaintext, the process is *encrypt,encrypt,encrypt*.
3. CBC Mode
    - Also known as Cipher Block Chaining, which be able to encrypt long bits plaintext.
  
# GUI
- We use tkinter to create the user interface. Relative layout is used for better demonstration, but some particular devices still see wrong layout.

# How to use
- Download ***S-AES.py*** and ***utility.py***, and you need to download some packages to meet the environment it runs on.

# Results
- Go to ***Test results.md*** in this repository for further information :)
