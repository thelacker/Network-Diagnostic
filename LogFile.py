# -*- coding: utf-8 -*-
import os
import datetime

#Функция создания лог файла
#Имя файла - текущая дата
def newLog(ip, check_status):
    logfilePath = os.getcwd()+"\\"+str(datetime.date.today())+".txt"
    logfile = open(logfilePath, "a+")
    defineLogTime(logfile)
    defineLogStatus(logfile, ip, check_status)

#Функция определения времени проверки
def defineLogTime(logfile): #write status into log file
    logfile.write(("Time: {0}").format(str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)))

#Функция определения статуса проверки
def defineLogStatus(logfile, ip, check_status): #write status into log file
    logfile.write(("\t\tip: {0}  \t\t Status: {1}\n").format(ip, check_status))

#Функция закрытия лог файла
def close_log(logfile):
    logfile.close()
