import asyncore
import socket
import six
from six.moves import queue


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((host, port))
        self.listen(5)
        self.client_handlers = []

    def handle_accept(self):
        socket, info = self.accept()
        six.print_("accepted client {}".format(info))
        self.client_handlers.append(ClientHandler(self, socket, info))

    def broadcast(self, sender_socket, message):
        six.print_("broadcasting message {}".format(message))
        for client_handler in self.client_handlers:
            if client_handler != sender_socket:
                try:
                    client_handler.say(six.b(message))
                except:
                    client_handler.close()
                    self.client_handlers.remove(client_handler)

    def handle_read(self):
        six.print_("server received message {}".format(six.ensure_str(self.recv(1024))))


class ClientHandler(asyncore.dispatcher):

    def __init__(self, server, socket, info):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server
        self.socket = socket
        self.info = info
        self.message_box = queue.Queue(maxsize=20)

    def say(self, message):
        self.message_box.put(message)

    def writable(self):
        return not self.message_box.empty()

    def handle_read(self):
        msg = six.ensure_str(self.recv(1024))
        self.server.broadcast(self, msg)

    def handle_write(self):
        msg = self.message_box.get()
        if not len(msg) > 1024:
            self.send(msg)


if __name__ == "__main__":
    server = Server("localhost", 33020)

    six.print_("loop()")
    asyncore.loop()




