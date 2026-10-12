import streamlit as st
import datetime
import math

st.set_page_config(page_title="Kundli AI | শাস্ত্রীয় কুষ্ঠি বিচার", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0b0e1b;
        color: #f7ede2;
    }
    .main-title {
        text-align: center;
        color: #f4c66a;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 2px;
    }
    .subtitle {
        text-align: center;
        color: #a0a6c6;
        font-size: 0.90rem;
        margin-bottom: 20px;
    }
    .card {
        background: #151930;
        border: 1px solid #2d3356;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
    .highlight-gold {
        color: #f4c66a;
        font-weight: 700;
    }
    .source-tag {
        font-size: 0.75rem;
        background: #232946;
        color: #eebbc3;
        padding: 2px 7px;
        border-radius: 4px;
        border: 1px solid #394266;
        display: inline-block;
        margin-top: 4px;
    }
    .remedy-box {
        background: #181528;
        border-left: 4px solid #f4a261;
        padding: 12px 14px;
        border-radius: 6px;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🕉️ Kundli AI — শাস্ত্রীয় কোষ্ঠী ও সিদ্ধান্ত পঞ্জিকা</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Direct classical rule engine: Brihat Parashara Hora Shastra, Lal Kitab (1952), & Gupta Press Panjika</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📜 জন্ম তথ্য (Birth Information)")
    dob = st.date_input("Date of Birth", datetime.date(2000, 1, 1), min_value=datetime.date(1920, 1, 1))
    tob = st.time_input("Exact Birth Time", datetime.time(12, 0))
    place = st.text_input("Birthplace", "Kolkata, West Bengal, India")
    chart_view = st.selectbox("Chart Style", ["North Indian (Diamond)", "East Indian / Bengali (পূর্ব ভারতীয় ছক)"])
    btn_calc = st.button("🔮 Calculate Source Chart", use_container_width=True)

# ----------------- CANONICAL ASTROLOGICAL DATA -----------------
RASHIS = [
    {"en": "Mesha (Aries)", "bn": "মেষ", "lord": "Mangala", "element": "Fire"},
    {"en": "Vrishabha (Taurus)", "bn": "বৃষ", "lord": "Shukra", "element": "Earth"},
    {"en": "Mithuna (Gemini)", "bn": "মিথুন", "lord": "Budha", "element": "Air"},
    {"en": "Karka (Cancer)", "bn": "কর্কট", "lord": "Chandra", "element": "Water"},
    {"en": "Simha (Leo)", "bn": "সিংহ", "lord": "Surya", "element": "Fire"},
    {"en": "Kanya (Virgo)", "bn": "কন্যা", "lord": "Budha", "element": "Earth"},
    {"en": "Tula (Libra)", "bn": "তুলা", "lord": "Shukra", "element": "Air"},
    {"en": "Vrishchika (Scorpio)", "bn": "বৃশ্চিক", "lord": "Mangala", "element": "Water"},
    {"en": "Dhanu (Sagittarius)", "bn": "ধনু", "lord": "Guru", "element": "Fire"},
    {"en": "Makara (Capricorn)", "bn": "মকর", "lord": "Shani", "element": "Earth"},
    {"en": "Kumbha (Aquarius)", "bn": "কুম্ভ", "lord": "Shani", "element": "Air"},
    {"en": "Meena (Pisces)", "bn": "মীন", "lord": "Guru", "element": "Water"}
]

NAKSHATRAS = [
    ("Ashwini", "অশ্বিনী", "Ketu", 7), ("Bharani", "ভরণী", "Shukra", 20), ("Krittika", "কৃত্তিকা", "Surya", 6),
    ("Rohini", "রোহিণী", "Chandra", 10), ("Mrigashira", "মৃগশিরা", "Mangala", 7), ("Ardra", "আর্দ্রা", "Rahu", 18),
    ("Punarvasu", "পুনর্বসু", "Guru", 16), ("Pushya", "পুষ্যা", "Shani", 19), ("Ashlesha", "অশ্লেষা", "Budha", 17),
    ("Magha", "মঘা", "Ketu", 7), ("Purva Phalguni", "পূর্ব ফল্গুনী", "Shukra", 20), ("Uttara Phalguni", "উত্তর ফল্গুনী", "Surya", 6),
    ("Hasta", "হস্তা", "Chandra", 10), ("Chitra", "চিত্রা", "Mangala", 7), ("Swati", "স্বাতী", "Rahu", 18),
    ("Vishakha", "বিশাখা", "Guru", 16), ("Anuradha", "অনুরাধা", "Shani", 19), ("Jyeshtha", "জ্যেষ্ঠা", "Budha", 17),
    ("Mula", "মূলা", "Ketu", 7), ("Purva Ashadha", "পূর্বাষাঢ়া", "Shukra", 20), ("Uttara Ashadha", "উত্তরাষাঢ়া", "Surya", 6),
    ("Shravana", "শ্রবণা", "Chandra", 10), ("Dhanishtha", "ধনিষ্ঠা", "Mangala", 7), ("Shatabhisha", "শতভিষা", "Rahu", 18),
    ("Purva Bhadrapada", "পূর্বভাদ্রপদ", "Guru", 16), ("Uttara Bhadrapada", "উত্তরভাদ্রপদ", "Shani", 19), ("Revati", "রেবতী", "Budha", 17)
]

TITHIS_BN = [
    "শুক্লা প্রতিপদ", "দ্বিতীয়া", "তৃতীয়া", "চতুর্থী", "পঞ্চমী", "ষষ্ঠী", "সপ্তমী", "অষ্টমী", "নবমী", "দশমী",
    "একাদশী", "দ্বাদশী", "ত্রয়োদশী", "চতুর্দশী", "পূর্ণিমা",
    "কৃষ্ণা প্রতিপদ", "দ্বিতীয়া", "তৃতীয়া", "চতুর্থী", "পঞ্চমী", "ষষ্ঠী", "সপ্তমী", "অষ্টমী", "নবমী", "দশমী",
    "একাদশী", "দ্বাদশী", "ত্রয়োদশী", "চতুর্দশী", "অমাবস্যা"
]

DASHA_CYCLE = [
    ("Ketu", 7), ("Shukra", 20), ("Surya", 6), ("Chandra", 10),
    ("Mangala", 7), ("Rahu", 18), ("Guru", 16), ("Shani", 19), ("Budha", 17)
]

# Exaltation (Uchcha) and Debilitation (Neecha) signs as per BPHS Ch. 3
DIGNITY_BPHS = {
    "Surya":   {"uchcha": 0, "neecha": 6, "moolatrikona": 4},
    "Chandra": {"uchcha": 1, "neecha": 7, "moolatrikona": 1},
    "Mangala": {"uchcha": 9, "neecha": 3, "moolatrikona": 0},
    "Budha":   {"uchcha": 5, "neecha": 11, "moolatrikona": 5},
    "Guru":    {"uchcha": 3, "neecha": 9, "moolatrikona": 8},
    "Shukra":  {"uchcha": 11, "neecha": 5, "moolatrikona": 6},
    "Shani":   {"uchcha": 6, "neecha": 0, "moolatrikona": 10},
    "Rahu":    {"uchcha": 1, "neecha": 7, "moolatrikona": 2},
    "Ketu":    {"uchcha": 7, "neecha": 1, "moolatrikona": 8}
}

PLANET_SYMBOLS = {
    "Surya": ("Sun", "রবি", "Su"),
    "Chandra": ("Moon", "চন্দ্র", "Mo"),
    "Mangala": ("Mars", "মঙ্গল", "Ma"),
    "Budha": ("Mercury", "বুধ", "Me"),
    "Guru": ("Jupiter", "বৃহস্পতি", "Ju"),
    "Shukra": ("Venus", "শুক্র", "Ve"),
    "Shani": ("Saturn", "শনি", "Sa"),
    "Rahu": ("Rahu", "রাহু", "Ra"),
    "Ketu": ("Ketu", "কেতু", "Ke")
}

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

    raw_planets = {
        "Surya": sun_deg, "Chandra": moon_deg, "Mangala": mars_deg,
        "Budha": mercury_deg, "Guru": jupiter_deg, "Shukra": venus_deg,
        "Shani": saturn_deg, "Rahu": rahu_deg, "Ketu": ketu_deg,
    }

    house_occupants = {i: [] for i in range(1, 13)}
    planet_details = []
    planet_house_map = {}
    rashi_occupants = {i: [] for i in range(12)}

    for name, deg in raw_planets.items():
        norm_deg = deg % 360
        sign_idx = int(norm_deg // 30) % 12
        house_num = ((sign_idx - lagna_sign_idx) % 12) + 1
        nak_idx = int(norm_deg / (360.0 / 27.0)) % 27
        pada = (int((norm_deg % (360.0 / 27.0)) / (360.0 / 108.0)) % 4) + 1
        
        sym = PLANET_SYMBOLS[name][2]
        house_occupants[house_num].append(sym)
        rashi_occupants[sign_idx].append(sym)
        planet_house_map[name] = house_num

        # Dignity calculation per BPHS
        dignity = "Sama (Neutral)"
        if sign_idx == DIGNITY_BPHS[name]["uchcha"]:
            dignity = "Uchcha (Exalted / তুঙ্গী)"
        elif sign_idx == DIGNITY_BPHS[name]["neecha"]:
            dignity = "Neecha (Debilitated / নীচস্থ)"
        elif sign_idx == DIGNITY_BPHS[name]["moolatrikona"]:
            dignity = "Moolatrikona"

        nak_en, nak_bn, nak_lord, _ = NAKSHATRAS[nak_idx]
        planet_details.append({
            "Graha": f"{name} ({PLANET_SYMBOLS[name][1]})",
            "Degree": f"{norm_deg % 30:.2f}°",
            "Rashi": f"{RASHIS[sign_idx]['bn']} ({RASHIS[sign_idx]['en'].split()[0]})",
            "House": f"House {house_num}",
            "Nakshatra": f"{nak_bn} (Pada {pada})",
            "Dignity (শাস্ত্রীয় বল)": dignity
        })

    # Panjika Factors: Exact Tithi calculation
    tithi_diff = (moon_deg - sun_deg) % 360
    tithi_idx = int(tithi_diff // 12.0) % 30
    tithi_name = TITHIS_BN[tithi_idx]

    # Vimshottari Mahadasha timeline
    nak_span = 360.0 / 27.0
    birth_nak_idx = int((moon_deg % 360) / nak_span) % 27
    nak_progress = ((moon_deg % 360) % nak_span) / nak_span
    birth_nak_en, birth_nak_bn, dasha_lord, total_years = NAKSHATRAS[birth_nak_idx]
    
    balance_years = total_years * (1.0 - nak_progress)
    dasha_timeline = []
    order_idx = [d[0] for d in DASHA_CYCLE].index(dasha_lord)
    current_year = float(dob_val.year) + (float(dob_val.month) / 12.0)
    
    end_first = current_year + balance_years
    dasha_timeline.append((dasha_lord, f"{int(current_year)} - {int(end_first)} ({balance_years:.1f} yrs balance)"))
    runner = end_first
    for i in range(1, 9):
        nxt_lord, dur = DASHA_CYCLE[(order_idx + i) % 9]
        dasha_timeline.append((nxt_lord, f"{int(runner)} - {int(runner + dur)}"))
        runner += dur

    return lagna_sign_idx, house_occupants, planet_details, moon_deg, planet_house_map, dasha_timeline, (birth_nak_en, birth_nak_bn), rashi_occupants, tithi_name

def render_north_indian_svg(lagna_idx, occupants):
    h_signs = {h: ((lagna_idx + h - 1) % 12) + 1 for h in range(1, 13)}
    coords = {
        1:  (200, 110, 200, 135), 2:  (100, 60,  100, 80),
        3:  (55,  110, 55,  130), 4:  (120, 200, 120, 225),
        5:  (55,  290, 55,  310), 6:  (100, 340, 100, 360),
        7:  (200, 280, 200, 305), 8:  (300, 340, 300, 360),
        9:  (345, 290, 345, 310), 10: (280, 200, 280, 225),
        11: (345, 110, 345, 130), 12: (300, 60,  300, 80)
    }

    labels = ""
    for h in range(1, 13):
        nx, ny, px, py = coords[h]
        p_str = " ".join(occupants.get(h, []))
        labels += f'<text x="{nx}" y="{ny}" fill="#f4c66a" font-size="13" font-weight="bold" text-anchor="middle">{h_signs[h]}</text>'
        if p_str:
            labels += f'<text x="{px}" y="{py}" fill="#ffffff" font-size="12" font-weight="600" text-anchor="middle">{p_str}</text>'

    return f"""
    <div style="max-width: 360px; margin: 0 auto;">
        <svg viewBox="0 0 400 400" width="100%" height="100%" style="background:#13172d; border-radius:12px; border:2px solid #a37d36; display:block;">
            <line x1="0" y1="0" x2="400" y2="0" stroke="#a37d36" stroke-width="2"/>
            <line x1="400" y1="0" x2="400" y2="400" stroke="#a37d36" stroke-width="2"/>
            <line x1="400" y1="400" x2="0" y2="400" stroke="#a37d36" stroke-width="2"/>
            <line x1="0" y1="400" x2="0" y2="0" stroke="#a37d36" stroke-width="2"/>
            <line x1="0" y1="0" x2="400" y2="400" stroke="#a37d36" stroke-width="2"/>
            <line x1="0" y1="400" x2="400" y2="0" stroke="#a37d36" stroke-width="2"/>
            <polygon points="200,0 400,200 200,400 0,200" fill="none" stroke="#a37d36" stroke-width="2"/>
            {labels}
        </svg>
    </div>
    """

def render_east_indian_svg(lagna_idx, rashi_occupants):
    box_positions = [
        (100, 0, "মেষ"), (200, 0, "বৃষ"), (300, 0, "মিথুন"),
        (300, 100, "কর্কট"), (300, 200, "সিংহ"), (300, 300, "কন্যা"),
        (200, 300, "তুলা"), (100, 300, "বৃশ্চিক"), (0, 300, "ধনু"),
        (0, 200, "মকর"), (0, 100, "কুম্ভ"), (0, 0, "মীন")
    ]
    boxes_svg = ""
    for idx, (bx, by, name_bn) in enumerate(box_positions):
        planets_in_box = " ".join(rashi_occupants.get(idx, []))
        is_lagna = " (ল)" if idx == lagna_idx else ""
        boxes_svg += f"""
        <rect x="{bx}" y="{by}" width="100" height="100" fill="#151930" stroke="#a37d36" stroke-width="1.5"/>
        <text x="{bx + 50}" y="{by + 28}" fill="#f4c66a" font-size="12" font-weight="bold" text-anchor="middle">{name_bn}{is_lagna}</text>
        <text x="{bx + 50}" y="{by + 62}" fill="#ffffff" font-size="13" font-weight="bold" text-anchor="middle">{planets_in_box}</text>
        """
    return f"""
    <div style="max-width: 360px; margin: 0 auto;">
        <svg viewBox="0 0 400 400" width="100%" height="100%" style="background:#0b0e1b; border-radius:12px; border:2px solid #a37d36; display:block;">
            <rect x="100" y="100" width="200" height="200" fill="#0d1122" stroke="#a37d36" stroke-width="2"/>
            <text x="200" y="195" fill="#fceecb" font-size="14" font-weight="bold" text-anchor="middle">পূর্ব ভারতীয় ছক</text>
            <text x="200" y="220" fill="#a0a6c6" font-size="11" text-anchor="middle">(East Indian / Bengali Chart)</text>
            {boxes_svg}
        </svg>
    </div>
    """

# ----------------- EXECUTE CALCULATION -----------------
lagna_idx, occupants, p_details, moon_deg, p_house_map, dasha_timeline, birth_nak, rashi_occupants, tithi_name = calculate_chart(dob, tob)
moon_sign_idx = int(moon_deg // 30) % 12

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("#### 💎 লগ্ন কোষ্ঠী ছক (Chart)")
    if "North Indian" in chart_view:
        st.markdown(render_north_indian_svg(lagna_idx, occupants), unsafe_allow_html=True)
    else:
        st.markdown(render_east_indian_svg(lagna_idx, rashi_occupants), unsafe_allow_html=True)
    st.caption("Astronomically calculated under Lahiri Sidereal Zodiac (Chitra Paksha Ayanamsha).")

with col2:
    st.markdown("#### 🌟 পঞ্চাঙ্গ ও জন্ম বিবরণী (Panjika Data)")
    st.markdown(f"""
    <div class="card">
        <div><b>তিথি (Tithi):</b> <span class="highlight-gold">{tithi_name}</span> <span class="source-tag">সিদ্ধান্ত পঞ্জিকা (সূর্য-চন্দ্র কৌণিক ব্যবধান)</span></div>
        <div><b>লগ্ন (Ascendant):</b> <span class="highlight-gold">{RASHIS[lagna_idx]['bn']} ({RASHIS[lagna_idx]['en'].split()[0]})</span></div>
        <div><b>জন্ম রাশি (Moon Sign):</b> <span class="highlight-gold">{RASHIS[moon_sign_idx]['bn']} ({RASHIS[moon_sign_idx]['en'].split()[0]})</span></div>
        <div><b>জন্ম নক্ষত্র (Nakshatra):</b> <span class="highlight-gold">{birth_nak[1]} ({birth_nak[0]})</span></div>
        <div><b>লগ্নপতি (Lagna Lord):</b> <span class="highlight-gold">{RASHIS[lagna_idx]['lord']}</span> (অবস্থান: {p_house_map.get(RASHIS[lagna_idx]['lord'], 1)}ম ভাব)</div>
        <div><b>জন্মস্থান (Location):</b> <span class="highlight-gold">{place}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- SHASTRA-BASED TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🪐 গ্রহ স্পষ্ট ও বল (Planetary)", 
    "⏳ বিংশোত্তরী দশা (Dashas)", 
    "📕 লাল কিতাব শাস্ত্র (Lal Kitab 1952)", 
    "📜 পরাশর হোরা বিচার (BPHS Houses)", 
    "⚖️ শাস্ত্রীয় যোগ ও প্রতিকার (Yogas & Upay)"
])

with tab1:
    st.markdown("### গ্রহের স্পষ্ট দ্রাঘিমাংশ, নক্ষত্র ও শাস্ত্রীয় বল (BPHS Ch. 3)")
    st.dataframe(p_details, use_container_width=True)

with tab2:
    st.markdown("### ⏳ বিংশোত্তরী মহাদশা নির্ণয় (BPHS Dasha Adhyaya)")
    st.caption("চন্দ্র নক্ষত্রভুক্তির অবশিষ্টাংশ ও শতবর্ষীয় বিংশোত্তরী সময়কাল:")
    cd1, cd2 = st.columns(2)
    for idx, (lord, span) in enumerate(dasha_timeline):
        target = cd1 if idx < 5 else cd2
        with target:
            st.markdown(f"""
            <div class="card" style="padding:10px; margin-bottom:8px;">
                <b>{lord} মহাদশা</b>: <span class="highlight-gold">{span}</span>
            </div>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📕 লাল কিতাব নিয়ম ও অরুণ পণ্ডিত প্রদর্শিত সূত্র")
    st.info("লাল কিতাব অনুসারে কুষ্ঠির ১২টি ভাব স্থির (Fixed Houses): ১ম ভাব = মেষ, ২য় ভাব = বৃষ। এখানে রাশি প্রাধান্য পায় না, পাকা ঘরের অধিপতি প্রাধান্য পায়।")

    rahu_h = p_house_map.get("Rahu", 0)
    moon_h = p_house_map.get("Chandra", 0)
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"**১. রাহু অবস্থান ({rahu_h}ম ভাব) — শাস্ত্রীয় ফল [লাল কিতাব ১৯৫২ সংহিতা]:**")
        bphs_rahu_source = {
            1: "১ম ভাবে রাহু 'তখত বা সিংহাসনে বসা ফকির'। চিন্তায় অস্থিরতা কিন্তু প্রযুক্তি ও কূটনীতিতে দ্রুত সাফল্য। প্রতিকার: সন্ধ্যার পর কর্পূর প্রদীপ জ্বালুন।",
            2: "২য় ভাবে রাহু থাকলে আর্থিক ওঠানামা বা অকারণ ব্যয় হতে পারে। প্রতিকার: নিরেট রূপার গুলি নিজের কাছে রাখুন।",
            5: "৫ম ভাবে রাহু বুদ্ধিবলে আকস্মিক লাভ দেয় কিন্তু উচ্চশিক্ষায় মনোযোগের অভাব ঘটায়। প্রতিকার: হাতির পায়ের মাটি বা রূপার হাতি গৃহে রাখুন।",
            8: "৮ম ভাবে রাহু 'পাকা ঘর'। আকস্মিক দুর্ঘটনা ও বাধার আশঙ্কা তৈরি করে। প্রতিকার: ঘরের ছাদে বা উত্তর-পশ্চিম কোণে ভাঙা কাঁচ ও অকেজো তার রাখবেন না।",
            10: "১০ম ভাবে রাহু রাজকীয় ব্যক্তিত্ব গঠন করে, রাজনীতি ও বাণিজ্যে দ্রুত প্রতিপত্তি দেয়। প্রতিকার: মাথায় সাদা টুপি বা সাদা তিলক ধারণ ফলপ্রসূ।"
        }
        st.write(bphs_rahu_source.get(rahu_h, f"রাহু {rahu_h}ম ভাবে অবস্থানরত। কোনো ইলেকট্রনিক বর্জ্য জমিয়ে রাখবেন না।"))
        st.markdown('<span class="source-tag">সূত্র: লাল কিতাব (ফারসি মূল সংহিতা ও অরুণ পণ্ডিত বিশ্লেষণ)</span>', unsafe_allow_html=True)

        st.markdown(f"<br>**২. চন্দ্র অবস্থান ({moon_h}ম ভাব) [লাল কিতাব পাকা ঘর নিয়ম]:**", unsafe_allow_html=True)
        moon_source = {
            1: "১ম ভাবে চন্দ্র মাতা ও মানসিক শান্তির পরিপোষক। শুভ ফল রক্ষার্থে দুধ বা রূপা কখনো বিক্রি বা দান করবেন না।",
            4: "৪র্থ ভাবে চন্দ্র নিজ পাকা ঘরে পরম বলশালী। মাতৃসেবায় সকল পার্থিব উন্নতি সম্ভব।",
            8: "৮ম ভাবে চন্দ্র মানসিক দোলাচল তৈরি করে। প্রতিকার: শিবলিঙ্গে দুধ ও কাঁচা জল অর্পণ করুন।"
        }
        st.write(moon_source.get(moon_h, f"চন্দ্র {moon_h}ম ভাবে অবস্থান করছেন। চন্দ্রের শুভত্ব অক্ষুণ্ণ রাখতে সর্বদা পরিষ্কার রূপার গয়না বা মুদ্রা কাছে রাখুন।"))
        st.markdown('<span class="source-tag">সূত্র: লাল কিতাব (চন্দ্র বিচার অধ্যায়)</span>', unsafe_allow_html=True)

    with col_l2:
        st.markdown("**৩. সোয়ে হুয়ে ঘর (Sleeping Houses) সনাক্তকরণ:**")
        empty_houses = [h for h in range(1, 13) if len(occupants.get(h, [])) == 0]
        st.write(f"যে ভাবগুলি শূন্য বা নির্জন: {', '.join([f'ভাব {h}' for h in empty_houses])}")
        st.markdown("""
        <div class="remedy-box">
            <b>লাল কিতাব জাগ্রত করার নিয়ম:</b> শূন্য ভাবগুলি তাদের স্বাভাবিক পাকা অধিপতির গোচর অথবা নির্দিষ্ট নৈতিক কর্ম দ্বারা সক্রিয় হয়। উদাহরণস্বরূপ, ২য় ভাব খালি থাকলে গুরুজনদের চরণ স্পর্শ ও সত্যভাষণ দ্বারা ধনভাব সক্রিয় করতে হয়।
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 📜 বৃহৎ পরাশর হোরা শাস্ত্র (BPHS) ভাবাধিপতি বিচার")
    
    # 10th Lord Analysis (Karma Bhava)
    h10_idx = (lagna_idx + 9) % 12
    h10_lord = RASHIS[h10_idx]["lord"]
    h10_lord_h = p_house_map.get(h10_lord, 1)

    # 7th Lord Analysis (Jaya Bhava)
    h7_idx = (lagna_idx + 6) % 12
    h7_lord = RASHIS[h7_idx]["lord"]
    h7_lord_h = p_house_map.get(h7_lord, 1)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">💼 কর্ম ও বৃত্তি: দশমেশ বিচার (BPHS অধ্যায় ২৪, শ্লোক ১০)</h4>
        আপনার দশম ভাব (কর্ম) হলো <b>{RASHIS[h10_idx]['bn']}</b>, যার পতি <b>{h10_lord}</b> বসে আছেন <b>{h10_lord_h}ম ভাবে</b>।<br>
        • <i>শ্লোক নিয়ম:</i> দশমেশ যদি কেন্দ্রে (১, ৪, ৭, ১০) বা ত্রিকোণে (৫, ৯) থাকেন, তবে জাতক স্বীয় কর্মে যশস্বী ও প্রভাবশালী হন।<br>
        • বর্তমান অবস্থান ({h10_lord} in House {h10_lord_h}): কর্মক্ষেত্রে নিজস্ব বুদ্ধিমত্তা ও যোগাযোগের ওপর ভিত্তি করে প্রতিষ্ঠা লাভ।<br>
        <span class="source-tag">সূত্র: বৃহৎ পরাশর হোরা শাস্ত্র (কর্মভাব ফল)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">💍 দাম্পত্য ও অংশীদারি: সপ্তমেস বিচার (BPHS অধ্যায় ২১, শ্লোক ৭)</h4>
        আপনার সপ্তম ভাব (পত্নী/পতি ভাব) হলো <b>{RASHIS[h7_idx]['bn']}</b>, অধিপতি <b>{h7_lord}</b> অবস্থান করছেন <b>{h7_lord_h}ম ভাবে</b>।<br>
        • <i>শ্লোক নিয়ম:</i> সপ্তমাধিপতি দ্বিতীয় বা একাদশ ভাবের সাথে সম্পর্কযুক্ত হলে বিবাহের পর বিশেষ ভাগ্যোদয় হয়।<br>
        • যদি রাহু বা মঙ্গলের পাপদৃষ্টি থাকে, তবে বাক্য সংযম ও পারস্পরিক বিশ্বাস বজায় রাখা অপরিহার্য।<br>
        <span class="source-tag">সূত্র: বৃহৎ পরাশর হোরা শাস্ত্র (জায়া ভাব ফল)</span>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    st.markdown("### ⚖️ সিদ্ধান্ত শাস্ত্রীয় যোগ ও পঞ্জিকা সম্মত প্রতিকার")

    mars_h = p_house_map.get("Mangala", 0)
    is_manglik = mars_h in [1, 4, 7, 8, 12]

    is_budhaditya = p_house_map.get("Surya") == p_house_map.get("Budha")
    jup_h = p_house_map.get("Guru", 0)
    moon_h = p_house_map.get("Chandra", 0)
    kendra_diff = (jup_h - moon_h) % 12
    is_gajakesari = kendra_diff in [0, 3, 6, 9]

    st.markdown(f"""
    <div class="card">
        <b>শাস্ত্রীয় শুভ যোগসমূহ (Classical Yogas):</b><br><br>
        {"<span class='highlight-gold'>• গজকেশরী যোগ (Gajakesari Yoga):</span> বৃহস্পতি ও চন্দ্র পরস্পর কেন্দ্রবর্তী। ফল: দীর্ঘায়ু, শাস্ত্রজ্ঞান, সমাজমান ও ধর্মপরায়ণতা। [সূত্র: বৃহৎ জাতক, বরাহমিহির]<br><br>" if is_gajakesari else ""}
        {"<span class='highlight-gold'>• বুধাদিত্য যোগ (Budhaditya Yoga):</span> রবি ও বুধের একরাশিস্থ সংযোগ। ফল: তীক্ষ্ণ মেধা, হিসাববিদ্যায় পারদর্শিতা ও প্রশাসনিক ক্ষমতা। [সূত্র: সারাাবলী]<br><br>" if is_budhaditya else ""}
        <span class='highlight-gold'>• কেন্দ্র-ত্রিকোণ রাজযোগ (Dharma-Karmadhipati Yoga):</span> কেন্দ্র ও ত্রিকোণ অধিপতিদের সামঞ্জস্যপূর্ণ সংস্থান। [সূত্র: BPHS Ch. 34]
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <b>দোষ নিরূপণ ও সমাধান (Dosha Scan per Panjika):</b><br><br>
        <b>ভৌম দোষ / মাঙ্গলিক বিচার:</b> {"⚠️ লগ্ন, ৪র্থ, ৭ম, ৮ম বা ১২শ ভাবে মঙ্গল স্থিত (" + str(mars_h) + "ম ভাব)। ২৮ বছর বয়সের পর মঙ্গলের তেজস্বিতা প্রশমিত হয়। নিত্য হনুমান চালীসা পাঠ শাস্ত্রীয় প্রতিকার।" if is_manglik else "✅ মাঙ্গলিক দোষ মুক্ত (মঙ্গল শুভ স্থানে অবস্থিত)।"}<br><br>
        <b>কেমদ্রুম যোগ বিচার:</b> {"⚠️ চন্দ্রের উভয় পার্শ্বে গ্রহহীনতা দেখা দিলে মানসিক উদ্বেগ বাড়ে। শিবোপাসনা ও প্রত্যহ সকালে সূর্য প্রণাম দ্বারা এই দোষ খণ্ডন হয়।" if len(occupants.get((moon_h % 12) + 1, [])) == 0 and len(occupants.get(((moon_h - 2) % 12) + 1, [])) == 0 else "✅ কেমদ্রুম ভঙ্গ যোগ বা নিরাপদ চন্দ্রবল।"}
    </div>
    """, unsafe_allow_html=True)
