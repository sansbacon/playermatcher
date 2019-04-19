# -*- coding: utf-8 -*-
# test_player_mflxref.py

import logging
import random
import sys
import unittest

from playermatcher.match import *


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Match_test(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.players = ['Joe Thomas', 'Thomas Johnson', 'Thomas Joseph',
                         'Joseph Thime', 'Timmy Johnson']

    @property
    def player(self):
        return random.choice(self.players)

    def test_read_input(self):
        '''
        prompt, timeout, timeoutmsg
        '''
        prompt = 'Enter value: '
        default = 'Hello!'
        val = read_input(prompt, 1, default)
        self.assertEqual(val, default)

    def test_player_match_fuzzy(self):
        '''
        to_match, match_from
        returns match, conf
        '''
        pl = self.player
        match, conf = player_match_fuzzy(pl, self.players)
        self.assertEqual(match, pl)
        self.assertGreater(conf, 0)

    def test_player_match_interactive(self):
        '''
        to_match, match_from, choices, timeout
        returns match
        '''
        pl = self.player
        match, conf = player_match_interactive(pl, self.players, timeout=1, default=pl)
        self.assertEqual(match, pl)
        self.assertGreater(conf, 0)
        pl = 'John Thomas'
        match, conf = player_match_interactive(pl, self.players, timeout=1, default=pl)
        self.assertNotEqual(match, pl)
        self.assertGreater(conf, 0)

    def test_player_name_dict(self):
        '''
        players, full_name_key, first_name_key, last_name_key
        returns defaultdict
        '''
        l = [{'full_name': 'Joe Thomas', 'pos': 'WR'},
             {'full_name': 'Tom Johnson', 'pos': 'TE'}]
        d = player_name_dict(l, full_name_key='full_name')
        self.assertIsInstance(d, defaultdict)

    def test_player_namepos_dict(self):
        '''
        players, pos_key, full_name_key, first_name_key, last_name_key
        returns defaultdict
        '''
        l = [{'full_name': 'Joe Thomas', 'pos': 'WR'},
             {'full_name': 'Tom Johnson', 'pos': 'TE'}]
        d = player_namepos_dict(l, full_name_key='full_name', pos_key='pos')
        self.assertIsInstance(d, defaultdict)

    def test_player_match(self):

        '''
        Tries direct match, then fuzzy match, then interactive

        Args:
            to_match(str):
            match_from(list): of str
            thresh(int): threshold for quality of match (1-100), default 90
            timeout(int): how long to wait for interactive prompt, default 2

        Returns:
            str

        '''
        pl = self.player
        match = player_match(pl, self.players, thresh=85, timeout=1)
        self.assertEqual(match, pl)
        pl = 'John Thomas'
        match = player_match(pl, self.players, thresh=70, timeout=1)
        self.assertNotEqual(match, pl)


if __name__=='__main__':
    unittest.main()