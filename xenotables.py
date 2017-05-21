import socket
import json
from threading import Thread


class XenoTable:
    def __init__(self,ip,port):
        self.__connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__connection.connect((ip,port))
        self.ip = ip
        self.port = port
        self.recv(1)
    def save(self,string):
        self.send("S*" + string + "*")
        return self.recv(1)[0] == "true"
    def load(self,string):
        self.send("L*" + string + "*")
        return self.recv(1)[0] == "true"
    def run(self,msg):
        self.send("R*" + msg + "*")
    def recv(self,limit):
        command = ""
        num = 0
        while True:
            char = self.__connection.recv(1).decode("UTF-8")
            if char == "*":
                num += 1
                if num == limit:
                    break
            command += char
        return command.split("*")
    def send(self,msg):
        self.__connection.send(msg.encode("UTF-8"))
    @property
    def ping(self):
        self.send("I*")
        self.recv(1)
        return True
    def put(self,name,val):
        illegals = ["*","\\","/"]
        val = json.dumps(val)
        check = [name,val]
        names = ["Identifier" , "Value"]
        for item in range(len(check)):
            for ill in illegals:
                if ill in check[item]:
                    raise NameError(names[item] + " cannot contain " + ill)
        self.send(("P*" + name + "*" + val + "*"))
    def get(self,name):
        if "*" in name:
            raise NameError("Identifier cannot contain *")
        self.send("G*" + name + "*")
        command = self.recv(1)
        if command[0] == "KeyError":
            raise KeyError("The data for the given key was not found")
        else:
            return json.loads(command[0])
    def getAll(self):
        return self.get("../")
    def pop(self,name):
        self.send("O*" + name + "*")
        command = self.recv(1)
        if command[0] == "KeyError":
            raise KeyError("The data for the given key was not found")
        else:
            return json.loads(command[0])
    def getCallable(self,name,call):
        if "*" in name:
            raise NameError("Identifier cannot contain *")
        if "*" in call:
            raise NameError("Call cannot contain *")
        self.send("M*" + name + "*" + call + "*")
        command = self.recv(1)
        if command[0] == "KeyError":
            raise KeyError("The data for the given key was not found")
        elif command[0] == "IndexError":
            raise IndexError("list index out of range")
        elif command[0] == "TypeError":
            raise TypeError("Object not subscriptable")
        elif command[0] == "SyntaxError":
            raise SyntaxError("invalid syntax")
        else:
            return json.loads(command[0])
    def append(self,name,data):
        self.send("A*" + name + "*" + json.dumps(data) + "*")
        command = self.recv(1)
        if command[0] == "AttributeError":
            raise AttributeError("Data has no attribute 'append'")
    def getNewTable(self):
        self.send("N*")
        command = ""
        while True:
            char = self.__connection.recv(1).decode("UTF-8")
            if char == "*":
                break
            command += char
        return XenoTable(self.ip,int(command))
    def closeServer(self):
        self.send("C*close*")
        self.__connection.close()
    def logout(self):
        self.send("C*logout*")
        self.__connection.close()
    def __str__(self):
        return "XenoTable bound to " + self.ip + ":" + str(self.port)
