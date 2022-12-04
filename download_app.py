'''
Description: Module to download pressure, wind and temperature.
Output folder structure
/grib/(wind,pressure,tmpr)
  - 20220202 (date)
    - 12 (run 0,6,12,18)
      - gfs.f000.grb2
      - gfs.f003.grb2
      - gfs.f006.grb2
      - gfs.f012.grb2
      - gfs.f015.grb2
      - gfs.f018.grb2
      - gfs.f021.grb2
      - gfs.f024.grb2
'''
import sys
import argparse
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import threading
from grib_data_downloader import GribDataDownloader


def download_pressure(levelOfDetail, obj_DataDownloader):
  obj_DataDownloader.download_gfs(levelOfDetail, "PRES", "lev_80_m_above_ground", "/Users/yunusparvej/Downloads/grib/pressure/")
  threading.Timer(20.0, updateGribFiles, [levelOfDetail]).start()

def download_wind(levelOfDetail, obj_DataDownloader):
  obj_DataDownloader.download_gfs(levelOfDetail, "UGRD,VGRD", "lev_10_m_above_ground", "/Users/yunusparvej/Downloads/grib/wind/")
  threading.Timer(20.0, updateGribFiles, [levelOfDetail]).start()

def download_temperature(levelOfDetail, obj_DataDownloader):
  obj_DataDownloader.download_gfs(levelOfDetail, "TMP", "lev_surface", "/Users/yunusparvej/Downloads/grib/tmpr/")
  threading.Timer(20.0, updateGribFiles, [levelOfDetail]).start()



def updateGribFiles(levelOfDetail):
  down_load_path = "/Users/yunusparvej/Downloads/grib"
  obj_DataDownloader = GribDataDownloader(down_load_path)
  print("Checking For Updates")
  download_pressure(levelOfDetail,obj_DataDownloader)
  download_wind(levelOfDetail,obj_DataDownloader)
  download_temperature(levelOfDetail,obj_DataDownloader)

if __name__ == '__main__':

     # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--level", default="p25", type=str, help="level of detail p25 --> 0.25 Degree, p50 --> 0.50 Degree, p1 --> 1 Degree")
    args = parser.parse_args() 
    input_level = "p25"
    for arg in sys.argv:
        print (arg)  
    if len(sys.argv) == 1:
        print(f'No arguments passed - running the script with default level of detail p25')  
        input_level = "p25"  
    else:
        input_level =str(args.level).strip()    
        if  input_level=="p25" or input_level=="p50" or input_level=="p1":
            print(f'Running script with level of detail - {input_level}') 
        else:
            sys.exit(
            "Invalid level of detail provided"
            )

    # print(f'args.l - {args.l}')    

    print ("Download / Update Started...")
    # level of detail p25 --> 0.25 Degree, p1 --> 1 Degree
    # updateGribFiles('p25')
    updateGribFiles(input_level)
   
    
   