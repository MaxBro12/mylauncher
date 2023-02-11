class CreateDbError(Exception):
    def __init__(self, error):
        self.txt = f'Ошибка в создании базы данных: {error}'
        super().__init__(self.txt)


class LoadDbError(Exception):
    def __init__(self, error):
        self.txt = f'Ошибка в создании базы данных: {error}'
        super().__init__(self.txt)
