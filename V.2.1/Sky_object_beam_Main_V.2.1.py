from skyfield import api as skyapi
from skyfield import named_stars
from skyfield.api import Star, load
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime,timezone
import juliandate
import time
import json
import SOB_V_2_1_radec_to_altaz as calFunction
import pandas as pd

ts = load.timescale()
t = ts.now()

la = 13.70305556
long = 100.5265

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
julian_date_now = pd.Timestamp(now).to_julian_date()
print(f"Pandas Julian Date : {julian_date_now}")
jd_now = now.toordinal() + 1721424.5 + (now.hour + now.minute / 60 + now.second / 3600) / 24
print(f"Julian Date : {jd_now}")

st = calFunction.getSTgregorian(now)
lst = calFunction.getLocalST(st, long)
ha = calFunction.getHourAngle(lst, ra)
az, al = calFunction.getAltazimuth(la, ra, dec, ha)

#-------------------- Print results --------------------#
stlist = calFunction.decimal_to_arc_hms(st)
ralist = calFunction.decimal_to_arc_hms(ra)
halist = calFunction.decimal_to_arc_hms(ha)
declist = calFunction.decimal_to_arc_deg(dec)
azlist = calFunction.decimal_to_arc_deg(az)
altlist = calFunction.decimal_to_arc_deg(al)
print(f"    RA : {ralist[0]}h {int(ralist[1])}m {round(ralist[2], 1)}s")
print(f"    DEC : {declist[0]}° {int(declist[1])}' {round(declist[2], 1)}\"")
print(f"    HA : {halist[0]}h {int(halist[1])}m {round(halist[2], 1)}s")
print(f"    ST : {stlist[0]}h {int(stlist[1])}m {round(stlist[2], 1)}s")
print(f"    AZ : {azlist[0]}° {int(azlist[1])}' {round(azlist[2], 1)}\"")
print(f"    AL : {altlist[0]}° {abs(int(altlist[1]))}' {abs(round(altlist[2], 3))}\"")
