from server import UDP_server


if __name__ == "__main__":
    server = UDP_server(8891)
    server.start()
    server.join()
