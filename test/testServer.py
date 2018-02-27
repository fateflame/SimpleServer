import socket
from os import fork
import select


class server:
    def __init__(self):
        self.port = 10002
        # host = socket.INADDR_ANY
        self.host = ""
        self.ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_sock.bind((self.host, self.port))

    def listen(self):
        self.ser_sock.listen(1)
        accept_list = []

        while True:
            rset = [self.ser_sock] + accept_list
            wset = []
            xset = []

            r, w, x = select.select(rset, wset, xset, None)
            nready = len(r+w+x)

            if self.ser_sock in r:
                conn, cli_addr = self.ser_sock.accept()
                print("build connection with {0}".format(cli_addr))
                conn.sendall("build connection")
                accept_list.append(conn)
                nready -= 1
                if nready <= 0:
                    continue
            for conn in accept_list:
                if conn in r:
                    data = conn.recv(1024)
                    if len(data) > 0:
                        conn.sendall(data)
                    elif len(data) == 0:
                        print "close a client"
                        conn.close()
                        accept_list.remove(conn)
                    nready -= 1
                    if nready <= 0:
                        break



if __name__ == "__main__":
    s = server()
    s.listen()



