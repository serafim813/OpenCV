import os
import time
import concurrent.futures
from tasks import read_video, list_files

if __name__ == '__main__':
    start = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        for file in list_files:
            read_video(str(file))

    print(time.time() - start, 'sec')
