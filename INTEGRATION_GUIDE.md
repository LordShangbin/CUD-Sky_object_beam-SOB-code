# Starpointer Web ↔ Sky Object Beam Integration Guide

## What Was Done

The Starpointer web application now communicates with the Sky Object Beam Python script (`Sky_object_beam_Main_V.2.1.py`) through a Flask API server.

### Changes Made:

1. **Created Flask API Server** (`V.2.1/api_server.py`)
   - Wraps the existing Sky_object_beam_Main_V.2.1.py logic
   - Exposes REST API endpoint for star pointing
   - No changes to core calculation logic
   - Same output format as original script

2. **Updated Starpointer Web App** (`Starpointer/src/App.tsx`)
   - Modified `handlePoint()` function to call the API
   - Sends star name to Python backend
   - Displays results in browser alert
   - Logs output to console

3. **Added Helper Files**
   - `V.2.1/start_api.bat` - Easy server startup
   - `V.2.1/test_api.py` - API testing script
   - `V.2.1/API_README.md` - Detailed documentation

## How to Use

### Step 1: Start the Python API Server

**Option A: Use the batch file**
```
Double-click: V.2.1/start_api.bat
```

**Option B: Command line**
```bash
cd V.2.1
python api_server.py
```

You should see:
```
==================================================
Sky Object Beam API Server
==================================================
Server running on http://localhost:5000
Endpoint: POST /api/point-to-star
==================================================
```

### Step 2: Start the Starpointer Web App

In a **separate terminal**:
```bash
cd Starpointer
npm run dev
```

### Step 3: Use the Application

1. Open browser to **http://localhost:5173** (your Starpointer web app)
2. Browse and select a star from the list
3. Click **"Point to star"** button
4. The Python script runs automatically
5. An alert popup shows the calculation results
6. Check the Python server console to see the same output

**Note:** The web app runs on port **5173** and the API server runs on port **5000**. Both must be running!

## What Happens When You Click "Point to Star"

```
┌─────────────────┐
│  Web Browser    │
│  (Starpointer)  │
└────────┬────────┘
         │ 1. User clicks "Point to star" (e.g., "Sirius")
         │
         ▼
┌─────────────────┐
│   JavaScript    │ 2. handlePoint() sends HTTP POST
│   (App.tsx)     │    to http://localhost:5000/api/point-to-star
└────────┬────────┘    Body: { "name": "Sirius" }
         │
         ▼
┌─────────────────┐
│  Flask Server   │ 3. Receives star name
│  (api_server.py)│    Sets inp = "Sirius"
└────────┬────────┘    Runs calculation logic
         │
         ▼
┌─────────────────┐
│  Sky Object     │ 4. Calculates RA, Dec, Az, Alt
│  Beam Logic     │    (Same as original script)
│  (V.2.1)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Console        │ 5. Prints to Python server console:
│  Output         │    ST : 12h 34m 56.7s
└─────────────────┘    RA : 6h 45m 8.9s
         │             DEC : -16° 42' 58.0"
         │             HA : 5h 49m 47.8s
         ▼             AZ : 135° 23' 45.6"
┌─────────────────┐    AL : 45° 12' 34.567"
│  Browser Alert  │
│  Shows Output   │ 6. Same output shown to user
└─────────────────┘
```

## Example Output

When you click "Point to star" for **Sirius**, you'll see:

**In Browser Alert:**
```
Star: Sirius

    ST : 12h 34m 56.7s
    RA : 6h 45m 8.9s
    DEC : -16° 42' 58.0"
    HA : 5h 49m 47.8s
    AZ : 135° 23' 45.6"
    AL : 45° 12' 34.567"
```

**In Python Server Console:**
```
=== Pointing to: Sirius ===
    ST : 12h 34m 56.7s
    RA : 6h 45m 8.9s
    DEC : -16° 42' 58.0"
    HA : 5h 49m 47.8s
    AZ : 135° 23' 45.6"
    AL : 45° 12' 34.567"
```

## Testing the API

Run the test script to verify everything works:

```bash
cd V.2.1
python test_api.py
```

This will test the API with several stars and show you the results.

## Troubleshooting

### "Failed to connect to Sky Object Beam API"
- ✓ Make sure `api_server.py` is running
- ✓ Check the server is on port 5000
- ✓ Verify no firewall is blocking localhost

### "Object not found"
- ✓ Star name must exist in the database
- ✓ Try with known stars: Sirius, Polaris, Vega, Betelgeuse
- ✓ Check capitalization (first letter uppercase)

### Port 5000 Already in Use
Edit `api_server.py` line 127:
```python
app.run(debug=True, port=5001)  # Change to different port
```

Then update Starpointer `App.tsx` line 250:
```typescript
const response = await fetch('http://localhost:5001/api/point-to-star', {
```

## Original Script Still Works

The original `Sky_object_beam_Main_V.2.1.py` still works exactly as before:

```bash
cd V.2.1
python Sky_object_beam_Main_V.2.1.py
```

It will prompt for star name and show the same output.

## Files Modified/Created

### Created:
- ✓ `V.2.1/api_server.py` - Flask API wrapper
- ✓ `V.2.1/start_api.bat` - Batch file to start server
- ✓ `V.2.1/test_api.py` - API testing script
- ✓ `V.2.1/API_README.md` - API documentation

### Modified:
- ✓ `Starpointer/src/App.tsx` - handlePoint() function now calls API

### Unchanged:
- ✓ `V.2.1/Sky_object_beam_Main_V.2.1.py` - Original script intact
- ✓ All calculation logic remains the same
- ✓ Output format remains identical
