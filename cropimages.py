import glob
import Image
import sys
import os

CONFIGFILE = 'vampy.cfg'

def read_conf_file(filename):
    imgcfg = {}
    try:
        conffile = open(filename, 'r')
    except IOError:
        return imgcfg
    lines = conffile.readlines()
    conffile.close()
    for line in lines:
        key, value = line.split(None,1)
        imgcfg[key] = value.rstrip('\n')
    return imgcfg
    
def rewrite_conf_file(params, filename):
    for side in ('left', 'right', 'top', 'bottom'):
        params[side] = '0'
    file = open(filename, 'w')
    for key, value in params.items():
        if isinstance(value, str):
            line = '%s\t%s\n'%(key, value)
        elif isinstance(value, (list, tuple)):
            line = str(key)+len(value)*'\t%s'%value+'\n'
        file.write(line)
    file.close()
    
def cropnsave(dirname):
    savedir = dirname+'-croped'
    os.mkdir(savedir)
    configfile = os.path.join(dirname, CONFIGFILE)
    imgparams = read_conf_file(configfile)
    filelist = glob.glob(os.path.join(dirname, '*.png'))
    for i, file in enumerate(filelist):
        img = Image.open(file)
        w, h = img.size
        box = (int(imgparams['left']), int(imgparams['top']), 
                w-int(imgparams['right']), h-int(imgparams['bottom']))
        imgc = img.crop(box)
        dir, name = os.path.split(file)
        savename = os.path.join(savedir, name)
        imgc.save(savename)
        print 'Saved image %i of %i'%(i+1, len(filelist))
    saveconfig = os.path.join(savedir, CONFIGFILE)
    rewrite_conf_file(imgparams, saveconfig)
    
if __name__=='__main__':
    dirname = sys.argv[1]
    cropnsave(dirname)