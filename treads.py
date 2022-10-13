import threading, queue
#from video_read_from_file import read_video
import shutil
import cv2
import sqlite3 as lite
from sqlite import videos_table
import os


class Worker:
    def __init__(self, que):
        self.que = que  # список файлов

    def read_video(name):
        # Создаем объект захвата видео, в этом случае мы читаем видео из файла

        vid_capture = cv2.VideoCapture('in/' + name)

        file_count = 0
        while (vid_capture.isOpened()):
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
                # 20 в миллисекундах
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

    def worker(self):
        while True:
            # Получаем задание (имя файла) из очереди
            job = self.que.get(block=True, timeout=0.1)
            # открываем видео из очереди
            Worker.read_video(str(job)[3:])
            # Перемещаем файл из директории in в директорию out
            shutil.move(str(job), 'out/')
            # Сообщаем очереди что задача выполнена
            self.que.task_done()

class Que():
    def __init__(self, list_files):
        self.list_files = list_files  # список файлов

    # создаем и заполняем очередь именами файлов
    def que(self):
        que = queue.Queue()
        file_count = 0
        for file in self.list_files:
            file_count += 1
            que.put(file)

        if que.qsize():
            # Создаем и запускаем потоки
            if file_count < 10:
                n_thead = file_count
            else:
                n_thead = 10
            for _ in range(n_thead):
                Workers = Worker(que)
                th = threading.Thread(target=Workers.worker, args=(), daemon=True)
                #Worker.read_video('is42.mp4123')
                th.start()

            # Блокируем дальнейшее выполнение
            # программы до тех пор пока потоки
            # не обслужат все элементы очереди
            que.join()
        else:
            print('Файлы не найдены.')


