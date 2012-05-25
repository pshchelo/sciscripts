"""R = C*M

d
	dextran

s
	sucrose

g
	glucose

"""
from __future__ import division

# water density in mg/ml
Rw = 1000

# molecular weights in g/mol = mg/mmol
Ms = 342.3
Mg = 180.16
Md = 500000

# mass concentration of dextran, mg/mg
Pd = 0.1

Rd = Rw * Pd / (1 - Pd) # ignoring volume expansion

Cd = Rd / Md
Rg = Rd * (Md - Ms) / (Ms - Mg) * Mg / Md

Cg = Rg/Mg

Rs = Rd + Rg

Cs = Rs/Ms

print 10*'='

print "Dextran: %i Da at %.3f mg/ml = %.6f mM"%(Md, Rd, 1000*Cd)

print "Glucose: %.3f mg/ml = %.3f mM"%(Rg, 1000*Cg)

print "Sucrose: %.3f mg/ml = %.3f mM"%(Rs, 1000*Cs)

print 10*'='
