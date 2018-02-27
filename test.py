import select
import sys


if __name__ == "__main__":
    i = 1
    while True:
        r,w,x = select.select([sys.stdin], [], [], None)
        print(i)
        i += 1
        ret = r[0].read()
        if not ret:
            try:
                sys.stdin.next()
            except StopIteration:
                continue
        print(ret)
