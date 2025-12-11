import numpy as np
from datetime import datetime,timezone

def isLeap(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False
    
def arc_to_decimal(hms):
    h, m, s = hms
    sign = -1 if h < 0 else 1
    h = abs(h)
    decimal = sign * (h + m/60 + s/3600)
    return decimal

def decimal_hms_to_arc(decimal):
    sign = -1 if decimal < 0 else 1
    decimal = abs(decimal)
    h = int(decimal)
    m = int((decimal - h) * 60)
    s = (decimal - h - m/60) * 3600
    # Restore sign to hours
    return [sign * h, m, s]

def decimal_deg_to_arc(x):
    x = deg_to_hms(x)
    return decimal_hms_to_arc(x)

def hms_to_deg(x):
    return x/24 * 360

def deg_to_hms(x):
    return x/360 * 24

def getJulianDate(now):
    JD = now.toordinal() + 1721424.5 + (now.hour + now.minute / 60 + now.second / 3600) / 24
    return JD

def getSiderealTime(now, method, getJD=getJulianDate):
    if method == 'julian':
        gmst_at_j2000 = [18, 41, 50.54841]  #Define GMST at the start of julian (J2000) in hms 
        gmst_at_j2000_decimal = arc_to_decimal(gmst_at_j2000)
        J2000 = getJD(now) - 2451545.0 #get days since J2000
        Sidereal_JD = J2000 * (366.24219 / 365.24219) #Convert tropical date to sidereal date
        utc_sidereal_time = (gmst_at_j2000_decimal + (Sidereal_JD * 24)) % 24
        return utc_sidereal_time
        
    elif method == 'gregorian':
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
    else:
        raise ValueError("Method error, must be only 'julian' or 'gregorian'")


def getLocalST(utc_sidereal_time, long):
    local_sidereal_time = (utc_sidereal_time + (long / 15)) % 24
    return local_sidereal_time

def getHourAngle(lst, ra):
    HA = (lst - ra) % 24
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