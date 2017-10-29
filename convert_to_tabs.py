
class TabConverter(object):
    _arrangement = [('e', 2), ('a', 2), ('d', 3), ('g', 3), ('b', 3), ('e', 4)]
    _progression = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', ]

    def geodesic_increment(self, note):
        note_name, note_num = note
        ind = self._progression.index(note_name) + 1
        max_ind = len(self._progression)
        next_note_name = self._progression[ind % max_ind]
        if ind >= max_ind:
            next_note_octave = note_num + 1
        else:
            next_note_octave = note_num
        return (next_note_name, next_note_octave)

    def print_bar(self, bar):
        print '-',
        for string in self._arrangement:
            print string, '-',

    def print_guitar(self):
        print '-',
        for string in self._arrangement:
            print string[0] + str(string[1]) + ' ',
        print '\n  _____________________',
        string_states = self._arrangement
        pad_chars = 3
        pad_char = ' '

        for k in range(10):
            string_states = map(self.geodesic_increment, string_states)
            print
            for note in string_states:
                print '  |',
            print
            print pad_char,
            for note in string_states:
                note_txt = ''.join(map(str, note))
                padding = (pad_chars - len(note_txt)) * pad_char
                print note_txt + padding,


bar = [
    [('F', '3'), ('F', '4')],
    [('C', '0'), ('F', '3'), ('F', '4')],
    [('C', '0'), ('F', '3'), ('F', '4')],
    [('F', '3'), ('F', '4')],
    [('C', '0'), ('F', '3')],
    [('C', '0'), ('F', '3'), ('F', '4')],
    [('F', '3'), ('F', '4'), ('C', '5')],
    [('C', '0'), ('F', '3')],
    [('C', '0'), ('F', '3'), ('F', '4')],
    [('C', '0'), ('F', '3'), ('F', '4'), ('C', '5')],
    [('C', '0'), ('F', '3'), ('F', '4')],
]

tc = TabConverter()
# tc.print_bar(bar)
# tc.print_guitar()

note = ('e', 2)
for k in range(55):
    print note
    note = tc.geodesic_increment(note)