class Communicator(Thread):
    Communicators = {}
    CurrentPort = 80
    debug = True
    
    @staticmethod
    def myIP():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    @staticmethod
    def localSock():
        ip = CC.myIP()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                sock.bind((ip,Communicator.CurrentPort))
                break
            except OSError as e:
                Communicator.CurrentPort += 1
                if Communicator.debug:
                    print(Communicator.CurrentPort)
        return sock      
    
    @staticmethod
    def createSock(ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                sock.bind((ip,Communicator.CurrentPort))
                break
            except OSError as e:
                Communicator.CurrentPort += 1
                if Communicator.debug:
                    print(Communicator.CurrentPort)
        return sock

    def init(self,sock,data,com):
        super().__init__()
        self.sock = sock
        self.port = sock.getsockname()[1]
        self.ip = sock.getsockname()[0]
        self.start()
        self.data = data
        com.append((self.port,self.ip))
    def __init__(self,sock,data,com):
        self.init(sock,data,com)
    def recv(self,limit):
        command = ""
        num = 0
        while True:
            char = self.connection.recv(1).decode("UTF-8")
            if char == "*":
                num += 1
                if num == limit:
                    break
            command += char
        return command.split("*")
    def send(self,msg):
        self.connection.send(msg.encode("UTF-8"))
    def run(self):
        self.status = True
        try:
            if Communicator.debug:
                print("Listening at",self.port)
            self.sock.listen(16)
            self.connection = self.sock.accept()[0]
            Communicator(self.sock,self.data,[])
            self.send("true*")
            while self.status:
                command = self.recv(1)
                #Put
                if command[0] == "P":
                    command = self.recv(2)
                    self.data[command[0]] = json.loads(command[1])
                #Get
                elif command[0] == "G":
                    command = self.recv(1)
                    if command[0] == "../":
                        self.send(json.dumps(self.data) + "*")
                    else:
                        try:
                            self.send(json.dumps(self.data[command[0]]) + "*")
                        except KeyError as e:
                            self.send("KeyError*")
                #Create New
                elif command[0] == "N":
                    newSock = Communicator.createSock(self.ip)
                    self.connection.send((str(newSock[1]) + "*").encode("UTF-8"))
                    if Communicator.debug:
                        print("Sent",newSock[1])
                    Communicator(newSock,{},[])
                #Join Table
                elif command[0] == "R":
                    if Communicator.debug:
                        print("recieving")
                    s = self.recv(1)[0]
                    if Communicator.debug:
                        print("recieved")
                    try:
                        exec(s)
                    except:
                        pass
                #Execute command
                elif command[0] == "C":
                    command = self.recv(1)
                    if command[0] == "close":
                        self.connection.close()
                        if Communicator.debug:
                            print("Closed Server")
                        self.status = False
                    elif command[0] == "logout":
                        self.connection.close()
                        if Communicator.debug:
                            print("Logged Out")
                        break
                elif command[0] == "O":
                    command = self.recv(1)
                    try:
                        self.send(json.dumps(self.data.pop(command[0])) + "*")
                    except KeyError as e:
                        self.send("KeyError*")
                elif command[0] == "M":
                    if Communicator.debug:
                        print("Make")
                    command = self.recv(2)
                    try:
                        exec("self.send(json.dumps(self.data[\"" + command[0] + "\"]" + command[1] + ") + \"*\")")
                    except KeyError:
                        self.send("KeyError*")
                    except IndexError:
                        self.send("IndexError*")
                    except TypeError:
                        self.send("TypeError*")
                    except SyntaxError:
                        self.send("SyntaxError*")
                elif command[0] == "I":
                    self.send("*")
                elif command[0] == "S":
                    command = self.recv(1)
                    file = open(command[0] + ".txt", "w")
                    file.write(json.dumps(self.data))
                    file.close()
                    self.send("true*")
                elif command[0] == "L":
                    command = self.recv(1)
                    file = open(command[0] + ".txt","r")
                    self.data = json.loads(file.read())
                    self.send("true*")
                elif command[0] == "A":
                    command = self.recv(2)
                    try:
                        self.data[command[0]].append(json.loads(command[1]))
                        self.send("*")
                    except AttributeError:
                        self.send("AttributeError*")
        finally:
            self.connection.close()
            self.status = False
CC = Communicator
XT = XenoTable
CC.debug = False

def __main():
    global d
    global l
    global s
    global c
    global x
    d = {}
    l = []
    s = CC.localSock()
    c = CC(s,d,l)
    x = XT(c.ip,c.port)

if __name__ == "__main__":
    print("started xenotable")
    CC.CurrentPort = 80
    c = CC(CC.localSock(),{},[])
    print(c.ip,c.port)

