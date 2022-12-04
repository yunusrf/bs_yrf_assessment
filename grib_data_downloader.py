'''
Description: Download the grib files (wind,pressure,temperature) from the nomads NOAA site.

'''
from __future__ import print_function
from datetime import datetime
import os
import subprocess
import errno
import requests

import threading

filters = ['filter_gfs_1p00.pl?file=', 'filter_gfs_0p25.pl?file=','filter_gfs_0p50.pl?file=']
pgrb2s = ['z.pgrb2.1p00.f', 'z.pgrb2.0p25.f', 'z.pgrb2.1p50.f']
# SERVER = "https://nomads.ncep.noaa.gov/cgi-bin/"
SERVER = "http://nomads.ncep.noaa.gov/cgi-bin/"
# http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=gfs.t12z.pgrbf12.grib2&lev_500_mb=on&var_TMP=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&showurl=&dir=%2Fgfs.2009020612" -o my_file
# http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs.pl?file=gfs.t12z.pgrbf12.grib2&lev_500_mb=on&var_TMP=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&showurl=&dir=%2Fgfs.2009020612
  
# every six hours the model generates new files.
timelist = ['00', '06', '12', '12'] 
DOWNLOADS_PATH = ""
VARIABLES = ""
LEVEL = ""


class GribDataDownloader:

    def __init__(self, download_path):
        self.download_path = download_path

    def createPgrb2(self, detail):
        if detail == 'p1':
            print(f'pgrb2s[0] = {pgrb2s[0]}')
            return pgrb2s[0]
        elif detail == 'p25':
            print(f'pgrb2s[1] = {pgrb2s[1]}')
            return pgrb2s[1]
        elif detail == 'p50':
            print(f'pgrb2s[2] = {pgrb2s[2]}')
            return pgrb2s[2]    


    def createServerByDetail(self, detail):
        if detail == 'p1':
            return SERVER + filters[0]
        elif detail == 'p25':
            return SERVER + filters[1]
        elif detail == 'p50':
            return SERVER + filters[2]    
            



    def createServerByTime(self, time, detail):
        if time == 0:
            result = self.createServerByDetail(detail) + 'gfs.t' + timelist[0] + self.createPgrb2(detail)
            return result
        elif time == 1:
            result = self.createServerByDetail(detail) + 'gfs.t' + timelist[1] + self.createPgrb2(detail)
            return result
        elif time == 2:
            result = self.createServerByDetail(detail) + 'gfs.t' + timelist[2] + self.createPgrb2(detail)
            return result
        elif time == 3:
            result =self.createServerByDetail(detail) + 'gfs.t' + timelist[3] + self.createPgrb2(detail)
            return result


    def fileExistInServer(self, url, hour, run):
        url_final = url + '{:03d}'.format(hour)
        result = self.create_url(url_final) + '/' + timelist[run] + '/atmos'
        print(result, end="\n")
        r = requests.get(result, stream=True)
        return r.status_code, result


    def fileIsDownloaded(self, run):
        dateString = self.createDateFolder()
        datefolder = DOWNLOADS_PATH + dateString + '/' + str(run) + '/'
        if os.path.exists(os.path.dirname(datefolder)):
            path, dirs, files = next(os.walk(os.path.dirname(datefolder)))
            if len(files) == 9:
                print('Total Files on run ' + str(run) + ' = ' + str(len(files)))
                return True
            else:
                print('Total Files on run ' + str(run) + ' = ' + str(len(files)))
                return False
        else:
            return False

    def check_and_download(self, hour, time, detail):
        print(f'hour >={hour} and hour < {hour + 6}', end="\n")
        if self.fileIsDownloaded(hour):
            print('files already downloaded', end="\n")
            return
        SERVER_URL = self.createServerByTime(time, detail)
        counter = 0
        for i in range(0, 25, 3):
            exist = self.fileExistInServer(SERVER_URL, i, time)
            print(exist[0], end="\n")
            if exist[0] == 404:
                break
            if exist[0] == 200:
                counter += 1
        if counter == 9:
            for i in range(0, 25, 3):
                self.download_file(exist[1], hour, i)    

    def download_gfs(self, detail, variables, level, output):
        now = datetime.utcnow()
        global DOWNLOADS_PATH
        DOWNLOADS_PATH = output
        
        global VARIABLES
        VARIABLES = variables

        global LEVEL
        LEVEL = level

        if 0 <= now.hour < 6:
            self.check_and_download(0,0, detail)
        elif 6 <= now.hour < 12:
            self.check_and_download(6,1, detail)
        elif 12 <= now.hour < 18:
            self.check_and_download(12,2,detail)
        elif 18 <= now.hour < 24:
            self.check_and_download(18,3,detail)


    def download_file(self, url, run, hour):
        dateString = self.createDateFolder()
        datefolder = DOWNLOADS_PATH + dateString + '/' + str(run) + '/'
        filename = 'gfs.f' + '{:03d}'.format(hour) + '.grb2'
        local_filename = datefolder + filename
        print(local_filename)
        r = requests.get(url, stream=True)
        if not os.path.exists(os.path.dirname(datefolder)):
            try:
                os.makedirs(os.path.dirname(datefolder))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        wrongTime = 'gfs.t' + '{:02d}'.format(run) + 'z.pgrb2.0p25.f024'
        filetoreplace = 'gfs.t' + '{:02d}'.format(run) + 'z.pgrb2.0p25.f' + '{:03d}'.format(hour)
        url = url.replace(wrongTime, filetoreplace)
        print(url)
        wgetcmd = "curl -o " + local_filename + " -L '" + url + "'"
        subprocess.call(wgetcmd, shell=True)
        return local_filename


    def createDateFolder(self):
        u = datetime.utcnow()
        dateString = str(u.year) + '{:02d}'.format(u.month) + '{:02d}'.format(u.day)
        return dateString

    def create_url(self, SERVER_URL):
        url = SERVER_URL + '&' + LEVEL + '=on'
        variables = VARIABLES.split(',')
        for item in variables:
            url = url + '&var_' + item + '=on'
        # Set the area of interest (AOI) here
        # To Test area of interest - 161°E to 180°E and 51°S to 31°S.
        url = url + '&leftlon=0&rightlon=360&toplat=90&bottomlat=-90'
        dateString = self.createDateFolder()
        url = url + '&dir=%2Fgfs.' + dateString
        return url
