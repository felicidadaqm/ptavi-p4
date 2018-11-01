#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import os.path
from datetime import datetime, timedelta


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    client_dicc = {}

    def register2json(self):
        """
        Creates json file
        """
        with open('registered.json', 'w') as json_file:
            json.dump(self.client_dicc, json_file)

    def json2registered(self):
        """
        Checks if there's a json file,
        if not, it creates it
        """
        if os.path.exists('registered.json'):
            with open('registered.json', 'w') as json_file:
                json.dump(self.client_dicc, json_file)
        else:
            self.register2json()

    def timeout(self):
        """
        Searchs for expired users
        """
        user_list = []
        for user in self.client_dicc:
            expiration = datetime.strptime(
                            self.client_dicc[user][1][1], '%Y-%m-%d %H:%M:%S')
            actual_time = datetime.now()
            if actual_time >= expiration:
                user_list.append(user)
        for user in user_list:
            del self.client_dicc[user]

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """

        self.wfile.write(b"Hemos recibido tu peticion \n")
        for line in self.rfile:
            ip = self.client_address[0]

            if line.decode('utf-8') == '\r\n':
                continue
            else:
                request = line.decode('utf-8').split(" ")

            if request[0] == 'REGISTER':
                email = request[1][request[1].find(':')+1:]

            elif request[0] == 'Expires:':
                if int(request[1]) == 0 and email != "":
                    try:
                        print("\n" + "Recibida petición de borrado")
                        del self.client_dicc[email]
                        self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')
                    except KeyError:
                        print("Este usuario no existe" + "\n")
                elif email != "":
                    print("\n" + "Recibida petición de registro")
                    seconds = timedelta(seconds=int(request[1]))
                    expiration = datetime.now() + seconds
                    self.client_dicc[email] = [
                            ("address:", ip),
                            ("expires:", str(expiration)[:-7])]
                    self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')

            elif request[0] != 'REGISTER' and request[0] != 'Expires':
                email = ""
                print("\n" + "Recibida petición inválida")
                self.wfile.write(b'Peticion invalida' + b'\r\n\r\n')

        self.timeout()
        self.json2registered()
        print(self.client_dicc)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: server.py port")
        sys.exit()

    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)
    print("Lanzando servidor UDP...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
