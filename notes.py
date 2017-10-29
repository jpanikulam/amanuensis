def clean_split(text, delim=','):
    text = text.strip()
    return map(lambda o: o.strip(), text.split(delim))


def read_notes(file):
    notes = {}
    for line in file:
        split = clean_split(line, ',')[:-1]
        if split[-1] == '':
            continue
        notes[(split[0], int(split[1]))] = float(split[2])
    return notes


# Map notes to frequencies
notes = read_notes(open('notes.txt'))

# Map frequencies to note tuples
inv_notes = {v: k for k, v in notes.items()}

if __name__ == '__main__':
    path = 'notes.txt'
    with open(path) as f:
        read_notes(f)
