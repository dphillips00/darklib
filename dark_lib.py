# -*- coding: utf-8 -*-

"""
Spyder Editor
#!/Users/dan/anaconda/bin/python
This is a temporary script file.
"""
dir = '/Volumes/Omega/astro'
import subprocess
import exiftool
findstr = "find %s -path '*dark*CR2' | grep -vi 'flat'" % (dir)
p = subprocess.Popen(findstr, stdout=subprocess.PIPE, shell=True)

filelist = p.stdout.read().decode('utf-8').rstrip()
filearr = filelist.split('\n')
class darkfile(object):
    def __init__(self, filename):
        self.filename = filename
        with exiftool.ExifTool() as et:
            self.metadata = et.get_tags(['Model', 'ISO', 'ExposureTime',\
            'LongExposureNoiseReduction','LongExposureNoiseReduction2',\
            'CameraTemperature'], filename)
        def temp(self):
            return int(self.metadata)
darklist = []
for file in filearr:
    print file
    try:
        darklist.append(darkfile(file))
    except ValueError:
        print "exif error: skipped file %s" %file        
        pass