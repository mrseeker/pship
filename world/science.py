from world import set as setter
from world import alerts, errors,unparse,constants, utils
from pygnuplot import gnuplot

def test_plot(self):
    g = gnuplot.Gnuplot()
    g.cmd("set terminal dumb size 120, 30")
    print (g.plot("[-10:10] sin(x),atan(x),cos(atan(x))"))