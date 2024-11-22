class AddException(Exception):
    pass
class SetException(Exception):
    pass
class MinMaxException(Exception):
    pass
class DeleteException(Exception):
    pass
class SearchException(Exception):
    pass

class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_left(self):
        return self.a
    def  get_right(self):
        return self.b

class Vertex:
    def __init__(self, key, value, parent):
        self.key = key
        self.value = value
        self.index = 0
        self.is_visited = False
        self.left = None
        self.right = None
        self.parent = parent

    def info(self):
        if self.parent is None:
            return f"[{self.key} {self.value}]"
        else:
            return f"[{self.key} {self.value} {self.parent.key}]"

    def is_leaf(self):
        return self.left is None and self.right is None

    def has_parent(self):
        return self.parent is not None

    def is_left_child(self):
        return self.parent.left == self


def rotate(rotate_vertex):
    if rotate_vertex.parent.left == rotate_vertex:  # splay_ is a left child
        if rotate_vertex.right is not None:
            rotate_vertex.parent.left = rotate_vertex.right
            rotate_vertex.right.parent = rotate_vertex.parent
        else:
            rotate_vertex.parent.left = None
        rotate_vertex.right = rotate_vertex.parent
    else:  # splay_ is a right child
        if rotate_vertex.left is not None:
            rotate_vertex.parent.right = rotate_vertex.left
            rotate_vertex.left.parent = rotate_vertex.parent
        else:
            rotate_vertex.parent.right = None
        rotate_vertex.left = rotate_vertex.parent
    grandparent  = rotate_vertex.parent.parent
    if grandparent is not None:
        if grandparent.left == rotate_vertex.parent:
            grandparent.left = rotate_vertex
        else:
            grandparent.right = rotate_vertex
    rotate_vertex.parent.parent = rotate_vertex
    rotate_vertex.parent = grandparent

def merge(left_merge_tree, right_merge_tree):
    if left_merge_tree.root is None and right_merge_tree.root is None:
        return None
    elif left_merge_tree.root is None:
        return right_merge_tree.root
    elif right_merge_tree.root is None:
        return left_merge_tree.root
    else:
        max_in_left_subtree = left_merge_tree.internal_max()
        left_merge_tree.splay(max_in_left_subtree)
        left_merge_tree.root.right = right_merge_tree.root
        right_merge_tree.root.parent = left_merge_tree.root
        return left_merge_tree.root


