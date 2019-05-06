import socket
import cv2
import os
import time
from playsound import playsound

host = ''
port = 5560

storedValue = "stored_value string"
pictureFilename = ""
pictureNumber = 0
fileFilename = ""
fileNumber = 0

cap = cv2.VideoCapture(0)

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")

    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket successfully binded")

    return s

def setupConnection():
    s.listen(1)
    conn, address = s.accept()
    print("Connected to " + address[0] + ":" + str(address[1]))
    return conn

def showVideo():
    ret, frame = cap.read() 
    cv2.imshow('Image', frame)
    print("gone through frame")

def serverFunction(conn):
    global pictureFilename
    global pictureNumber
    global fileFilename
    global fileNumber

    print("Passed: call to serverFunction\n")
    
    while True:
##        #OpenCV Stuff
##        ret, frame = cap.read() 
##        cv2.imshow('Image', frame)
##        cv2.imwrite("image.jpg", frame)
        #print("Picture created, file size: {}".format(os.path.getsize("image.jpg")))

        #print("Passed: first save of image (not in PICTURE command)")

        #Server Stuff
        data = conn.recv(4096)
        if data != "":
            data = data.decode('utf-8')
            dataMessage = data.split(' ', 1)
            command = dataMessage[0]
            print("Passed: call to recv (recieved content)\n")

            if command == 'PICTURE':
                print("PICTURE command recieved")
                
                #Create picture to send.
                pictureFilename = "pictureToSend-{}.jpg".format(pictureNumber)
                ret, frame = cap.read() 
                cv2.imshow('Image', frame)
                cv2.imwrite(pictureFilename, frame)
                
                print("Picture '{}' created, file size: {}".format(pictureFilename, os.path.getsize(pictureFilename)))
                conn.sendall(str(os.path.getsize(pictureFilename)).encode())

                print("passed length send")
                confirmation = conn.recv(4096)
                confirmation = confirmation.decode('utf-8')
                if confirmation == 'POSITIVE':
                    print("recieved confirmation")

                    pic = open(pictureFilename, 'rb')
                    chunk = pic.read(4096)
                    length = len(chunk)
                    while chunk:
                        conn.sendall(chunk)
                        chunk = pic.read(4096)
                        length += len(chunk)
                    conn.sendall(chunk)
                    print("Passed: end of picture\n")

                    
            elif command == 'OUTPUT':
                playAudio(conn)
            elif command == 'TEST':
                print('Test command recieved.')
            else:
                conn.sendall("unrecognized command")
        else:
            continue 

def playAudio(conn):
    print("playAudio function called.")
    conn.sendall('READY')
    filesize = long(conn.recv(4096))
    conn.sendall('POSITIVE')

    fileFilename = "audioToPlay-{}.mp3".format(fileNumber)
    f = open(fileFilename, 'wb')
    data = conn.recv(4096)
    totalRecv = len(data)
    f.write(data)
    while totalRecv < filesize:
        data = conn.recv(4096)
        totalRecv += len(data)
        f.write(data)
    print("Download comlete.")
    playsound(fileFilename)
 
s = setupServer()

while True:
    try:
        ret, frame = cap.read()
        cv2.imshow('Frame', frame)
        conn = setupConnection()
        serverFunction(conn)
        #showVideo()
    except:
##        command = input("Continue? [y/n]")
##        if command == 'y':
##            continue
##        elif command == 'n':
##            break
        print("Should be shutting down, but continuing anyways.")
        cv2.destroyAllImages()
        break
        
print("Server shutting down.")