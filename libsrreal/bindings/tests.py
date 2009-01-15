#!/usr/bin/env python
"""A small test for the bindings."""

from pyobjcryst import *
from __init__ import *
import numpy

def getNi(numscat = 1):

    if numscat < 1: numscat = 1

    pi = numpy.pi
    c = Crystal(3.52, 3.52, 3.52, "225")
    for i in xrange(numscat):
        sp = ScatteringPowerAtom("Ni%i"%i, "Ni")
        sp.SetBiso(8*pi*pi*0.003)
        c.AddScatteringPower(sp)
        atomp = Atom(0, 0, 0, "Ni%i"%i, sp, 1.0/numscat)
        c.AddScatterer(atomp)
    return c

def getLaMnO3():

    pi = numpy.pi
    crystal = Crystal(5.486341, 5.619215, 7.628206, 90, 90, 90, "P b n m")
    # La1
    sp = ScatteringPowerAtom("La1", "La")
    sp.SetBiso(8*pi*pi*0.003)
    atom = Atom(0.996096, 0.0321494, 0.25, "La1", sp)
    crystal.AddScatteringPower(sp)
    crystal.AddScatterer(atom)
    # Mn1
    sp = ScatteringPowerAtom("Mn1", "Mn")
    sp.SetBiso(8*pi*pi*0.003)
    atom = Atom(0, 0.5, 0, "Mn1", sp)
    crystal.AddScatteringPower(sp)
    crystal.AddScatterer(atom)
    # O1
    sp = ScatteringPowerAtom("O1", "O")
    sp.SetBiso(8*pi*pi*0.003)
    atom = Atom(0.0595746, 0.496164, 0.25, "O1", sp)
    crystal.AddScatteringPower(sp)
    crystal.AddScatterer(atom)
    # O2
    sp = ScatteringPowerAtom("O2", "O")
    sp.SetBiso(8*pi*pi*0.003)
    atom = Atom(0.720052, 0.289387, 0.0311126, "O2", sp)
    crystal.AddScatteringPower(sp)
    crystal.AddScatterer(atom)

    return crystal

def printBonds():

    c = getNi()
    bi = BondIterator(c, 0, 4)
    getUnitCell(c)

    scl = c.GetScatteringComponentList()
    for sc in scl:
        bi.setScatteringComponent(sc)
        bi.rewind()
        while(not bi.finished()):
            bp = bi.getBondPair()
            print bp
            bi.next()
    return

def printPDF():
    
    c = getNi()
    #c = getLaMnO3()
    rvals = numpy.arange(0, 10, 0.05)
    biter = BondIterator(c)
    bwcalc = JeongBWCalculator()

    pdfcalc = PDFCalculator(biter, bwcalc)
    pdfcalc.setQmax(30)
    pdfcalc.setCalculationPoints(rvals)
    bwcalc.setDelta2(0)
    pdf1 = timeCalculation(pdfcalc)
    bwcalc.setDelta2(5)
    pdf2 = timeCalculation(pdfcalc)


    if 0:
        from pylab import plot, show
        plot(rvals, pdf1, rvals, pdf2)
        show()
    
    return

def timeCalculation(pdfcalc):
    import time
    t1 = time.time()
    pdf = pdfcalc.getPDF()
    t2 = time.time()
    print 1000*(t2-t1);
    return pdf

def speedTest():
    """Make some changes to the crystal and calculate the PDF each time."""


    crystal = getLaMnO3()
    rvals = numpy.arange(0, 10, 0.05)
    biter = BondIterator(crystal)
    bwcalc = JeongBWCalculator()

    pdfcalc = PDFCalculator(biter, bwcalc)
    pdfcalc.setQmax(30)
    pdfcalc.setCalculationPoints(rvals)
    bwcalc.setDelta2(0)

    print "Times are in ms"

    print "Initial calculation = ",
    pdf1 = timeCalculation(pdfcalc)

    # Change the bwcalc. This should take about the same time.
    bwcalc.setDelta2(5)
    print "Change in BW calculator = ",
    pdf2 = timeCalculation(pdfcalc)

    # Change an x-coordinate
    scatla = crystal.GetScatt("La1")
    scatla.GetClockScatterer().Print()
    scatla.SetX(0.8)
    scatla.GetClockScatterer().Print()
    print "Change in atom coordinate = ",
    pdf3 = timeCalculation(pdfcalc)

    # Change an thermal parameter
    pi = numpy.pi
    sp = crystal.GetScatteringPower("La1")
    sp.SetBiso(8*pi*pi*0.008)
    print "Change in Biso = ",
    pdf4 = timeCalculation(pdfcalc)

    # Change another atom
    scato1 = crystal.GetScatt("O1")
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.05)
    scato1.GetClockScatterer().Print()
    print "Change in atom coordinate = ",
    pdf5 = timeCalculation(pdfcalc)

    # Change properties of two atoms. Should
    #print scatla.GetX()
    scatla.GetClockScatterer().Print()
    scatla.SetX(0.9)
    scatla.GetClockScatterer().Print()
    #print scatla.GetX()
    #scatla.SetX(0.8)
    #print scatla.GetX()
    #scatla.SetX(0.9)
    #print scatla.GetX()
    #scato1.SetX(0.07)
    #print scato1.GetX()
    #scato1.SetX(0.06)
    #print scato1.GetX()
    #print scato1.GetX()
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.07)
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.071)
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.072)
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.073)
    scato1.GetClockScatterer().Print()
    scato1.SetX(0.074)
    scato1.GetClockScatterer().Print()
    #print scato1.GetX()
    print "Change in two atoms = ",
    pdf6 = timeCalculation(pdfcalc)

    if 0:
        from pylab import plot, show
        plot(rvals, pdf1, rvals, pdf2, rvals, pdf3, rvals, pdf4, 
                rvals, pdf5, rvals, pdf6)
        show()
    return

def scalingTest():
    
    rvals = numpy.arange(0, 10, 0.05)
    bwcalc = JeongBWCalculator()

    print "PDF calculation"
    for i in range(10):
        c = getNi(i+1)
        biter = BondIterator(c)

        pdfcalc = PDFCalculator(biter, bwcalc)
        pdfcalc.setQmax(30)
        pdfcalc.setCalculationPoints(rvals)
        print "%-2i scatterers"%(i+1,), 
        pdf = timeCalculation(pdfcalc)

    print "Unit cell generation"
    import time
    for i in range(10):
        c = getNi(i+1)
        t1 = time.time()
        getUnitCell(c)
        t2 = time.time()
        print 1000*(t2-t1)


if __name__ == "__main__":
    
    #scalingTest()
    speedTest()

