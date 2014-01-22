# -*- coding: utf-8 -*-
"""
Puts month abbreviation inside curly braces in BibTeX file.

This is apparently needed by bibtexFile.dot macros (http://www.rennes.supelec.fr/ren/perso/etotel/bibtexWord/index.html)

Usage:
    curlybracesmonth bibfile.bib
Output:
    creates bibfile_new.bib next to bibfile.bib
"""
import sys
import os.path

if len(sys.argv) == 1:
    print __doc__
    sys.exit()

with open(sys.argv[1]) as fin:
    data = fin.readlines()

out = []
for line in data:
    if 'month = ' in line.lower() and '{' not in line:
        start, end = line.split(' = ')
        month = end.strip()[:-1]
        if len(month) < 3:
            out.append(line)
        else:
            out.append('%s = {%s},\n'%(start, month))
    else:
        out.append(line)

oldname, oldext = os.path.splitext(sys.argv[1])
newname = oldname+'_new'
with open(newname+oldext, 'w') as fout:
    fout.writelines(out)

