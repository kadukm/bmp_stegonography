﻿Описание
--------
Стеганография в формате .bmp.
Утилита предназначена для тайной передачи данных в картинке формата .bmp методом LSB (Least Significant Bits).



Общая информация
--------
Версия: 1.1
Дата: 18.11.2017
Автор: Кадук Михаил
E-mail: mk.shark25@gmail.com



Состав
--------
Пользовательская утилита - steg.py
GUI-реализация - gui.py
Тесты - tests/
Вспомогательные модули - modules/



Справка по использованию
--------
Утилита доступна для использования в двух версиях: консольная и графическая.
Для запуска графической версии достаточно просто открыть файл "steg.py" 
****Пример запуска графической версии через консоль:
	steg.py

Для запуска утилиты через консоль доступны следующие опции:
Обязательные опции:
--encode, -e		Кодирование файла (имя файла указывается сразу после опции)
--in, -i		Картинка, в которую Вы хотите спрятать информацию (имя картинки указывается сразу после опции)
--decode, -d		Декодирование файла (имя файла указывается сразу после опции)
--as, -a		Файл, в который нужно сохранить результат работы (указывается сразу после опции)
Необязательные опции:
--with, -w		С какими параметрами шифрования кодировать/декодировать файл (параметры указываются сразу после опции)
--safe, -s		Безопасный режим (после данной опции ничего не указывается, проверяется только наличие самой опции)

Опция WITH:
После данной опции следуют параметры кодирования в следующем строковом формате: "r1g1b1".
Вместо единиц в примере выше могут стоять любые числа от 0 до 8 включительно (но не одновременно три нуля).
Буквы r, g, b могут следовать в любом порядке.
***Примеры указания опций:
	-w r1g1b1
	-w g3r0b8
	-w b0g3r4
Если эту опцию не указывать, то кодирование будет происходить в формате "r1g1b1".

Опция SAFE:
Картинка, в которой зашифрована информация, может повредиться. В некоторых случаях это особенно критично, поэтому утилитой предусмотрен безопасный режим.
При указании опции "-s", если окажется, что информация повреждена, программа экстренно завершится.
Проверка целостности информации происходит при помощи метода CRC.

****Пример шифрования файла "data.txt" в картинку "source.bmp" со стандартными параметрами кодирования, сохранив результат в "res.bmp":
	steg.py -e data.txt -i source.bmp -s res.bmp
****Пример декодирования из картинки"encoded.bmp" в файл "decoded.txt" с параметрами кодирования "r=1, g=2, b=3":
	steg.py -d encoded.bmp -a decoded.txt -w r1g2b3
****Пример безопасного декодирования из картинки "encoded.bmp" в файл "decoded.txt" со стандартными параметрами:
	steg.py -d encoded.bmp -a decoded.txt -s



Описание алгоритма кодирования
--------
Сначала считывается информация из файла, выбранного для шифрования.
Далее к полученной информации добавляется CRC-полином (в начало) и CRC-code (в конец). В итоге информация выглядит так:
	CRC-полином(65 бит) + сама_информация + CRC-код(от 0 до 64 бит - в зависимости от полинома).
Перед, непосредственно, информацией для кодирования добавляется 4 доп. байта, в которых хранится длина кодируемой информации.
Нужно это для того, чтобы при декодировании не извлекать лишние данные.
В итоге, если картинка не слишком мала, информация шифруется в нее методом LSB (Least Significant Bits) в каждый из каналов по указанным ранее параметрам кодирования.



Описание алгоритма декодирования
-------
Сначала извлекаются первые 4 байта, в которых хранится длина кодируемой информации.
Далее извлекается остальная, нужная информация.
Из этой информации береутся первые 65 бит, в которых содержится CRC-многочлен.
После чего происходит проверка целостности данных.
Если данные повреждены, в графической версии пользователь может либо продожить, несмотря на повреждения, либо отменить декодирование. В консольной версии данная опция указывается при запуске.
При продолжении из конца данных удаляется CRC-код.
Полученные после этих манипуляций данные и есть зашифрованная информация.