#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    client_dicc={}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion \n")
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'))
            petición = line.decode('utf-8').split(" ")

            if petición[0] == 'REGISTER':
                dirección = petición[1][petición[1].find(':')+1:]
                ip = self.client_address[0]
                self.client_dicc[dirección] = ip
                self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')

            elif petición[0] == 'Expires:' and int(petición[1]) == 0:
                del self.client_dicc[dirección]
                self.wfile.write(b'SIP/2.0 200 OK' + b'\r\n\r\n')

        print(self.client_dicc)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegistrerHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
