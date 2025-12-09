from flask import Flask, request, jsonify
from flask_cors import CORS
from skyfield import api as skyapi
from skyfield import named_stars
from skyfield.api import Star, load
from skyfield.data import hipparcos
import numpy as np
from datetime import datetime, timezone
import json
import SOB_V_2_1_radec_to_altaz as calFunc

app = Flask(__name__)
CORS(app)

# Load data once at startup
ts = load.timescale()
la = 13.70305556
long = 100.5005

#-------------------- Load Sky object data --------------------#
with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
stardict = named_stars.named_star_dict

filepath = f'V.2.1\\Deep_sky_object_data.json'
deep_sky_objects = json.load(open(filepath))

print("✓ Sky object data loaded successfully")
#-------------------- Connect with Web backend --------------------#
@app.route('/api/point-to-star', methods=['POST'])
def point_to_star():
    try:
        data = request.get_json()
        star_name = data.get('name', '').capitalize()
        
        if not star_name:
            return jsonify({'error': 'Star name is required'}), 400
        
        print(f"\n=== Pointing to: {star_name} ===")
        
        t = ts.now()
        #-------------------- Get (RA, DEC) --------------------#
        # Stars
        if star_name in stardict:
            star = Star.from_dataframe(df.loc[stardict[star_name]])
            astrometric = earth.at(t).observe(star)
            ra, dec, distance = astrometric.radec()
            ra = ra.degrees
            dec = dec.degrees
            object_type = 'star'
        # Planets
        elif star_name + ' barycenter' in planets:
            planet = planets[star_name + ' barycenter']
            astrometric = earth.at(t).observe(planet)
            ra, dec, distance = astrometric.radec()
            ra = ra.degrees
            dec = dec.degrees
            object_type = 'planet'
        # Deep sky object
        elif star_name.upper() in deep_sky_objects.keys():
            pos = deep_sky_objects[star_name.upper()]
            ra = pos['RA']
            dec = pos['Dec']
            name = pos['Name'][0]
            object_type = 'deep_sky'
        else:
            return jsonify({'error': f'Object "{star_name}" not found!'}), 404
        
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
        output = f"    ST : {stlist[0]}h {stlist[1]}m {round(stlist[2], 1)}s\n"
        output += f"    RA : {ralist[0]}h {ralist[1]}m {round(ralist[2], 1)}s\n"
        output += f"    DEC : {declist[0]}° {declist[1]}' {round(declist[2], 1)}\"\n"
        output += f"    HA : {halist[0]}h {halist[1]}m {round(halist[2], 1)}s\n"
        output += f"    AZ : {azlist[0]}° {azlist[1]}' {round(azlist[2], 1)}\"\n"
        output += f"    AL : {altlist[0]}° {altlist[1]}' {abs(round(altlist[2], 3))}\""
        
        print(output)
        
        return jsonify({
            'success': True,
            'name': star_name,
            'type': object_type,
            'output': output,
            'data': {
                'st': f"{stlist[0]}h {stlist[1]}m {round(stlist[2], 1)}s",
                'ra': f"{ralist[0]}h {ralist[1]}m {round(ralist[2], 1)}s",
                'dec': f"{declist[0]}° {declist[1]}' {round(declist[2], 1)}\"",
                'ha': f"{halist[0]}h {halist[1]}m {round(halist[2], 1)}s",
                'az': f"{azlist[0]}° {azlist[1]}' {round(azlist[2], 1)}\"",
                'al': f"{altlist[0]}° {altlist[1]}' {abs(round(altlist[2], 3))}\""
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
#-------------------- Check server Health --------------------#
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Sky Object Beam API is running'})
#-------------------- Run server --------------------#
if __name__ == '__main__':
    print("\n" + "="*50)
    print("Sky Object Beam API Server")
    print("="*50)
    print("Server running on http://localhost:5000")
    print("Endpoint: POST /api/point-to-star")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
