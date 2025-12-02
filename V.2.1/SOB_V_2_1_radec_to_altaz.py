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

def getSTgregorian(now):
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
    return utc_sidereal_time % 24

def getSTjulian(dt):
    # Reference: https://aa.usno.navy.mil/faq/docs/GAST.php
    JD = 367 * dt.year - int((7 * (dt.year + int((dt.month + 9) / 12))) / 4) + int((275 * dt.month) / 9) + dt.day + 1721013.5
    T = (JD - 2451545.0) / 36525
    GMST = 280.46061837 + 360.98564736629 * (JD - 2451545) + 0.000387933 * T**2 - (T**3) / 38710000
    GMST = GMST % 360
    GMST_in_hours = GMST / 15
    return GMST_in_hours

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