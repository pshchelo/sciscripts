#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Calculate centrifuge parameters."""
from __future__ import division
import math
import sys
from PySide import QtGui

class CentrifugePanel(QtGui.QWidget):
    def __init__(self, parent):
        super(CentrifugePanel, self).__init__(parent=parent)
        self.initPanel()
        
    def initPanel(self):
        anglelabel = QtGui.QLabel('Inclination angle')
        self.inclangle = QtGui.QDoubleSpinBox(self)
        self.inclangle.setSuffix(u' °')
        self.inclangle.setRange(0, 90)
        self.inclangle.setValue(45)
        self.inclangle.valueChanged.connect(self.updateResult)
        
        diameterlabel = QtGui.QLabel('Vescile Diameter', self)
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
        
        minrotradlabel = QtGui.QLabel('Min rotation radius, mm', self)
        self.minrotationradius = QtGui.QDoubleSpinBox(self)
        self.minrotationradius.setRange(0,1000)
        self.minrotationradius.setValue(30)
        self.minrotationradius.valueChanged.connect(self.updateResult)
        
        maxrotradlabel = QtGui.QLabel('Max rotation radius, mm', self)
        self.maxrotationradius = QtGui.QDoubleSpinBox(self)
        self.maxrotationradius.setRange(0,1000)
        self.maxrotationradius.setValue(62)
        self.maxrotationradius.valueChanged.connect(self.updateResult)

        self.result = QtGui.QLabel()
        self.updateResult()
        
        grid = QtGui.QGridLayout()
        
        items = [(anglelabel, self.inclangle),
                (diameterlabel, self.diameter),
                (timelabel, self.time),
                (indensitylabel, self.indensity),
                (outdensitylabel, self.outdensity),
                (outviscositylabel, self.outviscosity),
                (minrotradlabel, self.minrotationradius),
                (maxrotradlabel, self.maxrotationradius),
                ]
                
        for index, item in enumerate(items):
            label, widget = item
            grid.addWidget(label, index, 0)
            grid.addWidget(widget, index, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addSpacing(10)
        vbox.addWidget(self.result)
        
        self.setLayout(vbox)
                
    def updateResult(self):
        self.result.setText('&omega; = <b>%i rpm</b>'%self.centrifuge())
    
    def centrifuge(self):
        """Calculates separation parameters for centrifugation."""
        diameter = self.diameter.value()  #in um
        time = self.time.value()  # in s
        density_in = self.indensity.value()  # in mg/ml
        density_out = self.outdensity.value()  # in mg/ml
        visc_out = self.outviscosity.value()  # in cP = mPa s
        r1 = self.minrotationradius.value()  # in whatever
        r2 = self.maxrotationradius.value()  # in whatever
        inclination = math.pi*self.inclangle.value() / 180 # now in radians
        # in (rad/sec)**2, 1e9 due to diameter in um and visosity in cP
        angvelsqr = 18e9*visc_out*math.log(r2/r1) / (math.cos(inclination) *
                diameter**2 * time * (density_in - density_out))
        #in rpm
        angvel = math.sqrt(angvelsqr)*30/math.pi
        return angvel
        
class GravityPanel(QtGui.QWidget):
    def __init__(self, parent):
        super(GravityPanel, self).__init__(parent=parent)
        self.initPanel()
        
    def initPanel(self):
        diameterlabel = QtGui.QLabel('Vescile Diameter', self)
        self.diameter = QtGui.QDoubleSpinBox(self)
        self.diameter.setSuffix(u' µm')
        self.diameter.setRange(1, 500)
        self.diameter.setValue(20)
        self.diameter.valueChanged.connect(self.updateResult)

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
        
        falllabel = QtGui.QLabel('Fall distance, mm', self)
        self.falldistance = QtGui.QDoubleSpinBox(self)
        self.falldistance.setRange(0,1000)
        self.falldistance.setValue(30)
        self.falldistance.valueChanged.connect(self.updateResult)

        self.result = QtGui.QLabel()
        self.updateResult()
        
        grid = QtGui.QGridLayout()
        
        items = [(diameterlabel, self.diameter),
                (indensitylabel, self.indensity),
                (outdensitylabel, self.outdensity),
                (outviscositylabel, self.outviscosity),
                (falllabel, self.falldistance),
                ]
                
        for index, item in enumerate(items):
            label, widget = item
            grid.addWidget(label, index, 0)
            grid.addWidget(widget, index, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addSpacing(10)
        vbox.addWidget(self.result)
        
        self.setLayout(vbox)
    
    def updateResult(self):
        seconds = self.gravity()
        hours = seconds // 3600
        self.result.setText(
            't = <b>%i s</b> &asymp; <b>%i h</b>'%(seconds, hours))
    
    def gravity(self):
        """Calculates time for separation in gravity field."""
        diameter = self.diameter.value() # in um
        density_in = self.indensity.value()  # in mg/ml
        density_out = self.outdensity.value()  # in mg/ml
        visc_out = self.outviscosity.value()  # in cP = mPa s
        length = self.falldistance.value()  # in mm
        g = 9.81  # m/s**2
        
        # in seconds, 1e6 due to units of length, diameter and viscosity
        time = 18e6*visc_out*length / (
                            g*diameter*diameter*(density_in-density_out))
        return time

class Separation(QtGui.QWidget):
    def __init__(self):
        super(Separation, self).__init__()
        notebook = QtGui.QTabWidget(self)
        centrifuge = CentrifugePanel(self)
        gravity = GravityPanel(self)
        notebook.addTab(centrifuge, 'Centrifuge')
        notebook.addTab(gravity, 'Gravity')
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(notebook)
        self.setLayout(vbox)
        self.setWindowTitle("Vesicle separation")
        self.show()
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = Separation()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#    fr = Centrifuge()
#    print fr.calculate()
