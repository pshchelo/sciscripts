from visual.controls import *

fps = 60
deltaphi = pi / (2*fps)
Lves = 3
Wves = 2


def prepare_scene():
    xaxis = arrow(pos=(-3.1,-3.1,0.1), axis=(1,0,0), color=color.red)
    yaxis = arrow(pos=(-3.1,-3.1,0.1), axis=(0,1,0), color=color.green)
    zaxis = arrow(pos=(-3.1,-3.1,0.1), axis=(0,0,1), color=color.blue)
    ## zero = points(pos=[(0,0,0),], color=color.yellow, size=10)

    for i in range(5):
        arrow(pos=(-3,i-2,0), axis=(i+1,0,0), shaftwidth=0.1, fixedwidth = True)

def change_material():
    if mat.value:
        vesicle.material = materials.wood
    else:
        vesicle.material = materials.emissive

def set_mode():
    vesicle.mode = modemnu.value
    title.text = vesicle.mode
    modes[vesicle.mode][0]()

def tanktread():
    vesicle.axis = (1,1,0)
    vesicle.length = Lves

def init_thumble():
    x,y,z = vesicle.axis
    vesicle.axis = vector(x,y,0)
    vesicle.length = Lves

def thumble():
    vesicle.rotate(angle=-deltaphi, axis=(0,0,1))

def init_tremble():
    vesicle.t = 0
    vesicle.axis = (2,0,0)
    vesicle.length = Lves-1
    
def tremble():
    vesicle.t += deltaphi
    if vesicle.t > pi:
        vesicle.t = 0
    x = sin(vesicle.t)
    y = sin(2*vesicle.t)
    vesicle.axis = vector(2+x,y,0)
    
def init_kayak():
    vesicle.axis = (4,1,0)
    vesicle.length = Lves
    
def kayak():
    vesicle.rotate(angle=deltaphi, axis=(1,0,0))
    
modes = {
        'Tank-treading': (tanktread, tanktread),
        'Thumbling': (init_thumble, thumble),
        'Trembling': (init_tremble, tremble),
        'Kayaking': (init_kayak, kayak),
         }
         
disp = display(title='Vesicle in shear flow', pos=(0,0), width=400, height=400, range=4)
prepare_scene()
vesicle = ellipsoid(pos=(0,0,0),
    length=Lves, height=Wves, width=Wves, 
    color=color.green, opacity=0.8,
    material=materials.emissive,
    )
vesicle.mode=modes.keys()[0]
vesicle.t=0
title = text(pos=(0,2.5,0), width=3, height=0.5, align='center', color=color.yellow, 
                    text=modes.keys()[0])

c = controls(title='Controls', width=250, height=220, 
                     x=400, y=0, range=4)
mat = toggle(pos=(-2.5,1.5), width=1, height=1,
             text0='Fluo', text1='Textured', 
             action=lambda: change_material(),
             )
modemnu = menu(pos=(1,1.5), width=4, height=1, text='Motion mode')
for m in modes.keys():    
    modemnu.items.append((m, lambda: set_mode()))

while True:
    rate(fps)
    modes[vesicle.mode][1]()
    