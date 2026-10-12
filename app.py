import streamlit as st
import datetime
import math

st.set_page_config(page_title="Kundli AI | শাস্ত্রীয় কোষ্ঠী বিচার", page_icon="🕉️", layout="wide")

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
    .graha-card {
        background: #14182e;
        border-left: 5px solid #f4c66a;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        border-top: 1px solid #282e50;
        border-right: 1px solid #282e50;
        border-bottom: 1px solid #282e50;
    }
    .highlight-gold {
        color: #f4c66a;
        font-weight: 700;
    }
    .remedy-box {
        background: #1b172a;
        border: 1px dashed #f4a261;
        padding: 12px 14px;
        border-radius: 6px;
        margin: 10px 0;
    }
    .ritual-box {
        background: #112233;
        border-left: 4px solid #2a9d8f;
        padding: 10px 12px;
        border-radius: 4px;
        margin-top: 8px;
    }
    .badge {
        display: inline-block;
        background: #232946;
        color: #eebbc3;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🕉️ Kundli AI — শাস্ত্রীয় কোষ্ঠী ও প্রতিকার বিচার</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Classic Vedic Panchang, House Placements, Graha Phal & Traditional Remedial Rituals</div>', unsafe_allow_html=True)

# ----------------- SIDEBAR INPUTS -----------------
with st.sidebar:
    st.markdown("### 📜 জন্ম তথ্য (Birth Details)")
    dob = st.date_input("Date of Birth / জন্মতারিখ", datetime.date(2000, 1, 1), min_value=datetime.date(1920, 1, 1))
    tob = st.time_input("Birth Time / সময়", datetime.time(12, 0))
    place = st.text_input("Birthplace / জন্মস্থান", "Kolkata, West Bengal, India")
    chart_view = st.selectbox("Chart Style / ছকের ধরন", ["North Indian (উত্তর ভারতীয় ছক)", "East Indian (পূর্ব ভারতীয়/বাঙালি ছক)"])
    btn_calc = st.button("🔮 কোষ্ঠী বিচার ও প্রতিকার দেখুন", use_container_width=True)

# ----------------- ASTROLOGICAL MATRICES -----------------
RASHIS = [
    {"en": "Aries", "bn": "মেষ", "lord": "Mangala", "element": "Fire (অগ্নি)", "nature": "উদ্যমী ও আত্মবিশ্বাসী"},
    {"en": "Taurus", "bn": "বৃষ", "lord": "Shukra", "element": "Earth (পৃথ্বী)", "nature": "ধৈর্যশীল ও সৌন্দর্যপ্রিয়"},
    {"en": "Gemini", "bn": "মিথুন", "lord": "Budha", "element": "Air (বায়ু)", "nature": "বুদ্ধিমান ও যোগাযোগে পটু"},
    {"en": "Cancer", "bn": "কর্কট", "lord": "Chandra", "element": "Water (জল)", "nature": "সংবেদনশীল ও স্নেহময়"},
    {"en": "Leo", "bn": "সিংহ", "lord": "Surya", "element": "Fire (অগ্নি)", "nature": "নেতৃত্বপ্রিয় ও তেজস্বী"},
    {"en": "Virgo", "bn": "কন্যা", "lord": "Budha", "element": "Earth (পৃথ্বী)", "nature": "বিশ্লেষণাত্মক ও হিসাবি"},
    {"en": "Libra", "bn": "তুলা", "lord": "Shukra", "element": "Air (বায়ু)", "nature": "ন্যায়পরায়ণ ও ভারসাম্যপ্রিয়"},
    {"en": "Scorpio", "bn": "বৃশ্চিক", "lord": "Mangala", "element": "Water (জল)", "nature": "দৃঢ়প্রতিজ্ঞ ও রহস্যসন্ধানী"},
    {"en": "Sagittarius", "bn": "ধনু", "lord": "Guru", "element": "Fire (অগ্নি)", "nature": "ধার্মিক ও উচ্চাকাঙ্ক্ষী"},
    {"en": "Capricorn", "bn": "মকর", "lord": "Shani", "element": "Earth (পৃথ্বী)", "nature": "কঠোর পরিশ্রমী ও শৃঙ্খলাপরায়ণ"},
    {"en": "Aquarius", "bn": "কুম্ভ", "lord": "Shani", "element": "Air (বায়ু)", "nature": "মানবদরদী ও উদ্ভাবনী"},
    {"en": "Pisces", "bn": "মীন", "lord": "Guru", "element": "Water (জল)", "nature": "আধ্যাত্মিক, দয়ালু ও দূরদর্শী"}
]

NAKSHATRAS = [
    ("Ashwini", "অশ্বিনী", "Ketu", 7, "দ্রুত কাজ সম্পন্ন করার ক্ষমতা ও উদ্যম"),
    ("Bharani", "ভরণী", "Shukra", 20, "সৃজনশীলতা, সততা ও দায়িত্বশীল মনোভাব"),
    ("Krittika", "কৃত্তিকা", "Surya", 6, "স্পষ্টবাদিতা, একাগ্রতা ও লক্ষ্যভেদ ক্ষমতা"),
    ("Rohini", "রোহিণী", "Chandra", 10, "আকর্ষণীয় ব্যক্তিত্ব, শিল্পানুরাগ ও মাধুর্য"),
    ("Mrigashira", "মৃগশিরা", "Mangala", 7, "অনুসন্ধানী মন, কৌতূহল ও ভ্রমণপ্রিয়তা"),
    ("Ardra", "আর্দ্রা", "Rahu", 18, "তীক্ষ্ণ বুদ্ধি ও প্রতিকূলতা জয়ের সামর্থ্য"),
    ("Punarvasu", "পুনর্বসু", "Guru", 16, "সহনশীলতা, আশাবাদ ও আত্মশুদ্ধি"),
    ("Pushya", "পুষ্যা", "Shani", 19, "সেবামূলক মানসিকতা ও গভীর দায়িত্ববোধ"),
    ("Ashlesha", "অশ্লেষা", "Budha", 17, "কূটনৈতিক মেধা, তীক্ষ্ণ বিচার ও সতর্কতা"),
    ("Magha", "মঘা", "Ketu", 7, "পিতৃকুল বা পূর্বপুরুষের আশীর্বাদ ও ব্যক্তিত্বের প্রভাব"),
    ("Purva Phalguni", "পূর্ব ফল্গুনী", "Shukra", 20, "সৌখিনতা, সামাজিক জনপ্রিয়তা ও স্নেহশীলতা"),
    ("Uttara Phalguni", "উত্তর ফল্গুনী", "Surya", 6, "দয়ালু স্বভাব, নীতিপরায়ণতা ও বিশ্বস্ততা"),
    ("Hasta", "হস্তা", "Chandra", 10, "হস্তশিল্প বা প্রযুক্তিবিদ্যায় দক্ষতা ও চতুরতা"),
    ("Chitra", "চিত্রা", "Mangala", 7, "নকশা, বিন্যাস ও মৌলিক পরিকল্পনায় নৈপুণ্য"),
    ("Swati", "স্বাতী", "Rahu", 18, "স্বাধীনচেতা ভাব, ব্যবসায়িক দূরদৃষ্টি ও স্বাবলম্বন"),
    ("Vishakha", "বিশাখা", "Guru", 16, "লক্ষ্যে পৌঁছানোর অদম্য সংকল্প ও তেজ"),
    ("Anuradha", "অনুরাধা", "Shani", 19, "বন্ধুত্বভাব, সংগঠন ক্ষমতা ও ধৈর্য"),
    ("Jyeshtha", "জ্যেষ্ঠা", "Budha", 17, "নেতৃত্বের অহংকার নিয়ন্ত্রণ ও দ্রুত সিদ্ধান্ত গ্রহণ"),
    ("Mula", "মূলা", "Ketu", 7, "মূল সত্য অনুসন্ধানের গভীর ইচ্ছা ও দার্শনিক বোধ"),
    ("Purva Ashadha", "পূর্বাষাঢ়া", "Shukra", 20, "দৃঢ় মনোবল, প্রত্যুৎপন্নমতিত্ব ও সুবক্তা"),
    ("Uttara Ashadha", "উত্তরাষাঢ়া", "Surya", 6, "নম্রতা, দীর্ঘস্থায়ী সাফল্য ও সম্মান"),
    ("Shravana", "শ্রবণা", "Chandra", 10, "শ্রবণক্ষমতা, জ্ঞান আহরণ ও শাস্ত্রচর্চা"),
    ("Dhanishtha", "ধনিষ্ঠা", "Mangala", 7, "সঙ্গীত, ছন্দ ও সংগঠনবিদ্যায় পারদর্শিতা"),
    ("Shatabhisha", "শতভিষা", "Rahu", 18, "গূঢ় জ্ঞান, চিকিৎসা বা গবেষণায় সাফল্য"),
    ("Purva Bhadrapada", "পূর্বভাদ্রপদ", "Guru", 16, "সত্যনিষ্ঠা ও ত্যাগের মাধ্যমে উন্নতি"),
    ("Uttara Bhadrapada", "উত্তরভাদ্রপদ", "Shani", 19, "শান্ত স্বভাব, দূরদৃষ্টি ও স্থিতপ্রজ্ঞতা"),
    ("Revati", "রেবতী", "Budha", 17, "সহানুভূতি, দয়া ও আর্থিক সুরক্ষা")
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

DIGNITY_BPHS = {
    "Surya":   {"uchcha": 0, "neecha": 6, "own": [4]},
    "Chandra": {"uchcha": 1, "neecha": 7, "own": [3]},
    "Mangala": {"uchcha": 9, "neecha": 3, "own": [0, 7]},
    "Budha":   {"uchcha": 5, "neecha": 11, "own": [2, 5]},
    "Guru":    {"uchcha": 3, "neecha": 9, "own": [8, 11]},
    "Shukra":  {"uchcha": 11, "neecha": 5, "own": [1, 6]},
    "Shani":   {"uchcha": 6, "neecha": 0, "own": [9, 10]},
    "Rahu":    {"uchcha": 1, "neecha": 7, "own": [10]},
    "Ketu":    {"uchcha": 7, "neecha": 1, "own": [8]}
}

PLANET_NAMES = {
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

# ----------------- CALCULATION ENGINE -----------------
def calculate_astrology(dob_val, tob_val):
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
        
        sym = PLANET_NAMES[name][2]
        house_occupants[house_num].append(sym)
        rashi_occupants[sign_idx].append(sym)
        planet_house_map[name] = house_num

        dignity = "Sama (সাধারণ অবস্থান)"
        if sign_idx == DIGNITY_BPHS[name]["uchcha"]:
            dignity = "Uchcha (তুঙ্গী - পরম শুভ বল)"
        elif sign_idx == DIGNITY_BPHS[name]["neecha"]:
            dignity = "Neecha (নীচস্থ - দুর্বল বল)"
        elif sign_idx in DIGNITY_BPHS[name]["own"]:
            dignity = "Swa-kshetra (স্বক্ষেত্র - নিজস্ব বল)"

        nak_en, nak_bn, nak_lord, _, _ = NAKSHATRAS[nak_idx]
        planet_details.append({
            "Graha": f"{PLANET_NAMES[name][0]} ({PLANET_NAMES[name][1]})",
            "Degree": f"{norm_deg % 30:.2f}°",
            "Rashi": f"{RASHIS[sign_idx]['bn']} ({RASHIS[sign_idx]['en']})",
            "House": f"House {house_num}",
            "Nakshatra": f"{nak_bn} (পদ {pada})",
            "Dignity": dignity
        })

    # Tithi Calculation (Panjika rule: 12 degrees per Tithi)
    tithi_diff = (moon_deg - sun_deg) % 360
    tithi_idx = int(tithi_diff // 12.0) % 30
    tithi_name = TITHIS_BN[tithi_idx]

    # Vimshottari Mahadasha
    nak_span = 360.0 / 27.0
    birth_nak_idx = int((moon_deg % 360) / nak_span) % 27
    nak_progress = ((moon_deg % 360) % nak_span) / nak_span
    birth_nak_en, birth_nak_bn, dasha_lord, total_years, nak_trait = NAKSHATRAS[birth_nak_idx]
    
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

    return lagna_sign_idx, house_occupants, planet_details, moon_deg, planet_house_map, dasha_timeline, (birth_nak_en, birth_nak_bn, nak_trait), rashi_occupants, tithi_name

# ----------------- SVG CHARTS -----------------
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

# ----------------- EXECUTE LOGIC -----------------
lagna_idx, occupants, p_details, moon_deg, p_house_map, dasha_timeline, birth_nak, rashi_occupants, tithi_name = calculate_astrology(dob, tob)
moon_sign_idx = int(moon_deg // 30) % 12

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("#### 💎 জন্ম কোষ্ঠী চক্র (Chart)")
    if "North Indian" in chart_view:
        st.markdown(render_north_indian_svg(lagna_idx, occupants), unsafe_allow_html=True)
    else:
        st.markdown(render_east_indian_svg(lagna_idx, rashi_occupants), unsafe_allow_html=True)
    st.caption("Lahiri Sidereal Zodiac (Chitra Paksha Ayanamsha) — সিদ্ধান্ত পঞ্জিকা সম্মত গণনা")

with col2:
    st.markdown("#### 🌟 পঞ্চাঙ্গ পরিচয় ও মৌলিক শক্তি (Identity & Strengths)")
    st.markdown(f"""
    <div class="card">
        <div><b>লগ্ন (Lagna):</b> <span class="highlight-gold">{RASHIS[lagna_idx]['bn']} ({RASHIS[lagna_idx]['en']})</span> — <i>তত্ত্ব: {RASHIS[lagna_idx]['element']}</i></div>
        <div><b>জন্ম রাশি (Moon Sign):</b> <span class="highlight-gold">{RASHIS[moon_sign_idx]['bn']} ({RASHIS[moon_sign_idx]['en']})</span></div>
        <div><b>জন্ম নক্ষত্র (Nakshatra):</b> <span class="highlight-gold">{birth_nak[1]} ({birth_nak[0]})</span></div>
        <div><b>তিথি (Panchang Tithi):</b> <span class="highlight-gold">{tithi_name}</span></div>
        <div><b>লগ্নপতি (Ascendant Lord):</b> <span class="highlight-gold">{RASHIS[lagna_idx]['lord']}</span> (অবস্থান: {p_house_map.get(RASHIS[lagna_idx]['lord'], 1)}ম ভাব)</div>
        <div><b>জন্মস্থান (Location):</b> <span class="highlight-gold">{place}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌟 আপনার শক্তি ও প্রকৃতি (Your Strengths)",
    "🪐 ৯টি গ্রহের ফল ও প্রতিকার (Graha Phal & Upay)",
    "📅 সাপ্তাহিক প্রতিকার সূচি (Weekly Action Plan)",
    "📊 গ্রহের স্পষ্ট ছক ও মহাদশা (Dasha Table)",
    "⚖️ রাজযোগ ও দোষ বিচার (Yogas & Doshas)"
])

with tab1:
    st.markdown("### 🌟 শাস্ত্র অনুসারে আপনার জন্মগত শক্তি ও স্বভাব (Core Strengths)")
    
    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">১. লগ্ন শক্তি (Lagna Personality & Physical Strength)</h4>
        আপনার লগ্ন হলো <b>{RASHIS[lagna_idx]['bn']} ({RASHIS[lagna_idx]['en']})</b>। এর অধিপতি গ্রহ <b>{RASHIS[lagna_idx]['lord']}</b>।<br>
        • <b>সহজ ব্যাখ্যা (Simple Explanation):</b> আপনার স্বভাবের মূল ভিত্তি হলো <i>{RASHIS[lagna_idx]['nature']}</i>। {RASHIS[lagna_idx]['element']} হওয়ার কারণে আপনার সিদ্ধান্ত নেওয়ার ক্ষমতা এবং দূরদর্শিতা প্রবল।<br>
        • <b>পরামর্শ:</b> লগ্নপতি বলবান রাখতে নিজের শারীরিক স্বাস্থ্য ও নীতিপরায়ণতা বজায় রাখুন।
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">২. মন ও বুদ্ধির শক্তি: চন্দ্র রাশি ও নক্ষত্র (Mental Strengths)</h4>
        আপনার রাশি হলো <b>{RASHIS[moon_sign_idx]['bn']}</b> এবং নক্ষত্র হলো <b>{birth_nak[1]}</b>।<br>
        • <b>সহজ ব্যাখ্যা (Simple Explanation):</b> শাস্ত্র মতে আপনার মনের প্রকৃতি: <i>{birth_nak[2]}</i>।<br>
        • <b>কর্মদক্ষতা:</b> চন্দ্র ও নক্ষত্র শক্তির কারণে আপনি যেকোনো কাজে সূক্ষ্ম বিচার ও সামাজিক যোগাযোগ কাজে লাগিয়ে সাফল্য পেতে পারেন।
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">৩. তিথি প্রভাব (Panchang Tithi Influence)</h4>
        আপনার জন্মতিথি <b>{tithi_name}</b>।<br>
        • তিথির শুভত্ব বৃদ্ধি করতে নিয়মিত গুরুজনদের প্রতি ভক্তি এবং শুদ্ধাচার বজায় রাখা উচিত।
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🪐 ৯টি গ্রহের অবস্থান, শুভ-অশুভ ফল ও শাস্ত্রীয় প্রতিকার")
    st.caption("প্রতিটি গ্রহ কোন ঘরে আছে, তার ফলে কী ঘটবে, কোনো খারাপ প্রভাব থাকলে কীভাবে তা দূর করবেন এবং কী নিয়ম বা পূজা করবেন:")

    # Detailed knowledge map per Graha and House
    GRAHA_DATA = {
        "Surya": {
            "name_bn": "সূর্য (Sun / রবি)",
            "signifies": "আত্মা, পিতা, কর্মক্ষেত্রে সম্মান, সরকারি কাজ ও জীবনীশক্তি",
            10: {
                "good": "১০ম ভাবে সূর্য পরম দিকবল (Digbala) লাভ করে। কর্মক্ষেত্রে নেতৃত্ব, প্রশাসনিক সম্মান, কর্মে উচ্চপদ ও পিতার আশীর্বাদ লাভ হয়। (High leadership, career recognition & respect from superiors).",
                "bad": "অতিরিক্ত অহংকার বা ক্রোধের কারণে উর্ধ্বতন কর্তৃপক্ষের সাথে মতবিরোধ হতে পারে। (Ego clashes with authorities if uncontrolled).",
                "remedy": "প্রতিদিন সকালে পিতাকে সম্মান করুন। অহংকার ত্যাগ করে সততার সাথে কাজ করুন। (Respect father daily, maintain humility).",
                "ritual": "প্রত্যহ সকালে স্নানের পর তামার পাত্রে জল নিয়ে পূর্বদিকে মুখ করে সূর্যকে অর্ঘ্য দিন এবং 'ওঁ সূর্যায় নমঃ' জপ করুন। (Offer water from copper vessel to rising Sun daily)."
            },
            "default": {
                "good": "আত্মবিশ্বাস ও তেজ বৃদ্ধি করে। আত্মমর্যাদা বজায় থাকে। (Gives self-confidence and vitality).",
                "bad": "মাথা গরম হওয়া বা চোখের সমস্যা দেখা দিতে পারে। (Tendency of short temper or eye strain).",
                "remedy": "পিতৃস্থানীয় ব্যক্তিদের সেবা করুন। (Honor elder father-figures).",
                "ritual": "সকালে আদিত্য হৃদয় স্তোত্র বা গায়ত্রী মন্ত্র পাঠ শুভ। (Recite Gayatri Mantra daily)."
            }
        },
        "Chandra": {
            "name_bn": "চন্দ্র (Moon / সোম)",
            "signifies": "মন, মানসিক শান্তি, মাতা, কল্পনাশক্তি ও তরল পদার্থ",
            8: {
                "good": "৮ম ভাবে চন্দ্র গভীর অন্তর্দৃষ্টি, রহস্যবিদ্যা, গবেষণা ও সূক্ষ্ম বিশ্লেষণী মেধা দান করে। (Deep intuition, occult interests & research ability).",
                "bad": "মানসিক দোলাচল, অতিরিক্ত দুশ্চিন্তা, ঘুমের অনিয়ম ও অজানা ভয় কাজ করতে পারে। (Mental anxiety, overthinking & emotional swings).",
                "remedy": "মাথা ঠান্ডা রাখুন। রূপার জিনিস ব্যবহার করুন এবং মায়ের সেবা করুন। রূপা কখনো দান বা বিক্রি করবেন না। (Keep silver, respect mother, avoid selling family silver).",
                "ritual": "প্রতি সোমবার শিবলিঙ্গে কাঁচা দুধ ও জল অর্পণ করুন। রাতে রূপার পাত্রে জল রেখে সকালে তা পান করুন। (Offer milk/water to Shivling on Mondays; drink water from silver vessel)."
            },
            "default": {
                "good": "সংবেদনশীল ও সৃষ্টিশীল মন তৈরি করে। (Creative, empathetic mind).",
                "bad": "মেজাজের দ্রুত পরিবর্তন বা সর্দিকাশির প্রবণতা। (Mood fluctuations).",
                "remedy": "পরিবারের মহিলাদের সন্তুষ্ট রাখুন। (Keep maternal figures happy).",
                "ritual": "সোমবার শিবপূজা এবং জল অপচয় রোধ করা পরম প্রতিকার। (Worship Lord Shiva on Mondays)."
            }
        },
        "Mangala": {
            "name_bn": "মঙ্গল (Mars / ভৌম)",
            "signifies": "সাহস, পরাক্রম, ভূমি, রক্ত ও ভ্রাতৃত্ব",
            1: {
                "good": "১ম ভাবে মঙ্গল অসীম সাহস, নির্ভীক চরিত্র, দ্রুত সিদ্ধান্ত নেওয়ার ক্ষমতা ও তেজস্বী শরীর প্রদান করে। (Boldness, energy, quick execution).",
                "bad": "লগ্নে মঙ্গলের কারণে মাঙ্গলিক প্রভাব তৈরি হয়। আকস্মিক রাগ, চোট-আঘাতের সম্ভাবনা বা কঠোর কথার প্রবণতা থাকে। (Lagna Manglik: anger, risk of minor cuts/burns, harsh speech).",
                "remedy": "রাগ নিয়ন্ত্রণ করুন। ভাই ও সহকর্মীদের সাথে সুসম্পর্ক রাখুন। (Control impulsive anger, be supportive of brothers).",
                "ritual": "প্রতি মঙ্গলবার হনুমান চালীসা পাঠ করুন। মঙ্গলবার মিষ্টি বা গুড় দান করুন। (Recite Hanuman Chalisa on Tuesdays; donate sweets/jaggery)."
            },
            "default": {
                "good": "কর্মোদ্যম ও বাধাবিপত্তি অতিক্রম করার মনোবল দেয়। (High courage to fight obstacles).",
                "bad": "অস্থিরতা বা বিরোধের আশঙ্কা। (Restlessness or conflicts).",
                "remedy": "মিষ্টি কথা বলুন এবং কাউকে প্রতারণা করবেন না। (Speak sweetly).",
                "ritual": "মঙ্গলবার লাল রঙের মিষ্টি দান ও সুন্দরকাণ্ড পাঠ শুভ। (Donate red sweets on Tuesday)."
            }
        },
        "Budha": {
            "name_bn": "বুধ (Mercury / সৌমা)",
            "signifies": "বুদ্ধি, ব্যবসা, হিসাব, বাক্য ও যোগাযোগ দক্ষতা",
            10: {
                "good": "১০ম ভাবে বুধ কর্মক্ষেত্রে বুদ্ধিমত্তা, ব্যবসায়িক দূরদৃষ্টি, হিসাবরক্ষণ ও দক্ষ যোগাযোগের মাধ্যমে খ্যাতি আনে। (Sharp business mind, accountancy, consultancy success).",
                "bad": "একক সিদ্ধান্তে স্থির না থাকতে পারলে কর্মে ঘনঘন পরিবর্তন হতে পারে। (Distraction from pursuing multiple goals at once).",
                "remedy": "ছোট বোন বা কন্যা সন্তানদের স্নেহ ও উপহার দিন। মিথ্যা কথা পরিহার করুন। (Respect sisters and young girls; avoid dishonesty).",
                "ritual": "বুধবার গরুকে সবুজ ঘাস বা পালং শাক খাওয়ান। বিষ্ণু সহস্রনাম পাঠ অতি শুভ। (Feed green grass to cows on Wednesdays)."
            },
            "default": {
                "good": "তীক্ষ্ণ স্মৃতিশক্তি ও বাচনিক নৈপুণ্য। (Good speech & analytical power).",
                "bad": "সিদ্ধান্তহীনতা বা নার্ভের দুর্বলতা। (Indecision).",
                "remedy": "গাছপালা পরিচর্যা করুন। (Plant green trees).",
                "ritual": "বুধবার তুলসী মঞ্চে জল নিবেদন করুন। (Water Tulsi plant on Wednesdays)."
            }
        },
        "Guru": {
            "name_bn": "বৃহস্পতি (Jupiter / দেবগুরু)",
            "signifies": "জ্ঞান, ধর্ম, শিক্ষকতা, সন্তান ও দৈব কৃপা",
            2: {
                "good": "২য় ভাবে বৃহস্পতি সুবক্তা করে তোলে। সৎ পথে অর্থ উপার্জন, পরিবারে মর্যাদা ও সত্যভাষণের ফল দেয়। (Knowledgeable speech, honest wealth creation, family respect).",
                "bad": "কারো প্রতি অতিরিক্ত অন্ধবিশ্বাস রাখলে আর্থিক ক্ষতি হতে পারে। (Blind faith causing financial oversights).",
                "remedy": "কখনো গুরুজন বা শিক্ষকদের অবমাননা করবেন না। বিনামূল্যে কিছু গ্রহণ করবেন না। (Respect teachers; never accept things for free).",
                "ritual": "প্রত্যহ সকালে কপালে কেশর বা হলুদ-চন্দনের তিলক লাগান। বৃহস্পতিবার ছোলার ডাল বা হলুদ ফল দান করুন। (Apply Kesar/Haldi tilak daily; donate yellow items on Thursday)."
            },
            "default": {
                "good": "ন্যায়পরায়ণতা ও সার্বিক শুভত্ব বজায় রাখে। (Brings wisdom & moral balance).",
                "bad": "অতি উদারতা বা অলসতা। (Excessive optimism).",
                "remedy": "ধর্মগ্রন্থ বা শিক্ষামূলক কাজে সহায়তা করুন। (Support educational causes).",
                "ritual": "বৃহস্পতিবার বিষ্ণু পূজা ও গুরুর আশীর্বাদ গ্রহণ। (Worship Lord Vishnu on Thursdays)."
            }
        },
        "Shukra": {
            "name_bn": "শুক্র (Venus / দৈত্যগুরু)",
            "signifies": "প্রেম, দাম্পত্য, ধন-সম্পদ, যানবাহন ও সৌন্দর্য",
            11: {
                "good": "১১শ ভাবে শুক্র বিভিন্ন উৎস থেকে অর্থপ্রাপ্তি, বন্ধুভাগ্য, বিলাসবহুল জীবন ও নারীদের সহযোগিতায় সৌভাগ্য দেয়। (Multiple income sources, luxury, financial gains through networks).",
                "bad": "অতিরিক্ত শৌখিনতায় অপচয় বা কামপ্রবণতার কারণে আর্থিক ক্ষতি হতে পারে। (Overspending on luxury or temptations).",
                "remedy": "সর্বদা পরিষ্কার ও পরিচ্ছন্ন পোশাক পরুন। ঘরের পরিবেশ সুগন্ধি রাখুন। (Wear neat, clean clothes; maintain a fragrant living space).",
                "ritual": "শুক্রবার সাদা মিষ্টি বা ক্ষীর দরিদ্রদের দান করুন। মা লক্ষ্মীর পূজা করুন। (Donate white sweets/curd on Fridays; worship Goddess Lakshmi)."
            },
            "default": {
                "good": "সৌন্দর্য ও সামাজিক জনপ্রিয়তা বৃদ্ধি করে। (Social charm and luxury).",
                "bad": "অর্থনৈতিক অসাবধানতা। (Financial carelessness).",
                "remedy": "স্ত্রী ও নারীদের পূর্ণ সম্মান দিন। (Respect women in life).",
                "ritual": "শুক্রবার শ্রীসূক্ত পাঠ পরম ফলপ্রসূ। (Recite Sri Suktam on Friday)."
            }
        },
        "Shani": {
            "name_bn": "শনি (Saturn / কর্মফলদাতা)",
            "signifies": "কর্ম, পরিশ্রম, শৃঙ্খলা, আয়ু ও সাধারণ মানুষ",
            2: {
                "good": "২য় ভাবে শনি জাতককে বাস্তববাদী করে। কঠোর পরিশ্রমের মাধ্যমে স্থায়ী অর্থ ও দীর্ঘস্থায়ী সম্পত্তি অর্জিত হয়। (Practical financial sense; wealth through persistent hard work).",
                "bad": "মেষ রাশিতে শনি নীচস্থ হলে প্রারম্ভিক জীবনে ধন সঞ্চয়ে বিলম্ব, পারিবারিক মনোমালিন্য বা মুখের কর্কশ কথা তৈরি করে। (Delayed wealth accumulation in early years; harsh tone).",
                "remedy": "শ্রমিক, দিনমজুর ও সাফাইকর্মীদের সাহায্য করুন। মদ, মাংস ও জুয়া সম্পূর্ণরূপে বর্জন করুন। (Help manual laborers; avoid alcohol, meat, and unethical gains).",
                "ritual": "শনিবার সরিষার তেল দান (ছায়াদান) করুন অথবা কালো কুকুরকে রুটি খাওয়ান। সন্ধ্যায় শনি মন্দিরে বা অশ্বত্থ তলায় সরিষার তেলের প্রদীপ জ্বালুন। (Feed stray dogs on Saturdays; light mustard oil lamp under Peepal tree)."
            },
            "default": {
                "good": "ধৈর্য ও স্থিতিশীলতা দান করে। (Patience and long-term endurance).",
                "bad": "কাজে অযথা বিলম্ব বা একাকীত্ব। (Delays in progress).",
                "remedy": "অসহায় মানুষের সেবা করুন। (Help the needy).",
                "ritual": "শনিবার হনুমান চালীসা বা শনি চালীসা পাঠ। (Recite Hanuman/Shani Chalisa on Saturday)."
            }
        },
        "Rahu": {
            "name_bn": "রাহু (Rahu / মায়াবী গ্রহ)",
            "signifies": "আকস্মিক উন্নতি, প্রযুক্তি, উচ্চাকাঙ্ক্ষা ও রাজনীতি",
            10: {
                "good": "১০ম ভাবে রাহু জাতককে কৌশলী, প্রযুক্তিনির্ভর ও রাতারাতি প্রভাবশালী করে তুলতে পারে। রাজনীতি ও আধুনিক ব্যবসায় বিশেষ শুভ। (Success in tech, modern trade, strategic influence).",
                "bad": "কাজে অস্থিরতা, আকস্মিক অপবাদ বা কর্মক্ষেত্রে গোপন শত্রুর উপদ্রব সৃষ্টি হতে পারে। (Workplace politics, sudden volatility, distractions).",
                "remedy": "ঘরে বা ছাদে কখনো ভাঙা ইলেকট্রনিক সামগ্রী, অকেজো কাঁচ বা পুরনো তার জমিয়ে রাখবেন না। (Do not store broken electronics, scrap, or faulty wiring at home).",
                "ritual": "পকেটে বা গলায় একটি নিরেট রূপার চারকোনা টুকরো রাখুন। সন্ধ্যার পর ঘরে কর্পূর প্রদীপ জ্বালান। (Keep a square solid silver piece; burn camphor at evening)."
            },
            "default": {
                "good": "আউট-অব-দ্য-বক্স চিন্তা ও উদ্ভাবনী মেধা। (Unconventional thinking).",
                "bad": "বিভ্রান্তি, অলীক কল্পনা ও অতিরিক্ত ঝুঁকি নেওয়ার প্রবণতা। (Confusion & illusions).",
                "remedy": "নেশাদ্রব্য থেকে সম্পূর্ণ দূরে থাকুন। (Stay away from addictions).",
                "ritual": "কুষ্ঠ রোগীদের সাহায্য এবং শিবলিঙ্গে জল নিবেদন। (Help the afflicted; Shiva puja)."
            }
        },
        "Ketu": {
            "name_bn": "কেতু (Ketu / মোক্ষকারক)",
            "signifies": "আধ্যাত্মিকতা, বৈরাগ্য, গুপ্তবিদ্যা ও আত্মশুদ্ধি",
            4: {
                "good": "৪র্থ ভাবে কেতু আধ্যাত্মিক চর্চা, অন্তর্মুখী শান্তি এবং নিজস্ব আদর্শে অবিচল থাকার শক্তি দেয়। (Spiritual detachment, philosophical peace).",
                "bad": "নিজের গৃহপরিবেশে মন না বসা, মানসিক অতৃপ্তি বা মায়ের স্বাস্থ্যে চিন্তা। (Inner dissatisfaction at home, emotional detachment).",
                "remedy": "গৃহের বয়োবৃদ্ধ ও মায়ের যত্ন নিন। হলুদ বা কেশর নিয়মিত ব্যবহার করুন। (Care for elderly maternal figures).",
                "ritual": "কালো ও সাদা (চিতকবরা) কুকুরকে প্রতিদিন খাদ্য বা রুটি দিন। গণেশ পূজা করুন। (Feed dual-colored dogs daily; worship Lord Ganesha)."
            },
            "default": {
                "good": "গভীর অন্তর্দৃষ্টি ও লোভহীন চরিত্র। (Spiritual insight & detachment).",
                "bad": "লক্ষ্যহীনতা বা সম্পর্কে অহেতুক উদাসীনতা। (Lack of direction).",
                "remedy": "কুকুর বা প্রাণীদের প্রতি সদয় হোন। (Be kind to street animals).",
                "ritual": "গণেশ দ্বাদশ নাম স্তোত্র পাঠ। (Recite Ganesha mantras)."
            }
        }
    }

    for graha_key in ["Surya", "Chandra", "Mangala", "Budha", "Guru", "Shukra", "Shani", "Rahu", "Ketu"]:
        h_pos = p_house_map.get(graha_key, 1)
        g_info = GRAHA_DATA[graha_key]
        house_specific = g_info.get(h_pos, g_info["default"])
        
        st.markdown(f"""
        <div class="graha-card">
            <h4 style="color:#f4c66a;margin:0 0 4px 0;">{g_info['name_bn']} — অবস্থান: {h_pos}ম ভাব (House {h_pos})</h4>
            <div style="font-size:0.85rem;color:#a0a6c6;margin-bottom:8px;">কারক তত্ত্ব: {g_info['signifies']}</div>
            
            <p><b>✨ শুভ প্রভাব (What will happen good):</b><br>{house_specific['good']}</p>
            <p><b>⚠️ সম্ভাব্য ঝুঁকি বা অশুভ প্রভাব (Risks / Bad effects if afflicted):</b><br>{house_specific['bad']}</p>
            
            <div class="remedy-box">
                <b>🛠️ কী করলে ভালো হবে (How to correct it / Simple Lifestyle Upay):</b><br>
                {house_specific['remedy']}
            </div>
            
            <div class="ritual-box">
                <b>🙏 নির্দিষ্ট আচার ও পূজা (Exact Ritual & Mantra):</b><br>
                {house_specific['ritual']}
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📅 সাপ্তাহিক প্রতিকার ও দৈনন্দিন নিয়ম সূচি (Weekly Action Plan)")
    st.info("আপনার কোষ্ঠীর সকল গ্রহের সামঞ্জস্য ও মানসিক প্রশান্তির জন্য এই সাপ্তাহিক সহজ নিয়মগুলি পালন করুন:")

    st.markdown("""
| বার (Day) | নিয়ন্ত্রক গ্রহ | কী করবেন (Simple Action in Bengali & English) | কী লাভ হবে (Direct Purpose) |
| :--- | :--- | :--- | :--- |
| **সোমবার (Monday)** | চন্দ্র (Moon) | শিবলিঙ্গে কাঁচা দুধ ও জল অর্পণ; রূপার গয়না বা মুদ্রা কাছে রাখা। *(Offer milk/water to Shivling; carry silver)* | মানসিক অস্থিরতা, অতিরিক্ত চিন্তা ও দুশ্চিন্তা দূর হয়। |
| **মঙ্গলবার (Tuesday)** | মঙ্গল (Mars) | হনুমান চালীসা পাঠ এবং মিষ্টি বা গুড় বিতরণ; রাগ নিয়ন্ত্রণ। *(Recite Hanuman Chalisa; donate jaggery/sweets)* | মাঙ্গলিক তেজ শান্ত হয়, রক্ত ও গৃহস্থালি সম্পর্কের শুভত্ব বাড়ে। |
| **বুধবার (Wednesday)** | বুধ (Mercury) | গরুকে সবুজ ঘাস/পালং শাক খাওয়ানো; বোন বা ছোট মেয়েদের উপহার। *(Feed green grass to cows; respect sisters)* | বুদ্ধি, ব্যবসায়িক সিদ্ধান্ত ও আর্থিক বাণিজ্যে দ্রুত উন্নতি হয়। |
| **বৃহস্পতিবার (Thursday)** | বৃহস্পতি (Jupiter) | কপালে চন্দন বা হলুদের তিলক লাগানো; শিক্ষক ও গুরুজনদের সম্মান। *(Apply Chandan/Haldi tilak; honor teachers)* | জ্ঞান, মানসিক স্থৈর্য ও পারিবারিক জীবনে দৈব আশীর্বাদ লাভ। |
| **শুক্রবার (Friday)** | শুক্র (Venus) | পরিচ্ছন্ন সুগন্ধি পোশাক পরিধান; দরিদ্র নারীদের সাদা মিষ্টি দান। *(Wear clean, fragrant clothes; donate white sweets)* | ধনলাভ, দাম্পত্য সুখ ও সামাজিক আকর্ষণ বৃদ্ধি পায়। |
| **শনিবার (Saturday)** | শনি ও রাহু | কালো কুকুরকে রুটি দান; সরিষার তেলের প্রদীপ জ্বালানো; ঘর থেকে বর্জ্য দূর। *(Feed stray dogs; light mustard oil lamp)* | কর্মক্ষেত্রের বাধা, বিলম্ব এবং আকস্মিক দুর্যোগ দূর হয়। |
| **রবিবার (Sunday)** | সূর্য (Sun) | সকালে তামার পাত্রে সূর্যকে জল অর্পণ; পিতাকে ভক্তিভরে প্রণাম। *(Offer water to rising Sun from copper vessel; honor father)* | তেজ, সমাজে সম্মান, আত্মবিশ্বাস ও জীবনীশক্তি বৃদ্ধি পায়। |
""", unsafe_allow_html=True)

with tab4:
    st.markdown("### 📊 গ্রহের স্পষ্ট দ্রাঘিমাংশ ও বিংশোত্তরী মহাদশা")
    st.dataframe(p_details, use_container_width=True)

    st.markdown("#### ⏳ বিংশোত্তরী মহাদশা কাল (Vimshottari Dasha Sequence)")
    st.caption("চন্দ্র নক্ষত্রের ভুক্তির ওপর ভিত্তি করে শতবর্ষীয় মহাদশা হিসাব:")
    col_d1, col_d2 = st.columns(2)
    for idx, (lord, span) in enumerate(dasha_timeline):
        t_col = col_d1 if idx < 5 else col_d2
        with t_col:
            st.markdown(f"""
            <div class="card" style="padding:10px; margin-bottom:8px;">
                <b>{lord} মহাদশা:</b> <span class="highlight-gold">{span}</span>
            </div>
            """, unsafe_allow_html=True)

with tab5:
    st.markdown("### ⚖️ শাস্ত্রীয় শুভ যোগ ও দোষ বিচার")
    
    mars_h = p_house_map.get("Mangala", 0)
    is_manglik = mars_h in [1, 4, 7, 8, 12]

    is_budhaditya = p_house_map.get("Surya") == p_house_map.get("Budha")
    jup_h = p_house_map.get("Guru", 0)
    moon_h = p_house_map.get("Chandra", 0)
    kendra_diff = (jup_h - moon_h) % 12
    is_gajakesari = kendra_diff in [0, 3, 6, 9]

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">চিহ্নিত শুভ যোগসমূহ (Auspicious Yogas)</h4>
        {"<span class='badge'>গজকেশরী যোগ (Gajakesari)</span> বৃহস্পতি ও চন্দ্র কেন্দ্রবর্তী। গভীর প্রজ্ঞা, দীর্ঘায়ু ও সমাজমান লাভ হয়।<br><br>" if is_gajakesari else ""}
        {"<span class='badge'>বুধাদিত্য যোগ (Budhaditya)</span> রবি ও বুধের যুগল অবস্থান। তীক্ষ্ণ মেধা, হিসাববিদ্যায় পারদর্শিতা ও প্রশাসনিক ক্ষমতা।<br><br>" if is_budhaditya else ""}
        <span class='badge'>লগ্ন-কেন্দ্র শুভত্ব</span> লগ্ন ও ত্রিকোণাধিপতির শুভ সামঞ্জস্য।
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#f4c66a;margin:0 0 6px 0;">দোষ নিরূপণ ও সমাধান (Dosha Scan)</h4>
        <b>ভৌম দোষ / মাঙ্গলিক বিচার:</b> {"⚠️ লগ্ন, ৪র্থ, ৭ম, ৮ম বা ১২শ ভাবে মঙ্গল অবস্থিত (" + str(mars_h) + "ম ভাব)। ২৮ বছর বয়সের পর এর তেজ প্রশমিত হয়। হনুমান চালীসা পাঠ ও রাগ দমন প্রধান প্রতিকার।" if is_manglik else "✅ মাঙ্গলিক দোষ মুক্ত। মঙ্গল শুভ স্থানে স্থিত।"}<br><br>
        <b>কেমদ্রুম দোষ বিচার:</b> {"⚠️ চন্দ্রের উভয় পার্শ্বস্থ ঘর গ্রহহীন হলে একাকীত্ব বা দুশ্চিন্তা দেখা দিতে পারে। শিবপূজা ও সোমবারে দুধ অর্পণ দ্বারা দোষ খণ্ডন হয়।" if len(occupants.get((moon_h % 12) + 1, [])) == 0 and len(occupants.get(((moon_h - 2) % 12) + 1, [])) == 0 else "✅ কেমদ্রুম ভঙ্গ যোগ বা নিরাপদ চন্দ্রবল।"}
    </div>
    """, unsafe_allow_html=True)
