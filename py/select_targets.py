import sys
import glob
import numpy
import fitsio
import esutil
from pydl.pydlutils import yanny
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
    # Match against already drilled targets
    data= esutil.numpy_util.add_fields(data,[('FLAG_DONT_OBSERVE', int)])
    data['FLAG_DONT_OBSERVE']= 0
    yannyfiles= glob.glob('../target_info/plateHolesSorted-*.par')
    for yannyfile in yannyfiles:
        drillFile= yanny.yanny(filename=yannyfile,np=True)
        drilled= drillFile['STRUCT1']
        # spherematch
        h=esutil.htm.HTM()
        m1,m2,d12 = h.match(data['RA'],data['DEC'],
                            drilled['target_ra'],drilled['target_dec'],
                             2./3600.,maxmatch=1)
        data['FLAG_DONT_OBSERVE'][m1]= 1
    # Write to file
    fitsio.write(outfile,data[numpy.random.permutation(len(data))],
                 clobber=True)
    return None

if __name__ == '__main__':
    select_targets(sys.argv[1],int(sys.argv[2]))
