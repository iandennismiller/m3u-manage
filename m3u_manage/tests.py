# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from unittest import TestCase


class BasicTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_basic(self):
    #     "ensure the minimum test works"
    #     self.assertEqual(mesh(1), 2)

    def test_true(self):
        "ensure the minimum test works"
        self.assertTrue(True)

    def test_curate(self):
        "ensure the minimum test works"
        from . import curate
        self.assertTrue(curate("etc/example-config.json"))

    def test_mesh(self):
        "ensure the minimum test works"
        from . import mesh, combine_m3us
        self.assertTrue(combine_m3us(["", ""]))
        self.assertTrue(mesh(outfile="/tmp/out.m3u", filenames=[""]))

    def test_analyze(self):
        "ensure the minimum test works"
        from . import analyze
        self.assertTrue(analyze("etc"))

    # @attr("skip")
    # def test_skip(self):
    #     "this always fails, except when it is skipped"
    #     self.assertTrue(False)
