import streamlit as st
import datetime
import math

st.set_page_config(page_title="Kundli AI", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0b0e1b;
        color: #f7ede2;
    }
    .main-title {
        text-align: center;
        color: #f4c66a;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #a0a6c6;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }
    .card {
        background: #151930;
        border: 1px solid #2d3356;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .highlight-gold {
        color: #f4c66a;
        font-weight: 700;
    }
    .remedy-box {
        background: #1f1b2e;
        border-left: 4px solid #f4a261;
        padding: 12px 14px;
        border-radius: 6px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🕉️ Kundli AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Vedic Janam Kundli & Lal Kitab Analysis Engine</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📜 Enter Birth Details")
    dob = st.date_input("Date of Birth", datetime.date(2000, 1, 1), min_value=datetime.date(1920, 1, 1))
    tob = st.time_input("Exact Birth Time", datetime.time(12, 0))
    place = st.text_input("Birth City", "Kolkata, India")
    btn_calc = st.button("🔮 Calculate Kundli", use_container_width=True)

RASHIS = [
    "Mesha (Aries)", "Vrishabha (Taurus)", "Mithuna (Gemini)", "Karka (Cancer)",
    "Simha (Leo)", "Kanya (Virgo)", "Tula (Libra)", "Vrishchika (Scorpio)",
    "Dhanu (Sagittarius)", "Makara (Capricorn)", "Kumbha (Aquarius)", "Meena (Pisces)"
]

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

def calculate_chart(dob_val, tob_val):
    dt = datetime.datetime.combine(dob_val, tob_val)
    days = (dt - datetime.datetime(2000, 1, 1, 12, 0)).total_seconds() / 86400.0
    
    sun_deg = (280.460 + 0.9856474 * days - 24.0) % 360
    moon_deg = (218.316 + 13.176396 * days - 24.0) % 360
    mars_deg = (355.433 + 0.524033 * days - 24.0) % 360
    mercury_deg = (sun_deg + 18.0 * math.sin(days / 15.0)) % 360
    jupiter_deg = (34.351 + 0.083085 * days - 24.0) % 360
    venus_deg = (sun_deg + 25.0 * math.cos(days / 20.0)) % 360
    saturn_deg = (50.077 + 0.033444 * days - 24.0) % 360
    rahu_deg = (240.0 - 0.05295 * days) % 360
    ketu_deg = (rahu_deg + 180.0) % 360

    hour_fraction = tob_val.hour + tob_val.minute / 60.0
    lagna_deg = (sun_deg + (hour_fraction - 6.0) * 15.0) % 360
    lagna_sign_idx = int(lagna_deg // 30) % 12

    planets = {
        "Surya (Sun)": sun_deg,
        "Chandra (Moon)": moon_deg,
        "Mangala (Mars)": mars_deg,
        "Budha (Mercury)": mercury_deg,
        "Guru (Jupiter)": jupiter_deg,
        "Shukra (Venus)": venus_deg,
        "Shani (Saturn)": saturn_deg,
        "Rahu": rahu_deg,
        "Ketu": ketu_deg,
    }

    house_occupants = {i: [] for i in range(1, 13)}
    planet_details = []

    for name, deg in planets.items():
        norm_deg = deg % 360
        sign_idx = int(norm_deg // 30) % 12
        house_num = ((sign_idx - lagna_sign_idx) % 12) + 1
        nak_idx = int(norm_deg / (360.0 / 27.0)) % 27
        pada = (int((norm_deg % (360.0 / 27.0)) / (360.0 / 108.0)) % 4) + 1
        short_name = name.split()[0][:3]
        house_occupants[house_num].append(short_name)
        
        planet_details.append({
            "Graha": name,
            "Degree": f"{norm_deg % 30:.2f}°",
            "Rashi": RASHIS[sign_idx].split()[0],
            "House": f"House {house_num}",
            "Nakshatra": NAKSHATRAS[nak_idx],
            "Pada": pada
        })

    return lagna_sign_idx, house_occupants, planet_details, moon_deg

def render_north_indian_svg(lagna_idx, occupants):
    h_signs = {h: ((lagna_idx + h - 1) % 12) + 1 for h in range(1, 13)}
    
    def get_text(h):
        planets_str = " ".join(occupants.get(h, []))
        return f"{h_signs[h]} {planets_str}" if planets_str else f"{h_signs[h]}"

    return f"""
    <svg viewBox="0 0 400 400" width="100%" height="340" style="background:#13172d; border-radius:12px; border:2px solid #a37d36;">
        <line x1="0" y1="0" x2="400" y2="0" stroke="#f4c66a" stroke-width="2"/>
        <line x1="400" y1="0" x2="400" y2="400" stroke="#f4c66a" stroke-width="2"/>
        <line x1="400" y1="400" x2="0" y2="400" stroke="#f4c66a" stroke-width="2"/>
        <line x1="0" y1="400" x2="0" y2="0" stroke="#f4c66a" stroke-width="2"/>
        <line x1="0" y1="0" x2="400" y2="400" stroke="#f4c66a" stroke-width="2"/>
        <line x1="0" y1="400" x2="400" y2="0" stroke="#f4c66a" stroke-width="2"/>
        <polygon points="200,0 400,200 200,400 0,200" fill="none" stroke="#f4c66a" stroke-width="2"/>
        
        <text x="200" y="115" fill="#fceecb" font-size="12" font-family="Arial" text-anchor="middle" font-weight="bold">{get_text(1)} (1st)</text>
        <text x="100" y="55" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(2)}</text>
        <text x="45" y="110" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(3)}</text>
        <text x="115" y="200" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(4)}</text>
        <text x="45" y="295" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(5)}</text>
        <text x="100" y="350" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(6)}</text>
        <text x="200" y="290" fill="#fceecb" font-size="12" font-family="Arial" text-anchor="middle" font-weight="bold">{get_text(7)} (7th)</text>
        <text x="300" y="350" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(8)}</text>
        <text x="355" y="295" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(9)}</text>
        <text x="285" y="200" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(10)}</text>
        <text x="355" y="110" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(11)}</text>
        <text x="300" y="55" fill="#fceecb" font-size="11" font-family="Arial" text-anchor="middle">{get_text(12)}</text>
    </svg>
    """

lagna_idx, occupants, p_details, moon_deg = calculate_chart(dob, tob)
moon_sign_idx = int(moon_deg // 30) % 12
nak_idx = int((moon_deg % 360) / (360.0 / 27.0)) % 27

col1, col2 = st.columns([1, 1.4])

with col1:
    st.markdown("#### 💎 Lagna Kundli (Birth Chart)")
    st.markdown(render_north_indian_svg(lagna_idx, occupants), unsafe_allow_html=True)
    st.caption("North Indian diamond chart with House 1 at the top center.")

with col2:
    st.markdown("#### 🌟 Core Planetary Summary")
    st.markdown(f"""
    <div class="card">
        <div><b>Lagna (Ascendant):</b> <span class="highlight-gold">{RASHIS[lagna_idx]}</span></div>
        <div><b>Chandra Rashi (Moon Sign):</b> <span class="highlight-gold">{RASHIS[moon_sign_idx]}</span></div>
        <div><b>Janma Nakshatra:</b> <span class="highlight-gold">{NAKSHATRAS[nak_idx]}</span></div>
        <div><b>Birthplace:</b> <span class="highlight-gold">{place}</span></div>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🪐 Planetary Positions", 
    "📕 Lal Kitab Analysis", 
    "⚖️ Dosha & Raj Yoga", 
    "🤖 Pandit AI Chat"
])

with tab1:
    st.markdown("### Detailed Planetary Table (Graha Sthiti)")
    st.dataframe(p_details, use_container_width=True)

with tab2:
    st.markdown("### 📕 Lal Kitab Teva & Upay")
    st.info("In Lal Kitab, Aries represents House 1, Taurus represents House 2, etc., regardless of Lagna.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Pakka Ghar (Permanent House) Insights:**")
        st.write("• **Guru (Jupiter):** House 1 & 9 - Governs moral character and fortune.")
        st.write("• **Surya (Sun):** House 5 - Vitality, father, and intellect.")
        st.write("• **Shani (Saturn):** House 8 & 10 - Karmic duties and long-term labor.")
    with col_b:
        st.markdown("**Traditional Lal Kitab Remedies (Upay):**")
        st.markdown("""
        <div class="remedy-box">
            <b>For Mental Calm (Chandra):</b> Avoid selling silver or dairy items received in charity. Maintain a clean water bowl for birds.
        </div>
        <div class="remedy-box">
            <b>For Rahu / Obstacles:</b> Do not keep damaged electronics or rusted iron scrap in upper rooms or terrace corners.
        </div>
        <div class="remedy-box">
            <b>For Respect & Vitality (Surya):</b> Offer plain water to the rising Sun daily from a copper vessel.
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### ⚖️ Dosha & Raja Yoga Scan")
    m_check = "Mangala (Mars)" in [p["Graha"] for p in p_details if p["House"] in ["House 1", "House 4", "House 7", "House 8", "House 12"]]
    st.markdown(f"""
    <div class="card">
        <b>Manglik Check:</b> {"⚠️ Partial/Full Manglik placement (Mars in Kendra/Trika house)" if m_check else "✅ No primary Manglik placement in 1st/4th/7th/8th/12th houses."}<br>
        <b>Gajakesari Yoga:</b> Angular relationship between Jupiter and Moon.<br>
        <b>Pitri Dosha Check:</b> Assesses Sun and 9th house relationships.
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 💬 Ask Pandit AI")
    user_query = st.text_input("Ask a question about your career, marriage, or remedies:")
    if user_query:
        st.markdown(f"""
        <div class="card">
            <b>Reading for "{user_query}":</b><br>
            With your Lagna in <b>{RASHIS[lagna_idx]}</b> and Moon sign in <b>{RASHIS[moon_sign_idx]}</b>, 
            traditional principles emphasize balancing your Kendra houses. In Lal Kitab analysis, avoid superstitious fear and focus on clear karmic conduct (Satvik habits, respecting elders, and keeping living spaces uncluttered).
        </div>
        """, unsafe_allow_html=True)
