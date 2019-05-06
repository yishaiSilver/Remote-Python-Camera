import cv2

cap = cv2.VideoCapture(0)

def main():
	while True:
		ret, frame = cap.read()
		try:
			cv2.imshow('Frame', frame)
		except:
			print('Unable to display frame.')

		if cv2.waitKey(20) & 0xFF == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			break

if __name__ == "__main__":
	main()