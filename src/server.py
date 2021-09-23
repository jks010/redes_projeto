import socket
import threading

class Server:
    def __init__(self):
        self.start_server()

    def start_server(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Digite a porta para conexão --> '))

        self.clients = []

        self.s.bind((host,port))
        self.s.listen(100)
        
        print('host: '+str(host))
        print('port: '+str(port))

        self.username_lookup = {}

        while True:
            c, addr = self.s.accept()

            username = c.recv(1024).decode()
            #pas = c.recv(1024).decode()
            #self.senha(pas,c)
        
            print('Novo usuario. User: '+str(username))
            self.broadcast('Um novo usuário na sala. User: '+username)

            self.username_lookup[c] = username
            
            self.clients.append(c)
             
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
    
    
    def broadcast(self,msg):
        for connection in self.clients:
            connection.send(msg.encode())

    def handle_client(self,c,addr):
        while True:
            try:
                msg = c.recv(1024)
            except:
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                
                print(str(self.username_lookup[c])+' saiu.')
                self.broadcast(str(self.username_lookup[c])+' saiu da sala.')

                break

            if msg.decode() == self.username_lookup[c]+' - quit':
                c.shutdown(socket.SHUT_RDWR)
                self.clients.remove(c)
                print(str(self.username_lookup[c])+' saiu.')
                self.broadcast(str(self.username_lookup[c])+' saiu da sala.')

                break
            if msg.decode() != '':
                print('\nNova mensagem: '+str(msg.decode()))
                for connection in self.clients:
                    if connection != c:
                        connection.send(msg)

server = Server()
