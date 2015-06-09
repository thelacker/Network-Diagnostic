# -*- coding: utf-8 -*-
import subprocess
import LogFile
import Report
import threading
import time


#Функция вызова системной функции ping
#Обработка ошибок
def systemCommandCheckIP(Command):
    Output = None
    Error = None
    try:
        Output = subprocess.check_output(Command,stderr = subprocess.STDOUT,shell='True')
    except subprocess.CalledProcessError as e:
        Error =  e.output #Invalid command raises this exception
    if Output:
        Stdout = Output.split("\n")
    else:
        Stdout = []
    if Error:
        Stderr = Error.split("\n")
    else:
        Stderr = []
    return (Stdout,Stderr)


#Функция проверки доступности ip
#Задает необходимые параметры и вызывает системную функцию
#Вывод на экран информации о доступности ip
#Запись результатов в лог
def checkReachability(ip, ops):
    host = ip
    noofpackets = 2
    timeout = 5000 #in milliseconds
    command = 'ping {0} {1} -w {2} {3}'.format(ops,noofpackets,timeout,host)
    Stdout,Stderr = systemCommandCheckIP(command)
    if Stdout:
        print("Host [{}]   \tis reachable.".format(host))
        LogFile.newLog(host, "Reachable")
    else:
        print("Host [{}]   \tis unreachable!".format(host))
        LogFile.newLog(host, "Unreachable")
        recheck = threading.Thread(target=recheckIfUnreachable, args = (host, ops))
        recheck.start()


#Функцию чтения ip из базы данных
def fromDataBase (ipDataBase, opSys):
    ipDataBase = open(ipDataBase, "r")
    for ip in ipDataBase:
        if ip.find('#') == -1:
            checkReachability(ip.replace("\n", ""), opSys)
        else:
            pass
    ipDataBase.close()

#Функция повторной проверки доступности ip при первой неудаче
#Функция вызывается в отдельном потоке и,
# после некоторого ожидания, смотрит доступность снова
def recheckIfUnreachable(host, ops):
    time.sleep(180)
    print '..............'+'Second try'+'..............'
    noofpackets = 2
    timeout = 5000 #in milliseconds
    command = 'ping {0} {1} -w {2} {3}'.format(ops,noofpackets,timeout,host)
    Stdout,Stderr = systemCommandCheckIP(command)
    if Stdout:
        print("Host [{}] is now reachable.".format(host))
        print '......................................'
        LogFile.newLog(host, "Reachable")
    else:
        print("Host [{}] is unreachable.".format(host))
        LogFile.newLog(host, "Unreachable")
        Report.sendEmail("ip:" + host + " is still unreachable")
        print 'Report sent!'
        print '......................................'
