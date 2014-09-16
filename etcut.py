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
    return index_seq, idx


def gen_cut_w_thru_escape_sequences(char_range):
    start_pos, end_pos = char_range

    def cut_func(L):
        buf = []
        char_seq = L.decode('utf-8')
        index_seq, char_count = add_index_w_neglecting_escape_sequence(char_seq)
        assert len(index_seq) == len(char_seq)
        if start_pos is None:
            sp = 0
        elif start_pos < 0:
            sp = char_count + start_pos
        else:
            sp = start_pos
        sp = max(0, min(char_count, sp))
        if end_pos is None:
            ep = char_count
        elif end_pos < 0:
            ep = char_count + end_pos
        else:
            ep = end_pos
        ep = max(0, min(char_count, ep))
        for c, i in zip(char_seq, index_seq):
            if i is None or sp <= i < ep:
                buf.append(c)
        return u''.join(buf).encode('utf-8')

    return cut_func


USAGE = '''
Etcut, Escape-sequence Thru-ing CUT command.

Usage: %s RANGE [INPUT]

Removes characters appears out of RANGE in each line in INPUT.
RANGE's format is either 'start_pos:end_pos', ':end_pos', or 'start_pos:',
where each position is 0-based index.
When start_pos or end_pos is omitted, the default value is 0 or end-of-line.
An index can be a negative value. Such negative index is counted from a end of line
(that is, the last character is -1 and the second last character is -2, and so on).
'''


def main(argv):
    argv0 = argv.pop(0)

    char_range_str = argv.pop(0)

    if argv:
        input_file = argv.pop(0)

    if argv:
        sys.exit("error: too many command-line arguments")

    i = char_range_str.find(':')
    if i < 0:
        v = int(char_range_str)
        char_range = (v, v + 1)
    else:
        start_str, end_str = char_range_str[:i], char_range_str[i + 1:]
        start_pos = int(start_str) if start_str else None
        end_pos = int(end_str) if end_str else None
        char_range = (start_pos, end_pos)

    cut_func = gen_cut_w_thru_escape_sequences(char_range)

    write = sys.stdout.write
    if input_file:
        with open(input_file, 'rb') as inp:
            for L in inp:
                L = L.rstrip('\n')
                write(cut_func(L))
                write('\n')
    else:
        for L in sys.stdin:
            L = L.rstrip('\n')
            write(cut_func(L))
            write('\n')


if __name__ == '__main__':
    main(sys.argv)
