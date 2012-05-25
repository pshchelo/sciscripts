#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""R = C*M

d
	dextran

s
	sucrose

g
	glucose

"""
from __future__ import division
import sys
from PySide import QtGui

class Sugars(QtGui.QWidget):
    """"""
    def __init__(self):
        super(Sugars, self).__init__()
        self.initUI()
        
    def initUI(self):
        
        dextrmasslabel = QtGui.QLabel("Dextran molar mass", self)
        self.dextranmass = QtGui.QSpinBox(self)
        self.dextranmass.setRange(0,1000)
        self.dextranmass.setValue(500)
        self.dextranmass.setSuffix(" kDa")
        self.dextranmass.valueChanged.connect(self.updateResult)
        
        dextrconclabel = QtGui.QLabel("Dextran weight concentration", self)
        self.dextranconc = QtGui.QDoubleSpinBox(self)
        self.dextranconc.setRange(0,100)
        self.dextranconc.setValue(5)
        self.dextranconc.setSuffix(" w%")
        self.dextranconc.valueChanged.connect(self.updateResult)
        
        self.result = QtGui.QLabel(self)
        self.updateResult()
        
        grid = QtGui.QGridLayout()
        grid.addWidget(dextrmasslabel, 0, 0)
        grid.addWidget(self.dextranmass, 0, 1)
        grid.addWidget(dextrconclabel, 1, 0)
        grid.addWidget(self.dextranconc, 1, 1)
        grid.addWidget(self.result, 3, 0, 1, 2)
        
        self.setLayout(grid)
        self.setWindowTitle("Sugars")
        self.show()
        
    def updateResult(self):
        Md, Rd, Cd, Rg, Cg, Rs, Cs = self.calculate()
        result = "Dextran: %i Da at %.3f mg/ml = %.6f mM\n"%(Md, Rd, 1000*Cd)
        result += "Glucose: %.3f mg/ml = %.3f mM\n"%(Rg, 1000*Cg)
        result += "Sucrose: %.3f mg/ml = %.3f mM"%(Rs, 1000*Cs)
        
        self.result.setText(result)
    
    def calculate(self):
        # water density in mg/ml
        Rw = 1000
        
        # molecular weights in g/mol = mg/mmol
        Ms = 342.3
        Mg = 180.16
        Md = self.dextranmass.value()*1000
        
        # mass concentration of dextran, mg/mg
        Pd = self.dextranconc.value()/100
        
        Rd = Rw * Pd / (1 - Pd) # ignoring volume expansion
        
        Cd = Rd / Md
        Rg = Rd * (Md - Ms) / (Ms - Mg) * Mg / Md
        
        Cg = Rg/Mg
        
        Rs = Rd + Rg
        
        Cs = Rs/Ms
        
        return Md, Rd, Cd, Rg, Cg, Rs, Cs

def main():
    app = QtGui.QApplication(sys.argv)
    window = Sugars()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()