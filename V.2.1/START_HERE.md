# 🚀 START HERE - Your System Uses `py` Command

Your system uses the Python launcher (`py`) instead of `python` command.

---

## ✅ DO THIS NOW (Simple 2-Step Fix)

### Step 1: Install Everything
Open the `V.2.1` folder and double-click:
```
install_simple.bat
```

You'll see it installing Flask, Skyfield, NumPy, etc.  
**Wait until it says "Installation complete!"**

### Step 2: Start the Server
Double-click:
```
start_api_simple.bat
```

You should see:
```
✓ Sky object data loaded successfully

==================================================
Sky Object Beam API Server
==================================================
Server running on http://localhost:5000
Endpoint: POST /api/point-to-star
==================================================
```

**🎉 Success!** Leave this window open.

---

## 🌐 Now Use Your Web App

1. Your web app is already running on **http://localhost:5173**
2. Open it in your browser
3. Select any star (try Sirius, Polaris, Vega)
4. Click **"Point to star"** button
5. You'll see an alert popup with the calculations!

---

## 📊 What You'll See

**In the browser alert:**
```
Star: Sirius

    ST : 12h 34m 56.7s
    RA : 6h 45m 8.9s
    DEC : -16° 42' 58.0"
    HA : 5h 49m 47.8s
    AZ : 135° 23' 45.6"
    AL : 45° 12' 34.567"
```

**In the Python server window (same output):**
```
=== Pointing to: Sirius ===
    ST : 12h 34m 56.7s
    RA : 6h 45m 8.9s
    DEC : -16° 42' 58.0"
    HA : 5h 49m 47.8s
    AZ : 135° 23' 45.6"
    AL : 45° 12' 34.567"
```

---

## ⚠️ If It Still Doesn't Work

Try the virtual environment method:

1. `setup_venv.bat` (wait for completion)
2. `start_api_venv.bat`

---

## 🎯 Summary

| File | What It Does |
|------|--------------|
| **install_simple.bat** | Installs packages using `py -m pip` |
| **start_api_simple.bat** | Starts server using `py` |
| setup_venv.bat | Alternative: virtual environment setup |
| start_api_venv.bat | Alternative: start with virtual env |

---

## ✅ Expected Result

- API Server: Running on port 5000 ✓
- Web App: Running on port 5173 ✓
- Click "Point to star" → See calculations ✓

**That's it!** 🌟
