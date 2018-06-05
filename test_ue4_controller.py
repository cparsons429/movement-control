from datetime import datetime
import socket

TCP_IP = '127.0.0.1'
TCP_IN = 5000
TCP_OUT = 5001
BUFFER_SIZE = 1024

SEC_BETWEEN_FIRE = 0.04
SEC_OF_FIRING = 3


# A test script to send / receive data to / from UE4
# This will enable us to have an external program controlling our Character, to run that program on a different
# machine, and to receive sensory input from our Character


def main():
    """
    Gives me 15 seconds to open the game in UE4. Then types '0' 100 times / sec for 3 secs. This triggers motion in the
    Character. Will also print output received from UE4.

    :return:
    """
    # wait 10 seconds
    now = datetime.now()
    later = now

    while (later - now).total_seconds() < 10.0:
        later = datetime.now()

    # sending input to UE4
    in_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    in_port.connect((TCP_IP, TCP_IN))

    # receiving output from UE4
    out_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    out_port.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    out_port.bind((TCP_IP, TCP_OUT))
    out_port.listen(1)

    # wait 5 seconds
    now = datetime.now()
    later = now

    while (later - now).total_seconds() < 5.0:
        later = datetime.now()

    i = 0

    while True:
        later = datetime.now()

        # print any output received
        out_connect, _ = out_port.accept()
        out_data = out_connect.recv(BUFFER_SIZE)
        if len(out_data) > 0:
            print(out_data)

        # type '0' 25 times / sec for 3 secs, using delta timing
        if i < int(SEC_OF_FIRING / SEC_BETWEEN_FIRE) and (later - now).total_seconds() >= SEC_BETWEEN_FIRE:
            now = later
            i += 1

            in_port.send('0')

if __name__ == '__main__':
    main()

