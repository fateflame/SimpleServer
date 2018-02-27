import socket
import sys
import select


class client:
    def __init__(self):
        self.cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, addr="localhost", ser_port = 10002):
        self.cli_sock.connect((addr, ser_port))
        self.str_cli()

    def str_cli(self, fp=sys.stdin):
        eof = False
        while True:
            rset = []
            wset = []
            xset = []
            if not eof:
                rset.append(sys.stdin)
            rset.append(self.cli_sock)
            r, w, x = select.select(rset, wset, xset, None)
            if self.cli_sock in r:
                ret = self.cli_sock.recv(1024)
                if len(ret) is 0:
                    if eof:
                        print("close normally")
                        return
                    else:
                        print("server terminated prematurely")
                        exit(1)
                sys.stdout.write(ret+'\n')
            if fp in r:
                ret = fp.readline()[:-1]
                if ret == "":     # EOF
                    eof = True
                    self.cli_sock.shutdown(socket.SHUT_WR)
                    continue
                self.cli_sock.sendall(ret)
                #print('already send')


if __name__ == "__main__":
    c = client()
#    c.connect(addr="10.13.33.185", ser_port=10001)
    c.connect()
