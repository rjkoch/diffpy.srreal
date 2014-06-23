#!/usr/bin/env python

"""Unit tests for diffpy.srreal.scatteringfactortable
"""


import os
import unittest
import cPickle

from diffpy.srreal.scatteringfactortable import ScatteringFactorTable


class LocalTable(ScatteringFactorTable):
    def clone(self):  return LocalTable(self)
    def create(self): return LocalTable()
    def _standardLookup(self, smbl, q):   return q + 1
    def radiationType(self):   return "LTB"
    def type(self):   return "localtable"
    def ticker(self):
        self.tcnt += 1
        return ScatteringFactorTable.ticker(self)
    tcnt = 0

LocalTable()._registerThisType()


##############################################################################
class TestScatteringFactorTable(unittest.TestCase):

    def setUp(self):
        self.sftx = ScatteringFactorTable.createByType('X')
        self.sftn = ScatteringFactorTable.createByType('N')
        return

    def tearDown(self):
        return

    def test_class_registry(self):
        """check if instances are aliased by radiationType().
        """
        ltb = ScatteringFactorTable.createByType('LTB')
        self.failUnless(type(ltb) is LocalTable)
        ltb2 = ScatteringFactorTable.createByType('localtable')
        self.failUnless(type(ltb2) is LocalTable)
        return

    def test_ticker(self):
        """check ScatteringFactorTable.ticker()
        """
        from diffpy.srreal.eventticker import EventTicker
        et0 = EventTicker(self.sftx.ticker())
        self.sftx.setCustomAs('D', 'H')
        et1 = self.sftx.ticker()
        self.assertNotEqual(et0, et1)
        self.failUnless(et0 < et1)
        return

    def test_ticker_override(self):
        """check Python override of ScatteringFactorTable.ticker.
        """
        from diffpy.srreal.eventticker import EventTicker
        from diffpy.srreal.pdfcalculator import PDFCalculator
        lsft = LocalTable()
        self.assertEqual(0, lsft.tcnt)
        et0 = lsft.ticker()
        self.assertEqual(1, lsft.tcnt)
        et1 = ScatteringFactorTable.ticker(lsft)
        self.assertEqual(1, lsft.tcnt)
        self.assertEqual(et0, et1)
        et0.click()
        self.assertEqual(et0, et1)
        # check that implicit ticker call from PDFCalculator is
        # handled by Python override of the ticker method.
        pc = PDFCalculator()
        pc.scatteringfactortable = lsft
        pc.ticker()
        self.assertEqual(2, lsft.tcnt)
        return

    def test_pickling(self):
        """check pickling of ScatteringFactorTable instances.
        """
        self.assertEqual(0, len(self.sftx.getCustomSymbols()))
        self.sftx.setCustomAs('Na', 'Na', 123)
        self.sftx.setCustomAs('Calias', 'C')
        self.assertEqual(2, len(self.sftx.getCustomSymbols()))
        sftx1 = cPickle.loads(cPickle.dumps(self.sftx))
        self.assertEqual(2, len(sftx1.getCustomSymbols()))
        self.assertAlmostEqual(123, sftx1.lookup('Na'), 12)
        self.assertEqual(self.sftx.lookup('C'), sftx1.lookup('Calias'))
        self.assertEqual(self.sftx.type(), sftx1.type())
        return

    def test_pickling_derived(self):
        """check pickling of a derived classes.
        """
        lsft = LocalTable()
        self.assertEqual(3, lsft._standardLookup('Na', 2))
        self.assertEqual(set(), lsft.getCustomSymbols())
        lsft.foobar = 'asdf'
        lsft.setCustomAs('Na', 'Na', 123)
        self.assertEqual(1, len(lsft.getCustomSymbols()))
        lsft1 = cPickle.loads(cPickle.dumps(lsft))
        self.assertEqual(1, len(lsft1.getCustomSymbols()))
        self.assertAlmostEqual(123, lsft1.lookup('Na'), 12)
        self.assertEqual('asdf', lsft1.foobar)
        self.assertEqual(lsft.type(), lsft1.type())
        self.assertEqual(3, lsft1._standardLookup('Cl', 2))
        self.assertEqual(1, lsft1.lookup('H'))
        return

# End of class TestScatteringFactorTable

if __name__ == '__main__':
    unittest.main()

# End of file
