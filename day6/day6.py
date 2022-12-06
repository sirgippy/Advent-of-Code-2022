def find_marker(datastream, marker_len):
    sequence = datastream[0:marker_len]
    for marker, character in enumerate(datastream[marker_len:]):
        if len(set(sequence)) == marker_len:
            return marker + marker_len
        sequence = sequence[1:marker_len] + character


with open('input.txt') as input_file:
    datastream = input_file.readline().strip()

print(find_marker(datastream, 4))
print(find_marker(datastream, 14))
