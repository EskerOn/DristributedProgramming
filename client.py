import socket
import threading
import random
import time
from jsonutils import encodeJSON, decodeJSON, messageType
class Client():
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer = ""
        self.reciver = None
        try:
            self.client.connect((self.HOST, self.PORT))
            print("[SERVER]: Conexion establecida")
            self.startListenServer()
        except socket.error:
            print("constructor error")
        
        
    def startListenServer(self):
        self.reciver = threading.Thread(target=self.receiveMessage)
        #self.reciver.setDaemon(True)
        self.reciver.start()    

    def receiveMessage(self):
        while True :
            try:
                #print("atento")
                #print("recibiendo mensajes")
                message = self.client.recv(8192)
                message = decodeJSON(message)
                if message['type'] == messageType['Data']:
                    #print("recibo")
                    result= message['res']
                    #time.sleep(2)
                    self.buffer=result
                elif message['type'] == messageType['Exit']:
                    print("JOJO")
                    break
            except socket.error:
                print("socket error")
                pass
            except ValueError:
                print("socket error")
                pass
        print("JUASJUAS")

    def getBuffer(self):
        time.sleep(1)
        response=self.buffer
        self.buffer=None
        return response

    def sendMessage(self, op, res=None):
        #while True :
        try:
            if res == None:
                self.client.send(encodeJSON(messageType['Operation'], op))
            elif res =="S":
                self.client.send(encodeJSON(messageType['Exit'], op))
            else:
                self.client.send(encodeJSON(messageType['Data'], op, res))
        except socket.error:
            pass
        except ValueError:
            pass
def main():
    mode=(int(input('Elige modo: 0 =cliente ligero, 1 = balanceado, 2 = pesado: ')))
    #mode=0 0 =cliente ligero, 1 = balanceado, 2 = pesado
    op=None
    cl= Client('127.0.0.1', 1908)
    print('Calculadora basica:\nEscribe tu operación y presiona enter\nPor ejemplo: a + b \nPara salir escribe "S".')
    op=input('Introduce tu operación: ')
    while not (op == 'S'):
        if mode == 0:
            cl.sendMessage(op)
            res=cl.getBuffer()
            print("= {}".format(res))
        elif mode == 1:
            if random.randint(0,100)%2 == 0:
                cl.sendMessage(op)
                res=cl.getBuffer()
                print("= {}".format(res))
            else:
                res=eval(op)
            cl.sendMessage(op, res)
            if cl.getBuffer() == 1:
                print("= {}".format(res))
            else:
                print("Error de comunicación")
        elif mode == 2:
            res=eval(op)
            cl.sendMessage(op, res)
            if cl.getBuffer() == 1:
                print("= {}".format(res))
            else:
                print("Error de comunicación")
        op=input('Introduce tu operación: ')
    cl.sendMessage("S","S")
    print("JAJA")    
    #cl.client.close()

main()
