import sys
import numpy
import fitsio
from galpy.util import bovy_coords
import mwdust
def select_targets(outfile,location):
    numpy.random.seed(location)
    datafilename= '../target_info/SecQuanObj_%03i+00.fits' % location
    data= fitsio.read(datafilename)
    # De-redden
    ak= data['AK']
    aj= ak*2.5
    j0= data['J_M']-aj
    k0= data['K_M']-ak
    # Cut on jk0,h
    indx= ((j0-k0) > 0.8)*(data['H_M'] > 12.)*(data['H_M'] < 13.)
    data= data[indx]
    # setup dust map
    dmap= mwdust.Marshall06(filter='2MASS H')
    # Calculate A_H(7 kpc) according to Marshall et al. (2006)
    ahdmap= numpy.zeros(len(data))
    lb= bovy_coords.radec_to_lb(data['RA'],data['DEC'],degree=True)
    for ii in range(len(data)):
        ahdmap[ii]= dmap(lb[ii,0],lb[ii,1],7.)
    # Cut on AH <= 1.4
    indx= ahdmap <= 1.4
    data= data[indx]
    # Write to file
    fitsio.write(outfile,data[numpy.random.permutation(len(data))])
    return None

if __name__ == '__main__':
    select_targets(sys.argv[1],int(sys.argv[2]))
