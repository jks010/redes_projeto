import PySimpleGUI as sg
import socket
import threading
from collections import deque

class Chat():
    def __init__(self):
        
   
    
        sg.theme('DarkAmber')
        
        layout = [  

        [sg.Text(size=(30,3), key=1)],
        [sg.Text(size=(30,3), key=2)],
        [sg.Text(size=(30,3), key=3)],
        [sg.Text(size=(30,3), key=4)],

        [sg.Text(size=(30,3), key=5)],
        [sg.Text(size=(30,3), key=6)],
        [sg.Text(size=(30,3), key=7)],
        [sg.Text("Digite o nome do Usuário", size=(30,3), key=8)],


        [sg.InputText(key='input')],

        [sg.Button('Enviar'), sg.Button('Sair')] ]

        
        self.window = sg.Window('Window Title', layout)
        

        text = []
        self.i=1
        self.flag=1
        
        self.rec = deque()
        self.rec.append('') 
        
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    
        host = '127.0.0.1'
        
        port  = 5556
        self.s.connect((host,port))
        
       

        while True:
            event, self.values = self.window.read()


            username =  self.values['input']
            if event == 'Enviar':
                self.window['input'].update('')
                self.window[8].update('')
                self.s.send(username.encode())
                break

        receive_msgs = threading.Thread(target=self.recv,args=())
        receive_msgs.setDaemon(True)
        receive_msgs.start()
         
        while True:
            event, self.values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Sair': # if user closes window or clicks cancel
                self.s.send((username+' - quit').encode())        
                #self.s.close()
                
                self.flag=0
                break
            
            text.append(self.values['input'])
            self.rec.append(username+' - '+self.values['input'])
            self.s.send((username+' - '+self.values['input']).encode())

            self.array2keys()
            
            self.window['input'].update('')
            

            
    
    def recv(self):
        
        while self.flag==1:     
            
            self.rec.append(self.s.recv(1204).decode())
            
            self.array2keys()
            
        self.s.close() 
        


    def array2keys(self):
        if(len(self.rec)>8):
            self.rec.popleft()
        for c in range(1,len(self.rec)):
            self.window[c].update(self.rec[c])
    

#s.close()
#window.close()


c = Chat()
