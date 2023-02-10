from core import UserInp


class Program(UserInp):
    def __init__(self, config: dict = ..., args: list = None):
        super().__init__(config, args)
        self.adt_commands = {
        }
        self.commands.update(self.adt_commands)

        # ! Запуск в режиме 1 команды
        if args is not None:
            self.run_only_arg(args)
