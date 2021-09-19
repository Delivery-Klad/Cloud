import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox

root = tk.Tk()
num_pattern = r'^1[0-1]+$'
double_pattern = r'[0-9]+.[0-9]+[+e[0-9]*]?'
URL_pattern = r'^https?:\/{2}[\w-]+(\.\w+)+((\/\w+)|(\.\w+))*\/?$'

"""

http://test.tst.ru/qq/ww/ee/rr/tst.ru.ru/test.tst.test/ - True
http://test.tst.ru/qq/ww/ee/rr/tst.ru.ru/test.tst.test// - False
http://test.tst.ru/qq/ww/ee/rr/tst.ru.ru/test.tst.test..ru - False
http://test.tst.ru/123 - True
https://test.tst.ru/123 - True
https://test.tst.ru/123. - False
https://regexr.com - True
https://regexr/com - False


"""


def num(text):
    result = re.match(num_pattern, text)
    if result:
        messagebox.showinfo("Успех", "Строка является двоичным числом")
    else:
        messagebox.showerror("Провал", "Строка не является двоичным числом")


def double_num(text):
    print(text)
    result = re.findall(double_pattern, text)
    if result:
        messagebox.showinfo("Успех", "Вещественные числа: " + str(result))
    else:
        messagebox.showerror("Провал", "В строке нет вещественных чисел")


def URL(text):
    print(text)
    result = re.match(URL_pattern, text)
    if result:
        messagebox.showinfo("Успех", "Строка является корректным абсолютным URL")
    else:
        messagebox.showerror("Провал", "Строка не является корректным абсолютным URL")


label_num = tk.Label(root, font=10, text="Двоичное число", fg='black')
label_num.place(relx=0.011, rely=0.20, relwidth=0.20, relheight=0.15)

button_num = tk.Button(root, text="выбрать", bg='#2E8B57', command=lambda: num(entry_num.get()))
button_num.place(relx=0.8, rely=0.20, relwidth=0.15, relheight=0.15)

entry_num = tk.Entry(root, font=12)
entry_num.place(relx=0.19, rely=0.20, relwidth=0.60, relheight=0.15)

label_URL = tk.Label(root, font=10, text="URL", fg='black')
label_URL.place(relx=0.014, rely=0.6, relwidth=0.20, relheight=0.15)

button_URL = tk.Button(root, text="выбрать", bg='#2E8B57', command=lambda: URL(entry_URL.get()))
button_URL.place(relx=0.8, rely=0.6, relwidth=0.15, relheight=0.15)

entry_URL = tk.Entry(root, font=12)
entry_URL.place(relx=0.19, rely=0.6, relwidth=0.60, relheight=0.15)

label_double = tk.Label(root, font=10, text="Вещественное число", fg='black')
label_double.place(relx=0, rely=0.4, relwidth=0.20, relheight=0.15)

button_double = tk.Button(root, text="выбрать", bg='#2E8B57', command=lambda: double_num(entry_double.get()))
button_double.place(relx=0.8, rely=0.4, relwidth=0.15, relheight=0.15)

entry_double = tk.Entry(root, font=12)
entry_double.place(relx=0.19, rely=0.4, relwidth=0.60, relheight=0.15)

if __name__ == "__main__":
    root.title("regular expressions")
    root.geometry("1100x200")
    root.resizable(False, False)
    root.mainloop()
