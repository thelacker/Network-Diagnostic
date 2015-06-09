# -*- coding: utf-8 -*-
import smtplib

#TODO:

def sendEmail(message):
    #From
    fromaddr = 'Notice <m.dyatlov.andrey@gmail.com>'
    #To
    toaddr = 'Administrator <dyatlikos3000@yandex.ru>'
    #Topic
    subj = 'Notification from system'
    #Message
    msg_txt = 'Notice:\n\n ' + message + '\n\nBye!' #

    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( fromaddr, toaddr, subj, msg_txt)


    username = 'm.dyatlov.andrey'
    password = 'cc'




    #server = smtplib.SMTP('smtp.gmail.com:587')
    #server.set_debuglevel(1);
    #server.starttls()
    #server.login(username,password)
    #server.sendmail(fromaddr, toaddr, msg)
    #server.quit()