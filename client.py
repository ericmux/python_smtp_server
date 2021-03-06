#!/usr/bin/python
import sys
import socket
import datetime
import time

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
toaddr = sys.argv[3] if len(sys.argv) > 3 else "nobody@example.com"
fromaddr = sys.argv[4] if len(sys.argv) > 4 else "nobody@example.com"

def send(socket, message):
    # In Python 3, must convert message to bytes explicitly.
    # In Python 2, this does not affect the message.
    socket.send(message.encode('utf-8'))

def sendmsg(msgid, hostname, portnum, sender, receiver):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, portnum))

        send(s, "HELO %s\r\n" % socket.gethostname())
        print(s.recv(1000))

        send(s, "MAIL FROM: %s\r\n" % sender)
        print(s.recv(1000))

        send(s, "RCPT TO: %s\r\n" % receiver)
        print(s.recv(1000))

        send(s, "RCPT TO: %s\r\n" % receiver)
        print(s.recv(1000))

        ## Send bogus commands.
        st = time.time()
        for i in xrange(11):
            time.sleep(1.0)
            print time.time() - st
            send(s, "MAIL FROM: %s\r\n" % sender)
            print(s.recv(1000))

        send(s, "DATA\r\nFrom: %s\r\nTo: %s\r\nDate: %s -0500\r\nSubject: msg %d\r\n\r\nContents of message %d end here.\r\n.\r\n" % (sender, receiver, datetime.datetime.now().ctime(), msgid, msgid))

        time.sleep(1.0)

        print(s.recv(1000))
    except IOError:
        pass


    print "END %d" % msgid

for i in range(1, 10):
    sendmsg(i, host, port, fromaddr, toaddr)