class DBT:
    def __init__(self, root = None):
        self.root = root
        if self.root is not None:
            self.root.parent = None
        self.table = []
        self.is_table_passed = False

    def add(self, key, value):
        if self.root is None:
            self.root = Vertex(key, value, None)
        else:
            current_vertex = self.root
            while True:
                if key < current_vertex.key:
                    if current_vertex.left is None:
                        current_vertex.left = Vertex(key, value, current_vertex)
                        current_vertex.left.is_visited = self.is_table_passed
                        self.splay(current_vertex.left)
                        break
                    else:
                        current_vertex = current_vertex.left

                elif key > current_vertex.key:
                    if current_vertex.right is None:
                        current_vertex.right = Vertex(key, value, current_vertex)
                        current_vertex.right.is_visited = self.is_table_passed
                        self.splay(current_vertex.right)
                        break
                    else:
                        current_vertex = current_vertex.right
                else:   # key == cur_.key
                    self.splay(current_vertex)
                    raise AddException("This key is already in use.")

    def set(self, key, value):
        current_vertex = self.root
        previous_vertex = current_vertex
        while True:
            if current_vertex is None:
                self.splay(previous_vertex)
                raise SetException("There is no key to set.")
            if key == current_vertex.key:
                current_vertex.value = value
                self.splay(current_vertex)
                break
            elif key < current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.left
            elif key > current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.right

    def print(self):
        output = ''
        if self.root is None:
            output = '_'
        else:

            self.form_table()
            for level in range(len(self.table)):
                current_index = -1
                level_size = 2 ** level
                for vertex in self.table[level]:
                    output += "_ " * (vertex[0] - 1 - current_index) + vertex[1].info()
                    current_index = vertex[0]
                    if current_index + 1 < level_size:
                        output += ' '
                if current_index + 1 < level_size:
                    output += "_ " * (level_size - 2 - current_index) + '_'
                output += '\n'
        return output

    def search(self, key):
        current_vertex = self.root
        previous_vertex = current_vertex
        while True:
            if current_vertex is None:
                self.splay(previous_vertex)
                raise SearchException("There is no such key to search")
            if key == current_vertex.key:
                self.splay(current_vertex)
                return current_vertex.value
            elif key < current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.left
            elif key > current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.right

    def min(self):
        current_vertex = self.root
        if current_vertex is not None:
            while current_vertex.left is not None:
                current_vertex = current_vertex.left
            self.splay(current_vertex)
            return current_vertex
        else:
            raise MinMaxException("Tree is empty")

    def max(self):
        current_vertex = self.root
        if current_vertex is not None:
            while current_vertex.right is not None:
                current_vertex = current_vertex.right
            self.splay(current_vertex)
            return current_vertex
        else:
            raise MinMaxException("Tree is empty")

    def internal_min(self, root = None):
        if root is None:
            root = self.root
        current_vertex = root
        if current_vertex is not None:
            while current_vertex.left is not None:
                current_vertex = current_vertex.left
            return current_vertex
        else:
            return None

    def internal_max(self, root = None):
        if root is None:
            root = self.root
        current_vertex = root
        if current_vertex is not None:
            while current_vertex.right is not None:
                current_vertex = current_vertex.right
            return current_vertex
        else:
            return None

    def delete(self, key):
        current_vertex = self.root
        previous_vertex = current_vertex
        while True:
            if current_vertex is None:
                self.splay(previous_vertex)
                raise DeleteException
            if key == current_vertex.key:
                self.splay(current_vertex)
                self.root = merge(DBT(self.root.left), DBT(self.root.right))
                break
            elif key < current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.left
            elif key > current_vertex.key:
                previous_vertex = current_vertex
                current_vertex = current_vertex.right


    def form_table(self): # tree is not empty, there is check in print()
        self.table.clear()
        level = 0
        current_vertex = self.root
        while True:

            if len(self.table) < level + 1:  # increasing tables size
                self.table.append([])

            if current_vertex.is_visited == self.is_table_passed:  #adding vertex in table
                if level == 0:
                    current_vertex.index = 0
                else:
                    if current_vertex.is_left_child():
                        current_vertex.index = current_vertex.parent.index * 2
                    else:
                        current_vertex.index = current_vertex.parent.index * 2 + 1
                self.table[level].append([current_vertex.index, current_vertex])

                current_vertex.is_visited = not current_vertex.is_visited

            if current_vertex.left is not None and current_vertex.left.is_visited == self.is_table_passed:  # tree's passage
                level += 1
                current_vertex=current_vertex.left
            elif current_vertex.right is not None and current_vertex.right.is_visited == self.is_table_passed:
                level += 1
                current_vertex=current_vertex.right
            else:
                level -= 1
                if current_vertex != self.root:
                    current_vertex = current_vertex.parent
                else:
                    break


        self.is_table_passed = not self.is_table_passed


        # if len(self.table) < level + 1:
        #     self.table.append([])
        #
        # if current_vertex is None:
        #     current_vertex = self.root
        #     current_vertex.index = 0
        # else:
        #     if is_left_child:
        #         current_vertex.index = current_vertex.parent.index * 2
        #     else:
        #         current_vertex.index = current_vertex.parent.index * 2 + 1
        # self.table[level].append([current_vertex.index, current_vertex.info()])
        #
        # if current_vertex.is_leaf():
        #     return 0
        # else:
        #     if current_vertex.left is not None:
        #         self.form_table(level + 1, current_vertex.left, True)
        #     if current_vertex.right is not None:
        #         self.form_table(level + 1, current_vertex.right, False)


    def splay(self, splay_vertex):
        while splay_vertex != self.root:
            if splay_vertex.parent == self.root:  # zig
                rotate(splay_vertex)
                self.root = splay_vertex
            elif (splay_vertex.parent.parent.left == splay_vertex.parent and splay_vertex.parent.left == splay_vertex
                or splay_vertex.parent.parent.right == splay_vertex.parent and splay_vertex.parent.right == splay_vertex):
                                                # splay_ and his parent are both left or both right children:
                                                # "zig - zig"
                if splay_vertex.parent.parent == self.root:
                    self.root = splay_vertex
                rotate(splay_vertex.parent)
                rotate(splay_vertex)
            else: # if splay_ is left child and his parent is right or vice versa
                if splay_vertex.parent.parent == self.root:
                    self.root = splay_vertex
                rotate(splay_vertex)     # "zig-zag"
                rotate(splay_vertex)


    def split(self,  split_vertex):
        self.splay(split_vertex)
        return  Pair(split_vertex, split_vertex.right)



def main():
    input_tree = DBT()
    while True:
        try:
            command_string = input()
            if len(command_string) == 0:
                break
            command_info = command_string.split()
            match command_info[0]:
                case 'add':
                    try:
                        input_tree.add(int(command_info[1]), command_info[2])
                    except AddException:
                        print("error")
                case 'set':
                    try:
                        input_tree.set(int(command_info[1]), command_info[2])
                    except SetException:
                        print("error")
                case 'delete':
                    try:
                        input_tree.delete(int(command_info[1]))
                    except DeleteException:
                        print("error")
                case 'search':
                    try:
                        found_value = input_tree.search(int(command_info[1]))
                        print(f'1 {found_value}')
                    except SearchException:
                        print('0')
                case 'min':
                    try:
                        min_vertex = input_tree.min()
                        print(f'{min_vertex.key} {min_vertex.value}')
                    except MinMaxException:
                        print("error")
                case 'max':
                    try:
                        max_vertex = input_tree.max()
                        print(f'{max_vertex.key} {max_vertex.value}')
                    except MinMaxException:
                        print("error")
                case 'print':
                    print(input_tree.print(), end='')
        except EOFError:
            break


if __name__ == '__main__':
   main()

