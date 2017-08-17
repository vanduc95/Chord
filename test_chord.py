from node import *


def create_chord():
    # create addresses
    while True:
        address_list = map(lambda addr: Address('127.0.0.1', addr),
                           list(set(map(lambda x: random.randrange(10000, 50000), range(settings.CREATE_NODE)))))
        # keep unique ones
        # address_list = sorted(set(address_list))
        id_list = set(map(lambda addr: addr.__hash__(), address_list))
        if len(address_list) == len(id_list):
            break;

    for i in range(len(address_list)):
        node = Node(address_list[i])
        if len(node_list) == 0:
            node.join(node)
        else:
            # use a random already created peer's address as a remote
            node.join(node_list[random.randrange(len(node_list))])
        node_list.append(node)

    for i in range(len(address_list)):
        print address_list[i]


def detail_node():
    for i in range(len(node_list)):
        print 'id: %s' % node_list[i].id
        print 'succ: {} ; pred: {}'.format(node_list[i].successor().id, node_list[i].predecessor.id)
        for j in range(settings.LOGSIZE):
            print 'finger[%s]:%s' % (j, node_list[i].finger_table[j].node.id)
        print '---------------'


def lookup():
    key = int(raw_input("Choose key?"))
    node = node_list[random.randrange(len(node_list))].find_successor(key)
    print 'Node: {} - id: {}'.format(node.address.__str__(), node.id)


def join():
    id_list = map(lambda node: node.address.__hash__(), node_list)
    print id_list
    while True:
        address = Address('127.0.0.1', random.randrange(10000, 50000))
        if address.__hash__() not in id_list:
            break;
    new_node = Node(address)

    if len(node_list) == 0:
        new_node.join(new_node)
    else:
        new_node.join(node_list[random.randrange(len(node_list))])
    node_list.append(new_node)
    print new_node.id


def leave():
    id = int(raw_input("Choose node?"))
    for i in range(len(node_list)):
        if node_list[i].address.__hash__() == id:
            node_list[i].leave()
            del node_list[i]
            break;


if __name__ == '__main__':
    global node_list
    node_list = []
    create_chord()

    ans = True
    while ans:
        detail_node()
        print ("""
        1.Lookup key
        2.Join node
        3.Leave node
        4.Quit
        """)

        ans = raw_input("What would you like to do? ")
        if ans == "1":
            lookup()
        elif ans == "2":
            join()
        elif ans == "3":
            leave()
        elif ans == "4":
            break;
        elif ans != "":
            print("\n Not Valid Choice Try again")
