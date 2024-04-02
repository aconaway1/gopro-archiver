import threading

FILES = [ "a", "b", "c", "d", "e", "f", "g"]

def do_something(file):
    print(file)

for file in FILES:
    x = threading.Thread(target=do_something, args=(file))
    x.start()