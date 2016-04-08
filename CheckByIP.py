# -*- coding: utf-8 -*-
import subprocess
import LogFile
import Report
import threading
import time
from Serialisation import *
import pickle
from Telegram import get_constructions

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
        if status[0] == 0:
            ip_dict_write(ip, [0, 0])
        if status[0] == 1:
            if status[1]>2:
                recheckIfUnreachable(ip, ops)
                ip_dict_write(ip, [0, 0])
            else:
                ip_dict_write(ip, [1, status[1]+1])
        if status[0] == 2:
            ip_dict_write(ip, [0, 0])
        if status[0] == 3:
            ip_dict_write(ip, [1, 0])
    else:
        print("Host [{}]   \tis unreachable!".format(host))
        LogFile.newLog(host, "Unreachable")
        if int(status[0]) == 0:
            ip_dict_write(ip, [2, 0])
        if int(status[0]) == 1:
            ip_dict_write(ip, [3, 0])
        if status[0] == 2:
            if int(status[1])>2:
                recheck = threading.Thread(target=recheckIfUnreachable, args = (host, ops))
                ip_dict_write(ip, [3, 0])
                recheck.start()
            else:
                ip_dict_write(ip, [2, int(status[1])+1])
        if int(status[0]) == 3:
            ip_dict_write(ip, [3, 0])


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
    time.sleep(5)
    status = ip_dict_read(host)
    str = '..............'+'Second try'+'..............\n'
    noofpackets = 2
    timeout = 500 #in milliseconds
    command = 'ping {0} {1} -w {2} {3}'.format(ops,noofpackets,timeout,host)
    Stdout,Stderr = systemCommandCheckIP(command)
    if Stdout:
        str += ("Host [{}] is now reachable.\n".format(host))
        str += '......................................\n'
        LogFile.newLog(host, "Reachable")
        status = ip_dict_read(ip)
        if status[0] == 1:
            ip_dict_write(host, [0, 0])
        else:
            ip_dict_write(host, [1, 0])
        constructions = get_constructions()
        bot = constructions["bot"]
        for chat_id in constructions["update"]:
            bot.sendMessage(chat_id, text='{0} is online'.format(constructions[host]))
        print str
    else:
        str += ("Host [{}] is unreachable.\n".format(host))
        LogFile.newLog(host, "Unreachable")
        Report.sendEmail("ip:" + host + " is still unreachable")
        str += 'Report sent!\n'
        str += '......................................\n'
        ip_dict_write(host, [3, 0])
        constructions = get_constructions()
        bot = constructions["bot"]
        for chat_id in constructions["update"]:
            bot.sendMessage(chat_id, text='{0} is offline'.format(constructions[host]))
        print str
