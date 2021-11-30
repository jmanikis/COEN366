from ServerSide import ServerSide
from ClientSide import ClientSide

#   Unit Test for running a file transfer between clients

ss = ServerSide()
cs = ClientSide("test_pc", "0.0.0.0", "8080", "8081")


def write_file():
    with open("files/test.txt", "a") as file:
        for i in range(2000):
            file.write(f"{i} ")


# write_file()

cs.RQ = 3
dl_req = cs.DOWNLOAD("test.txt")
stuff = cs.parse_reply(dl_req)
for thing in stuff:
    cs.parse_reply(thing)
