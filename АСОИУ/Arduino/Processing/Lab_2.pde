// Авторы: Бовкун Екатерина
// Время создания: 11.04.2022 14:20
// Версия: 0.3

import processing.serial.*; // подключаем библиотеку Serial

float internalTemp; // переменная, которая будет хранить значение "влажности"
float internalCelsius; // переменная, которая будет хранить значение "температуры"
String myString = null; // изначально имеем пустую строку
Serial myPort; // Порт

boolean firstContact = true; // первый контакт
boolean sucContact = false; // успешность коннекта

// метод инициализации
void setup() {
  size(700, 700); // размер окна
  myPort = new Serial(this, "COM10", 9600); // задаём параметры порта, с которым будем работать
}

// отображение данных в самом приложении 
// (т.е. методспециальный системный метод, который отвечает за внешнюю 
// оболочку приложения)
void draw() {
  // если контакт не удался (например, изменена скорость), то выполняется данный if
  if (sucContact == false) {
    background(0); // фон: чёрный
    textSize(34); // размер шрифта
    // отображение строки(строка, отступ слева, отступ сверху
    text("Выберите скорость 9600 baud", 50, 50);  
    return;
  }
  // если контакт успешный (поступило в порт значение из Arduino [А]), 
  // то проходим по данному циклу
  while (myPort.available() > 0) { // хоть что-то появилось новое
    background(0);
    textSize(34);
    myString = myPort.readStringUntil('\n');
    if (myString != null) {
      println(myString);
      
      String[] q = splitTokens(myString); // работать будем со строковыми значениями (всегда)
      internalTemp = parseFloat(q[0]); // парсим первое значение массива q
      internalCelsius = parseFloat(q[1]); // парсим второе значение массива q      
      
      // отображение данных (температура и влажность) в приложении
      text("Влажность: ", 50, 100);
      text(internalCelsius, 350, 100);
      text("Температура: ", 50, 150);
      text(internalTemp, 350, 150);
    }
  }
}

// Обработчик событий порта Serial
void serialEvent( Serial myPort) { //формируем строку из данных, которые поступают
  if (firstContact) {
    myString = myPort.readString(); //убеждаемся, что наши данные не пустые перед тем, как продолжить
    println(myString);
    // если приходит на вход А, то очищаем данные порта и отправляем В, 
    // чтобы выйти из цикла в методе establishContact() в Arduino 
    if (myString.equals("A")) {
      myPort.clear();
      myPort.write("B");
      sucContact = true;
      println("Законектился...");
      myPort.bufferUntil('\n');
    }
    firstContact = false; // обращаем в false, тк изначально сюда заходим,
    // соответственно, уже не будет являться первым входом
    println("Я ТУТЬ!");
    return;
  }
}
