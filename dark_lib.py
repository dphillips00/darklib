# -*- coding: utf-8 -*-

"""
Spyder Editor
#!/Users/dan/anaconda/bin/python
This is a temporary script file.
"""
dir = '/Volumes/Omega/astro'
import subprocess
import fractions

class darkfile(object):
    def __init__(self, filename):
        self.filename = filename
        self.metadict = {}
        execstr = 'exiftool -Model -ISO -ExposureTime \
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
            
if __name__ == "__main__":
    findstr = "find %s -path '*dark*CR2' | grep -vi 'flat'" % (dir)
    p = subprocess.Popen(findstr, stdout=subprocess.PIPE, shell=True)
    
    filelist = p.stdout.read().decode('utf-8').rstrip()
    filearr = filelist.split('\n')
    
    darklist = []
    for file in filearr: 
        print file 
        try:
            darklist.append(darkfile(file))
        except ValueError:
            print "exif error: skipped file %s" %file        
            pass
    
        