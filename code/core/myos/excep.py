class OsException(Exception):
    def __init__(self):
        self.txt = 'Неизвестная OS'
        super().__init__(self.txt)
