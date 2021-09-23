import socket
import threading


class Client:
    
    def __init__(self):
        

       
     self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
        while 1:
            try:
                #host = input('Enter host name --> ')
                #port = int(input('Enter port --> '))
                host  = '127.0.0.1'
                port  = 5556
                self.s.connect((host,port))
                
                break
            except:
                print("Erro de conexão")

        self.username = input('Digite o nome de usuário --> ')
        self.s.send(self.username.encode())
        

        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_thread = threading.Thread(target=self.input_handler,args=("continue",))
        input_thread.start()
        
    def handle_messages(self):
        flag=1 
        while flag:
            try:
                print(self.s.recv(1204).decode())
                
            except:
                print("Até")
                flag=0
        
    
    def input_handler(self,arg):
        current_t = threading.currentThread()
        msg = '' 
        
       
        while(msg!='quit'):
            msg = input()
            self.s.send((self.username+' - '+msg).encode())
            
            current_t = False
        
        self.s.close()
        
        

client = Client()
