import logging
import multiprocessing
import os
import queue
from multiprocessing.connection import Client

import sptr.commands.commands as basic_commands
from sptr.core.settings import Settings
from sptr.core.share import SettingsAware
from sptr.core.share import TranslatorAware
from sptr.core.translator import Translator
from sptr.ext.communication_handler import RemoteConsoleHandler, \
    check_address_availability
from sptr.ui.widgets.console import Console

LOG = logging.getLogger(__name__)


def launch_client(address, settings, commands):
    LOG.info('Client side launching')
    msg = ''
    import sys
    if settings.stdin:
        for msg in sys.stdin:
            with Client(address, ) as conn:
                conn.send(msg)
    if commands:
        for c in commands:
            with Client(address, ) as conn:
                conn.send(c)


def handle_queue(tr):
    try:
        msg = tr.rch.queue.get(0)
        print(msg)
        tr.execute(msg)
    except queue.Empty:
        pass
    finally:
        if tr.rch.is_continue:
            tr.ui.after(100, handle_queue, tr)


def launch_server(address, settings: Settings):
    LOG.info('Server side launching')
    tr = Translator(settings)

    from sptr.core.actions import Actions
    # include = dir(Actions)
    filtr = ['settings']
    LOG.info('Loading commands from Actions')
    tr.commands.load_commands_from_object(Actions, filtr, tr)

    LOG.info('Loading commands from basic_commands')
    tr.commands.load_commands_from_module(basic_commands)
    tr.initialize()
    tr.rch = RemoteConsoleHandler(address)

    import threading
    tr.rch_thread = threading.Thread(target=tr.rch.run)
    LOG.info("Starting remote console handler")
    tr.rch_thread.start()

    tr.ui.after(100, handle_queue, tr)
    tr.ui.mainloop()


def main():
    from sptr.ext.logutils import setup_logging

    setup_logging(debug=False)

    LOG.info(f"PID: {os.getpid()}")

    settings = Settings()
    SettingsAware.settings_set(settings)
    args = parse_arguments()

    command_names = ['translate', 'search', 'show', 'hide']
    commands = []
    for name in vars(args):
        if name not in command_names:
            print(name, type(name))
            settings.set(name, getattr(args, name))
        else:
            attr = getattr(args, name)
            try:
                if attr:
                    command = name
                    for w in attr:
                        command += ' ' + w
                    commands.append(command)
            except TypeError:
                commands.append(name)
    print(commands)

    address = ('localhost', settings.remote_console_port)

    if settings.server:
        if not check_address_availability(address):
            print("server already started.")
            return 0
        else:
            launch_server(address, settings)
    else:
        launch_client(address, settings, commands)


def parse_arguments():
    from argparse import ArgumentParser
    # TODO watch ArgParse

    parser = ArgumentParser()

    parser.add_argument('-s', '--server', action='store_true', default=False,
                        help='run stdr server side')
    parser.add_argument('-i', '--stdin', action='store_true', default=False,
                        help='read commanad from stdio')
    parser.add_argument('-t', '--translate', nargs='*',
                        help='translate word')
    parser.add_argument('--search', nargs='*',
                        help='search word')
    parser.add_argument('-c', '--config', default='', type=str,
                        help='specify config file')
    parser.add_argument('--show', action='store_true',
                        help='show server window, if started')
    parser.add_argument('--hide', action='store_true',
                        help='hide server window, if started')

    return parser.parse_args()


print(__name__)
if __name__ == '__main__':
    main()
