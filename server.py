import socket
import sys
import os
from jsonutils import encodeJSON, decodeJSON, messageType
import threading
from time import sleep
port = 1908
class Server():
    def __init__(self, port):
        self.HOST = "0.0.0.0"
        self.PORT = port
        self.states=list()
        self.history=list()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.HOST, self.PORT))
        except OSError:
            print("Error al hacer bind")
        self.server.listen(1)
        print("Server en la IP : {} PORT : {} ".format(self.HOST, self.PORT))

        while True:
            try:
                connection, addr = self.server.accept()
                print(addr)
                print("{} conectado con puerto {}".format(addr[0], addr[1]))
                self.myThread = threading.Thread(target= self.clientThread, args=(connection, addr))
                #self.myThread.setDaemon = True
                self.myThread.start()
                #self.clientThread(connection, addr)
            except (KeyboardInterrupt, SystemError):
                socket.close()
                print("Servidor cerrado?")
                raise
    
    def clientThread(self, connection, addr):
        nclose = True
        while nclose:
            os.system("cls")
            for item in self.history:
                self.states.append(item)
            if self.states:
                print("Historial:\nOperación    -   Resultado")
                #sys.stdout.write("\r"+str(self.states))
                #sys.stdout.flush()
                for state in self.states:
                    print("{} -> {}".format(state[0], state[1]))
                self.states = []
            else:
                print("Sin historial")
            try:
                message = connection.recv(8192)
                message = decodeJSON(message)
                messagetype = message['type']
                #Chose or chage username
                if messagetype == messageType['Operation']:
                    print("Recibo operación: ", end="\r")
                    sleep(0.5)
                    print(" "*len("Recibo operación: "), end="\r")
                    
                    #username = message['content']
                    print(message['operation'], end = "\r")
                    sleep(0.5)
                    print(" "*len(message['operation']), end="\r")
                    try:
                        result=eval(message['operation'])
                    except:
                        result = "Syntax error"
                    #print("Resultado: {}".format(result), end="\r")
                    #sleep(0.5)
                    #print(" "*len(message['operation']), end="\r")
                    print("Envio resultado: {}".format(result), end="\r")
                    sleep(0.5)
                    print(" "*len("Envio resultado: {}".format(result)), end="\r")
                    connection.send(encodeJSON(messageType['Data'],None ,result))
                    self.history.append([message['operation'], result])
                elif messagetype == messageType['Data']:
                    self.history.append([message['operation'], message['res']])
                    connection.send(encodeJSON(messageType['Data'],None , 1))
                elif messagetype == messageType['Exit']:
                    connection.send(encodeJSON(messageType['Exit'],None , 1))
                    nclose = False
            except:
                pass

if __name__ == "__main__":           
    server = Server(int(port))
                        