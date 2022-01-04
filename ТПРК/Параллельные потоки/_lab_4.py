import random
from threading import Thread, Condition

condition = Condition() # Условная переменная для синхрона 2-х потоков
buffer = []

cnt_operations = 1000 # Количество операций
N = 3

def create_array(): # функция для генерации массива
    for _ in range(cnt_operations):
        condition.acquire() # блокировка ресурсов всех потоков (thread2), кроме текущего
        while len(buffer) >= N:
            condition.wait() # снятие блокировки, а затем происходит блокирование исполнения кода, до тех пор, пока другой поток не разбудит его, вызвав метод .notify()
        buffer.append(random.randint(10, 20))
        condition.notify() # пробуждение одного из потоков,ожидающих переменной условия, если таковые ожидают
        condition.release() # освобождение базовой блокировки

def if_second(): # функция для извлечения и возведения 2-го числа из сгенерированного массива
    count = 0
    for _ in range(cnt_operations-1):
        condition.acquire() # блокировка ресурсов всех потоков (thread1), кроме текущего
        while len(buffer) < N-1:
            condition.wait() # снятие блокировки, а затем происходит блокирование исполнения кода, до тех пор, пока другой поток не разбудит его, вызвав метод .notify()
        print("из 2п:" + str(buffer))
        if _ == 998:
            print("Первый поток" + "        " + str(999) + "        " + str(buffer[len(buffer) - 2]))
            print("Первый поток" + "        " + str(1000) + "        " + str(buffer[len(buffer) - 1]))
        else:
            print("Первый поток" + "        " + str(count + 1) + "        " + str(buffer[0]))
            print("Первый поток" + "        " + str(count + 2) + "        " + str(buffer[1]))
            if len(buffer) == N:
                print("Первый поток" + "        " + str(count + 3) + "        " + str(buffer[len(buffer) - 1]))
        print("---------------------------------–")
        print("Второй поток" + "        " + str(_+1) + "        " + str(buffer[1]**2))
        print("---------------------------------–")
        print("Удаляем:" + str(buffer.pop(0)))
        count += 1

        condition.notify() # пробуждение одного из потоков,ожидающих переменной условия, если таковые ожидают
        condition.release() # освобождение базовой блокировки


if __name__ == '__main__': # Главная функция, где вызываются потоки

    print("Номер потока     |  №  |  Значение")

    thread1 = Thread(target=create_array)
    thread2 = Thread(target=if_second)

    thread1.start() # вызов потока 1
    thread2.start() # вызов потока 2

    thread1.join() # завершение потока 1
    thread2.join() # завершение потока 2
