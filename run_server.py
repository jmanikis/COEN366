from server import UDP_server

#   Used to run a server through the command line
#   with specified port 8891

if __name__ == "__main__":
    server = UDP_server(8891)
    server.start()
    server.join()
