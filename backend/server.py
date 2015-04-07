# Main server thread
import socket
import thread

from game import Game


def client_thread(game, conn):
    # Receive init data from player
    player_data = conn.recv(1024)
    player = game.add_player(conn, player_data)

    while True:
        request = conn.recv(1024)
        if not request:
            print "NO DATA! THIS SHOULD NOT HAPPEN!!!"
            break

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
