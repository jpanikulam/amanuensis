
class TabConverter(object):
    _arrangement = ['e', 'a', 'd', 'g', 'b', 'e']
    _progression = ['a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', ]

    def geodesic_increment(self, note):
        ind = self._progression.index(note) + 1
        max_ind = len(self._progression)
        return self._progression[ind % max_ind]

    def print_bar(self, bar):
        print '-',
        for string in self._arrangement:
            print string, '-',

    def print_guitar(self):
        print '-',
        for string in self._arrangement:
            print string, '-',

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
                padding = (pad_chars - len(note)) * pad_char
                print note + padding,


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
tc.print_guitar()
