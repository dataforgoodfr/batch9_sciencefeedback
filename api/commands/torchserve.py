from flask import current_app as app
from flask_script import Command

from utils.config import COMMAND_NAME
from utils.torchserve import vectors_from_sentences, ping


@app.manager.add_command
class TorchserveCommand(Command):
    __doc__ = ''' e.g. `{} torchserve 'joy is a grace'` prints `AM`'''.format(COMMAND_NAME)
    name = 'torchserve'
    capture_all_args = True

    def run(self, args):
        if len(args) == 0:
            print(ping())
        else:
            print(vectors_from_sentences([' '.join(args)][0]))
