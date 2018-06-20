#author: Honna Gowri Manjunath honna.manjunath@colorado.edu
#Course: ITP - Network Engg track

import socket     #Importing socket library to create socket, send and receive data between client and server
import sys        #Importing sys library to take user input from command prompt
import os         #Importing os library to get the path of the file and to check if the file exists
cs=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #Creating the socket
Server_IP=sys.argv[1]       #Reading the user input of the Server IP and storing it in Server_IP
Server_port=sys.argv[2]     #Reading the user input of the server port and storing it in Server_port

'''
Printing the options for users to select
'''

print('*' *50)    
print("Kindly enter the command from the below options")
print("\n1)Get:Enter 1 \n2)Put:Enter 2 \n3)Rename:Enter 3 \n4)List:Enter 4 \n5)Exit:Enter 5 \n")
print( '*' *50)

'''
get_input function
This function when called gets the user input files from the server and stores it at the client as Received_<file name>
'''
def get_input():
    file_name=input("Please enter the desired file name: ") #Request the user for the input of the desired file
    cs.sendto(file_name.encode(),(Server_IP,int(Server_port))) #Send the file name to the server
    #data=''
    #while data=='':
    (data,address)=cs.recvfrom(64000) #Receive the data from the server
    message=data.decode() #Store the data in a variable to check if the file exists at the server end
    if (message=="doesn't exist"):
        print("File doesn't exist") 
    else:
        (contents,address)=cs.recvfrom(64000) #Receive the file size that the server is sending
        fSize=contents.decode()
        #print("File name received "+filename)
        print("File size received "+fSize)
        rfile=open('Received_'+ file_name,'wb') #Open a file
        Leftover=0
        while Leftover<int(fSize):
            print("Incoming client data")
            (Data,Address)=cs.recvfrom(64000) #Receive the data from client end
            rfile.write(Data) #Write the data into the file
            cs.sendto("ACK".encode(),Address) #Send acknowledgment that the data has been received
            print("ACK Sent")
            Leftover=Leftover+64000 #Increment the amount if data that needs to be received.
            print(Leftover)
        rfile.close()
    
        
'''
put_input function
This function when called sends the file present in the client directory to the server directory
'''
def put_input():
        file_name=input("Please enter the desired file name: ") #Enter the file name that needs to be sent
        c=os.path.isfile(file_name)  #Check if the file exists
        if(c==True): #If exists enter the loop
            cs.sendto(file_name.encode(),(Server_IP,int(Server_port)))
            fileSize=os.path.getsize(file_name) #Send the file name
            fileSize=str(fileSize)
            cs.sendto(fileSize.encode(),(Server_IP,int(Server_port))) #Send the file size name to the server
            #print("File name sent") 
            file=open(file_name,'rb') #Open the file to send it to the server
            Leftover=0
            cs.settimeout(7)
            while Leftover<int(fileSize):
                data=file.read(64000)
                print("Data Sent")
                cs.sendto(data,(Server_IP,int(Server_port)))  #Send the data to the server
                ACK="Not delivered"
                while ACK == "Not delivered":
                    try:
                        print("Waiting for ACK")
                        data=cs.recv(1024)
                        ACK=data.decode()
                    except socket.timeout(7):
                        cs.sendto(data,(Server_IP,int(Server_port)))  #Send the data to the server
                Leftover=Leftover+64000
                print("ACK Received")
                #print(Leftover)
            #print("Data sent")
        else:
            print("File doesn't exist") #If file doesn't exist notify the user that the file is not present
        cs.settimeout(70)
'''       
list_input function
This function when called present a list of files present in the server directory
'''               
def list_input():
    name=cs.recv(64000) #Received the data sent from the server
    data=name.decode()
    list1=data.split()
    for i in list1:
        print(i)   #Prints the file names one below the other
    
'''
rename_input funtion
This function when called replaced the old file name with the desired new name at the server end.
'''
def rename_input():
    old_name=input("Enter the old file name: ") #Enter the desired file name that needs to be changed
    cs.sendto(old_name.encode(),(Server_IP,int(Server_port))) #Send the file name to the server
    new_name=input("Enter the new file name: ")      #Enter the new file name that the file has to be replaced at the server end
    cs.sendto(new_name.encode(),(Server_IP,int(Server_port)))  #Send the new file name that shall be replaced with to the server
    (data,add)=cs.recvfrom(64000) #Receive the message sent across by the server
    print(data.decode())          
    
'''
Main program
'''

while(1):
    option=input("Enter the desired option: ")
    cs.sendto(option.encode(),(Server_IP,int(Server_port))) #Sending the user option to Server 
    if(option=='1'):
        get_input()
    elif(option=='2'):
        put_input()
    elif(option=='3'):
        rename_input()
    elif(option=='4'):
        list_input()
    
     
