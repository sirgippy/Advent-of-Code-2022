def mark_visible_trees(tree_list):
    tree_list[0]['visible'] = True
    max_height = tree_list[0]['height']
    for tree in tree_list[1:]:
        if tree['height'] > max_height:
            tree['visible'] = True
            max_height = tree['height']


def get_scenic_score(row_idx, column_idx, tree_grid):
    this_tree = tree_grid[row_idx][column_idx]

    column = [row[column_idx] for row in tree_grid]

    left = get_viewing_distance(this_tree, [tree for tree in reversed(tree_grid[row_idx][0:column_idx])])
    right = get_viewing_distance(this_tree, tree_grid[row_idx][column_idx + 1:])
    up = get_viewing_distance(this_tree, [tree for tree in reversed(column[0:row_idx])])
    down = get_viewing_distance(this_tree, column[row_idx + 1:])

    return left * right * up * down


def get_viewing_distance(this_tree, sight_line):
    viewing_distance = len(sight_line)
    for idx, tree in enumerate(sight_line):
        if tree['height'] >= this_tree['height']:
            viewing_distance = idx + 1
            break
    return viewing_distance


with open('input.txt') as input_file:
    rows = [line.strip() for line in input_file.readlines()]

tree_grid = [[{'height': int(height), 'visible': False} for height in row] for row in rows]

for row in tree_grid:
    mark_visible_trees(row)
    mark_visible_trees([tree for tree in reversed(row)])

for idx in range(0, len(tree_grid[0])):
    column = [row[idx] for row in tree_grid]
    mark_visible_trees(column)
    mark_visible_trees([tree for tree in reversed(column)])

print(sum([sum([1 for tree in row if tree['visible']]) for row in tree_grid]))
print(
    max(
        [max(
            [get_scenic_score(r, c, tree_grid) for c in range(len(tree_grid[0]))]
        ) for r in range(len(tree_grid))]
    )
)
