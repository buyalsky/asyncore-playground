import asyncore,six,socket
from six.moves import queue


class Client(asyncore.dispatcher):
    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.connect((host, port))
        self.message_box = queue.Queue(maxsize=20)

    def say(self, message):
        self.message_box.put(message)
        six.print_("queued message {}".format(message))

    def writable(self):
        return not self.message_box.empty()

    def handle_write(self):
        msg = self.message_box.get()
        self.send(six.b(msg))

    def handle_read(self):
        msg = six.ensure_str(self.recv(1024))
        six.print_("{} received message {}".format(self.name,msg))


if __name__=="__main__":
    client1 = Client("localhost", 33020, "client1")
    client2 = Client("localhost", 33020, "client2")
    client3 = Client("localhost", 33020, "client3")
    client4 = Client("localhost", 33020, "client4")
    client5 = Client("localhost", 33020, "client5")

    client1.say("hey 1")
    client2.say("hey 2")
    client3.say("hey 3")
    client4.say("hey 4")
    client5.say("hey 5")

    asyncore.loop()