#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 19:30:30 2018

@author: ksu
"""
import unittest
from geobot import geojson_processing

suite = unittest.TestSuite()

class TestGeoBot(unittest.TestCase):

    def test_document_type(self):
       new_file = open('sample1.geojson','wb+')
       self.assertEqual({'Polygon': 1, 'LineString': 1, 'Point': 1}, geojson_processing(new_file))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGeoBot)
print(suite)
unittest.TextTestRunner().run(suite)

