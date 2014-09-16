#coding: utf-8

import unittest

import etcut

class EtcutTest(unittest.TestCase):
    def test_add_index_w_neglecting_escape_sequence_simple(self):
        for inp in [u'', u'123456789', u'\n', u'\t', u' ', u'  123  ']:
            act_index_seq = etcut.add_index_w_neglecting_escape_sequence(inp)
            exp_index_seq = list(xrange(len(inp))) + [len(inp)]

            self.assertEqual(act_index_seq, exp_index_seq)
            self.assertSequenceEqual([inp[i] for i in act_index_seq[:-1]], inp)

    def test_add_index_w_neglecting_escape_sequence(self):
        escape_sequence_text_red = u'\x1b[31m'
        escape_sequence_text_reset = u'\x1b[m'
        inp = u'An ' + escape_sequence_text_red + u'apple' + escape_sequence_text_reset + ' is red.'
        act_index_seq = etcut.add_index_w_neglecting_escape_sequence(inp)
        exp_index_seq = [0,1,2] + \
                [None] * len(escape_sequence_text_red) + \
                [3,4,5,6,7] + \
                [None] * len(escape_sequence_text_reset) + \
                [8,9,10,11,12,13,14,15] + \
                [16]

        self.assertEqual(act_index_seq, exp_index_seq)

    def test_CutWithThruingEscapeSequence_wo_any_modification(self):
        sut = etcut.CutWithThruingEscapeSequence((None, None), starting_leader=None, ending_leader=None)
        for inp in [u'', u'123456789', u'\n', u'\t', u' ', u'  123  ']:
            inp_index_seq = list(xrange(len(inp))) + [len(inp)]
            act = sut._cut(inp, inp_index_seq)
            exp = inp
            self.assertEqual(act, exp)

    def test_CutWithThruingEscapeSequence_simple(self):
        sut = etcut.CutWithThruingEscapeSequence((0, 3), starting_leader=None, ending_leader=None)
        inp_and_exp = [
            (u'', u''),
            (u'123', u'123'),
            (u'123456789', u'123'),
            (u'\n', u'\n'),
            (u' ', u' '),
            (u'  123  ', u'  1'),
        ]
        for inp, exp in inp_and_exp:
            inp_index_seq = list(xrange(len(inp))) + [len(inp)]
            act = sut._cut(inp, inp_index_seq)
            self.assertEqual(act, exp)

        sut = etcut.CutWithThruingEscapeSequence((-3, None), starting_leader=None, ending_leader=None)
        inp_and_exp = [
            (u'', u''),
            (u'123', u'123'),
            (u'123456789', u'789'),
            (u'\n', u'\n'),
            (u' ', u' '),
            (u'  123  ', u'3  '),
        ]
        for inp, exp in inp_and_exp:
            inp_index_seq = list(xrange(len(inp))) + [len(inp)]
            act = sut._cut(inp, inp_index_seq)
            self.assertEqual(act, exp)

        sut = etcut.CutWithThruingEscapeSequence((3, 6), starting_leader=None, ending_leader=None)
        inp_and_exp = [
            (u'', u''),
            (u'123', u''),
            (u'123456789', u'456'),
            (u'\n', u''),
            (u' ', u''),
            (u'  123  ', u'23 '),
        ]
        for inp, exp in inp_and_exp:
            inp_index_seq = list(xrange(len(inp))) + [len(inp)]
            act = sut._cut(inp, inp_index_seq)
            self.assertEqual(act, exp)

    def test_CutWithThruingEscapeSequence_w_escape_sequence(self):
        sut = etcut.CutWithThruingEscapeSequence((0, 3), starting_leader=None, ending_leader=None)
        escape_sequence_text_red = u'\x1b[31m'
        escape_sequence_text_reset = u'\x1b[m'
        char_seq = u'An ' + escape_sequence_text_red + u'apple' + escape_sequence_text_reset + ' is red.'
        index_seq = etcut.add_index_w_neglecting_escape_sequence(char_seq)
        act = sut._cut(char_seq, index_seq)
        self.assertEqual(act, u'An ' + escape_sequence_text_red + escape_sequence_text_reset)

        sut = etcut.CutWithThruingEscapeSequence((3, 6), starting_leader=None, ending_leader=None)
        act = sut._cut(char_seq, index_seq)
        self.assertEqual(act, escape_sequence_text_red + u'app' + escape_sequence_text_reset)

        sut = etcut.CutWithThruingEscapeSequence((-3, None), starting_leader=None, ending_leader=None)
        act = sut._cut(char_seq, index_seq)
        self.assertEqual(act, escape_sequence_text_red + escape_sequence_text_reset + u'ed.')


if __name__ == "__main__":
    unittest.main()
