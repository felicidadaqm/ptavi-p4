#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    client_dicc={}

    def register2json(self):
        with open('registered.json', 'w') as json_file:
            json.dump(self.client_dicc, json_file)

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
                print("El cliente nos manda ", line.decode('utf-8'))
                petición = line.decode('utf-8').split(" ")

            if petición[0] == 'REGISTER':
                dirección = petición[1][petición[1].find(':')+1:]
                self.client_dicc[dirección] = ("address:", ip)
                self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')

            elif petición[0] == 'Expires:':
                if int(petición[1]) == 0:
                    del self.client_dicc[dirección]
                    self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')  
                else:
                    self.client_dicc[dirección] = [("address:", ip), ("expires:", int(petición[1]))]
                    self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')     

        print(self.client_dicc)
        print("-------")
        self.register2json()

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
        SIPRegisterHandler.register2json()
    except KeyboardInterrupt:
        print("Finalizado servidor")
