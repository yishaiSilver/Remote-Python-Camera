import cv2
import run_inference
import silverStandardCMD as silver
import time
import playsound
import cv2
import socket
import os
from getkeys import key_check

host = 'localhost'
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

silver.main()
run_inference.initSound()

def main():
	#cap = cv2.VideoCapture(1) 
	#last_time = time.time()

	while True:
		keys =key_check()

		if 'A' in keys:
			
			s.send(str.encode("PICTURE"))
			filesize = s.recv(4096)
			filesize = filesize.decode('utf-8')
			print("recieved file of length: {}\n".format(filesize))
			filesize = int(filesize)

			s.send(str.encode('POSITIVE'))

			f = open("image.jpg", 'wb')
			data = s.recv(4096)
			totalRecv = len(data)

			while data:
				print("Still recieving data")
				f.write(data)
				data = s.recv(4096)
				totalRecv += len(data)
				print(os.path.getsize("image.jpg")/4096)
				# if data.decode('utf-8') == "":
				# 	break
				if totalRecv == filesize:
					f.write(data)
					break

			f.close()

			# while totalRecv < filesize:
			# 	data = s.recv(4096)
			# 	totalRecv += len(data)
			# 	f.write(data)
			# 	print(os.path.getsize("image.jpg")/1024)
			
			print("Download complete. Filesize is {}. Full transfer: {}".format(os.path.getsize("image.jpg"), filesize == os.path.getsize("image.jpg")))

			# s.close()







			sound = run_inference.predict("image.jpg")

			# s.send(str.encode("OUTPUT"))
			# confirmation = s.recv(4096)
			# if confirmation == 'READY':
			# 	s.send(os.path.getsize(sound))
			# 	confirmation = s.recv(4096)
			# 	if confirmation == 'POSITIVE':
			# 		with open(sound, 'rb') as f:
			# 			bytesToSend = f.read(4096)
			# 			s.send(bytesToSend)
			# 			while bytesToSend != "":
			# 				bytesToSend = f.read(4096)
			# 				s.send(bytesToSend)




		# ret, frame = cap.read()
		# cv2.imshow('original',frame)

		# keys = key_check()

		# if 'A' in keys:
		# 	cv2.imwrite("image.jpg", frame)
		# 	run_inference.predict("image.jpg")
		# elif 'Q' in keys:
		# 	break
		# elif len(keys) == 1:
		# 	run_inference.set(keys[0])
		
		# if cv2.waitKey(20) & 0xFF == ord('q'):
		# 	# ser.write(b'q')
		# 	cap.release()
		# 	cv2.destroyAllWindows()
		# 	break

if __name__ == "__main__":
  main()