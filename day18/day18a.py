tree_dims = [(0, (1,2)), (1, (0, 2)), (2, (0, 1))]


def main(input_file_name):
    with open(input_file_name) as input_file:
        droplet = [
            [int(coord) for coord in line.strip().split(',')]
            for line in input_file.readlines() if line != '\n'
        ]
    trees = build_trees(droplet)
    return count_exposed_sides(trees, droplet)


def build_trees(droplet):
    return [
        build_tree(droplet, *tree_dims[0]),
        build_tree(droplet, *tree_dims[1]),
        build_tree(droplet, *tree_dims[2])
    ]


def build_tree(droplet, child_dim, branch_dims):
    tree = {}
    for cube in droplet:
        if cube[branch_dims[0]] not in tree.keys():
            tree[cube[branch_dims[0]]] = {}
        if cube[branch_dims[1]] not in tree[cube[branch_dims[0]]].keys():
            tree[cube[branch_dims[0]]][cube[branch_dims[1]]] = []
        tree[cube[branch_dims[0]]][cube[branch_dims[1]]].append(cube[child_dim])
    return tree


def count_exposed_sides(trees, droplet):
    sides = 0
    for cube in droplet:
        for tree_idx, tree in enumerate(trees):
            for direction in (-1, 1):
                if (
                        cube[tree_dims[tree_idx][0]] + direction
                        not in tree[cube[tree_dims[tree_idx][1][0]]][cube[tree_dims[tree_idx][1][1]]]
                ):
                    sides += 1
    return sides


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
