import numpy as np
from datetime import datetime,timezone

def isLeap(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False
    
def arc_to_decimal(list_x):
    return list_x[0] + (list_x[1] / 60) + (list_x[2] / 3600)

def decimal_to_arc_deg(x):
    x = x/360
    xdeg = (x - int(x)) * 360
    xarcmim = (xdeg - int(xdeg)) * 60
    xarcsec = (xarcmim - int(xarcmim)) * 60
    return [int(xdeg), int(xarcmim), xarcsec]

def decimal_to_arc_hms(x):
    x = deg_to_hms(x)
    return decimal_to_arc_deg(x)

def hms_to_deg(x):
    return x/24 * 360

def deg_to_hms(x):
    return x/360 * 24

def getSiderealTime(now):
    #-------------------- Get day -------------------------#
    day = now.day
    month = now.month
    year = now.year
    since_21mar = [344, 10, 40, 71, 101, 132, 163, 193, 224, 254, 285, 316] #count from 21 March to first day of each month
    day_since_vernal = 0.5 #sidereal year is start at 12:00 which is 0.5day slower than tropical year
    day_since_vernal += since_21mar[month - 3] + day
    if isLeap(year) and day > 344 and day < 365: #check (is leap year)? and (is after 29 Feb)?
        day_since_vernal += 1
    day_since_vernal %= 365
    #---------------- Convert datetime to sidereal time ---------------#
    second = now.second + (now.microsecond / 1e6)
    sec_since_vernal = (day_since_vernal * 24) + (now.hour) + (now.minute / 60) + (second / 3600) #change all to hours
    utc_sidereal_time = sec_since_vernal * (366.24219 / 365.24219) #Convert tropical time to sidereal time
    return utc_sidereal_time

def gmst_from_datetime(dt):
    # Convert to UTC Julian Date
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour + dt.minute/60 + dt.second/3600 + dt.microsecond/3.6e9
    if month <= 2:
        year -= 1
        month += 12
    A = int(year/100)
    B = 2 - A + int(A/4)
    JD = int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + hour/24 + B - 1524.5
    # Days since J2000
    D = JD - 2451545.0
    # GMST in hours (IAU 2006)
    GMST = 18.697374558 + 24.06570982441908 * D
    GMST %= 24
    return GMST

def getLocalST(utc_sidereal_time, long):
    local_sidereal_time = (utc_sidereal_time + (long / 15)) % 24
    return local_sidereal_time

def getHourAngle(lst, ra):
    HA = lst - ra
    return HA

def getAltazimuth(la, ra, dec, HA):
    #if HA < 0: HA = 24 + HA
    HA_in_deg = hms_to_deg(HA)
    s = lambda x: np.sin(np.deg2rad(x))
    c = lambda x: np.cos(np.deg2rad(x))
    t = lambda x: np.tan(np.deg2rad(x))
    al = np.rad2deg( np.asin((s(dec) * s(la)) + (c(dec) * c(la) * c(HA_in_deg))))
    az = np.rad2deg( np.acos((s(la) * s(al) - s(dec)) / (-c(la) * c(al))))
    if HA <= 12:  #East
        az = 360 - az
    return az, al