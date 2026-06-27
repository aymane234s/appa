# EcoAero Designer

An Electric Airplane Design and Simulation platform built with Streamlit.

Quickstart

1. Create a Python environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run app.py
```

Files

- `aerodynamics.py`: Aerodynamic helper functions (uses `aerosandbox` when available)
- `propulsion_weight.py`: Electric propulsion and battery sizing helpers
- `app.py`: Streamlit application connecting the modules with interactive sliders and Plotly charts

Notes

- `aerosandbox` is used for advanced aerodynamics if installed; fallback formulas are provided for convenience.
- This is a starter scaffold — extend models and validations as needed.
