import secrets
import tkinter as tk
import tkinter.messagebox
import threading
import time
import ttkbootstrap as ttk

from ttkbootstrap import Style
from tkinter import *

import utility as ut


def encryption(plaintext, key):
    k0, k1, k2 = ut.key_extend(key)
    text = ut.XOR(plaintext, k0)
    text = ut.nibblebyte_substitution(text, 0)
    text = ut.row_shift(text)
    text = ut.column_confuse(text, 0)
    text = ut.key_XOR(text, k1)
    temp = ""
    for column in range(len(text[0])):
        for row in range(len(text)):
            temp += str(text[row][column])
    text = ut.nibblebyte_substitution(temp, 0)
    text = ut.row_shift(text)
    text = ut.key_XOR(text, k2)
    ciphertext = ''
    for column in range(len(text[0])):
        for row in range(len(text)):
            ciphertext += str(text[row][column])
    return ciphertext


def decryption(ciphertext, key):
    k0, k1, k2 = ut.key_extend(key)
    text = ut.XOR(ciphertext, k2)
    text = [[text[0:4], text[8:12]], [text[4:8], text[12:16]]]
    text = ut.row_shift(text)
    text = text[0][0] + text[1][0] + text[0][1] + text[1][1]
    text = ut.nibblebyte_substitution(text, 1)
    text = ut.key_XOR(text, k1)
    text = ut.column_confuse(text, 1)
    text = ut.row_shift(text)
    text = text[0][0] + text[1][0] + text[0][1] + text[1][1]
    text = ut.nibblebyte_substitution(text, 1)
    text = ut.key_XOR(text, k0)
    plaintext = text[0][0] + text[1][0] + text[0][1] + text[1][1]
    return plaintext


# 获取密钥函数
def generate_key(length):
    key = secrets.randbits(length)
    # 转为二进制，左零补全为10-bit
    key_bin = bin(key).replace('0b', '').zfill(10)
    return key_bin


def char_to_binary(char):
    # 将字符转换为ASCII码
    ascii_code = ord(char)
    # 将ASCII码转换为8位二进制数
    binary_string = str(bin(ascii_code))[2:].zfill(16)
    return binary_string


# 判断是否为2的次方
def is_power_of_two(n):
    return n != 0 and (n & (n - 1)) == 0


