#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Calculate centrifuge parameters
"""
import math
import sys
from PySide import QtCore, QtGui

class Centrifuge(QtGui.QWidget):
    def __init__(self):
        super(Centrifuge, self).__init__()
        self.initGui()
        
    def initGui(self):
        hint = QtGui.QLabel(u'For 45˚ inclined geometry', self)
        hint.setAlignment(QtCore.Qt.AlignHCenter)
        diameterlabel = QtGui.QLabel('Diameter', self)
        self.diameter = QtGui.QDoubleSpinBox(self)
        self.diameter.setSuffix(u' µm')
        self.diameter.setRange(1, 500)
        self.diameter.setValue(20)
        self.diameter.valueChanged.connect(self.updateResult)
        
        timelabel = QtGui.QLabel('Time', self)
        self.time = QtGui.QDoubleSpinBox(self)
        self.time.setSuffix(' s')
        self.time.setRange(60,86400)
        self.time.setValue(1800)
        self.time.valueChanged.connect(self.updateResult)

        indensitylabel = QtGui.QLabel('Inside density', self)
        self.indensity = QtGui.QDoubleSpinBox(self)
        self.indensity.setSuffix(' mg/ml')
        self.indensity.setRange(0,10000)
        self.indensity.setValue(1001)
        self.indensity.valueChanged.connect(self.updateResult)
        
        outdensitylabel = QtGui.QLabel('Outside density', self)
        self.outdensity = QtGui.QDoubleSpinBox(self)
        self.outdensity.setSuffix(' mg/ml')
        self.outdensity.setRange(0,10000)
        self.outdensity.setValue(1000)
        self.outdensity.valueChanged.connect(self.updateResult)
        
        outviscositylabel = QtGui.QLabel('Outside viscosity', self)
        self.outviscosity = QtGui.QDoubleSpinBox(self)
        self.outviscosity.setSuffix(' cP')
        self.outviscosity.setRange(0,1000)
        self.outviscosity.setValue(1)
        self.outviscosity.valueChanged.connect(self.updateResult)
        
        minrotradlabel = QtGui.QLabel('Min rotation radius', self)
        self.minrotationradius = QtGui.QDoubleSpinBox(self)
        self.minrotationradius.setRange(0,100)
        self.minrotationradius.setValue(3)
        self.minrotationradius.valueChanged.connect(self.updateResult)
        
        maxrotradlabel = QtGui.QLabel('Max rotation radius', self)
        self.maxrotationradius = QtGui.QDoubleSpinBox(self)
        self.maxrotationradius.setRange(0,100)
        self.maxrotationradius.setValue(6.2)
        self.maxrotationradius.valueChanged.connect(self.updateResult)

        self.result = QtGui.QLabel()
        self.updateResult()
        
        grid = QtGui.QGridLayout()
        grid.addWidget(diameterlabel, 0, 0)
        grid.addWidget(self.diameter, 0, 1)
        grid.addWidget(timelabel, 1, 0)
        grid.addWidget(self.time, 1, 1)
        grid.addWidget(indensitylabel, 2, 0)
        grid.addWidget(self.indensity,2, 1)
        grid.addWidget(outdensitylabel, 3, 0)
        grid.addWidget(self.outdensity, 3, 1)
        grid.addWidget(outviscositylabel, 4, 0)
        grid.addWidget(self.outviscosity, 4, 1)
        grid.addWidget(minrotradlabel, 5, 0)
        grid.addWidget(self.minrotationradius, 5, 1)
        grid.addWidget(maxrotradlabel, 6, 0)
        grid.addWidget(self.maxrotationradius, 6, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(hint)
        vbox.addSpacing(10)        
        vbox.addLayout(grid)
        vbox.addSpacing(10)
        vbox.addWidget(self.result)
        
        self.setLayout(vbox)  
        self.setWindowTitle("Centrifuge")
        self.show()
                
    def updateResult(self):
        self.result.setText('&omega; = <b>%i rpm</b>'%self.calculate())
    
    def calculate(self):
        diameter = self.diameter.value()  #in um
        time = self.time.value()  # in s
        density_in = self.indensity.value()  # in mg/ml
        density_out = self.outdensity.value()  # in mg/ml
        visc_out = self.outviscosity.value()  # in cP = mPa s
        r1 = self.minrotationradius.value()  # in whatever
        r2 = self.maxrotationradius.value()  # in whatever
        
        # in (rad/sec)**2, 1e9 due to diameter in um and visosity in cP
        angvelsqr = 18e9*visc_out*math.log(r2/r1) / (math.sqrt(2) *
                    diameter**2 * time * (density_in - density_out))
        #in rpm
        angvel = math.sqrt(angvelsqr)*30/math.pi
        return angvel
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = Centrifuge()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#    fr = Centrifuge()
#    print fr.calculate()
