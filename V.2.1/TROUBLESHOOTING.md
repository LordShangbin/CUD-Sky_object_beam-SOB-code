# Troubleshooting Guide - Flask ModuleNotFoundError

## Problem: "ModuleNotFoundError: No module named 'flask'"

This happens when Flask is installed in a different Python environment than the one running your script.

## 🔧 Solutions (Try in Order)

### Solution 1: Use Virtual Environment (RECOMMENDED)

This creates an isolated Python environment with all dependencies:

1. **Run setup:**
   ```
   Double-click: setup_venv.bat
   ```

2. **Start the server:**
   ```
   Double-click: start_api_venv.bat
   ```

This is the cleanest solution and won't conflict with other Python installations.

---

### Solution 2: Install with Python Module Command

Instead of `pip install`, use:

```
Double-click: install_requirements.bat
```

This uses `python -m pip install` which ensures packages go to the correct Python.

---

### Solution 3: Check Your Python Setup

1. **Run diagnostics:**
   ```
   Double-click: check_python.bat
   ```

2. **Look at the output:**
   - Do you see Flask in the list?
   - Is there more than one Python location?

3. **If you see multiple Python installations**, you need to either:
   - Use the virtual environment (Solution 1)
   - Or specify which Python to use

---

### Solution 4: Specify Full Python Path

If you know where Flask is installed:

1. Find your Python with Flask:
   ```cmd
   where python
   py --list-paths
   ```

2. Create `start_api_direct.bat`:
   ```batch
   @echo off
   "C:\Path\To\Your\Python\python.exe" api_server.py
   pause
   ```

Replace `C:\Path\To\Your\Python\python.exe` with your actual Python path.

---

### Solution 5: Use `py` Launcher

Try using the Python launcher:

Create `start_api_py.bat`:
```batch
@echo off
py -m flask --version
py api_server.py
pause
```

---

## 🧪 Testing After Fix

Once you've fixed the issue, test with:

```cmd
cd V.2.1
python test_api.py
```

You should see output like:
```
Testing /api/health endpoint...
Status: 200
Response: {'status': 'ok', 'message': 'Sky Object Beam API is running'}
✓ Health check passed
```

---

## 📋 Required Packages

Make sure ALL these are installed in the SAME Python environment:

- flask
- flask-cors
- skyfield
- numpy
- pandas
- requests (for testing)

---

## 🎯 Quick Reference

| Method | File to Run | When to Use |
|--------|-------------|-------------|
| Virtual Environment | `setup_venv.bat` then `start_api_venv.bat` | **Best option** - Clean, isolated |
| Direct Install | `install_requirements.bat` | If you want system-wide install |
| Check Setup | `check_python.bat` | Diagnose the issue |

---

## 💡 Still Having Issues?

### Check if Flask is really installed:

Open Command Prompt and try:
```cmd
python -c "import flask; print(flask.__version__)"
```

If this works but the script doesn't, you have multiple Python installations.

### Nuclear Option - Reinstall Everything:

```cmd
python -m pip uninstall flask flask-cors skyfield numpy pandas
python -m pip install flask flask-cors skyfield numpy pandas
```

---

## ✅ Expected Working Output

When the server starts correctly, you should see:

```
✓ Sky object data loaded successfully

==================================================
Sky Object Beam API Server
==================================================
Server running on http://localhost:5000
Endpoint: POST /api/point-to-star
==================================================

 * Serving Flask app 'api_server'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
```

If you see this, it's working! Open http://localhost:5173 and test "Point to star".
