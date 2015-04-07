# Main server thread
import socket
import thread
import json

from game import Game


def client_thread(game, conn):
    answer_data = json.dumps({'return': 'ok'})
    # Receive init data from player
    player_data = conn.recv(4096)
    conn.sendall(answer_data)
    print "PLAYER_DATA:", player_data
    print "waiting for other_data"
    other_data = conn.recv(1024)
    conn.sendall(answer_data)
    print "other_data:", other_data
    player = game.add_player(conn, player_data)

    while True:
        request = conn.recv(1024)
        if not request:
            print "NO DATA! THIS SHOULD NOT HAPPEN!!!"
            break
        print "REQUEST:", request

        answer_data = game.wait_for_answer(player)
        conn.sendall(answer_data)

    # Thread loop ended
    conn.close()


def main():
    game = Game()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 8080))
    sock.listen(3)

    while True:
        conn, addr = sock.accept()
        thread.start_new_thread(client_thread, (game, conn))

if __name__ == '__main__':
    main()