# 首页界面
class Welcome(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.commandStr = ttk.StringVar()
        self.createPage()

    def encryption_command(self):
        self.page.destroy()
        Encryption(self.root)

    def decryption_command(self):
        self.page.destroy()
        Decryption(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', pady=10, expand=True)
        sWelcome = tk.Label(self.page, text='S-AES密码系统', height=3, width=200,
                            bg='white',
                            font=('黑体', 26))
        sWelcome.pack(pady=10)

        combobox = ttk.Combobox(self.page, bootstyle='info', textvariable=self.commandStr)  # 获取用户输入的信息
        combobox['value'] = ('加密', '解密', '获取密钥', 'Crack', 'CBC', '多重加密', '多重加密解密')  # 组合框显示的选项
        combobox.current(0)
        combobox.pack(padx=5, pady=10)
        combobox.place(relx=0.45, rely=0.45)  # 组合框的位置和大小

        getStr = ['加密', '解密', '获取密钥', 'Crack', 'CBC', '多重加密', '多重加密解密']

        # 选择不同功能切换至不同界面
        def get_command():
            for index in range(len(getStr)):
                if self.commandStr.get() == getStr[index]:
                    flag = index
                    break
                else:
                    flag = 5
            if flag == 0:
                self.page.destroy()
                Encryption(self.root)
            elif flag == 1:
                self.page.destroy()
                Decryption(self.root)
            elif flag == 2:  # 获取密钥
                self.page.destroy()
                Welcome(self.root)
                key = str(generate_key(16))
                tk.messagebox.showinfo('Key Generated', '密钥请妥善保管:' + key)
            elif flag == 3:
                self.page.destroy()
                Crack(self.root)
            elif flag == 4:
                self.page.destroy()
                CBC(self.root)
            elif flag == 5:
                self.page.destroy()
                Multiple_Encryption(self.root)
            elif flag == 6:
                self.page.destroy()
                Multiple_Decryption(self.root)
            else:
                tk.messagebox.showerror('错误', '不提供该类型服务')

        op_label = tk.Label(self.page, text='选择操作类型', width=14, height=2, font=('黑体', 13), bg='white')
        op_label.place(relx=0.2, rely=0.44)

        # "确定"按钮
        confirm_button = ttk.Button(self.page, text='确定', bootstyle='primary.TButton', command=get_command, width=7)
        confirm_button.pack(padx=5, ipady=10)
        confirm_button.place(relx=0.42, rely=0.75)


# 加密界面
class Encryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        def encryption_ans():
            # 这里设置检查，防止用户不合理输入
            key = self.masterKey.get()
            flag = select_button()
            if len(key) != 16:
                tk.messagebox.showerror('Invalid Key', '密钥长度错误，请重新输入')
                return -1
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            if flag == 0:
                # ASCII版本
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：\n')
                text = self.plainText.get()
                plaintext = ''
                for letter in text:
                    letter = char_to_binary(letter)
                    letter = encryption(letter, key)
                    out = chr(int(letter, 2))
                    plaintext += out
                plainText_output.insert('insert', plaintext)
            else:
                text = self.plainText.get()
                if len(text) != 16:
                    tk.messagebox.showerror('Invalid PlainText', '明文错误，请重新输入')
                    return -1
                for i in range(len(text)):
                    if int(text[i]) != 1 and int(text[i]) != 0:
                        tk.messagebox.showerror('Invalid Key', '明文错误，请重新输入')
                        return -1
                text = encryption(text, key)
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：')
                plainText_output.insert('insert', text)

        # GUI界面
        sWelcome = tk.Label(self.page, text='加密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='ASCII', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='Binary', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 明文，主密钥输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.31)

        # 密钥输入显示为*号进行保密
        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 标签显示输入类别
        plaintext_label = tk.Label(self.page, text='明文', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '加密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "加密"按钮
        encrypt_button = ttk.Button(self.page, text='加密', bootstyle='success.TButton', command=encryption_ans,
                                    width=7)
        encrypt_button.place(relx=0.52, rely=0.8)


class Decryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.cipherText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.ansCheck = []
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        # 解密实现函数
        def decryption_ans():
            flag = select_button()
            key = self.masterKey.get()
            cipherText = self.cipherText.get()
            if len(key) != 16:
                tk.messagebox.showerror('Invalid Key', '密钥格式错误')
                return -1
            if flag == 1:
                if len(cipherText) != 16:
                    tk.messagebox.showerror('Invalid CipherText', '密文格式错误')
                    return -1
                for i in range(len(key)):
                    if int(key[i]) != 1 and int(key[i]) != 0:
                        tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                        return -1
                for i in range(len(cipherText)):
                    if int(cipherText[i]) != 1 and int(cipherText[i]) != 0:
                        tk.messagebox.showerror('Invalid Key', '密钥错误，请重新输入')
                        return -1
                text = decryption(cipherText, key)
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '解密结果：')
                plainText_output.insert('insert', text)
            else:
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：\n')
                ciphertext = ''
                for letter in cipherText:
                    letter = char_to_binary(letter)
                    letter = decryption(letter, key)
                    out = chr(int(letter, 2))
                    ciphertext += out
                plainText_output.insert('insert', ciphertext)

        # GUI界面
        sWelcome = tk.Label(self.page, text='解密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='ASCII', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='Binary', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, text='密文', width=9, height=3, font=('黑体', 13), bg='white')
        ciphertext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文，密钥输入栏
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.31)

        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 明文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '解密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "解密"按钮
        decrypt_button = ttk.Button(self.page, text='解密', bootstyle='success.TButton', command=decryption_ans,
                                    width=7)
        decrypt_button.place(relx=0.52, rely=0.8)  # 设计按钮的样式，大小和位置


class Crack(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.cipherText = ttk.StringVar()
        self.createPage()
        self.ans = []
        self.tag = 0
        self.first_find = {}

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        # 破解实现函数
        def worker01(num, Tid, iText, iCipher, ans):
            # 为了简便线程数量需要为2的n次方
            if not is_power_of_two(num):
                return -1
            scale = int((2 ** 16) / num)
            for index in range(Tid * scale, (Tid + 1) * scale):
                temp_key = str(bin(index)[2:].zfill(16))
                cipher = encryption(iText, temp_key)
                self.first_find[cipher] = temp_key

        def worker02(num, Tid, iText, iCipher, ans):
            print(f"Thread {Tid} is starting...")
            scale02 = int((2 ** 16) / num)
            flag02 = 0
            if self.tag == 1:
                return
            for index in range(Tid * scale02, (Tid + 1) * scale02):
                temp_key = str(bin(index)[2:].zfill(16))
                temp_ans = decryption(iCipher, temp_key)
                solved_ans = ''.join(str(i) for i in temp_ans)
                value = self.first_find.get(solved_ans, 0)
                if value != 0:
                    self.tag = 1
                    ans.append(self.first_find[solved_ans] + temp_key)
                    print("Key Found: " + self.first_find[solved_ans] + temp_key)
                    flag02 = 1
            print(len(self.ans))
            if flag02 == 0:
                print(f"Key not found in thread {Tid}\n")
                return -1

        # 创建64个线程进行密码破解
        def crack_func():
            threads = []
            start = time.time()
            for i in range(128):
                thread_id = i
                t = threading.Thread(target=worker01,
                                     args=(128, thread_id, self.plainText.get(), self.cipherText.get(), self.ans))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            print("写入已结束！")

            for i in range(128):
                thread_id = i
                if self.tag == 1:
                    break
                t = threading.Thread(target=worker02,
                                     args=(128, thread_id, self.plainText.get(), self.cipherText.get(), self.ans))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            end = time.time()
            running_time = str(end - start)
            print("运行时间为：" + running_time + "s")
            key_output.delete(0.0, tk.END)
            key_output.insert('insert', '破解结果：\n')
            for i in range(len(self.ans)):
                key_output.insert('insert', self.ans[i] + "\n")
            key_output.insert('insert', "运行时间: " + running_time + "s" + "\n")

        # GUI界面
        sWelcome = tk.Label(self.page, text='破解界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, text='明文', width=9, height=3, font=('黑体', 13), bg='white')
        ciphertext_label.place(relx=0.28, rely=0.24)
        plaintext_label = tk.Label(self.page, text='密文', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.32)

        # 明文，密文输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.26)
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.34)

        # 输出可能的密钥
        key_output = ttk.Text(self.page, height=9, width=30)
        key_output.place(relx=0.32, rely=0.45)
        key_output.insert('insert', '破解结果：')

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.83)

        # "破解"按钮
        crack_button = ttk.Button(self.page, text='破解', bootstyle='success.TButton', command=crack_func, width=7)
        crack_button.place(relx=0.52, rely=0.83)


class CBC(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.cipherText = ttk.StringVar()
        self.IVText = ttk.StringVar()
        self.button_str = StringVar()
        self.operation_str = StringVar()
        self.createPage()
        self.ans = []

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)
        self.button_str.set("明文")
        self.operation_str.set("加密")

        def select_button():
            if var.get() == 0:
                self.button_str.set("密文")
                self.operation_str.set("解密")
                return 0
            if var.get() == 1:
                self.button_str.set("明文")
                return 1

        def CBC_encryption(plaintext, IV, key):
            num_elements = (len(plaintext) + 15) // 16
            # 将字符串拆分成长度为16的元素，并在不足16位的元素左侧补全0
            char_arrays = []
            for i in range(num_elements):
                start = i * 16
                end = start + 16
                element = plaintext[start:end].ljust(16, '0')
                char_arrays.append(element)
            plaintext = char_arrays
            for i in range(len(plaintext)):
                initial_vector = IV
                plaintext[i] = ut.XOR(plaintext[i], initial_vector)
                IV, plaintext[i] = encryption(plaintext[i], key), encryption(plaintext[i], key)
            ciphertext = ''
            for i in range(len(plaintext)):
                ciphertext += plaintext[i]
            return ciphertext

        def CBC_decryption(ciphertext, initial_vector, key):
            num_elements = (len(ciphertext) + 15) // 16
            # 将字符串拆分成长度为16的元素，并在不足16位的元素左侧补全0
            char_arrays = []
            for i in range(num_elements):
                start = i * 16
                end = start + 16
                element = ciphertext[start:end].ljust(16, '0')
                char_arrays.append(element)
            ciphertext = char_arrays
            for i in range(len(ciphertext)):
                temp = ciphertext[i]
                ciphertext[i] = decryption(ciphertext[i], key)
                ciphertext[i] = ut.XOR(ciphertext[i], initial_vector)
                initial_vector = temp
            plaintext = ''
            for i in range(len(ciphertext)):
                plaintext += ciphertext[i]
            return plaintext

        def CBC_operation():
            flag = select_button()
            input_element = self.plainText.get()
            key = self.cipherText.get()
            initial_vector = self.IVText.get()
            res = ''
            if flag == 0:
                res = CBC_decryption(input_element, initial_vector, key)
            else:
                res = CBC_encryption(input_element, initial_vector, key)
            key_output.delete(0.0, tk.END)
            key_output.insert('insert', '结果：')
            key_output.insert('insert', res)

        # GUI界面
        sWelcome = tk.Label(self.page, text='Cipher Block Chaining', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='破解', variable=var, value=0, command=select_button)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='加密', variable=var, value=1, command=select_button)
        btn_bin.place(relx=0.5, rely=0.2)

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, textvariable=self.button_str, width=9, height=3, font=('黑体', 13),
                                    bg='white')
        ciphertext_label.place(relx=0.28, rely=0.24)
        plaintext_label = tk.Label(self.page, text='密钥', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.32)
        IV_label = tk.Label(self.page, text='初始向量', width=9, height=3, font=('黑体', 13), bg='white')
        IV_label.place(relx=0.28, rely=0.39)

        # 明文，密文输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.26)
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.34)
        cipherText_input = ttk.Entry(self.page, textvariable=self.IVText)
        cipherText_input.place(relx=0.43, rely=0.41)

        # 输出可能的密钥
        key_output = ttk.Text(self.page, height=9, width=30)
        key_output.place(relx=0.32, rely=0.50)
        key_output.insert('insert', '结果：')

        # 返回按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.83)

        # "确定"按钮
        crack_button = ttk.Button(self.page, textvariable=self.operation_str, bootstyle='success.TButton',
                                  command=CBC_operation, width=7)
        crack_button.place(relx=0.52, rely=0.83)


