// Автор: Бовкун Екатерина
// Время создания: 11.04.2022 14:20
// Версия: 0.3

// Метод, обеспечивающий обмен данными между Arduino и компьютером
void setup() {
  Serial.begin(9600); //инициализируем обмен данными по серийному протоколу со скоростью 9600 baud
  establishContact(); // вызов функции establishContact
  delay(500);
}

// Метод, обеспечивающий бесконечный повтор нашей программы
void loop() {
      Serial.print(analogRead(A1)); // считываем с пина А1
      Serial.print(" ");
      Serial.println(analogRead(A5)); // считаем с пина А5
      delay(1000);
}

// Метод establishContact() отсылает строку, которую мы ожидаем получить в Processing. 
// Если ответ приходит, значит Processing может получить данные.
void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print("A"); // отсылает заглавную A
    delay(300);
  }
}
