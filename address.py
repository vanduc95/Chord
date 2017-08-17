from settings import RING_SIZE


class Address(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)

    def __hash__(self):
        return hash(("%s:%s" % (self.ip, self.port))) % RING_SIZE

    def __str__(self):
        return "[\"%s\", %s]" % (self.ip, self.port)


if __name__ == '__main__':
    addr = Address("127.0.0.1", 43672)
    print "self id = %s , address = %s " % (addr.__hash__(), addr.__str__())
