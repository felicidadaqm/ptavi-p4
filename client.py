#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

try:
    server = sys.argv[1]
    port = int(sys.argv[2])
    register = str(sys.argv[3])
    dirección = str(sys.argv[4])
    expires = str(sys.argv[5])
except IndexError:
    print("Usage: client.py ip puerto registrer sip_adress expires_value")

LINE = register + " sip:" + dirección + " SIP/2.0\r\n" + "Expires: " + expires + "\r\n\r\n"

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((server, port))
        print("Enviando:", LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print('Recibido -- ', data.decode('utf-8'))

    print("Socket terminado.")
except ConnectionRefusedError:
    print("No hay ningún servidor escuchando en esa IP y puerto")
