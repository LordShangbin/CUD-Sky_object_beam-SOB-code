from skyfield import api as skyapi
from skyfield import named_stars
from skyfield.api import Star, load
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime,timezone

############################# pos setup #########################################
la = 13.70305556
long = 100.5265

deep_sky_objects = {
    'M112':{
        'RA': [12,41,22.6],
        'Dec': [-34,29,56.42],
        'Name': ['Unknown']
    },
    'M31': {
        'RA': [0, 44, 2.7],
        'Dec': [41, 16, 54.0],
        'Name': ['Andromeda Galaxy']
    },
    'M42': {
        'RA': [5, 35, 17.5],
        'Dec': [-5, 23, 28.6],
        'Name': ['Orion Nebula']
    },
    'M13': {
        'RA': [16, 41, 41.2],
        'Dec': [36, 27, 36.1],
        'Name': ['Hercules Cluster']
    },
    'M51': {
        'RA': [13, 29, 52.8],
        'Dec': [47, 11, 43.2],
        'Name': ['Whirlpool Galaxy']
    },
    'M57': {
        'RA': [18, 53, 35.1],
        'Dec': [32, 56, 54.3],
        'Name': ['Ring Nebula']
    },
    'NGC 869': {
        'RA': [2, 20, 14.0],
        'Dec': [57, 8, 23.0],
        'Name': ['Double Cluster']
    },
    'NGC 884': {
        'RA': [2, 20, 14.0],
        'Dec': [57, 8, 23.0],
        'Name': ['Double Cluster']
    },
    'NGC 7000': {
        'RA': [20, 58, 47.2],
        'Dec': [44, 20, 48.0],
        'Name': ['North America Nebula']
    },
    'NGC 4565': {
        'RA': [12, 36, 20.7],
        'Dec': [25, 59, 16.0],
        'Name': ['Needle Galaxy']
    },
    'NGC 6960': {
        'RA': [20, 45, 38.5],
        'Dec': [30, 43, 4.0],
        'Name': ['Veil Nebula']
    },
    'NGC 7293': {
        'RA': [22, 29, 38.9],
        'Dec': [-20, 50, 13.0],
        'Name': ['Helix Nebula']
    },
    'M45': {
        'RA': [3, 47, 24.6],
        'Dec': [24, 7, 0.0],
        'Name': ['The Pleiades']
    },
    'M44': {
        'RA': [8, 40, 24.3],
        'Dec': [19, 40, 48.0],
        'Name': ['The Beehive Cluster']
    },
    'M92': {
        'RA': [17, 17, 7.8],
        'Dec': [43, 8, 10.0],
        'Name': ['The Great Globular Cluster in Hercules']
    },
    'M8': {
        'RA': [18, 3, 37.2],
        'Dec': [-24, 23, 12.0],
        'Name': ['The Lagoon Nebula']
    },
}

def arc_to_decimal(list_x):
    return list_x[0] + (list_x[1] / 60) + (list_x[2] / 3600)
def decimal_to_arc_hms(x):
    x = x/24
    xhr = (x - int(x)) * 24
    xmin = (xhr - int(xhr)) * 60
    xsec = (xmin - int(xmin)) * 60
    return [int(xhr), int(xmin), xsec]
def decimal_to_arc_deg(x):
    x = x/360
    xdeg = (x - int(x)) * 360
    xarcmim = (xdeg - int(xdeg)) * 60
    xarcsec = (xarcmim - int(xarcmim)) * 60
    return [int(xdeg), int(xarcmim), xarcsec]
def hms_to_deg(x):
    return x/24 * 360
def deg_to_hms(x):
    return x/360 * 24

def getaltaz(rasp, decsp, la, long, sidlist):
    declist = [(int(decsp[0].split("deg")[0])), (int(decsp[1].split("'")[0])),(float(decsp[2].split('"')[0]))]
    if declist[0] >= 0 and (decsp[0].split("deg")[0]) != "-0":
        DEC = declist[0] + declist[1] / 60 + declist[2] / 3600
    else:
        DEC = declist[0] - declist[1] / 60 - declist[2] / 3600
    ralist = [(int(rasp[0].split("h")[0])), (int(rasp[1].split("m")[0])),(float(rasp[2].split("s")[0]))]
    if ralist[0] >= 0 and (rasp[0].split("h")[0]) != "-0":
        RA = arc_to_decimal(ralist)
    else:
        RA = ralist[0] - ralist[1] / 60 - ralist[2] / 3600
    HA = arc_to_decimal(sidlist) - arc_to_decimal(ralist)
    if HA < 0: HA = 24 + HA
    HA_in_deg = hms_to_deg(HA)
    s = lambda x: np.sin(np.deg2rad(x))
    c = lambda x: np.cos(np.deg2rad(x))
    t = lambda x: np.tan(np.deg2rad(x))
    al = np.rad2deg( np.asin((s(DEC) * s(la)) + (c(DEC) * c(la) * c(HA_in_deg))))
    az = np.rad2deg( np.acos((s(la) * s(al) - s(DEC)) / (-c(la) * c(al))))
    if HA <= 12:  #East
        az = 360 - az
    print("HA :",decimal_to_arc_hms(HA))
    print("SID :",sidlist)
    print(az,al)
    return az, al

