#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time
from datetime import datetime, timedelta


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
                    caduc = time.ctime(time.time() + int(petición[1]))
                    GTM_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
                    caducidad = str(GTM_time + " +" + petición[1][:-2])

                    seconds = timedelta(seconds=int(petición[1]))
                    caducid = datetime.now() + seconds
                    print(datetime.now() + seconds)
                    
                    print(time.strftime('%Y-%m-%d %H:%M:%S'))
                    print(caduc)

                    self.client_dicc[dirección] = [("address:", ip), ("expires:", caducidad)]
                    self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')     

 
        for user in self.client_dicc:
            caducidad = self.client_dicc[user][1][1]
            actual_time = datetime.now()
            print(caducidad) # ME HE QUEDADO POR AQUÍ


        print(self.client_dicc)
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
