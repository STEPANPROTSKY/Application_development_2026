import sys

class Node:
    __slots__ = ['data', 'next']
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.count = 0
        self.top = None
        self.botton = None

    def push(self, data):
        if self.count == 0:
            node = Node(data)
            self.top = node
            self.botton = node
            self.count += 1
        else:
            node = Node(data)
            self.botton.next = node
            self.botton = node
            self.count += 1
        print('ok')

    def pop(self):
        tmp = self.top.data
        self.top = self.top.next
        self.count -= 1
        print(tmp)

    def front(self):
        print(self.top.data)

    def size(self):
        print(self.count)

    def view(self):
        list = []
        node = self.top
        while node is not None:
            list.append(str(node.data))
            node = node.next
        print(', '.join(list))

    def clear(self):
        self.top = None
        self.botton = None
        self.count = 0
        print('ok')

    def exit(self):
        print('bye')
        exit()

    def hello_world(self):
        print("Hello, World!")

def main():
    queue = Queue()
    commands = {
        'push':  queue.push,
        'pop':   queue.pop,
        'front': queue.front,
        'size':  queue.size,
        'view':  queue.view,
        'clear': queue.clear,
        'hello': queue.hello_world,
    }
    
    for line in sys.stdin:
        parts = line.split()
        if not parts:
            continue
    
        name, *args = parts
    
        if name == 'exit':
            print('bye')
            break
    
        func = commands.get(name)
        if func is None:
            continue
    
        func(*map(int, args))

if __name__ == "__main__":
    main()