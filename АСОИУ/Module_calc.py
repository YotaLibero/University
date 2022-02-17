import math
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

    def square(self, a, b, c):
        discr = b ** 2 - 4 * a * c
        print("Дискриминант D = %.2f" % discr)
        if discr > 0:
            x1 = (-b + math.sqrt(discr)) / (2 * a)
            x2 = (-b - math.sqrt(discr)) / (2 * a)
            print("x1 = " + float("{0:.2f}".format(x1)) + "и" + "x2 = " + float("{0:.2f}".format(x2)))
            res = str("x1 = " + str(float("{0:.2f}".format(x1))) + "  и " +" x2 = " + str(float("{0:.2f}".format(x2))))
            result_x.set(res)
            return res
        elif discr == 0:
            x = -b / (2 * a)
            print("x = %.2f" % x)
            res = str("x = " + str(float("{0:.2f}".format(x))))
            result_x.set(res)
            return res
        else:
            print("Корней нет")
            res = str("Корней нет")
            result_x.set(res)
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


a = Label(root, text="a")
a.grid(row=0, column=0)
b = Label(root, text="b")
b.grid(row=1, column=0)
c = Label(root, text="c")
c.grid(row=2, column=0)

number_a = StringVar()
number_a.set('0')
Entry(root, textvariable=number_a).grid(row=0, column=1, sticky=W + E)
number_b = StringVar()
number_b.set('0')
Entry(root, textvariable=number_b).grid(row=1, column=1, sticky=W + E)
number_c = StringVar()
number_c.set('0')
Entry(root, textvariable=number_c).grid(row=2, column=1, sticky=W + E)
res = Label(root, text="=")
res.grid(row=3, column=1)
result_x = StringVar()
result_x.set('0')
Label(root, textvariable=result_x).grid(row=4, column=1)


number1 = StringVar()
number1.set('0')
Entry(root, textvariable=number1).grid(row=0, column=2, sticky=W + E)
number2 = StringVar()
number2.set('0')
Entry(root, textvariable=number2).grid(row=1, column=2, sticky=W + E)
equ = Label(root, text="=")
equ.grid(row=2, column=2)
result = StringVar()
result.set('0')
Label(root, textvariable=result).grid(row=3, column=2)

div = Button(root, text="/", command=lambda: Calculator.divide(root, float(number1.get()), float(number2.get())))
div.grid(row=0, column=3)
mul = Button(root, text="*", command=lambda: Calculator.multiply(root, float(number1.get()), float(number2.get())))
mul.grid(row=1, column=3)
mns = Button(root, text="-", command=lambda: Calculator.subtract(root, float(number1.get()), float(number2.get())))
mns.grid(row=2, column=3)
pls = Button(root, text="+", command=lambda: Calculator.add(root, float(number1.get()), float(number2.get())))
pls.grid(row=3, column=3)
computation = Button(root, text="Рассчитать", command=lambda: Calculator.square(root, float(number_a.get()), float(number_b.get()), float(number_c.get())))
computation.grid(row=4, column=3)
root.mainloop()
