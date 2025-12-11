// src/data/astronomy.ts
export type AstronomicalData = {
  siderealTime: string;
  azimuth: string;
  altitude: string;
  hourAngle: string;
};

// Default observer location (can be made configurable)
const OBSERVER_LAT = 40.7128; // degrees (e.g., New York)
const OBSERVER_LON = -74.0060; // degrees

function degreesToDMS(degrees: number): string {
  const absD = Math.abs(degrees);
  const d = Math.floor(absD);
  const m = Math.floor((absD - d) * 60);
  const s = ((absD - d - m / 60) * 3600).toFixed(1);
  const sign = degrees < 0 ? '-' : '';
  return `${sign}${d}° ${m}' ${s}"`;
}

function degreesToHMS(degrees: number): string {
  const hours = degrees / 15;
  const h = Math.floor(hours);
  const m = Math.floor((hours - h) * 60);
  const s = ((hours - h - m / 60) * 3600).toFixed(1);
  return `${h}h ${m}m ${s}s`;
}

function calculateJulianDate(date: Date): number {
  const year = date.getUTCFullYear();
  const month = date.getUTCMonth() + 1;
  const day = date.getUTCDate();
  const hour = date.getUTCHours();
  const minute = date.getUTCMinutes();
  const second = date.getUTCSeconds();
  
  let a = Math.floor((14 - month) / 12);
  let y = year + 4800 - a;
  let m = month + 12 * a - 3;
  
  const jdn = day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
  const jd = jdn + (hour - 12) / 24 + minute / 1440 + second / 86400;
  
  return jd;
}

function calculateGMST(jd: number): number {
  const T = (jd - 2451545.0) / 36525.0;
  let gmst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + T * T * (0.000387933 - T / 38710000.0);
  
  gmst = gmst % 360;
  if (gmst < 0) gmst += 360;
  
  return gmst;
}

function calculateLST(jd: number, longitude: number): number {
  const gmst = calculateGMST(jd);
  let lst = gmst + longitude;
  
  lst = lst % 360;
  if (lst < 0) lst += 360;
  
  return lst;
}

export function calculateAstronomicalData(ra: number, dec: number, observerLat: number = OBSERVER_LAT, observerLon: number = OBSERVER_LON): AstronomicalData {
  const now = new Date();
  const jd = calculateJulianDate(now);
  const lst = calculateLST(jd, observerLon);
  
  // Hour Angle = LST - RA
  let hourAngle = lst - ra;
  if (hourAngle < 0) hourAngle += 360;
  if (hourAngle > 180) hourAngle -= 360;
  
  // Convert to radians for calculations
  const haRad = hourAngle * Math.PI / 180;
  const decRad = dec * Math.PI / 180;
  const latRad = observerLat * Math.PI / 180;
  
  // Calculate Altitude
  const sinAlt = Math.sin(decRad) * Math.sin(latRad) + Math.cos(decRad) * Math.cos(latRad) * Math.cos(haRad);
  const altitude = Math.asin(sinAlt) * 180 / Math.PI;
  
  // Calculate Azimuth
  const cosAz = (Math.sin(decRad) - Math.sin(latRad) * sinAlt) / (Math.cos(latRad) * Math.cos(Math.asin(sinAlt)));
  let azimuth = Math.acos(Math.max(-1, Math.min(1, cosAz))) * 180 / Math.PI;
  
  if (Math.sin(haRad) > 0) {
    azimuth = 360 - azimuth;
  }
  
  return {
    siderealTime: degreesToHMS(lst),
    azimuth: `${azimuth.toFixed(2)}°`,
    altitude: `${altitude.toFixed(2)}°`,
    hourAngle: `${hourAngle.toFixed(2)}°`,
  };
}
