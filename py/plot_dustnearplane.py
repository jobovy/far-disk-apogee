import sys
import os, os.path
import pickle
import numpy
import matplotlib
matplotlib.use('Agg')
from galpy.util import save_pickles, bovy_plot
from matplotlib import cm
import mwdust
_NL= 221
_NB= 21
_SAVEFILE_MARSHALL= 'dustnearplane_marshall.sav'
_SAVEFILE_GREEN= 'dustnearplane_green.sav'
def plot_dustnearplane(plotname,green=False):
    if green: savefile= _SAVEFILE_GREEN
    else: savefile= _SAVEFILE_MARSHALL
    # Grid
    ls= numpy.linspace(15.,70.,_NL)
    bs= numpy.linspace(-2.,2.,_NB)
    if not os.path.exists(savefile):
        # Setup dust map
        if green:
            dmap= mwdust.Green15(filter='2MASS H')
        else:
            dmap= mwdust.Marshall06(filter='2MASS H')
        plotthis= numpy.empty((_NL,_NB))
        rad= 0.5 # deg
        for jj in range(_NB):
            print jj
            for ii in range(_NL):
                pa, ah= dmap.dust_vals_disk(ls[ii],bs[jj],7.,rad)
                plotthis[ii,jj]= numpy.sum(pa*ah)/numpy.sum(pa)
        save_pickles(savefile,plotthis)
    else:
        with open(savefile,'rb') as f:
            plotthis= pickle.load(f)
    # Now plot
    bovy_plot.bovy_print(fig_width=8.4,fig_height=4.)
    bovy_plot.bovy_dens2d(plotthis[::-1].T,origin='lower',cmap=cm.coolwarm,
#                          interpolation='nearest',
                          colorbar=True,shrink=0.45,
                          vmin=0.,vmax=2.-0.75*green,aspect=3.,
                          xrange=[ls[-1]+(ls[1]-ls[0])/2.,
                                  ls[0]-(ls[1]-ls[0])/2.],
                          yrange=[bs[0]-(bs[1]-bs[0])/2.,
                                  bs[-1]+(bs[1]-bs[0])/2.],
                          xlabel=r'$l\,\mathrm{(deg)}$',
                          ylabel=r'$b\,\mathrm{(deg)}$',
                          zlabel=r'$A_H\,(\mathrm{mag})$',
                          zorder=0)
    bovy_plot.bovy_text(r'$D = 7\,\mathrm{kpc}$',top_left=True,
                        color='w',size=16.)
    # Overplot fields
    glons= [34.,64.,27.]
    glats= [0.,0.,0.]
    colors= ['w','w','y']
    xs= numpy.linspace(-1.5,1.5,201)
    ys= numpy.sqrt(1.5**2.-xs**2.)
    for glon,glat,c in zip(glons,glats,colors):
        bovy_plot.bovy_plot(xs+glon,ys+glat,'-',overplot=True,zorder=1,lw=2.,
                            color=c)
        bovy_plot.bovy_plot(xs+glon,-ys+glat,'-',overplot=True,zorder=1,lw=2.,
                            color=c)
    bovy_plot.bovy_end_print(plotname)
    return None

if __name__ == '__main__':
    plot_dustnearplane(sys.argv[1],green=len(sys.argv) > 2)
