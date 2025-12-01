from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
import sys

# 1. Map common star names to their Hipparcos (HIP) Catalog ID
# You can add more stars to this list by looking up their HIP number.
STAR_MAP = {
    "sirius": 32349,
    "canopus": 30438,
    "arcturus": 69673,
    "alpha centauri": 71683,
    "vega": 91262,
    "rigel": 24436,
    "procyon": 37279,
    "betelgeuse": 27989,
    "altair": 97649,
    "aldebaran": 21421,
    "antares": 80763,
    "spica": 65474,
    "pollux": 37826,
    "fomalhaut": 113368,
    "deneb": 102098,
    "regulus": 49669,
    "polaris": 11767
}

def decimal_to_arc_hms(x):
    x = x/24
    xhr = (x - int(x)) * 24
    xmin = (xhr - int(xhr)) * 60
    xsec = (xmin - int(xmin)) * 60
    return [int(xhr), int(xmin), xsec]

def get_star_alt_az(star_name, lat, lon):
    print(f"\n--- Calculating for {star_name.title()} ---")

    # 2. Load Data (First run will download these files)
    print("Loading ephemeris and star catalog data...")
    ts = load.timescale()
    t = ts.now() # Use current time

    # Load planetary data (DE421) to find Earth's location in space
    eph = load('de421.bsp')
    earth = eph['earth']

    # Load the Hipparcos star catalog
    with load.open(hipparcos.URL) as f:
        df = hipparcos.load_dataframe(f)

    # 3. Locate the specific Star
    clean_name = star_name.lower().strip()

    if clean_name in STAR_MAP:
        hip_id = STAR_MAP[clean_name]
        star_data = df.loc[hip_id]
        star = Star.from_dataframe(star_data)
    else:
        print(f"Error: '{star_name}' not found in the internal simple map.")
        print("Try one of these: " + ", ".join(list(STAR_MAP.keys())[:5]) + "...")
        return

    # 4. Define the Observer's location on Earth
    # wgs84 is the standard coordinate system for GPS
    observer = earth + wgs84.latlon(lat, lon)

    # 5. Calculate Position
    # .observe() calculates the astrometric position
    # .apparent() accounts for light deflection and aberration
    astrometric = observer.at(t).observe(star)
    apparent = astrometric.apparent()

    # 6. Convert to Alt/Az
    alt, az, distance = apparent.altaz()

    return alt, az, t

if __name__ == "__main__":
    try:
        # --- User Inputs ---
        print("Note: Lat/Lon uses decimal degrees (e.g., 40.71, -74.00)")
        user_lat = 13.7024063
        user_lon = 100.5000699
        target_star = input("Enter star name (e.g., Sirius, Vega, Polaris): ")

        # Calculate
        result = get_star_alt_az(target_star, user_lat, user_lon)

        if result:
            alt, az, time = result

            print("\n" + "="*30)
            print(f"Observer Time (UTC): {time.utc_strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Target: {target_star.title()}")
            print("-" * 30)
            print(f"Altitude: {alt.degrees}°")
            print(f"Azimuth : {az.degrees}°")
            print("="*30)

            if alt.degrees > 0:
                print("The star is currently ABOVE the horizon.")
            else:
                print("The star is currently BELOW the horizon.")

    except ValueError:
        print("Invalid input. Please enter numbers for coordinates.")
    except KeyboardInterrupt:
        print("\nExited.")