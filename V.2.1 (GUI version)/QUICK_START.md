# 🚀 Quick Start Guide

## What This Does

Click "Point to star" in the web app → Python script runs → See RA/Dec/Az/Alt calculations!

## 🎯 Three Ways to Start

### Option 1: Start Everything at Once (Easiest!)
```
Double-click: start_all.bat
```
This starts both the API server and web app automatically.

### Option 2: Start Manually (More Control)

**Terminal 1 - API Server:**
```bash
cd V.2.1
python api_server.py
```

**Terminal 2 - Web App:**
```bash
cd Starpointer
npm run dev
```

### Option 3: API Server Only
```
Double-click: V.2.1/start_api.bat
```
Then start the web app separately.

## ✅ How to Use

1. **Start the servers** (using one of the options above)

2. **Open the web app** in your browser
   - Go to: **http://localhost:5173**

3. **Select a star** from the list
   - Try: Sirius, Polaris, Vega, or Betelgeuse

4. **Click "Point to star"** button

5. **See the output!**
   - Alert popup shows the calculations
   - Python console shows the same output
   - Both display: ST, RA, DEC, HA, AZ, AL

## 📊 Example Output

```
Star: Sirius

    ST : 12h 34m 56.7s
    RA : 6h 45m 8.9s
    DEC : -16° 42' 58.0"
    HA : 5h 49m 47.8s
    AZ : 135° 23' 45.6"
    AL : 45° 12' 34.567"
```

## 🌐 Port Setup

```
┌─────────────────────────────┐
│  http://localhost:5173      │  ← Your browser (Starpointer Web)
│  (Vite Dev Server)          │
└──────────────┬──────────────┘
               │ Sends star name
               │ via HTTP POST
               ▼
┌─────────────────────────────┐
│  http://localhost:5000      │  ← Flask API Server
│  (Python Backend)           │
└─────────────────────────────┘
```

**Both servers must be running!**
- Port **5173** = Web App
- Port **5000** = API Server

## 🔧 Requirements

- Python 3.x with packages:
  - flask
  - flask-cors
  - skyfield
  - numpy
  - pandas

- Node.js with npm (for web app)

### First Time Setup

If you get "ModuleNotFoundError: No module named 'flask'":

```
cd V.2.1
Double-click: setup_venv.bat
```

Then use `start_api_venv.bat` instead of `start_api.bat`.

See `V.2.1/FIX_FLASK_ERROR.md` for details.

## 🧪 Test the API

```bash
cd V.2.1
python test_api.py
```

This tests the API with multiple stars.

## ❓ Troubleshooting

**"Failed to connect to API"**
- Make sure the Python server is running on port 5000

**"Object not found"**
- Star name must be in the database
- Try known stars like Sirius, Polaris, Vega

**Port already in use**
- Change port in `api_server.py` (line 127)
- Update port in `App.tsx` (line 250)

## 📁 Key Files

| File | Purpose |
|------|---------|
| `V.2.1/api_server.py` | Flask API that runs the Python script |
| `V.2.1/Sky_object_beam_Main_V.2.1.py` | Original script (unchanged) |
| `Starpointer/src/App.tsx` | Web app (modified handlePoint function) |
| `start_all.bat` | Starts both servers |

## 📖 More Info

See `INTEGRATION_GUIDE.md` for detailed documentation.
