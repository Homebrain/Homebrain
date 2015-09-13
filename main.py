from dispatcher import Dispatcher
from modules.rest_listener.rest_listener import RestListener

def main():
        d=Dispatcher()
        d.start()
        RestListener(d).start()


if __name__=="__main__":

    main()