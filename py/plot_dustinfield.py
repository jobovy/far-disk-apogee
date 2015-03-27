import sys
import os, os.path
import pickle
import numpy
import matplotlib
matplotlib.use('Agg')
from galpy.util import save_pickles, bovy_plot
from matplotlib import cm
import mwdust
_NL= 201
_NB= 201
_SAVEFILE_MARSHALL= 'dustinfield_FIELD_marshall.sav'
_SAVEFILE_GREEN= 'dustinfield_FIELD_green.sav'
def plot_dustinfield(plotname,field,green=False):
    if green: savefile= _SAVEFILE_GREEN
    else: savefile= _SAVEFILE_MARSHALL
    savefile= savefile.replace('FIELD','%i' % field)
    # Grid
    ls= numpy.linspace(-1.75,1.75,_NL)+field
    bs= numpy.linspace(-1.75,1.75,_NB)
    if not os.path.exists(savefile):
        # Setup dust map
        if green:
            dmap= mwdust.Green15(filter='2MASS H')
        else:
            dmap= mwdust.Marshall06(filter='2MASS H')
        plotthis= numpy.empty((_NL,_NB))
        for jj in range(_NB):
            print jj
            for ii in range(_NL):
                plotthis[ii,jj]= dmap(ls[ii],bs[jj],7.)
        save_pickles(savefile,plotthis)
    else:
        with open(savefile,'rb') as f:
            plotthis= pickle.load(f)
    # Remove outside the field
    tls= numpy.tile(ls,(_NB,1)).T
    tbs= numpy.tile(bs,(_NL,1))
    plotthis[(tls-field)**2.+tbs**2. > 1.5**2.]= numpy.nan
    # Now plot
    bovy_plot.bovy_print()
    bovy_plot.bovy_dens2d(plotthis[::-1].T,origin='lower',cmap=cm.coolwarm,
                          interpolation='nearest',
#                          colorbar=True,shrink=0.45,
                          vmin=0.,vmax=2.-0.75*green,aspect=1.,
                          xrange=[ls[-1]+(ls[1]-ls[0])/2.,
                                  ls[0]-(ls[1]-ls[0])/2.],
                          yrange=[bs[0]-(bs[1]-bs[0])/2.,
                                  bs[-1]+(bs[1]-bs[0])/2.],
                          xlabel=r'$l\,\mathrm{(deg)}$',
                          ylabel=r'$b\,\mathrm{(deg)}$',
                          zlabel=r'$A_H\,(\mathrm{mag})$',
                          zorder=0)
    bovy_plot.bovy_text(r'$(l,b) = (%i,0)$' % field,top_left=True,
                        color='k',size=16.)
    bovy_plot.bovy_end_print(plotname)
    return None

if __name__ == '__main__':
    plot_dustinfield(sys.argv[1],field=int(sys.argv[2]),green=len(sys.argv) > 3)
