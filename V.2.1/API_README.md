# Sky Object Beam API Server

This API server allows the Starpointer web app to communicate with the Sky Object Beam Python script.

## Setup

### Prerequisites
Make sure you have installed:
- Python 3.x
- Flask
- Flask-CORS
- Skyfield
- NumPy
- Pandas

## How to Use

### 1. Start the API Server

**Option A: Double-click the batch file**
```
start_api.bat
```

**Option B: Run manually**
```bash
cd V.2.1
python api_server.py
```

The server will start on `http://localhost:5000`

### 2. Start the Starpointer Web App

In a separate terminal:
```bash
cd Starpointer
npm run dev
```

### 3. Point to a Star

1. Open the web app in your browser (usually http://localhost:5173)
2. Select a star from the list
3. Click the "Point to star" button
4. The Python script will run and calculate the coordinates
5. You'll see an alert with the output showing:
   - ST (Sidereal Time)
   - RA (Right Ascension)
   - DEC (Declination)
   - HA (Hour Angle)
   - AZ (Azimuth)
   - AL (Altitude)

### 4. Check the Console

The Python server console will show the same output that the original script showed, so you can see it running in real-time.

## API Endpoints

### POST /api/point-to-star
Point the telescope to a celestial object.

**Request:**
```json
{
  "name": "Sirius"
}
```

**Response:**
```json
{
  "success": true,
  "name": "Sirius",
  "type": "star",
  "output": "    ST : 12h 34m 56.7s\n    RA : 6h 45m 8.9s\n...",
  "data": {
    "st": "12h 34m 56.7s",
    "ra": "6h 45m 8.9s",
    "dec": "-16° 42' 58.0\"",
    "ha": "5h 49m 47.8s",
    "az": "135° 23' 45.6\"",
    "al": "45° 12' 34.567\""
  }
}
```

### GET /api/health
Check if the API server is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Sky Object Beam API is running"
}
```

## Troubleshooting

### "Failed to connect to Sky Object Beam API"
- Make sure the Python API server is running on port 5000
- Check that no firewall is blocking localhost connections
- Verify the server console shows "Server running on http://localhost:5000"

### "Object not found"
- The star name must match what's in the named_stars database
- Try capitalizing properly (e.g., "Sirius" not "sirius")
- Check the original Sky_object_beam_Main_V.2.1.py script works with that star name

### CORS Errors
- Make sure Flask-CORS is installed: `pip install flask-cors`
- The API server should automatically handle CORS headers
