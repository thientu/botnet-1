import random
from ...signals import on_exception
from .. import BaseResponder


def random_line(filename):
    """Gets a random line from file."""
    return random.choice(list(open(filename)))


class Quotes(BaseResponder):
    """Sends random lines from the files defined in config.

    Example module config:

        "botnet": {
            "quotes": {
                "command_name1": "filepath1",
                "command_name2": "filepath2"
            }
        }

    """ 

    config_namespace = 'botnet'
    config_name = 'quotes'

    def get_all_commands(self):
        rw = super(Quotes, self).get_all_commands()
        try:
            for command in self.config['module_config'][self.config_namespace][self.config_name].keys():
                rw.append(command)
        except:
            pass
        return rw

    def handle_privmsg(self, msg):
        if self.is_command(msg):
            key = self.get_command_name(msg)
            filename = self.config_get(key, None)
            if filename is not None:
                try:
                    line = random_line(filename)
                    self.respond(msg, line)
                except FileNotFoundError as e:
                    on_exception.send(self, e=e)


mod = Quotes
