#!/usr/bin/env python2

import sys
import string


def add_index_w_neglecting_escape_sequence(char_seq):
    index_seq = []
    in_escape_sequence = False
    idx = 0
    for c in char_seq:
        if in_escape_sequence:
            index_seq.append(None)
            if c in string.ascii_letters:
                in_escape_sequence = False
        else:
            if c == u'\x1b':
                in_escape_sequence = True
                index_seq.append(None)
            else:
                index_seq.append(idx)
                idx += 1
    index_seq.append(idx)
    return index_seq


class CutWithThruingEscapeSequence:
    def __init__(self, index_range, starting_leader=None, ending_leader=None):
        self.index_range = index_range
        self.starting_leader = starting_leader
        self.ending_leader = ending_leader

    def cut(self, text_utf8):
        char_seq = text_utf8.decode('utf-8')
        index_seq = add_index_w_neglecting_escape_sequence(char_seq)
        convertedL = self._cut(char_seq, index_seq)
        return convertedL.encode('utf-8')

    def _cut(self, char_seq, index_seq):
        start_pos, end_pos = self.index_range

        assert len(index_seq) == len(char_seq) + 1
        char_count = index_seq[-1]
        sp = 0 if start_pos is None else \
                char_count + start_pos if start_pos < 0 else \
                start_pos
        sp = max(0, min(char_count, sp))
        ep = char_count if end_pos is None else \
                char_count + end_pos if end_pos < 0 else \
                end_pos
        ep = max(0, min(char_count, ep))

        char_omitted_at_start = False
        char_omitted_at_end = False
        buf = []
        for c, i in zip(char_seq, index_seq):
            if i is None:
                buf.append(c)
            elif i < sp:
                char_omitted_at_start = True
            elif i >= ep:
                char_omitted_at_end = True
            else:
                buf.append(c)

        if char_omitted_at_start and self.starting_leader:
            buf.insert(0, self.starting_leader)
        if char_omitted_at_end and self.ending_leader:
            buf.append(self.ending_leader)

        return u''.join(buf)


USAGE = '''
Etcut, Escape-sequence Thru-ing CUT command.

Usage: %s [-l] RANGE [INPUT]

Removes characters appears out of RANGE in each line in INPUT.
RANGE's format is either 'start_pos:end_pos', ':end_pos', or 'start_pos:',
where each position is 0-based index.
When start_pos or end_pos is omitted, the default value is 0 or end-of-line.
An index can be a negative value. Such negative index is counted from a end of line
(that is, the last character is -1 and the second last character is -2, and so on).
'''


def main(argv):
    argv0 = argv.pop(0)

    opt_w_leader = False
    if argv and argv[0] in ('-l', '--with-leader'):
        opt_w_leader = True
        argv.pop(0)

    index_range_str = argv.pop(0)

    input_file = None
    if argv:
        input_file = argv.pop(0)

    if argv:
        sys.exit("error: too many command-line arguments")

    i = index_range_str.find(':')
    if i < 0:
        v = int(index_range_str)
        index_range = (v, v + 1)
    else:
        start_str, end_str = index_range_str[:i], index_range_str[i + 1:]
        start_pos = int(start_str) if start_str else None
        end_pos = int(end_str) if end_str else None
        index_range = (start_pos, end_pos)

    starting_leader, ending_leader = (u'... ', u' ...') if opt_w_leader else (None, None)
    cwt = CutWithThruingEscapeSequence(index_range, starting_leader, ending_leader)

    write = sys.stdout.write
    if input_file:
        with open(input_file, 'rb') as inp:
            for L in inp:
                L = L.rstrip('\n')
                write(cwt.cut(L))
                write('\n')
    else:
        for L in sys.stdin:
            L = L.rstrip('\n')
            write(cwt.cut(L))
            write('\n')


if __name__ == '__main__':
    main(sys.argv)
