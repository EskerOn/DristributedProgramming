import socket
import sys
from jsonutils import encodeJSON, decodeJSON, messageType
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
        try:
            connection, addr = self.server.accept()
            print(addr)
            print("{} conectado con puerto {}".format(addr[0], addr[1]))
            self.clientThread(connection, addr)
        except (KeyboardInterrupt, SystemError):
            socket.close()
            print("Servidor cerrado?")
            raise
    
    def clientThread(self, connection, addr):
        while True:
            for item in self.history:
                self.states.append(item)
            sys.stdout.write("\r"+str(self.states))
            sys.stdout.flush()
            self.states = []
            try:
                message = connection.recv(8192)
                message = decodeJSON(message)
                messagetype = message['type']
                #Chose or chage username
                if messagetype == messageType['Operation']:
                    print("recibo operación")
                    #username = message['content']
                    print(message['operation'])
                    result=eval(message['operation'])
                    print("res: {}".format(result))
                    print("Envio resultado")
                    connection.send(encodeJSON(messageType['Data'],None ,result))
                    self.history.append([message['operation'], result])
                elif messagetype == messageType['Data']:
                    self.history.append([message['operation'], message['res']])
                    connection.send(encodeJSON(messageType['Data'],None , 1))
            except:
                pass

if __name__ == "__main__":           
    server = Server(int(port))
                        