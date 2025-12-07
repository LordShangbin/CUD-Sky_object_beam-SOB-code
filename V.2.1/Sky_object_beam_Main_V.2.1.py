from skyfield import api as skyapi
from skyfield import named_stars
from skyfield.api import Star, load
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime,timezone
import juliandate
import time
import json
import SOB_V_2_1_radec_to_altaz as calFunc
import pandas as pd

ts = load.timescale()
t = ts.now()

la = 13.70305556
long = 100.5005

#-------------------- Load Sky object data --------------------#
# Load the JPL ephemeris DE421 (covers 1900-2050).
folder = "C:\\Users\\Shangbin\\OneDrive\\Documents\\Programming_Stuff\\Python\\Sky object beam"

with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
stardict = named_stars.named_star_dict

filepath = f'{folder}\\V.2.1\\Deep_sky_object_data.json'
deep_sky_objects = json.load(open(filepath))

#-------------------- Get (RA, DEC) --------------------#
# Stars #
inp = input("Star name : ").capitalize()
if inp in stardict:
    barnards_star = Star.from_dataframe(df.loc[stardict[inp]])
    astrometric = earth.at(t).observe(barnards_star)
    ra, dec, distance = astrometric.radec()
    ra = ra.degrees
    dec = dec.degrees
# Planets #
elif inp + ' barycenter' in planets:
    planet = planets[inp + ' barycenter']
    astrometric = earth.at(t).observe(planet)
    ra, dec, distance = astrometric.radec()
    ra = ra.degrees
    dec = dec.degrees
# Deep sky object #
elif inp.upper() in deep_sky_objects.keys():
    pos = deep_sky_objects[inp.upper()]
    ra = pos['RA']
    dec = pos['Dec']
    name = pos['Name'][0]
else:
    print("Object not found!")
    exit()

#-------------------- Convert (RA, DEC) to (Az, Alt) --------------------#
now = datetime.now(timezone.utc)
st = calFunc.getSiderealTime(now, method='julian')
lst = calFunc.getLocalST(st, long)
ha = calFunc.getHourAngle(lst, calFunc.deg_to_hms(ra))
az, al = calFunc.getAltazimuth(la, ra, dec, ha)

#-------------------- Print results --------------------#
stlist = calFunc.decimal_hms_to_arc(lst)
ralist = calFunc.decimal_deg_to_arc(ra)
halist = calFunc.decimal_hms_to_arc(ha)
declist = calFunc.decimal_hms_to_arc(dec)
azlist = calFunc.decimal_hms_to_arc(az)
altlist = calFunc.decimal_hms_to_arc(al)
print(f"    ST : {stlist[0]}h {stlist[1]}m {round(stlist[2], 1)}s")
print(f"    RA : {ralist[0]}h {ralist[1]}m {round(ralist[2], 1)}s")
print(f"    DEC : {declist[0]}° {declist[1]}' {round(declist[2], 1)}\"")
print(f"    HA : {halist[0]}h {halist[1]}m {round(halist[2], 1)}s")
print(f"    AZ : {azlist[0]}° {azlist[1]}' {round(azlist[2], 1)}\"")
print(f"    AL : {altlist[0]}° {altlist[1]}' {abs(round(altlist[2], 3))}\"")