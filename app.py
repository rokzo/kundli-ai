import streamlit as st
from datetime import date, time, datetime
from zoneinfo import ZoneInfo
import swisseph as swe
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

st.set_page_config(page_title="Kundli AI", page_icon="✨")
st.title("✨ Kundli AI")
st.caption("Vedic chart calculator prototype")

SIGNS = ["Aries (Mesha)", "Taurus (Vrishabha)", "Gemini (Mithuna)",
"Cancer (Karka)", "Leo (Simha)", "Virgo (Kanya)", "Libra (Tula)",
"Scorpio (Vrischika)", "Sagittarius (Dhanu)", "Capricorn (Makara)",
"Aquarius (Kumbha)", "Pisces (Meena)"]
NAKSHATRAS = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
"Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
"Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula",
"Purva Ashadha","Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha",
"Purva Bhadrapada","Uttara Bhadrapada","Revati"]
DASHA_LORDS = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,
"Jupiter":16,"Saturn":19,"Mercury":17}
PLANETS = [("Sun",swe.SUN),("Moon",swe.MOON),("Mars",swe.MARS),
("Mercury",swe.MERCURY),("Jupiter",swe.JUPITER),("Venus",swe.VENUS),
("Saturn",swe.SATURN),("Rahu (North Node)",swe.TRUE_NODE)]

@st.cache_data(ttl=86400, show_spinner=False)
def find_place(query):
    geo = Nominatim(user_agent="kundli_ai_prototype_contact_required_before_public_launch")
    loc = geo.geocode(query, timeout=12)
    if not loc:
        return None
    lat, lon = float(loc.latitude), float(loc.longitude)
    tz = TimezoneFinder().timezone_at(lat=lat, lng=lon)
    if not tz:
        return None
    return lat, lon, tz, loc.address

def sign_of(lon):
    idx = int((lon % 360) // 30)
    return idx, (lon % 30)

def nak_of(lon):
    step = 360/27
    pos = (lon % 360)/step
    idx = int(pos)
    pada = int((pos-idx)*4)+1
    return NAKSHATRAS[idx], min(pada,4), DASHA_LORDS[idx]

with st.form("birth"):
    dob = st.date_input("Date of birth", value=date(2000,1,1), min_value=date(1900,1,1), max_value=date.today())
    bt = st.time_input("Exact local birth time", value=time(12,0))
    place = st.text_input("Birthplace (city, region, country)", placeholder="Kolkata, West Bengal, India")
    st.selectbox("Language", ["English","বাংলা (Bengali)","हिन्दी (Hindi)"])
    go = st.form_submit_button("Calculate my chart", use_container_width=True)

if go:
    if not place.strip():
        st.error("Please enter a birthplace.")
    else:
        try:
            with st.spinner("Finding location and calculating chart…"):
                found = find_place(place.strip())
                if not found:
                    st.error("Could not find that place/time zone. Try a more specific city and country.")
                else:
                    lat, lon, tz, address = found
                    local = datetime.combine(dob,bt).replace(tzinfo=ZoneInfo(tz))
                    utc = local.astimezone(ZoneInfo("UTC"))
                    hour = utc.hour + utc.minute/60 + utc.second/3600
                    jd = swe.julday(utc.year,utc.month,utc.day,hour)
                    swe.set_sid_mode(swe.SIDM_LAHIRI)
                    asc_data = swe.houses_ex(jd,lat,lon,b'W',swe.FLG_SIDEREAL)[1]
                    asc = asc_data[0] % 360
                    asc_idx, asc_deg = sign_of(asc)
                    st.success("Basic chart calculated")
                    st.write("**Place found:**", address)
                    st.write("**Time zone:**", tz)
                    st.subheader("Ascendant (Lagna)")
                    st.metric("Sidereal Ascendant", SIGNS[asc_idx])
                    st.caption(f"Ascendant longitude: {asc:.4f}°")
                    rows=[]
                    flags=swe.FLG_SWIEPH|swe.FLG_SIDEREAL|swe.FLG_SPEED
                    for name,pid in PLANETS:
                        pos=swe.calc_ut(jd,pid,flags)[0][0] % 360
                        idx,deg=sign_of(pos)
                        nak,pada,lord=nak_of(pos)
                        rows.append({"Planet":name,"Longitude":f"{pos:.4f}°","Sign":SIGNS[idx],
                        "Degree":f"{deg:.2f}°","Whole-sign house":((idx-asc_idx)%12)+1,
                        "Nakshatra":nak,"Pada":pada})
                    ketu=(swe.calc_ut(jd,swe.TRUE_NODE,flags)[0][0]+180)%360
                    idx,deg=sign_of(ketu); nak,pada,lord=nak_of(ketu)
                    rows.append({"Planet":"Ketu (South Node)","Longitude":f"{ketu:.4f}°",
                    "Sign":SIGNS[idx],"Degree":f"{deg:.2f}°",
                    "Whole-sign house":((idx-asc_idx)%12)+1,"Nakshatra":nak,"Pada":pada})
                    st.subheader("Planetary positions")
                    st.dataframe(rows,use_container_width=True,hide_index=True)
                    moon=next(swe.calc_ut(jd,swe.MOON,flags)[0][0] % 360 for _ in [0])
                    nak,pada,lord=nak_of(moon)
                    fraction=(moon%(360/27))/(360/27)
                    balance=DASHA_YEARS[lord]*(1-fraction)
                    st.subheader("Moon Nakshatra")
                    st.write(f"**{nak}**, Pada {pada}")
                    st.subheader("Vimshottari Dasha")
                    st.write(f"Birth Nakshatra lord: **{lord}**")
                    st.write(f"Approximate remaining period at birth: **{balance:.2f} years**")
                    st.info("This is a basic calculation prototype. It does not yet provide a complete Dasha timeline, divisional charts, Yogas, or Lal Kitab analysis.")
        except Exception as e:
            st.error("Could not calculate this chart. Check the place and birth details, then try again.")
            st.caption(f"Technical detail: {type(e).__name__}: {e}")

st.divider()
left,right=st.columns(2)
with left:
    st.subheader("Vedic Astrology")
    st.write("Lahiri sidereal positions and whole-sign houses.")
with right:
    st.subheader("Lal Kitab")
    st.write("Separate Lal Kitab rules will be added only after source research and verification.")
st.caption("Astrology is a traditional belief system, not a scientifically established method of predicting life events.")
st.caption("Before public launch, review geocoding-service usage rules, privacy, testing, and Swiss Ephemeris licensing.")
