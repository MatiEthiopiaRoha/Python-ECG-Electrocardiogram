from PyQt4 import uic 
fin = open('GUI.ui','r')
fout = open('GUI.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()