#################### skyfield setup ###################
# class SOB_calculation:
#     def __init__():
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
planets = load('de421.bsp')
earth = planets['earth']
sun = planets['sun']
ra, dec, distance, ha, az, al = 0, 0, 0, 0, 0, 0
stardict = named_stars.named_star_dict
ts = load.timescale()
t = ts.now()
inp = input("Star Name : ")
app_sun_ra , app_sun_dec, app_sun_distance  = earth.at(t).observe(sun).apparent().radec()
############# star #############
if inp in stardict:
    barnards_star = Star.from_dataframe(df.loc[stardict[inp]])
    astrometric = earth.at(t).observe(barnards_star)
    ra, dec, distance = astrometric.radec()
############# planet #############
elif inp + ' barycenter' in planets:
    planet = planets[inp + ' barycenter']
    astrometric = earth.at(t).observe(planet)
    ra, dec, distance = astrometric.radec()
############# Deepsky object #############
elif inp.upper() in deep_sky_objects.keys():
    pos = deep_sky_objects[inp.upper()]
    rightas = pos['RA']
    decli = pos['Dec']
    name = pos['Name'][0]
    ra = str(rightas[0]) + "h " + str(rightas[1]) + "m " + str(rightas[2]) + "s"
    dec = str(decli[0]) + "deg " + str(decli[1]) + "' " + str(decli[2]) + '"'
############################ Get day ###############################
current_time = datetime.now(timezone.utc)
print(current_time)
datelist = str(current_time).split(" ")[0].split("-")
timelist = str(current_time).split(" ")[1].split("+")[0].split(":")
day_since_vernal = [344, 10, 40, 71, 101, 132, 163, 193, 224, 254, 285, 316]
day = 0.5 #sidereal year is start at 12:00 which is 0.5day slower than tropical year
day += day_since_vernal[int(datelist[1]) - 3] + float(datelist[2])
if int(datelist[0]) % 4 == 0 and int(datelist[0]) % 100 != 0:
    if day > 344 and day < 365:
        day += 1
if day >= 365:
    day = day - 365
##################### Get sidereal time ###############
sec_since_vernal = (day * 24 * 60 * 60) + (float(timelist[0]) * 3600) + (float(timelist[1]) * 60) + float(timelist[2])
local_sec_since_vernal = sec_since_vernal + (long * 60 * 60 / 15)
sidsec = local_sec_since_vernal * (366.24219 / 365.24219)
sidhour = sidsec / (60*60)
sidlist = decimal_to_arc_hms(sidhour)
ralist = str(ra).split(" ")
print(ra)
decsplist = str(dec).split(" ")
##################### Get Altaz #####################
declist = [(int(decsplist[0].split("deg")[0])), (int(decsplist[1].split("'")[0])),(float(decsplist[2].split('"')[0]))]
if declist[0] >= 0 and (decsplist[0].split("deg")[0]) != "-0":
    DEC = declist[0] + declist[1] / 60 + declist[2] / 3600
else:
    DEC = declist[0] - declist[1] / 60 - declist[2] / 3600
ralist = [(int(ralist[0].split("h")[0])), (int(ralist[1].split("m")[0])),(float(ralist[2].split("s")[0]))]
if ralist[0] >= 0 and (ralist[0].split("h")[0]) != "-0":
    RA = arc_to_decimal(ralist)
else:
    RA = ralist[0] - ralist[1] / 60 - ralist[2] / 3600
HA = arc_to_decimal(sidlist) - arc_to_decimal(ralist)
if HA < 0: HA = 24 + HA
HA_in_deg = hms_to_deg(HA)
s = lambda x: np.sin(np.deg2rad(x))
c = lambda x: np.cos(np.deg2rad(x))
t = lambda x: np.tan(np.deg2rad(x))
al = np.rad2deg( np.asin((s(DEC) * s(la)) + (c(DEC) * c(la) * c(HA_in_deg))))
az = np.rad2deg( np.acos((s(la) * s(al) - s(DEC)) / (-c(la) * c(al))))
if HA <= 12:  #East
    az = 360 - az
print("HA :",decimal_to_arc_hms(HA))
print("SID :",sidlist)
azlist = decimal_to_arc_deg(az)
altlist = decimal_to_arc_deg(al)
print(f"{azlist[0]}° {int(azlist[1])}' {round(azlist[2], 1)}''")
print(f"{altlist[0]}° {abs(int(altlist[1]))}' {abs(round(altlist[2], 3))}''")