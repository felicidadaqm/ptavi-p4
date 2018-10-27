#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    #line = str(" ".join(sys.argv[3::]))
    register = str(sys.argv[3])
    dirección = str(sys.argv[4])
except IndexError:
    print("Usage: client.py ip puerto registrer dirección")
    sys.exit()

LINE = register + " sip:" + dirección + " SIP/2.0"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
