# R5_SHOT — dashboard screenshots (product readiness)
Account: .codex-C. Effort: medium.
Owner files: reports/run4/screenshots/**, reports/run4/screenshots/README.md
Read: AGENTS.md, app/dashboard.py, reports/run4/demonstrator_v2.md.
Contract: start `streamlit run app/dashboard.py --server.headless true --server.port 8599` in the background, wait for it, capture each page
with an available headless browser (python playwright if installed; else Chrome/Edge `--headless --screenshot`), one PNG per page (overview,
pipeline run, facility load, tariff selector, monthly bill, FIN comparison). If no browser automation is available, write README.md with
MISSING and the exact reason. Stop the server afterwards. Do not edit app code. Light CPU only.
Gate: PNGs exist or README states MISSING with the error output.
