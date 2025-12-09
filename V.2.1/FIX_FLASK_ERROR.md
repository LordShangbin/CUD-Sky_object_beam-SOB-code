# 🔧 Quick Fix for Flask Error

## The Problem
```
ModuleNotFoundError: No module named 'flask'
OR
No module named 'pip'
```

Your system uses `py` launcher instead of `python` command.

---

## ✅ SIMPLEST SOLUTION (2 Steps)

### Step 1: Install Packages
```
Double-click: install_simple.bat
```
This uses `py -m pip install` which should work on your system (~30 seconds).

### Step 2: Start API Server
```
Double-click: start_api_simple.bat
```

**Done!** The server should now start successfully. 🎉

---

## 🔄 Alternative: Virtual Environment

If the simple method doesn't work:

### Step 1: Setup Virtual Environment
```
Double-click: setup_venv.bat
```
Wait for it to finish installing everything (~30 seconds).

### Step 2: Start API Server
```
Double-click: start_api_venv.bat
```

---

## 🧪 Test It Works

After the server starts, you should see:
```
✓ Sky object data loaded successfully

==================================================
Sky Object Beam API Server
==================================================
Server running on http://localhost:5000
```

---

## 🌐 Then Use Your Web App

1. Server is running on port 5000 ✓
2. Open browser: **http://localhost:5173**
3. Click "Point to star"
4. See the calculations! 🌟

---

## 📋 Quick Reference

| Method | Install | Start | When to Use |
|--------|---------|-------|-------------|
| **Simple** | `install_simple.bat` | `start_api_simple.bat` | Try this first! |
| Virtual Env | `setup_venv.bat` | `start_api_venv.bat` | If simple doesn't work |
| Manual | `install_requirements.bat` | `start_api.bat` | Alternative method |

---

## 📖 More Help

See `TROUBLESHOOTING.md` for detailed solutions.
