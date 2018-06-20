STEPS TO RUN THE PROGRAM

AT CLIENT END

1.	Kindly place the attached files “foo1.txt”, “foo2.jpg” and “foo3.jpg” in the client directory.
2.	Inputs are taken from the command prompt.
3.	Paste the main program on the python editor.
4.	Initiate the program through command prompt “Client.py 127.0.0.1 <Desired port number>”
5.	Feed in the inputs according to the request.
6.	There are 4 functions called in the program they are 
•	get_input: To get the file from the server directory.
•	put_input: To put the file from the client directory to the sever directory.
•	Rename_input: To rename the desired file at the server directory sending inputs from client end.
•	List_input:To list the files in the server directory.
7.      Order to execute the program. 
        a) Put a file foo1.txt/foo2.jpg/foo3.jpg
        b) List the files at the server end.
        c) Get the file which was placed previously.
        d) Rename the file.
        e) Exit the server.
        

AT SERVER END

1.	Inputs are taken from the command prompt.
2.	Paste the main program on the python editor.
3.	Initiate the program through command prompt “Server.py <Desired port number>”
4.	There are 5 functions called in the program they are 
•	get_input: To get the file from the server directory and sent it to the client.
•	put_input: To put the file from the client directory to the sever directory.
•	Rename_input: To rename the desired file at the server directory from the inputs received from client end.
•	List_input:To list the files in the server directory.
•	Exit_input: To exit the server gracefully.
5.      Order to execute the program. 
        a) Receive a file foo1.txt/foo2.jpg/foo3.jpg
        b) List the files at the server end.
        c) Send the file which was placed previously
        d) Rename the file.
        e) Exit the server.



NOTE: Python version used is 3.6.2