# 加密界面
class Multiple_Encryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.plainText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        def encryption_ans():
            # 这里设置检查，防止用户不合理输入
            key = self.masterKey.get()
            text = self.plainText.get()
            flag = select_button()
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            if len(text) != 16:
                tk.messagebox.showerror('Invalid PlainText', '明文错误，请重新输入')
                return -1
            for i in range(len(text)):
                if int(text[i]) != 1 and int(text[i]) != 0:
                    tk.messagebox.showerror('Invalid PlainText', '明文错误，请重新输入')
                    return -1
            if flag == 0:
                if len(key) != 32:
                    tk.messagebox.showerror('Invalid Key', '密钥长度错误，请重新输入')
                    return -1
                text = encryption(text, key[0:16])
                text = encryption(text, key[16:32])
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：')
                plainText_output.insert('insert', text)
            else:
                if len(key) != 48:
                    tk.messagebox.showerror('Invalid Key', '密钥长度错误，请重新输入')
                    return -1
                text = encryption(text, key[0:16])
                text = encryption(text, key[16:32])
                text = encryption(text, key[32:48])
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：')
                plainText_output.insert('insert', text)

        # GUI界面
        sWelcome = tk.Label(self.page, text='加密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='双重加密', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='三重加密', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 明文，主密钥输入栏
        plainText_input = ttk.Entry(self.page, textvariable=self.plainText)
        plainText_input.place(relx=0.43, rely=0.31)

        # 密钥输入显示为*号进行保密
        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 标签显示输入类别
        plaintext_label = tk.Label(self.page, text='明文', width=9, height=3, font=('黑体', 13), bg='white')
        plaintext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '加密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "加密"按钮
        encrypt_button = ttk.Button(self.page, text='加密', bootstyle='success.TButton', command=encryption_ans,
                                    width=7)
        encrypt_button.place(relx=0.52, rely=0.8)


class Multiple_Decryption(object):
    def __init__(self, master=None):
        self.page = None
        self.root = master  # 定义内部变量root
        self.root.geometry('820x660+900+450')  # 设置窗口大小
        self.cipherText = ttk.StringVar()
        self.masterKey = ttk.StringVar()
        self.ansCheck = []
        self.createPage()

    def iBack(self):
        self.page.destroy()
        Welcome(self.root)

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack(fill='both', ipadx=10, ipady=10, expand=True)

        def select_button():
            if var.get() == 0:
                return 0
            if var.get() == 1:
                return 1

        # 解密实现函数
        def decryption_ans():
            flag = select_button()
            key = self.masterKey.get()
            cipherText = self.cipherText.get()
            if len(cipherText) != 16:
                tk.messagebox.showerror('Invalid CipherText', '密文格式错误')
                return -1
            for i in range(len(key)):
                if int(key[i]) != 1 and int(key[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥内容错误,请重新输入')
                    return -1
            for i in range(len(cipherText)):
                if int(cipherText[i]) != 1 and int(cipherText[i]) != 0:
                    tk.messagebox.showerror('Invalid Key', '密钥错误，请重新输入')
                    return -1
            if flag == 1:
                if len(key) != 48:
                    tk.messagebox.showerror('Invalid Key', '密钥格式错误')
                    return -1
                text = decryption(cipherText, key[32:48])
                text = decryption(text, key[16:32])
                text = decryption(text, key[0:16])
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '解密结果：')
                plainText_output.insert('insert', text)
            else:
                if len(key) != 32:
                    tk.messagebox.showerror('Invalid Key', '密钥格式错误')
                    return -1
                plainText_output.delete(0.0, tk.END)
                plainText_output.insert('insert', '加密结果：\n')
                text = decryption(cipherText, key[16:32])
                text = decryption(text, key[0:16])
                plainText_output.insert('insert', text)

        # GUI界面
        sWelcome = tk.Label(self.page, text='解密界面', height=3, width=200,
                            bg='white',
                            font=('黑体', 20))
        sWelcome.pack()

        # 默认输入为二进制,用于判断哪个按钮被选中
        var = IntVar()
        var.set(1)
        btn_ascii = ttk.Radiobutton(self.page, text='双重加密', variable=var, value=0)
        btn_ascii.place(relx=0.32, rely=0.2)
        btn_bin = ttk.Radiobutton(self.page, text='三重加密', variable=var, value=1)
        btn_bin.place(relx=0.5, rely=0.2)

        # 标签显示输入类别
        ciphertext_label = tk.Label(self.page, text='密文', width=9, height=3, font=('黑体', 13), bg='white')
        ciphertext_label.place(relx=0.28, rely=0.28)
        key_label = tk.Label(self.page, text='主密钥', width=9, height=3, font=('黑体', 13), bg='white')
        key_label.place(relx=0.28, rely=0.36)

        # 密文，密钥输入栏
        cipherText_input = ttk.Entry(self.page, textvariable=self.cipherText)
        cipherText_input.place(relx=0.43, rely=0.31)

        masterKey_input = ttk.Entry(self.page, textvariable=self.masterKey, show='*')
        masterKey_input.place(relx=0.43, rely=0.39)

        # 明文输出
        plainText_output = ttk.Text(self.page, height=5, width=30)
        plainText_output.place(relx=0.32, rely=0.5)
        plainText_output.insert('insert', '解密结果：')

        # "返回"按钮
        quit_button = ttk.Button(self.page, text='返回', bootstyle='primary.TButton', command=self.iBack, width=7)
        quit_button.place(relx=0.35, rely=0.8)

        # "解密"按钮
        decrypt_button = ttk.Button(self.page, text='解密', bootstyle='success.TButton', command=decryption_ans,
                                    width=7)
        decrypt_button.place(relx=0.52, rely=0.8)  # 设计按钮的样式，大小和位置


win = ttk.Window()
style = Style(theme='yeti')
win.geometry('820x660+900+450')
win.title('Cryptography')
Welcome(win)
win.mainloop()
