from core import UserInp

from .settings import (
    config_file,
)


class Program(UserInp):
    def __init__(self, config: dict = ..., args: list = None):
        super().__init__(config, args)
        self.adt_commands = {
            'list': self.get_all_tracks,
            'add': self.add_track,
            'remove': self.remove_track,
            'show': self.show_track,
            'update': self.update,
            'get': self.downtrack,
        }
        self.commands.update(self.adt_commands)

        # ! Запуск в режиме 1 команды
        if args is not None:
            self.run_only_arg(args)

    # ! Для пользователя
    def get_all_tracks(self):
        pass

    def add_track(self):
        pass

    def remove_track(self):
        pass

    def show_track(self):
        pass

    def update(self):
        pass

    def downtrack(self):
        pass
