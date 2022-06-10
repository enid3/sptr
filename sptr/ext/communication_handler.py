import logging
from multiprocessing.connection import Listener, Client
from sptr.core.share import TranslatorAware
from queue import Queue

LOG = logging.getLogger(__name__)


def check_address_availability(address: (str, int)) -> bool:
    """
    check, if adress is already used by socket
    :param address:  address to be checked
    :return: True, if address is available, False otherwise.
    """

    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        err = sock.connect_ex(address)
        return bool(err)


class RemoteConsoleHandler(TranslatorAware):
    def __init__(self, address):
        self.address = address
        self.queue = Queue()
        self.is_continue = True

    def _run_server_side(self):
        LOG.info("Server side launching")
        LOG.info(f'Listenning adress {self.address}')
        with Listener(self.address, ) as listener:
            msg = ''
            while msg != "exit":
                conn = None
                try:
                    conn = listener.accept()
                    msg = conn.recv()
                    print(msg)
                    self.queue.put(msg)
                    """
                    try:
                        command = self.tr.commands.get_command(msg.split()[0], abbrev=True)(msg)
                    except Exception:
                        LOG.info("invalid command")
                    LOG.info(f"Command: {command}")
                    if command is not None:
                        LOG.info(f'Executing command {msg}')
                        # command.init_line(msg)
                        command.execute()
                    """
                except Exception as e:
                    print(e)
                    LOG.warning("Exception, during listenning")
                    pass
                finally:
                    if conn:
                        LOG.info("Closing connection..")
                        conn.close()
                        conn = None

    def run(self):
        self._run_server_side()
