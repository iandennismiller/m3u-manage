# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from unittest import TestCase
from . import main


class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic(self):
        "ensure the minimum test works"
        self.assertEqual(main(1), 2)

    @attr("skip")
    def test_skip(self):
        "this always fails, except when it is skipped"
        self.assertTrue(False)
