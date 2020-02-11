import logging
from pathlib import Path


BASE_DIR = Path(__file__).parent
SAVE_POINTS_DIR = BASE_DIR / 'save-points'


class SavePoint:
    """Является персистентным значением id ключа в случае аварийного завершения работы и перезапуска работы
    с момента завершения. Логика определения значения следует приоритету:
    1. кастомное значение при первом чтении
    2. персистентное значение в случае наличия
    3. начальное значение в случае отсутствия персистентного"""

    FILE_NAME = SAVE_POINTS_DIR / 'point_{host}_{table}'
    INITIAL_POINT = 1

    def __init__(self, host, table, point=INITIAL_POINT):
        self.host = host
        self.table = table
        self.point = point
        self.file_name = self.FILE_NAME.as_posix().format(host=host, table=table)
        self.file = None
        self._create_dir()

    def save(self, point):
        logging.info(f'save a point {point}')
        if self.file is None:
            self.file = open(self.file_name, 'w+')

        self.file.seek(0)
        self.file.write(str(point))
        self.file.flush()
        self.point = point

    def get(self):
        logging.info('get a point')
        if self.point == self.INITIAL_POINT and Path(self.file_name).exists():
            with open(self.file_name, 'r') as file:
                self.point = int(file.read())

        return self.point

    def _create_dir(self):
        if not SAVE_POINTS_DIR.exists():
            SAVE_POINTS_DIR.mkdir()
            logging.info(f'made the dir {SAVE_POINTS_DIR}')
