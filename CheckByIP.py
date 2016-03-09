# -*- coding: utf-8 -*-
import subprocess
import LogFile
import Report
import threading
import time
import pickle


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
    status = ip_dict_read(ip)
    host = ip
    noofpackets = 2
    timeout = 5 #in milliseconds
    command = 'ping {0} {1} -w {2} {3}'.format(ops,noofpackets,timeout,host)
    Stdout,Stderr = systemCommandCheckIP(command)
    if Stdout:
        print("Host [{}]   \tis reachable.".format(host))
        LogFile.newLog(host, "Reachable")
        ip_dict_write(ip, 0)
    else:
        print("Host [{}]   \tis unreachable!".format(host))
        LogFile.newLog(host, "Unreachable")
        recheck = threading.Thread(target=recheckIfUnreachable, args = (host, ops))
        if status == 0:
            ip_dict_write(ip, 1)
        if status == 1:
            ip_dict_write(ip, 2)
            recheck.start()


def ip_dict_write(ip, status):
    ip_dict = {}
    with open('ip_dict.txt', 'rb') as f:
        try:
            ip_dict = pickle.load(f)
        except:
            pass
    if status == 0:
        ip_dict[ip] = 0
    elif status == 1:
        ip_dict[ip] = 1
    elif status == 2:
        ip_dict[ip] = 2
    else:
        ip_dict[ip] = 3
    with open('ip_dict.txt', 'wb') as f:
        pickle.dump(ip_dict, f)


def ip_dict_read(ip = None):
    ip_dict = {}
    with open('ip_dict.txt', 'rb') as f:
        try:
            ip_dict = pickle.load(f)
        except:
            pass
    if ip == None:
        return ip_dict
    else:
        try:
            if ip_dict[ip]:
                return ip_dict[ip]
            else:
                return 0
        except:
            return 0


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
    time.sleep(1)
    str = '..............'+'Second try'+'..............\n'
    noofpackets = 2
    timeout = 500 #in milliseconds
    command = 'ping {0} {1} -w {2} {3}'.format(ops,noofpackets,timeout,host)
    Stdout,Stderr = systemCommandCheckIP(command)
    if Stdout:
        str += ("Host [{}] is now reachable.\n".format(host))
        str += '......................................\n'
        LogFile.newLog(host, "Reachable")
        ip_dict_write(host, 1)
        print str
    else:
        str += ("Host [{}] is unreachable.\n".format(host))
        LogFile.newLog(host, "Unreachable")
        Report.sendEmail("ip:" + host + " is still unreachable")
        str += 'Report sent!\n'
        str += '......................................\n'
        ip_dict_write(host, 3)
        print str
