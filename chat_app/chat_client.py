import asyncore, six, socket, sys, select


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


if __name__ == "__main__":

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(("localhost", 3230))

    while True:
        socket_list = [sys.stdin, c]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == c:
                data = six.ensure_str(sock.recv(4096))
                if not data:
                    six.print_('Disconnected from chat server')
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                c.send(six.b(msg))
                prompt()