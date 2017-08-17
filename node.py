from address import Address
from finger import Finger
import random
from utils import *


class Node(object):
    def __init__(self, address):
        self.address = address
        self.id = self.address.__hash__()
        self.finger_table = []
        self._generate_finger_table()

    def _generate_finger_table(self):
        """Generate finger's start in finger table"""
        # for i in range(0, settings.FINGER_TABLE_SIZE):
        for i in range(0, settings.LOGSIZE):
            _finger = Finger(self.id, i)
            self.finger_table.append(_finger)

    def successor(self):
        return self.finger_table[0].node

    def find_successor(self, id):
        """Ask node n to find id's successor"""
        print('Node {} - Find successor for {}'.format(str(self.id), str(id)))
        if in_interval(id, self.predecessor.id, self.id, equal_right=True):
            return self
        node = self.find_predecessor(id)
        return node.successor()

    def find_predecessor(self, id):
        """Ask node n to find id's precedecessor"""
        print ('Node {} - Find predecessor for {}'.format(str(self.id), str(id)))
        if id == self.id:
            return self.predecessor
        node = self
        while not in_interval(id, node.id,
                              node.successor().id, equal_right=True):
            node = node.closest_preceding_finger(id)
        return node

    def closest_preceding_finger(self, id):
        """Return closest finger preceding id"""
        print('Node {} - Get closest preceding finger for {}'.format(str(self.id), str(id)))
        # for i in range(settings.FINGER_TABLE_SIZE - 1, -1, -1):
        for i in range(settings.LOGSIZE - 1, -1, -1):
            _node = self.finger_table[i].node
            if _node and in_interval(_node.id, self.id, id):
                return _node
        return self

    def join(self, exist_node):
        """Node join the network with exist_node
        is an arbitrary in the network."""
        print('Node {} - join to ring with node {}'.format(str(exist_node.id), str(self.id)))
        if self == exist_node:
            for i in range(settings.LOGSIZE):
                self.finger_table[i].node = self
            self.predecessor = self
        else:
            self.init_finger_table(exist_node)
            self.update_others()
            # Move keys in (predecessor, self] from successor

    def init_finger_table(self, exist_node):
        """Initialize finger table of local node
        exist_node is an arbitrary node already in the network"""
        print('Node {} - Init finger table for {}'.format(str(exist_node.id), str(self.id)))
        self.finger_table[0].node = \
            exist_node.find_successor(self.finger_table[0].start)
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger_table[0].node = self
        # for i in range(settings.FINGER_TABLE_SIZE - 1):
        for i in range(settings.LOGSIZE - 1):
            if in_interval(self.finger_table[i + 1].start,
                           self.id, self.finger_table[i].node.id,
                           equal_left=True):
                self.finger_table[i + 1].node = self.finger_table[i].node
            else:
                self.finger_table[i + 1].node = \
                    exist_node.find_successor(self.finger_table[i + 1].start)

    def update_others(self):
        """Update all nodes whose finger table"""
        print('Node {} - Update others'.format(str(self.id)))
        # for i in range(settings.FINGER_TABLE_SIZE):
        for i in range(settings.LOGSIZE):
            # Find last node p whose ith finger might be n
            prev = decr(self.id, 2 ** i)
            p = self.find_predecessor(prev)
            # Different peusudo
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self, i)

    def update_finger_table(self, s, i):
        """If s is ith finger of n, update n's finger table with s"""
        print('Node {} - Update finger table for {}'.format(str(self.id), s.id))
        if in_interval(s.id, self.id,
                       self.finger_table[i].node.id, equal_left=True) and self.id != s.id:
            self.finger_table[i].node = s
            p = self.predecessor
            p.update_finger_table(s, i)

    def leave(self):
        """Leave ring"""
        self.successor().predecessor = self.predecessor
        # self.predecessor.finger_table[0].node = self.successor()
        self.update_others_leave()

    def update_others_leave(self):
        a = self.successor()
        while True:
            for i in range(len(a.finger_table)):
                if a.finger_table[i].node.id == self.id:
                    a.finger_table[i].node = self.successor()
            if a.successor().id == self.successor().id:
                break
            else:
                a = a.successor()


if __name__ == '__main__':
    node_list = []
    # node = Node(Address('127.0.0.1', '3309'))
    # node_list.append(node)
    # node.join(node)
    # print node_list[0]

    # create addresses
    address_list = map(lambda addr: Address('127.0.0.1', addr),
                       list(set(map(lambda x: random.randrange(40000, 50000), range(4)))))
    # keep unique ones
    address_list = sorted(set(address_list))

    for i in range(len(address_list)):
        node = Node(address_list[i])
        if len(node_list) == 0:
            node.join(node)
        else:
            # use a random already created peer's address as a remote
            node.join(node_list[random.randrange(len(node_list))])
        node_list.append(node)

    for i in range(len(node_list)):
        print 'id: %s' % node_list[i].id
        print 'succ: {} ; pred: {}'.format(node_list[i].successor().id, node_list[i].predecessor.id)
        for j in range(3):
            print 'finger[%s]:%s' % (j, node_list[i].finger_table[j].node.id)
        print '---------------'

    print node_list[2].find_successor(4).id
