#author: Honna Gowri Manjunath honna.manjunath@colorado.edu
#Course: ITP - Network Engg track

import socket    #Importing socket library to create socket, send and receive data between client and server
import sys  #Importing sys library to take user input from command prompt
import os  #Importing os library to get the path of the file and to check if the file exists
ss=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creating a socket for communication
Server_port=int(sys.argv[1]) #Taking the porting on which the server should listen
if (int(sys.argv[1])>5000):  #Applying a condition to take in only ports greater than 5000 
    ss.bind(('',Server_port)) #If the port is above 5000 bind it to the socket with the condition to accept any IP
    print(" Server Binded on port : "+ str(Server_port))
else:
    print("Port number should be greater than 5000")
    exit()
'''
get_input function
To send the file to the client when evoked
'''
def get_input():
    (filename,(IP,Port))=ss.recvfrom(64000) #Receive the filename from the client
    fname=filename.decode()
    address=(IP,Port)
    c=os.path.isfile(fname) #Check if the file exists
    if(c==True):
        print("file exist")
        ss.sendto("exist".encode(),address)
        fileSize=os.path.getsize(fname)
        #packet=fname + ' '+str(fileSize)
        ss.sendto(str(fileSize).encode(),address) #Send the file size.
        fopen=open(fname,'rb')#Open the file
        Leftover=0
        ss.settimeout(7)
        while Leftover<int(fileSize):
            data=fopen.read(64000)
            print("Data Sent")
            ss.sendto(data,address)  #Send the data.
            ACK="Not delivered"
            while ACK == "Not delivered":
                try:
                    print("Waiting for ACK")
                    data=ss.recv(1024)
                    ACK=data.decode()
                except socket.timeout(7):
                    ss.sendto(data,address)  #Resend the data to the server
            Leftover=Leftover+64000
            print("ACK Received")
            print(Leftover)
        file=fopen.read(64000)
        ss.sendto(file,address) #Send the next set of data to the client if ack is received.
    else:
        print("no such file")
        ss.sendto("doesn't exist".encode(),address)
        #fopen=open('Errormessage.txt','rb') 
        #file=fopen.read(64000)
        #ss.sendto(file,address) #Send across the data stating the file doesn't exist
    ss.settimeout(70)
'''
put_input 
This function when called saves the file send from the client in the servers directory
'''
def put_input():
    (a,Address)=ss.recvfrom(64000) #Receives the file name and size that needs to be saved once we receive the data
    filename=a.decode()
    (b,Address)=ss.recvfrom(64000)
    fileSize=b.decode()
    #print("File name received "+filename)
    #print("File size received "+fileSize)
    #print(File_name)
    rd=open(filename,'wb') #Open the file'
    Leftover=0
    while Leftover<int(fileSize):
        print("Incoming client data")
        (Data,Address)=ss.recvfrom(64000) #Receive the data from client end
        rd.write(Data)
        ss.sendto("ACK".encode(),Address)
        print("ACK Sent")
        Leftover=Leftover+64000
        print(Leftover)
    rd.close()
    #print(rd.decode())
'''
list_input 
This function when evoked will send the list of files present in the server directory
'''
def list_input(address):
    d=os.getcwd() #Get the directory path 
    files=os.listdir(d) #Get the files present in that directory
    str=''
    for item in files:
        str = str + item + ' '
    print(files)
    ss.sendto(str.encode(),address) #Send the data post converting it to a string 

'''
rename_input 
When this function is evoked it renames the files according to the users choice
'''
    
def rename_input():
    (on,address)=ss.recvfrom(64000)  #Get the old name of the file 
    old_name=on.decode()
    (nn,address)=ss.recvfrom(64000) #Get the new name of the file
    new_name=nn.decode()
    os.rename(old_name,new_name) #Rename the file
    ss.sendto(("Rename successfully done to :  " + new_name).encode(),address) #Send across an acknowledgment to the client 
    
'''
exit_input 
When this function is evoked the server shuts the socket an exits the program 
'''

def exit_input():
    ss.close() #Socket is closed 
    exit()

'''
Main function 
'''       

while(1):         
    (usero,address)=ss.recvfrom(64000) #Receive the option from the client end 
    option=usero.decode()
    print(option)
    if(option=='1'):
        get_input()
    elif (option=='2'):
        put_input()
    elif(option=='3'):
        rename_input()
    elif(option=='4'):
        print("Opt 4 ")
        list_input(address)
    elif(option=='5'):
        exit_input()
