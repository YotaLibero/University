from tkinter import Tk, W, E, Label, DoubleVar, StringVar
from tkinter.ttk import Frame, Button, Entry, Style


class Calculator:
    def __init__(self):
        pass

    def add(self, x1, x2):
        res = x1 + x2
        print(res)
        result.set(str(res))
        return res

    def multiply(self, x1, x2):
        res = x1 * x2
        print(res)
        result.set(str(res))
        return res

    def subtract(self, x1, x2):
        res = x1 - x2
        print(res)
        result.set(str(res))
        return res

    def divide(self, x1, x2):

        if (x2 == 0) & (x1 == 0):
            print(0)
            result.set("0")
            return 0

        if x2 != 0:
            res = x1 / x2
            result.set(str(res))
            print(res)
            return res

root = Tk()
root.title("Калькулятор на Tkinter")

Style().configure("TButton", padding=(0, 5, 0, 5), font='serif 10')

root.columnconfigure(0, pad=3)
root.columnconfigure(1, pad=3)

root.rowconfigure(0, pad=3)
root.rowconfigure(1, pad=3)
root.rowconfigure(2, pad=3)
root.rowconfigure(3, pad=3)

number1 = StringVar()
number1.set('0')
Entry(root, textvariable=number1).grid(row=0, column=0, sticky=W + E)
number2 = StringVar()
number2.set('0')
Entry(root, textvariable=number2).grid(row=1, column=0, sticky=W + E)
result = StringVar()
result.set('0')
Label(root, textvariable=result).grid(row=3, column=0)

div = Button(root, text="/", command=lambda: Calculator.divide(root, float(number1.get()), float(number2.get())))
div.grid(row=0, column=1)
mul = Button(root, text="*", command=lambda: Calculator.multiply(root, float(number1.get()), float(number2.get())))
mul.grid(row=1, column=1)
equ = Label(root, text="=")
equ.grid(row=2, column=0)
mns = Button(root, text="-", command=lambda: Calculator.subtract(root, float(number1.get()), float(number2.get())))
mns.grid(row=2, column=1)
pls = Button(root, text="+", command=lambda: Calculator.add(root, float(number1.get()), float(number2.get())))
pls.grid(row=3, column=1)
root.mainloop()
