Installing XFOIL and enabling high-fidelity airfoil analysis
=============================================================

To get the most accurate 2D airfoil polars (XFLR5-level accuracy) the app can use a local XFOIL installation.

1) Download XFOIL
   - Windows: download a prebuilt `xfoil.exe` from a trusted source, or build from source.
   - Mac / Linux: build from source or use package managers if available.

2) Install
   - Place `xfoil.exe` in a folder on your PATH, or copy it to `C:\XFOIL\xfoil.exe`.
   - Verify from a terminal:

```powershell
xfoil
# or full path
C:\XFOIL\xfoil.exe
```

3) Enable in the app
   - Open the `Airfoil Explorer` page and check `Enable XFOIL (if installed)`.
   - The app will automatically detect XFOIL and use it to compute polars.

AeroSandbox (optional, 3D/VLM capability)
-----------------------------------------
- Install via pip inside the project's virtual environment:

```powershell
& 'c:\Users\HP\Desktop\EcoAero_Project\venv\Scripts\pip.exe' install aerosandbox
```

- Then enable `Enable AeroSandbox (if installed)` in the `Airfoil Explorer` UI.

Notes
-----
- XFOIL is an external executable (not a Python package). The app includes fallbacks if XFOIL is not available.
- AeroSandbox integration is optional and best-effort; some advanced analyses may require additional configuration.
