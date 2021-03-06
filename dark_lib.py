# -*- coding: utf-8 -*-

"""
Spyder Editor
#!/Users/dan/anaconda/bin/python
This is a temporary script file.
"""
import subprocess
import os.path
import fractions
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
 
class darkfile(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadict = {}
        execstr = 'exiftool -d ' + r'"%Y%m%d_%H%M%S"' + ' -AllDates -Model -ISO -ExposureTime \
            -LongExposureNoiseReduction -LongExposureNoiseReduction2 \
            -CameraTemperature %s' % filename
        p = subprocess.Popen(execstr, stdout=subprocess.PIPE, shell=True)
        self.metadata = p.stdout.read().decode('utf-8').rstrip()
        for met_item in self.metadata.split('\n'):
            met_key, met_value = map(lambda mystr: mystr.strip(), 
                                        met_item.split(':'))
            self.metadict[met_key] =  met_value
    
# Rebel XT: no temperature reported. Rebel M: reported
        if "Camera Temperature" in self.metadict.keys():
            self.temp = int(self.metadict["Camera Temperature"].rstrip(' C'))
        else:
            self.temp = False
        self.ISO = int(self.metadict["ISO"])
# convert exposure times reported as e.g. '1/10':
        self.exptime = float(fractions.Fraction(self.metadict["Exposure Time"]))

        self.date = self.metadict["Modify Date"]
    
    def update_name(self, new_filename):
        self.filename = new_filename

def raw_to_tiff(tiff_dir, mydark):   #output directory & dark object
    
    if not os.path.exists(mydark.filename):
        print("%s not found" % mydark.filename)
        return
    
    newbase = mydark.date + '_' + 'ISO'+ str(mydark.ISO) + '_' + str(mydark.exptime) + 's.tiff'
    newname = tiff_dir.rstrip('/') + '/' + newbase

    if os.path.exists(newname):
        print("%s already exists; skipping" % newname)        
        mydark.update_name(newname)
        return
    else:
        execstr = 'dcraw -4 -T -D -c -t 0 %s > %s' % (mydark.filename, newname)
        execstr2 = 'exiftool -TagsFromFile        %s %s' % (mydark.filename, newname)
        print(execstr)
        p1 = subprocess.call(execstr, stdout=subprocess.PIPE, shell=True)
        p2 = subprocess.call(execstr2, stdout=subprocess.PIPE, shell=True)
#        print(newname)
        mydark.update_name(newname)

def build_data(the_list):
    #build array of data:
    return np.concatenate([get_data(aux.filename)[..., np.newaxis] \
                        for aux in the_list], axis=2)
	
def get_data(filename):
	return np.array(misc.imread(filename),dtype=np.int16)

def get_fulldata_raw(filename):
	#return full array, including non-image pixels (optical black etc.)
	execstr = 'dcraw -4 -T -E -c -t 0 %s > %s' % (filename, 'tmp.tiff')
	p1 = subprocess.call(execstr, stdout=subprocess.PIPE, shell=True)
	return get_data('tmp.tiff')
	p2 = subprocess.call('rm tmp.tiff',stdout=subprocess.PIPE, shell=True)

def add_darks(thedir, the_list):
    findstr = "find %s -path '*dark*CR2'" % (thedir) \
      + "; find %s -path '*dk*CR2'" % (thedir) \
      + "; find %s -path '*dark*tiff' | grep -vi 'flat'" % (thedir)
    p = subprocess.Popen(findstr, stdout=subprocess.PIPE, shell=True)
    
    filelist = p.stdout.read().decode('utf-8').rstrip()
    filearr = filelist.split('\n')
    
#    print filearr
    for file in filearr: 
        print(file)
        try:
            darklist.append(darkfile(file))
        except ValueError:
            print("exif error; skipped file %s" %file)
            pass

#if __name__ == "__main__":
#   raw_dir = '/Users/dan/phot'
#   raw_dir = '/Volumes/Omega/astro'
#   raw_dir = '/Volumes/Delta/phot_orig'
#raw_dir = '/Users/dan/code/darklib/tiff_tmp'
raw_dir = '/Users/dan/Desktop/dark/dark_warm'
tiff_dir='/Users/dan/code/darklib/warm_tiff'
#tiff_dir = '/Users/dan/code/darklib/tiff_tmp'

darklist = []
add_darks(raw_dir, darklist)
sub_EOSM = list(filter(lambda x: x.temp is not False, darklist))
for dark in sub_EOSM:
	raw_to_tiff(tiff_dir, dark)
#    sub_list = filter(lambda x: x.ISO == 800 and int(x.exptime) == 120, darklist)
#    a = build_data(sub_list)
