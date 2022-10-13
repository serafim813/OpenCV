import pathlib
from treads import Que
path = pathlib.Path('.')
# тестовый каталог с файлами
test_dir = 'in'
# Путь к тестовой директории
path_dir = path.joinpath(test_dir)
# получаем список файлов
list_files = path_dir.glob('*.mp4')

test = Que(list_files)
test.que()