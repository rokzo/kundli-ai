# Kundli AI — starter prototype

Files:
- `app.py`: Streamlit app with a basic Lahiri sidereal chart, planet longitudes, signs, whole-sign houses, Nakshatras and Padas.
- `requirements.txt`: required Python packages.

## Deploy
1. Create a GitHub repository named `kundli-ai`.
2. Add both files to the repository root.
3. Open https://share.streamlit.io/ and connect GitHub.
4. Choose Create app, select your repository, branch `main`, and entrypoint `app.py`, then deploy.

## Important before public launch
- This is a prototype, not a complete astrology product.
- Public Nominatim geocoding has usage policies and rate limits. Review its policy and use a compliant geocoding approach before public launch.
- Swiss Ephemeris is dual-licensed. Review the applicable license for your use; get a commercial license if needed.
- Verify results against trusted chart software and test time zones, daylight-saving transitions, and historical dates.
- This prototype uses whole-sign houses. It does not implement full Dasha timelines, divisional charts, Yogas, or Lal Kitab rules.
- Add a privacy notice and a clear data-handling policy before collecting birth details from public users.
