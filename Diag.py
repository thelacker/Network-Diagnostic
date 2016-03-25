# -*- coding: utf-8 -*-
import threading
import datetime
import os
import CheckByIP


#Класс сетевой диагностики
class NetworkDiagnostic: #timer for checking
    #Конструктор класса
    #Устанавливает время таймера перезапуска и определяет операционную систему
    def __init__(self, minutes):
        self.minutes = minutes
        if os.name == "nt": #Command for windows
            self.ops = "-n"
        else:
            self.ops = "-c"

    #Функция запуска проверки ip из базы данных
    def checkByIP(self):
        if self.ops == "nt": #Command for windows
            CheckByIP.fromDataBase("ipDataBase"+".txt", self.ops)
        else:
            CheckByIP.fromDataBase(os.getcwd()+"//"+"ipDataBase"+".txt", self.ops)

    #Запуск таймера
    #Обработка ошибок, вывод их на экран и запись в лог
    def launchTimer(self):
        try:
            print '-----------------'+str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)+'----------------'
            self.checkByIP()
            threading.Timer(self.minutes, self.launchTimer).start()
        except Exception as e:
            print "\n\n"+"!!! !!! !!!"+str(e)+"!!! !!! !!!"+"\n\n"
            self.log_file_path = os.getcwd()+"\\"+str(datetime.date.today())+".txt"
            self.log_file = open(self.log_file_path, "a+")
            self.log_file.write("\n\n"+"!!! !!! !!!"+ str(e) +"!!! !!! !!!"+"\n\n")
            self.log_file.close()
            self.launchTimer()


    #Вывод первоначальной информации и запуск функции такймера
    def initDiag(self):
        print 'Diagnostic started\nPeriod - '+str(self.minutes)+' minutes'
        self.launchTimer()
