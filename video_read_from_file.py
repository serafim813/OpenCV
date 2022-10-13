import cv2
import sqlite3 as lite
from sqlite import videos_table
import os


def read_video(name):
	# Создаем объект захвата видео, в этом случае мы читаем видео из файла

	vid_capture = cv2.VideoCapture('in/'+name)

	file_count = 0
	while(vid_capture.isOpened()):
			# Метод vid_capture.read() возвращают кортеж, первым элементом является логическое значение
			# а вторым кадр
		ret, frame = vid_capture.read()
		if ret == True:
			cv2.imshow('Look', frame)
			file_count += 1
			print('Кадр {0:04d}'.format(file_count))
			writefile = 'Resources/Image_sequence/is42_{0:04d}.jpg'.format(file_count)
			# ресайзим до размера 30x30
			dsize = (30, 30)
			output = cv2.resize(frame, dsize)
			# сохраняем изображение в директории Resources/Image_sequence/
			cv2.imwrite(writefile, output)
			# конвертируем результат в ч/б
			img_grey = cv2.imread(writefile, cv2.IMREAD_GRAYSCALE)
			thresh = 128
			img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
			binary = lite.Binary(img_binary)
			# записываем в бд
			result = videos_table.insert().execute(name=name, number=file_count, frame=binary)
			# задержка 20 миллисекунд
			key = cv2.waitKey(20)

			if (key == ord('q')) or key == 27:
				break
		else:
			break

	# Удаляем все файлы из директории Resources/Image_sequence/
	dir = 'Resources/Image_sequence/'
	for file in os.scandir(dir):
		os.remove(file.path)
	# Освободить объект захвата видео
	vid_capture.release()
	cv2.destroyAllWindows()