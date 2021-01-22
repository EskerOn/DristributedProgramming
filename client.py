import socket
import threading
import random
import time
from tkinter import *
from tkinter import ttk
from calc import Calculator
from tkinter import messagebox
import client
import argparse
from jsonutils import encodeJSON, decodeJSON, messageType
modes = {
    '0' : 'ligero',
    '1' : 'Balanceado',
    '2' : 'Pesado',
}
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
                    #print("JOJO")
                    break
            except socket.error:
                print("socket error")
                pass
            except ValueError:
                print("socket error")
                pass
        #print("JUASJUAS")

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


def on_closing():
        if messagebox.askokcancel("Salir", "Estás seguro de salir?"):
            cl.sendMessage("S","S")
            root.destroy()
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Calculadora Básica.')
    parser.add_argument('modo',help='Elige modo: \n0 =Cliente ligero, \n1 = Balanceado, \n2 = Pesado:\n')
    args = parser.parse_args()
    mode=int(args.modo)   
    cl= client.Client('127.0.0.1', 1908)
    root = Tk()
    root.title("Calculadora")
    calculator=Calculator(root, cl, mode)
    root.bind('<Return>', calculator.result)
    s=ttk.Style()
    #print(s.theme_names())
    s.theme_use('clam')
    #root.geometry("250x200") definir el tamaño por defecto
    root.resizable(0,0)
    messagebox.showinfo(message="La calculadora se está ejecutando en modo {}".format(modes['{}'.format(mode)]), title="Modo")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
