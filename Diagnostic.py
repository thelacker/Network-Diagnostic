# -*- coding: utf-8 -*-
import sys
#TODO:
sys.path.insert(0, 'D:\GitHub\Diag')
import Diag
import threading

#TODO:
#Функция запускка программы
#Создается поток цель которого - мониторинг командной строки
#Основной поток запускает диагностику сети и вызывает запуск таймера
def main():
    console = threading.Thread(target=ConsoleInput())
    console.start()
    timer = Diag.NetworkDiagnostic(1)
    timer.initDiag()

#TODO:
#Функция мониторинга командной строки для ввода команд
def ConsoleInput():
    switch = None
    if switch == 'exit':
        sys.exit()
    elif switch=='help':
        pass
    else:
        'Invalid command. Use \'help\' for list of commands'



#Перенаправление на запуск программы
if __name__ == "__main__":
    main()