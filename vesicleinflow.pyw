from __future__ import division
#from visual.controls import *
import visual as vis
import visual.controls as vc

fps = 60
deltaphi = -vis.pi / (2*fps)
Lves = 3
Wves = 2

def prepare_scene():
    vis.arrow(pos=(-3.1,-3.1,0.1), axis=(1,0,0), color=vis.color.red)
    vis.arrow(pos=(-3.1,-3.1,0.1), axis=(0,1,0), color=vis.color.green)
    vis.arrow(pos=(-3.1,-3.1,0.1), axis=(0,0,1), color=vis.color.blue)
    ## vis.points(pos=[(0,0,0),], color=vc.color.yellow, size=10)

    for i in range(5):
        vis.arrow(pos=(-3,i-2,0), axis=(i+1,0,0), shaftwidth=0.1, fixedwidth = True)

def change_material():
    if mat.value:
        vesicle.material = vis.materials.wood
    else:
        vesicle.material = vis.materials.emissive

def set_mode():
    vesicle.mode = modemnu.value
    title.text = vesicle.mode
    modes[vesicle.mode][0]()

def init_tanktread():
    vesicle.axis = (1,1,0)
    vesicle.length = Lves
    vesicle.width = Wves
    vesicle.hight = Wves
    vesicle.up = (0,1,0)

def tanktread():
    vesicle.up = vis.rotate(vesicle.up, deltaphi, axis=(0,0,1))

def init_thumble():
    vesicle.axis = (1,0,0)
    vesicle.length = Lves
    vesicle.width = Wves
    vesicle.hight = Wves
    vesicle.up = (0,1,0)

def thumble():
    vesicle.rotate(angle=deltaphi, axis=(0,0,1))

def init_tremble():
    vesicle.t = 0
    vesicle.axis = (1,0,0)
    vesicle.length = Lves
    vesicle.width = Wves
    vesicle.hight = Wves
    vesicle.up = (0,1,0)
    vesicle.volume = 4*vis.pi*Lves*Wves*Wves/3
    vesicle.Requal = (Lves*Wves*Wves)**(1/3)


def tremble():
    x = -vis.sin(vesicle.t)
    y = -0.5*vis.sin(2*vesicle.t)
    vesicle.axis = vis.vector(vesicle.Requal+x*(Lves-vesicle.Requal),y,0)
    # keep the volume constant
    w = vis.sqrt(0.75*vesicle.volume/vesicle.length/vis.pi)
    vesicle.width = w
    vesicle.height = w
    vesicle.t += deltaphi
    if vis.fabs(vesicle.t) > vis.pi:
        vesicle.t = 0

def init_kayak():
    vesicle.axis = (4,1,0)
    vesicle.length = Lves
    vesicle.width = Wves
    vesicle.hight = Wves
    vesicle.up = (0,1,0)

def kayak():
    vesicle.rotate(angle=deltaphi, axis=(1,0,0))

modes = {
        'Tank-treading': (init_tanktread, tanktread),
        'Thumbling': (init_thumble, thumble),
        'Trembling': (init_tremble, tremble),
        'Kayaking': (init_kayak, kayak),
         }

disp = vis.display(title='Vesicle in shear flow',
                   pos=(0,0), width=400, height=400, range=4)
prepare_scene()
vesicle = vis.ellipsoid(pos=(0,0,0),
    length=Lves, height=Wves, width=Wves,
    color=vis.color.green, opacity=0.8,
    material=vis.materials.emissive,
    )
vesicle.mode=modes.keys()[0]
modes[vesicle.mode][0]()
vesicle.t=0
vesicle.volume = 4*vis.pi*Lves*Wves*Wves/3
vesicle.Requal = (Lves*Wves*Wves)**(1/3)
title = vis.text(pos=(0,2.5,0), width=3, height=0.5, align='center',
             color=vis.color.yellow,
             text=modes.keys()[0])

c = vc.controls(title='Controls', width=250, height=220,
                 x=400, y=0, range=4)
mat = vc.toggle(pos=(-2.5,1.5), width=1, height=1,
             text0='Fluo', text1='Textured',
             action=lambda: change_material(),
             )
modemnu = vc.menu(pos=(1,1.5), width=4, height=1, text='Motion mode')
for m in modes.keys():
    modemnu.items.append((m, lambda: set_mode()))

while True:
    vis.rate(fps)
    modes[vesicle.mode][1]()
