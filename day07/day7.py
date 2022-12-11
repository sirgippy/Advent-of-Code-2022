class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.files = []

    def add_child(self, name):
        new_dir = Directory(name, self)
        self.children.append(new_dir)
        return new_dir

    def add_file(self, name, file_size):
        self.files.append((name, int(file_size)))

    def get_child(self, name):
        return next((d for d in self.children if d.name == name), None)

    def get_size(self):
        return sum([f[1] for f in self.files]) + sum([d.get_size() for d in self.children])

    def get_dirs_to_save(self, max_size=100000):
        dirs_to_save = []
        for dir in self.children:
            dirs_to_save += dir.get_dirs_to_save(max_size)
        if self.get_size() <= max_size:
            dirs_to_save.append(self)
        return dirs_to_save

    def smallest_possible(self, space_needed):
        smallest = None
        for child in self.children:
            smallest_in_child = child.smallest_possible(space_needed)
            if smallest_in_child and (not smallest or smallest_in_child.get_size() < smallest.get_size()):
                smallest = smallest_in_child
        if not smallest and self.get_size() > space_needed:
            smallest = self
        return smallest


root_dir = Directory('/', None)
current_dir = root_dir
with open('input.txt') as input_file:
    line = input_file.readline().strip()
    while line != '':
        if line[2:4] == 'cd':
            if line[5:] == '/':
                current_dir = root_dir
            elif line[5:] == '..':
                current_dir = current_dir.parent
            else:
                next_dir = current_dir.get_child(line[5:])
                if next_dir:
                    current_dir = next_dir
                else:
                    current_dir = current_dir.add_child(line[5:])
            line = input_file.readline().strip()
        else:  # must be ls
            line = input_file.readline().strip()
            while line != '' and line[0] != '$':
                if line[0:3] == 'dir':
                    child = current_dir.get_child(line[4:])
                    if not child:
                        current_dir.add_child(line[4:])
                else:
                    (file_size, name) = line.split(' ')
                    current_dir.add_file(name, file_size)
                line = input_file.readline().strip()

dirs_to_save = root_dir.get_dirs_to_save()
print(sum([d.get_size() for d in dirs_to_save]))

space_needed = root_dir.get_size() - 40000000
print(root_dir.smallest_possible(space_needed).get_size())
