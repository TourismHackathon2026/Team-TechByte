import streamlit as st
import sqlite3
import uuid
import base64
import time
import hashlib
from datetime import datetime

LOGO_URL = "https://i.postimg.cc/RVL0MqbQ/logo.png"

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Tourgram", page_icon=LOGO_URL, layout="wide", initial_sidebar_state="expanded")

# ── DATABASE ───────────────────────────────────────────────────────────────────
DB_PATH = "tourgram.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            avatar_b64 TEXT DEFAULT '',
            bio TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS places (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            district TEXT NOT NULL,
            image TEXT NOT NULL,
            caption TEXT DEFAULT '',
            history TEXT DEFAULT '',
            budget TEXT DEFAULT '',
            safety TEXT DEFAULT '',
            stars INTEGER DEFAULT 5,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            place_id TEXT NOT NULL,
            author TEXT NOT NULL,
            user_id TEXT,
            text TEXT NOT NULL,
            rating INTEGER DEFAULT 5,
            certified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(place_id) REFERENCES places(id)
        );
        CREATE TABLE IF NOT EXISTS votes (
            id TEXT PRIMARY KEY,
            place_id TEXT NOT NULL,
            user_id TEXT,
            session_id TEXT,
            vote_type TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            username TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Migration: add email column if missing (for existing DBs)
    try:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # column already exists

    c.execute("SELECT COUNT(*) FROM places")
    if c.fetchone()[0] == 0:
        seed_places = [
            ("p1","system","u/rajan_travels","Phewa Lake","Kaski",
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJkhK2TPskum-I6Uqf5HX3FFO2jMsD7_LNDw&s",
             "The jewel of Pokhara — serene, majestic, unforgettable.",
             "Phewa Lake is the second largest lake in Nepal, located in Pokhara. It has been a hub for travellers for centuries, with the iconic Tal Barahi Temple sitting on a small island at its centre. The lake reflects the Annapurna range on clear mornings, creating one of the most photographed scenes in all of Nepal.",
             "Entry free. Boat rides from NPR 500/hr. Rowboats available for self-rowing. Local restaurants along the lakeside offer meals from NPR 200–600. Accommodation nearby ranges from NPR 800 budget guesthouses to NPR 5000+ lakeside resorts.",
             "Very safe. Lifeguards present during peak hours. Avoid during heavy rain season. Wear life jackets on boats. The lakeside road can be busy — watch for traffic when walking.",5),
            ("p2","system","u/anita_explorer","Pashupatinath Temple","Kathmandu",
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyHqvQcW5pKYN4X8bFFl7aM9oolY3HTYzyYg&s",
             "Sacred, ancient, deeply spiritual — a must for every visitor to Nepal.",
             "One of the most sacred Hindu temples in the world, dating back to the 5th century. Dedicated to Lord Shiva, it sits on the banks of the Bagmati River. The temple complex includes hundreds of smaller shrines and is a UNESCO World Heritage Site. The evening aarti ceremony is breathtaking.",
             "Foreign nationals: NPR 1000 entry. Locals: free. Best visited early morning or during Shivaratri festival. Auto-rickshaws from Thamel cost around NPR 200. Allow 2–3 hours for a thorough visit.",
             "Safe. Follow dress code rules inside — conservative clothing required. Non-Hindus cannot enter the main temple but can observe from across the river. Keep valuables secure in crowded areas.",5),
            ("p3","system","u/bikram_hikes","Annapurna Base Camp","Kaski",
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTq3B0EGxY6Z2l9nN408GcOY2cN21LvqjNbHQ&s",
             "A 360° amphitheatre of Himalayan giants — nothing on earth compares.",
             "At 4,130m, ABC is one of the most iconic trekking destinations in the world. Surrounded by peaks over 7,000m including Annapurna I, Hiunchuli, and Machhapuchhre, it offers a 360° amphitheatre of the Himalayas that leaves every trekker speechless.",
             "Trek permits: ACAP NPR 3000 + TIMS NPR 2000. Guide recommended: NPR 2500/day. Porter: NPR 1800/day. Tea house accommodation NPR 300–600/night. Budget NPR 2500–4000/day total. 7–12 day round trip from Pokhara.",
             "Altitude sickness risk above 3000m. Acclimatise properly — do not rush the ascent. Carry altitude medication. Weather can change rapidly. Best seasons: March–May and September–November. Avoid monsoon season.",5),
            ("p4","system","u/sara_wanderer","Chitwan National Park","Chitwan",
             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuUxpwjHWDBdDhlnJsn1NF4GduMVQ6W_IVXA&s",
             "UNESCO wilderness where rhinos roam free and the jungle breathes.",
             "UNESCO World Heritage Site established in 1973. Home to one-horned rhinos, Bengal tigers, gharial crocodiles, and over 500 bird species. One of the best wildlife parks in Asia. The Rapti and Narayani rivers border the park, creating rich riparian ecosystems.",
             "Entry: NPR 1500 for foreigners. Jeep safari: NPR 2500. Elephant breeding centre: NPR 500. Canoe ride: NPR 800. Tharu cultural show: NPR 500. Budget NPR 6000–10000/day including accommodation in Sauraha.",
             "Stay with certified guides at all times inside the park. Do not wander alone near the jungle edges — rhinos and elephants can be aggressive. Wear muted colours. Best time: October–March. Avoid peak monsoon.",5),
            ("p5","system","u/deepak_lens","Boudhanath Stupa","Kathmandu",
             "https://lp-cms-production.imgix.net/2019-06/813869da84003e9ab623499ae2465723-bodhnath-stupa.jpg?w=1200&auto=format",
             "The all-seeing eyes of Buddha watching over the valley at dusk.",
             "One of the largest stupas in the world and a UNESCO World Heritage Site. A centre of Tibetan Buddhism in Nepal since the 14th century. The all-seeing eyes of Buddha watch over the valley from every angle. The stupa is surrounded by monasteries, shops, and cafes — a living spiritual hub.",
             "Entry: NPR 400 for foreigners, free for locals. Best visited at dawn or dusk for the butter lamp ceremony. Rooftop cafes around the stupa offer great views for NPR 300–500 meals. The surrounding market has thangkas, singing bowls and prayer flags.",
             "Very safe. Busy tourist area — watch for pickpockets in crowds. Dress modestly when entering monastery grounds. Walk clockwise around the stupa as per Buddhist tradition. Beggars are common — be respectful.",5),
            ("p6","system","u/mina_clicks","Rara Lake","Mugu",
             "https://highcampadventure.com/uploads/fullbanner/biggest-lake-of-nepal-rara-lake.webp",
             "Nepal's best-kept secret — crystal blue waters hidden in Karnali.",
             "Nepal's largest lake, hidden in the remote Karnali region at 2,990m elevation. Crystal-clear blue waters that shift from turquoise to deep cobalt depending on the light. Surrounded by dense pine and juniper forests. The Rara National Park surrounding it is home to red pandas, Himalayan black bears and over 200 bird species.",
             "Flight to Talcha from Nepalgunj: ~NPR 15,000 one way. Trek + permits: NPR 3000. Very limited accommodation nearby — basic lodges NPR 500–800. Carry enough cash as there are no ATMs. Budget NPR 4000–6000/day.",
             "Remote area with very limited phone signal or emergency services. Go with an experienced licensed guide — this is non-negotiable. Carry first aid, extra food and warm clothing. Weather is unpredictable. Best time: September–November.",5),
        ]
        c.executemany("INSERT INTO places (id,user_id,username,title,district,image,caption,history,budget,safety,stars) VALUES (?,?,?,?,?,?,?,?,?,?,?)", seed_places)

        seed_reviews = [
            (str(uuid.uuid4()),"p1","u/sara_wanderer",None,"Best sunrise I've ever seen. The reflection of Machhapuchhre on the lake is absolutely unreal — I cried.",5,1),
            (str(uuid.uuid4()),"p1","Guest123",None,"Absolutely stunning at sunrise! Highly recommend the boat ride out to the island temple.",5,0),
            (str(uuid.uuid4()),"p1","u/deepak_lens",None,"Photographed here for 3 days straight. The light in the early morning is magical.",5,1),
            (str(uuid.uuid4()),"p2","u/deepak_lens",None,"Spiritual and deeply peaceful experience. The evening aarti by the river is something I'll never forget.",5,1),
            (str(uuid.uuid4()),"p2","Guest123",None,"Must visit during Shivaratri — the atmosphere is absolutely electric.",5,0),
            (str(uuid.uuid4()),"p2","u/bikram_hikes",None,"Visited at 5am and had the ghats almost to myself. Profound experience.",5,1),
            (str(uuid.uuid4()),"p3","u/bikram_hikes",None,"Life-changing trek. Nothing prepares you for that view when you arrive at base camp.",5,1),
            (str(uuid.uuid4()),"p3","u/rajan_travels",None,"Did this in October — perfect weather, clear skies. Already planning to go back.",5,1),
            (str(uuid.uuid4()),"p4","u/mina_clicks",None,"Saw a one-horned rhino up close from the jeep — absolutely incredible! Also spotted a croc.",5,1),
            (str(uuid.uuid4()),"p4","Guest123",None,"Amazing jungle experience. The Tharu cultural show at night was a bonus.",4,0),
            (str(uuid.uuid4()),"p5","Guest123",None,"Peaceful and majestic. The evening kora walk around the stupa with butter lamps is magical.",4,0),
            (str(uuid.uuid4()),"p5","u/anita_explorer",None,"Come at dawn when the monks are doing prayers. Absolutely serene.",5,1),
            (str(uuid.uuid4()),"p6","u/rajan_travels",None,"Pure paradise. Worth every rupee and every step. The silence there is healing.",5,1),
            (str(uuid.uuid4()),"p6","u/sara_wanderer",None,"Took 3 flights and a 2-day trek to get here. Zero regrets. Most beautiful lake I've seen.",5,1),
        ]
        c.executemany("INSERT INTO reviews (id,place_id,author,user_id,text,rating,certified) VALUES (?,?,?,?,?,?,?)", seed_reviews)

        # Seed votes — boosted to feel real
        seed_votes = []
        default_votes = {
            "p1": (312, 8),
            "p2": (478, 14),
            "p3": (634, 11),
            "p4": (389, 22),
            "p5": (521, 17),
            "p6": (276, 6),
        }
        for pid, (ups, dns) in default_votes.items():
            for i in range(ups):
                seed_votes.append((str(uuid.uuid4()), pid, None, f"seed_up_{pid}_{i}", "up"))
            for i in range(dns):
                seed_votes.append((str(uuid.uuid4()), pid, None, f"seed_dn_{pid}_{i}", "down"))
        c.executemany("INSERT INTO votes (id,place_id,user_id,session_id,vote_type) VALUES (?,?,?,?,?)", seed_votes)

    conn.commit()
    conn.close()

init_db()

# ── DB HELPERS ─────────────────────────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def get_user_by_id(uid):
    conn = get_db(); r = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone(); conn.close()
    return dict(r) if r else None

def get_user_by_username(u):
    conn = get_db(); r = conn.execute("SELECT * FROM users WHERE username=?", (u,)).fetchone(); conn.close()
    return dict(r) if r else None

def get_user_by_email(e):
    conn = get_db(); r = conn.execute("SELECT * FROM users WHERE email=?", (e,)).fetchone(); conn.close()
    return dict(r) if r else None

def create_user(username, email, password):
    uid = str(uuid.uuid4())
    conn = get_db()
    try:
        conn.execute("INSERT INTO users (id,username,email,password_hash) VALUES (?,?,?,?)", (uid, username, email, hash_pw(password)))
        conn.commit(); conn.close(); return uid
    except sqlite3.IntegrityError:
        conn.close(); return None

def update_user_profile(uid, avatar_b64, bio):
    conn = get_db()
    conn.execute("UPDATE users SET avatar_b64=?, bio=? WHERE id=?", (avatar_b64, bio, uid))
    conn.commit(); conn.close()

def save_session(session_id, user_id, username):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO sessions (session_id,user_id,username) VALUES (?,?,?)", (session_id, user_id, username))
    conn.commit(); conn.close()

def load_session(session_id):
    conn = get_db(); r = conn.execute("SELECT * FROM sessions WHERE session_id=?", (session_id,)).fetchone(); conn.close()
    return dict(r) if r else None

def delete_session(session_id):
    conn = get_db(); conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,)); conn.commit(); conn.close()

def get_all_places():
    conn = get_db(); rows = conn.execute("SELECT * FROM places ORDER BY created_at DESC").fetchall(); conn.close()
    return [dict(r) for r in rows]

def get_place_by_id(pid):
    conn = get_db(); r = conn.execute("SELECT * FROM places WHERE id=?", (pid,)).fetchone(); conn.close()
    return dict(r) if r else None

def insert_place(d):
    conn = get_db()
    conn.execute("INSERT INTO places (id,user_id,username,title,district,image,caption,history,budget,safety,stars) VALUES (:id,:user_id,:username,:title,:district,:image,:caption,:history,:budget,:safety,:stars)", d)
    conn.commit(); conn.close()

def update_place(pid, title, district, caption, history, budget, safety):
    conn = get_db()
    conn.execute("UPDATE places SET title=?,district=?,caption=?,history=?,budget=?,safety=? WHERE id=?",
                 (title, district, caption, history, budget, safety, pid))
    conn.commit(); conn.close()

def delete_place(pid):
    conn = get_db()
    conn.execute("DELETE FROM reviews WHERE place_id=?", (pid,))
    conn.execute("DELETE FROM votes WHERE place_id=?", (pid,))
    conn.execute("DELETE FROM places WHERE id=?", (pid,))
    conn.commit(); conn.close()

def get_reviews(place_id):
    conn = get_db(); rows = conn.execute("SELECT * FROM reviews WHERE place_id=? ORDER BY created_at DESC", (place_id,)).fetchall(); conn.close()
    return [dict(r) for r in rows]

def insert_review(place_id, author, user_id, text, rating, certified):
    conn = get_db()
    conn.execute("INSERT INTO reviews (id,place_id,author,user_id,text,rating,certified) VALUES (?,?,?,?,?,?,?)",
                 (str(uuid.uuid4()), place_id, author, user_id, text, rating, certified))
    conn.commit(); conn.close()

def get_vote_counts(place_id):
    conn = get_db()
    up = conn.execute("SELECT COUNT(*) FROM votes WHERE place_id=? AND vote_type='up'", (place_id,)).fetchone()[0]
    dn = conn.execute("SELECT COUNT(*) FROM votes WHERE place_id=? AND vote_type='down'", (place_id,)).fetchone()[0]
    conn.close(); return up, dn

def get_user_vote(place_id, user_id=None, session_id=None):
    conn = get_db()
    if user_id:
        r = conn.execute("SELECT vote_type FROM votes WHERE place_id=? AND user_id=?", (place_id, user_id)).fetchone()
    else:
        r = conn.execute("SELECT vote_type FROM votes WHERE place_id=? AND session_id=?", (place_id, session_id)).fetchone()
    conn.close(); return r[0] if r else None

def cast_vote(place_id, vote_type, user_id=None, session_id=None):
    conn = get_db()
    existing = get_user_vote(place_id, user_id, session_id)
    if existing == vote_type:
        if user_id: conn.execute("DELETE FROM votes WHERE place_id=? AND user_id=?", (place_id, user_id))
        else: conn.execute("DELETE FROM votes WHERE place_id=? AND session_id=?", (place_id, session_id))
    elif existing:
        if user_id: conn.execute("UPDATE votes SET vote_type=? WHERE place_id=? AND user_id=?", (vote_type, place_id, user_id))
        else: conn.execute("UPDATE votes SET vote_type=? WHERE place_id=? AND session_id=?", (vote_type, place_id, session_id))
    else:
        conn.execute("INSERT INTO votes (id,place_id,user_id,session_id,vote_type) VALUES (?,?,?,?,?)",
                     (str(uuid.uuid4()), place_id, user_id, session_id, vote_type))
    conn.commit(); conn.close()

# ── AVATAR HELPERS ─────────────────────────────────────────────────────────────
def get_initials_svg(name, size=42):
    initials = "".join([w[0].upper() for w in name.replace("u/","").split("_") if w])[:2]
    colors = ["#0d9488","#0891b2","#7c3aed","#db2777","#ea580c","#16a34a","#dc2626"]
    color = colors[hash(name) % len(colors)]
    svg = f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg"><circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="{color}"/><text x="50%" y="50%" dominant-baseline="central" text-anchor="middle" font-family="Inter,sans-serif" font-size="{int(size/2.5)}" font-weight="700" fill="white">{initials}</text></svg>'
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"

def avatar_img(username, avatar_b64="", size=42):
    src = avatar_b64 if avatar_b64 and avatar_b64.startswith("data:image") else get_initials_svg(username, size)
    return f'<img src="{src}" style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;border:2px solid #14b8a6;flex-shrink:0;">'

# ── SESSION PERSISTENCE ────────────────────────────────────────────────────────
def init_session():
    if "session_token" not in st.session_state:
        params = st.query_params
        token = params.get("st", None)
        if token:
            sess = load_session(token)
            if sess:
                st.session_state.session_token = token
                st.session_state.logged_in = True
                st.session_state.username = sess["username"]
                st.session_state.user_id = sess["user_id"]
            else:
                st.session_state.session_token = str(uuid.uuid4())
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.user_id = None
        else:
            st.session_state.session_token = str(uuid.uuid4())
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_id = None

    defaults = {
        "page": "home",
        "selected_place": None,
        "selected_district": None,
        "auth_tab": "login",
        "expanded_cards": set(),
        "editing_place": None,
        "confirm_delete": None,
        "place_detail_id": None,
        "place_detail_from": "home",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

def go(page, place=None, district=None):
    st.session_state.page = page
    st.session_state.selected_place = place
    st.session_state.selected_district = district
    st.rerun()

def do_login(user_id, username):
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.user_id = user_id
    token = st.session_state.session_token
    save_session(token, user_id, username)
    st.query_params["st"] = token

def do_logout():
    delete_session(st.session_state.session_token)
    st.query_params.clear()
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.session_state.session_token = str(uuid.uuid4())

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; }}
.stApp, body {{ background: #f0fafa !important; }}
#MainMenu, footer, header {{ visibility: hidden !important; }}
div[data-testid="stDecoration"], div[data-testid="stToolbar"] {{ display: none !important; }}
button[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] button[kind="header"],
.st-emotion-cache-1rs6os, .st-emotion-cache-czk5ss {{
    display:none!important; visibility:hidden!important; pointer-events:none!important;
}}
section[data-testid="stSidebar"] {{
    background:#ffffff!important; border-right:2px solid #b2dfdb!important;
    min-width:230px!important; max-width:230px!important;
}}
section[data-testid="stSidebar"] .stButton > button {{
    width:100%!important; text-align:left!important; background:transparent!important;
    border:none!important; border-left:3px solid transparent!important;
    border-radius:0 8px 8px 0!important; color:#1a2e2e!important;
    font-size:15px!important; font-weight:500!important;
    padding:11px 18px!important; margin-bottom:2px!important; box-shadow:none!important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background:#e0f2f1!important; border-left-color:#00897b!important; color:#00796b!important;
}}
.block-container {{ padding:0!important; max-width:100%!important; }}

/* TOPBAR */
.tg-topbar {{
    display:flex; align-items:center; gap:12px;
    background:#ffffff; border-bottom:1.5px solid #b2dfdb;
    padding:10px 28px; box-shadow:0 1px 6px rgba(0,128,128,0.08);
}}
.tg-brand {{ display:flex; align-items:center; gap:10px; flex:1; }}
.tg-brand img {{ height:36px; width:auto; }}
.tg-brand span {{ font-size:20px; font-weight:700; color:#00796b; }}
.tg-userbadge {{ font-size:13px; font-weight:600; color:#00796b; background:#e0f2f1; padding:5px 14px; border-radius:20px; }}

.tg-page {{ padding:20px 28px 60px; }}
.tg-section-title {{ font-size:16px; font-weight:700; color:#00796b; margin:22px 0 12px; }}

/* THUMBNAIL CARDS — fixed size */
.tg-card-wrap {{
    background:#fff; border:1px solid #e0f2f1; border-radius:12px;
    overflow:hidden; box-shadow:0 1px 6px rgba(0,128,128,0.06);
    margin-bottom:4px; height:220px; display:flex; flex-direction:column;
    cursor:pointer; transition: box-shadow 0.2s, transform 0.15s;
}}
.tg-card-wrap:hover {{
    box-shadow:0 4px 16px rgba(0,128,128,0.18)!important;
    transform: translateY(-2px);
}}
.tg-card-img {{ width:100%; height:148px; object-fit:cover; display:block; flex-shrink:0; }}
.tg-card-footer {{ padding:6px 10px 4px; display:flex; align-items:center; gap:7px; flex:1; min-height:0; }}

/* PLACE CARD — side by side */
.place-card {{
    background:#fff; border:1px solid #e0f2f1; border-radius:16px;
    overflow:hidden; margin-bottom:24px;
    box-shadow:0 2px 12px rgba(0,128,128,0.07);
    display:flex; flex-direction:row; min-height:380px;
}}
.place-card-img-wrap {{
    width:42%; min-width:260px; max-width:42%; flex-shrink:0;
    position:relative; overflow:hidden;
}}
.place-card-img-wrap img {{
    width:100%; height:100%; object-fit:cover; display:block;
    min-height:380px; max-height:380px;
}}

/* Right panel — collapsed state: fixed height with fade */
.place-card-details {{
    flex:1; padding:18px 20px 14px; display:flex; flex-direction:column;
    position:relative; max-height:380px; overflow:hidden;
}}
/* Fade overlay at bottom when collapsed */
.place-card-details::after {{
    content:'';
    position:absolute;
    bottom:48px; left:0; right:0;
    height:60px;
    background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, rgba(255,255,255,0.97) 100%);
    pointer-events:none;
    transition: opacity 0.2s;
}}
/* When expanded remove fade and height limit */
.place-card-details.expanded {{
    max-height:none;
    overflow:visible;
}}
.place-card-details.expanded::after {{
    display:none;
}}
/* Scrollbar for details */
.place-card-details::-webkit-scrollbar {{ width:4px; }}
.place-card-details::-webkit-scrollbar-thumb {{ background:#b2dfdb; border-radius:4px; }}

.place-card-author {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
.place-card-author-name {{ font-size:13px; font-weight:700; color:#0f766e; }}
.place-card-author-sub {{ font-size:11px; color:#64748b; }}
.place-card-title {{ font-size:20px; font-weight:800; color:#1a2e2e; margin:0 0 3px; }}
.place-card-district {{ font-size:11px; color:#0d9488; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }}
.place-card-caption {{ font-size:13px; color:#475569; font-style:italic; margin-bottom:8px; padding:8px 12px; background:#f0fdfa; border-radius:8px; border-left:3px solid #14b8a6; }}
.info-label {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#0d9488; margin:6px 0 2px; }}
.info-text {{ font-size:13px; color:#334155; line-height:1.6; margin:0 0 4px; }}
.rating-badge {{ display:inline-flex; align-items:center; gap:4px; background:#fef9c3; color:#92400e; font-size:12px; font-weight:700; padding:3px 10px; border-radius:20px; margin-bottom:6px; border:1px solid #fde68a; }}
.review-bubble {{ background:#f0fdfa; padding:9px 12px; border-radius:10px; margin-bottom:7px; border-left:3px solid #14b8a6; }}
.review-author {{ font-size:12px; font-weight:700; color:#0f766e; }}
.review-text {{ font-size:12px; color:#1e293b; margin:2px 0 0; }}
.badge-cert {{ background:#d1fae5; color:#065f46; font-size:10px; font-weight:700; padding:2px 6px; border-radius:8px; margin-left:4px; }}
.badge-guest {{ background:#f1f5f9; color:#64748b; font-size:10px; font-weight:600; padding:2px 6px; border-radius:8px; margin-left:4px; }}

/* See more bar pinned at bottom of details panel */
.see-more-bar {{
    position:absolute;
    bottom:0; left:0; right:0;
    padding:8px 20px 10px;
    background:#fff;
    display:flex;
    justify-content:flex-end;
    align-items:center;
    border-top:1px solid #f0fafa;
    z-index:10;
}}

/* VOTE BUTTONS — green for up, red for down */
.vote-btn-up .stButton > button {{
    background:#f0fdfa!important; border:1.5px solid #99f6e4!important;
    color:#0f766e!important; border-radius:20px!important; padding:4px 16px!important; font-weight:700!important;
    transition: all 0.15s!important;
}}
.vote-btn-up .stButton > button:hover {{
    background:#d1fae5!important; border-color:#0d9488!important;
}}
.vote-btn-up-active .stButton > button {{
    background:#16a34a!important; border:1.5px solid #16a34a!important;
    color:#ffffff!important; border-radius:20px!important; padding:4px 16px!important; font-weight:700!important;
    box-shadow: 0 0 0 3px rgba(22,163,74,0.18)!important;
}}
.vote-btn-dn .stButton > button {{
    background:#fff5f5!important; border:1.5px solid #fecaca!important;
    color:#c62828!important; border-radius:20px!important; padding:4px 16px!important; font-weight:700!important;
    transition: all 0.15s!important;
}}
.vote-btn-dn .stButton > button:hover {{
    background:#fee2e2!important; border-color:#dc2626!important;
}}
.vote-btn-dn-active .stButton > button {{
    background:#dc2626!important; border:1.5px solid #dc2626!important;
    color:#ffffff!important; border-radius:20px!important; padding:4px 16px!important; font-weight:700!important;
    box-shadow: 0 0 0 3px rgba(220,38,38,0.18)!important;
}}

/* THREE DOT MENU */
.three-dot-wrap {{ position:relative; display:inline-block; }}
.action-menu-btn .stButton > button {{
    background:transparent!important; border:none!important; color:#64748b!important;
    font-size:18px!important; padding:2px 8px!important; border-radius:6px!important;
    box-shadow:none!important; min-width:0!important;
}}
.action-menu-btn .stButton > button:hover {{ background:#f1f5f9!important; }}

/* AUTH */
.auth-wrap {{ max-width:440px; margin:40px auto; background:#fff; border:1px solid #e0f2f1; border-radius:20px; padding:36px 32px; box-shadow:0 4px 24px rgba(0,128,128,0.09); }}
.auth-tab-row {{ display:flex; gap:0; border:1.5px solid #b2dfdb; border-radius:12px; overflow:hidden; margin-bottom:24px; }}
.auth-tab {{ flex:1; text-align:center; padding:11px 0; font-size:15px; font-weight:600; cursor:pointer; background:#f0fafa; color:#607d8b; }}
.auth-tab.active {{ background:#0d9488; color:#fff; }}

/* PROFILE */
.profile-header {{ display:flex; align-items:center; gap:20px; background:#fff; border:1px solid #e0f2f1; border-radius:16px; padding:24px; margin-bottom:20px; }}
.profile-stat {{ text-align:center; }}
.profile-stat-num {{ font-size:20px; font-weight:800; color:#0d9488; }}
.profile-stat-label {{ font-size:11px; color:#64748b; font-weight:600; }}

/* POST FORM */
.post-section-card {{ background:#f8fffe; border:1px solid #e0f2f1; border-radius:12px; padding:18px; margin-bottom:16px; }}
.post-step-label {{ font-size:12px; font-weight:700; color:#0d9488; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }}
.title-banner {{ background:linear-gradient(135deg,#ccfbf1 0%,#f0fdfa 100%); padding:24px; border-radius:16px; text-align:center; margin-bottom:24px; border:1px solid #99f6e4; }}
.title-banner h2 {{ color:#0f766e!important; font-weight:800; margin:0; font-size:1.8rem; }}
.tg-district-card {{ background:#fff; border:1px solid #e0f2f1; border-radius:12px; padding:20px 16px; text-align:center; box-shadow:0 1px 6px rgba(0,128,128,0.06); margin-bottom:4px; }}

/* BUTTONS GLOBAL */
.stButton > button {{ border-radius:8px!important; font-size:13px!important; font-weight:600!important; transition:all .15s!important; }}
.btn-primary .stButton > button {{ background:#0d9488!important; color:#fff!important; border:none!important; }}
.btn-primary .stButton > button:hover {{ background:#0f766e!important; }}
.btn-back .stButton > button {{ background:#fff!important; border:1px solid #b2dfdb!important; color:#00796b!important; }}
.btn-danger .stButton > button {{ background:#fff!important; border:1px solid #fca5a5!important; color:#dc2626!important; }}
.btn-showmore .stButton > button {{
    background:transparent!important; border:none!important; color:#0d9488!important;
    font-size:12px!important; font-weight:700!important;
    text-decoration:none!important; padding:0!important; box-shadow:none!important;
}}
.btn-showmore .stButton > button:hover {{ color:#0f766e!important; text-decoration:underline!important; }}

hr {{ border:none; border-top:1px solid #e0f2f1; margin:16px 0; }}

/* PLACE DETAIL PAGE */
.detail-card {{
    background:#fff; border:1px solid #e0f2f1; border-radius:16px;
    overflow:hidden; margin-bottom:24px;
    box-shadow:0 2px 12px rgba(0,128,128,0.07);
    display:flex; flex-direction:row; min-height:480px;
}}
.detail-card-img-wrap {{
    width:44%; min-width:280px; max-width:44%; flex-shrink:0;
    position:relative; overflow:hidden;
}}
.detail-card-img-wrap img {{
    width:100%; height:100%; object-fit:cover; display:block;
    min-height:480px;
}}
.detail-card-details {{
    flex:1; padding:24px 24px 16px; display:flex; flex-direction:column;
    position:relative; overflow-y:auto; max-height:600px;
}}
.detail-card-details::-webkit-scrollbar {{ width:4px; }}
.detail-card-details::-webkit-scrollbar-thumb {{ background:#b2dfdb; border-radius:4px; }}

@media (max-width: 700px) {{
    .place-card, .detail-card {{ flex-direction:column!important; }}
    .place-card-img-wrap, .detail-card-img-wrap {{
        width:100%!important; max-width:100%!important; min-width:0!important;
    }}
    .place-card-img-wrap img {{ min-height:200px!important; max-height:240px!important; }}
    .detail-card-img-wrap img {{ min-height:220px!important; max-height:260px!important; }}
    .place-card-details {{ max-height:none!important; }}
    .tg-page {{ padding:10px 8px 40px!important; }}
}}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;padding:16px 18px 12px;border-bottom:1px solid #e0f2f1;">
        <img src="{LOGO_URL}" style="height:30px;width:auto;">
        <span style="font-size:17px;font-weight:700;color:#00796b;">Tourgram</span>
    </div>""", unsafe_allow_html=True)

    if st.session_state.logged_in:
        user = get_user_by_id(st.session_state.user_id)
        av = avatar_img(st.session_state.username, user.get("avatar_b64","") if user else "", 36)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding:10px 18px;border-bottom:1px solid #e0f2f1;">
            {av}
            <div>
                <div style="font-size:13px;font-weight:700;color:#0f766e;">@{st.session_state.username}</div>
                <div style="font-size:11px;color:#64748b;">✓ Certified</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🏠  Home", key="nav_home"): go("home")
    if st.button("🗺️  Districts", key="nav_dist"): go("district")
    if st.button("📷  Post a Place", key="nav_post"): go("post" if st.session_state.logged_in else "auth")
    if st.session_state.logged_in:
        if st.button("👤  My Profile", key="nav_profile"): go("profile")
        if st.button("🚪  Logout", key="nav_logout"):
            do_logout(); go("home")
    else:
        if st.button("👤  Login / Sign Up", key="nav_login"): go("auth")

    st.markdown(f"<div style='margin-top:40px;padding:0 18px;font-size:12px;color:#90a4ae;'>Discover Nepal's hidden gems 🇳🇵</div>", unsafe_allow_html=True)

# ── TOPBAR ─────────────────────────────────────────────────────────────────────
user_html = f'<span class="tg-userbadge">👤 {st.session_state.username} ✓</span>' if st.session_state.logged_in else ""
st.markdown(f"""
<div class="tg-topbar">
  <div class="tg-brand">
    <img src="{LOGO_URL}" alt="Tourgram">
    <span>Tourgram</span>
  </div>
  {user_html}
</div>""", unsafe_allow_html=True)

# ── PLACE CARD (Community feed inline) ────────────────────────────────────────
def render_place_card(place, allow_edit=False, card_key_prefix=""):
    pid = place["id"]
    reviews = get_reviews(pid)
    up, dn = get_vote_counts(pid)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
    stars_html = "⭐" * int(round(avg_rating)) if reviews else ""

    uname = place["username"].lstrip("u/")
    user_obj = get_user_by_username(uname)
    av_b64 = user_obj.get("avatar_b64","") if user_obj else ""
    av_html = avatar_img(uname, av_b64, 38)

    is_expanded = pid in st.session_state.expanded_cards

    # Determine if right-side content is long enough to need "see more"
    combined_text = (
        place.get("caption","") +
        place.get("history","") +
        place.get("budget","") +
        place.get("safety","") +
        "".join(r["text"] for r in reviews[:2])
    )
    needs_see_more = len(combined_text) > 320

    # Own post
    own_post = st.session_state.logged_in and place.get("user_id") == st.session_state.user_id

    if allow_edit and own_post:
        hc1, hc2 = st.columns([6, 1])
        with hc2:
            st.markdown('<div class="action-menu-btn">', unsafe_allow_html=True)
            if st.button("⋯", key=f"menu_{card_key_prefix}{pid}"):
                current = st.session_state.get(f"menu_open_{pid}", False)
                st.session_state[f"menu_open_{pid}"] = not current
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get(f"menu_open_{pid}", False):
            m1, m2, m3 = st.columns([2,2,6])
            with m1:
                if st.button("✏️ Edit", key=f"edit_{card_key_prefix}{pid}"):
                    st.session_state.editing_place = pid
                    st.session_state[f"menu_open_{pid}"] = False
                    st.rerun()
            with m2:
                st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                if st.button("🗑️ Delete", key=f"del_{card_key_prefix}{pid}"):
                    st.session_state.confirm_delete = pid
                    st.session_state[f"menu_open_{pid}"] = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.confirm_delete == pid:
        st.warning(f"⚠️ Are you sure you want to delete **{place['title']}**? This cannot be undone.")
        cd1, cd2, cd3 = st.columns([1,1,5])
        with cd1:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("Yes, delete", key=f"confirm_del_{pid}"):
                delete_place(pid)
                st.session_state.confirm_delete = None
                st.success("Post deleted.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cd2:
            if st.button("Cancel", key=f"cancel_del_{pid}"):
                st.session_state.confirm_delete = None
                st.rerun()

    if st.session_state.editing_place == pid:
        with st.form(key=f"edit_form_{pid}"):
            st.markdown("**✏️ Edit Post**")
            e_title = st.text_input("Place name", value=place["title"])
            e_district = st.text_input("District", value=place["district"])
            e_caption = st.text_area("Caption", value=place.get("caption",""), height=60)
            e_history = st.text_area("History", value=place.get("history",""), height=70)
            e_budget = st.text_area("Budget", value=place.get("budget",""), height=70)
            e_safety = st.text_area("Safety", value=place.get("safety",""), height=70)
            s1, s2 = st.columns(2)
            with s1:
                save = st.form_submit_button("💾 Save Changes")
            with s2:
                cancel = st.form_submit_button("✕ Cancel")
            if save:
                update_place(pid, e_title, e_district, e_caption, e_history, e_budget, e_safety)
                st.session_state.editing_place = None
                st.success("Post updated!")
                st.rerun()
            if cancel:
                st.session_state.editing_place = None
                st.rerun()
        return

    # Build review HTML (2 max in collapsed, all in expanded)
    review_count = len(reviews)
    caption_html = f'<div class="place-card-caption">{place["caption"]}</div>' if place.get("caption") else ""
    rating_html = f'<div class="rating-badge">{stars_html} {avg_rating:.1f}/5 &nbsp;·&nbsp; {review_count} reviews</div>' if reviews else ""

    show_reviews = reviews if is_expanded else reviews[:2]
    reviews_html = ""
    for r in show_reviews:
        badge = '<span class="badge-cert">✓ Certified</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
        reviews_html += f'<div class="review-bubble"><span class="review-author">{r["author"]}</span>{badge}<p class="review-text">{r["text"]}</p></div>'

    details_class = "place-card-details expanded" if is_expanded else "place-card-details"

    st.markdown(f"""
    <div class="place-card" id="card-{pid}">
      <div class="place-card-img-wrap">
        <img src="{place['image']}" alt="{place['title']}">
      </div>
      <div class="{details_class}">
        <div class="place-card-author">
          {av_html}
          <div>
            <div class="place-card-author-name">@{uname}</div>
            <div class="place-card-author-sub">📍 {place['district']}</div>
          </div>
        </div>
        <div class="place-card-title">{place['title']}</div>
        <div class="place-card-district">{place['district']}</div>
        {caption_html}
        {rating_html}
        <div class="info-label">📜 History</div>
        <div class="info-text">{place.get('history','—')}</div>
        <div class="info-label">💰 Budget</div>
        <div class="info-text">{place.get('budget','—')}</div>
        <div class="info-label">🛡️ Safety</div>
        <div class="info-text">{place.get('safety','—')}</div>
        <div class="info-label">⭐ Reviews</div>
        {reviews_html}
        {"<div style='height:48px'></div>" if needs_see_more and not is_expanded else ""}
      </div>
    </div>""", unsafe_allow_html=True)

    # Vote + see more row
    user_vote = get_user_vote(pid, st.session_state.user_id, st.session_state.session_token)
    v1, v2, v3 = st.columns([1.2, 1.2, 7])
    with v1:
        up_class = "vote-btn-up-active" if user_vote == "up" else "vote-btn-up"
        st.markdown(f'<div class="{up_class}">', unsafe_allow_html=True)
        if st.button(f"▲ {up}", key=f"up_{card_key_prefix}{pid}"):
            cast_vote(pid, "up", st.session_state.user_id, st.session_state.session_token)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with v2:
        dn_class = "vote-btn-dn-active" if user_vote == "down" else "vote-btn-dn"
        st.markdown(f'<div class="{dn_class}">', unsafe_allow_html=True)
        if st.button(f"▼ {dn}", key=f"dn_{card_key_prefix}{pid}"):
            cast_vote(pid, "down", st.session_state.user_id, st.session_state.session_token)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with v3:
        if needs_see_more:
            # Right-aligned see more / see less
            sm_cols = st.columns([6, 1])
            with sm_cols[1]:
                st.markdown('<div class="btn-showmore">', unsafe_allow_html=True)
                label = "See less ▲" if is_expanded else "...See more ▼"
                if st.button(label, key=f"expand_{card_key_prefix}{pid}"):
                    if is_expanded:
                        st.session_state.expanded_cards.discard(pid)
                    else:
                        st.session_state.expanded_cards.add(pid)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # Extra reviews + write review when expanded
    if is_expanded:
        if len(reviews) > 2:
            for r in reviews[2:]:
                badge = '<span class="badge-cert">✓ Certified</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
                st.markdown(f'<div class="review-bubble"><span class="review-author">{r["author"]}</span>{badge}<p class="review-text">{r["text"]}</p></div>', unsafe_allow_html=True)

        with st.form(key=f"rev_form_{card_key_prefix}{pid}", clear_on_submit=True):
            rc1, rc2 = st.columns([4, 1])
            with rc1:
                new_text = st.text_input("Write a review…", label_visibility="collapsed", placeholder="Share your experience…")
            with rc2:
                new_rating = st.selectbox("⭐", [5,4,3,2,1], label_visibility="collapsed")
            submitted = st.form_submit_button("Post Review →")
            if submitted:
                if new_text.strip():
                    author = f"@{st.session_state.username}" if st.session_state.logged_in else "Guest123"
                    insert_review(pid, author, st.session_state.user_id, new_text.strip(), new_rating, 1 if st.session_state.logged_in else 0)
                    st.success("Review posted!")
                    st.rerun()
                else:
                    st.warning("Please write something first.")
        if not st.session_state.logged_in:
            st.caption("💡 Posting as Guest123. Log in for a ✓ Certified badge.")


# ── PLACE DETAIL PAGE (for thumbnail clicks) ───────────────────────────────────
def show_place_detail():
    pid = st.session_state.place_detail_id
    if not pid:
        go("home"); return

    place = get_place_by_id(pid)
    if not place:
        st.error("Place not found."); go("home"); return

    reviews = get_reviews(pid)
    up, dn = get_vote_counts(pid)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
    stars_html = "⭐" * int(round(avg_rating)) if reviews else ""

    uname = place["username"].lstrip("u/")
    user_obj = get_user_by_username(uname)
    av_b64 = user_obj.get("avatar_b64","") if user_obj else ""
    av_html = avatar_img(uname, av_b64, 42)

    is_expanded = f"detail_{pid}" in st.session_state.expanded_cards

    combined_text = (
        place.get("caption","") +
        place.get("history","") +
        place.get("budget","") +
        place.get("safety","") +
        "".join(r["text"] for r in reviews[:2])
    )
    needs_see_more = len(combined_text) > 320

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    back_from = st.session_state.get("place_detail_from", "home")
    if st.button("← Back", key="detail_back"):
        st.session_state.place_detail_id = None
        go(back_from)
    st.markdown('</div>', unsafe_allow_html=True)

    rating_html = f'<div class="rating-badge">{stars_html} {avg_rating:.1f}/5 &nbsp;·&nbsp; {len(reviews)} reviews</div>' if reviews else ""
    caption_html = f'<div class="place-card-caption">{place["caption"]}</div>' if place.get("caption") else ""

    show_reviews = reviews if is_expanded else reviews[:2]
    reviews_html = ""
    for r in show_reviews:
        badge = '<span class="badge-cert">✓ Certified</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
        reviews_html += f'<div class="review-bubble"><span class="review-author">{r["author"]}</span>{badge}<p class="review-text">{r["text"]}</p></div>'

    details_class = "detail-card-details expanded" if is_expanded else "detail-card-details"

    st.markdown(f"""
    <div class="detail-card">
      <div class="detail-card-img-wrap">
        <img src="{place['image']}" alt="{place['title']}">
      </div>
      <div class="{details_class}" style="{'max-height:none;' if is_expanded else ''}">
        <div class="place-card-author">
          {av_html}
          <div>
            <div class="place-card-author-name">@{uname}</div>
            <div class="place-card-author-sub">📍 {place['district']}</div>
          </div>
        </div>
        <div class="place-card-title" style="font-size:24px;">{place['title']}</div>
        <div class="place-card-district">{place['district']}</div>
        {caption_html}
        {rating_html}
        <div class="info-label">📜 History</div>
        <div class="info-text">{place.get('history','—')}</div>
        <div class="info-label">💰 Budget</div>
        <div class="info-text">{place.get('budget','—')}</div>
        <div class="info-label">🛡️ Safety</div>
        <div class="info-text">{place.get('safety','—')}</div>
        <div class="info-label">⭐ Reviews</div>
        {reviews_html}
        {"<div style='height:48px'></div>" if needs_see_more and not is_expanded else ""}
      </div>
    </div>""", unsafe_allow_html=True)

    # Vote + see more
    user_vote = get_user_vote(pid, st.session_state.user_id, st.session_state.session_token)
    v1, v2, v3 = st.columns([1.2, 1.2, 7])
    with v1:
        up_class = "vote-btn-up-active" if user_vote == "up" else "vote-btn-up"
        st.markdown(f'<div class="{up_class}">', unsafe_allow_html=True)
        if st.button(f"▲ {up}", key=f"detail_up_{pid}"):
            cast_vote(pid, "up", st.session_state.user_id, st.session_state.session_token)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with v2:
        dn_class = "vote-btn-dn-active" if user_vote == "down" else "vote-btn-dn"
        st.markdown(f'<div class="{dn_class}">', unsafe_allow_html=True)
        if st.button(f"▼ {dn}", key=f"detail_dn_{pid}"):
            cast_vote(pid, "down", st.session_state.user_id, st.session_state.session_token)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with v3:
        if needs_see_more:
            sm_cols = st.columns([6, 1])
            with sm_cols[1]:
                st.markdown('<div class="btn-showmore">', unsafe_allow_html=True)
                label = "See less ▲" if is_expanded else "...See more ▼"
                if st.button(label, key=f"detail_expand_{pid}"):
                    key = f"detail_{pid}"
                    if is_expanded:
                        st.session_state.expanded_cards.discard(key)
                    else:
                        st.session_state.expanded_cards.add(key)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # All extra reviews + write review always shown on detail page
    if is_expanded and len(reviews) > 2:
        for r in reviews[2:]:
            badge = '<span class="badge-cert">✓ Certified</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
            st.markdown(f'<div class="review-bubble"><span class="review-author">{r["author"]}</span>{badge}<p class="review-text">{r["text"]}</p></div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:14px;font-weight:700;color:#0f766e;margin-bottom:8px;">✍️ Write a Review</div>', unsafe_allow_html=True)
    with st.form(key=f"detail_rev_form_{pid}", clear_on_submit=True):
        rc1, rc2 = st.columns([4, 1])
        with rc1:
            new_text = st.text_input("Your review", label_visibility="collapsed", placeholder="Share your experience…")
        with rc2:
            new_rating = st.selectbox("⭐", [5,4,3,2,1], label_visibility="collapsed")
        submitted = st.form_submit_button("Post Review →")
        if submitted:
            if new_text.strip():
                author = f"@{st.session_state.username}" if st.session_state.logged_in else "Guest123"
                insert_review(pid, author, st.session_state.user_id, new_text.strip(), new_rating, 1 if st.session_state.logged_in else 0)
                st.success("Review posted!")
                st.rerun()
            else:
                st.warning("Please write something first.")
    if not st.session_state.logged_in:
        st.caption("💡 Posting as Guest123. Log in for a ✓ Certified badge.")

    st.markdown('</div>', unsafe_allow_html=True)


# ── HOME ───────────────────────────────────────────────────────────────────────
def show_home():
    places = get_all_places()
    by_id = {p["id"]: p for p in places}
    SECTIONS = [
        ("✨ Recommended for You", ["p1","p2","p3"]),
        ("🔥 Popular Right Now", ["p2","p3","p4","p5"]),
        ("📍 Must Visit", ["p3","p4","p5","p6"]),
        ("⭐ Highest Rated", ["p4","p5","p6","p1"]),
    ]

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    for sec_title, ids in SECTIONS:
        avail = [by_id[i] for i in ids if i in by_id]
        if not avail: continue
        st.markdown(f'<div class="tg-section-title">{sec_title}</div>', unsafe_allow_html=True)
        cols = st.columns(len(avail))
        for i, post in enumerate(avail):
            uname = post["username"].lstrip("u/")
            user_obj = get_user_by_username(uname)
            av_b64 = user_obj.get("avatar_b64","") if user_obj else ""
            with cols[i]:
                st.markdown(f"""
                <div class="tg-card-wrap">
                  <img class="tg-card-img" src="{post['image']}">
                  <div class="tg-card-footer">
                    {avatar_img(uname, av_b64, 24)}
                    <span style="font-size:11px;font-weight:700;color:#0f766e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">@{uname}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                btn_label = post["title"][:22] + ("…" if len(post["title"])>22 else "")
                if st.button(btn_label, key=f"thumb_{sec_title[:3]}_{post['id']}"):
                    st.session_state.place_detail_id = post["id"]
                    st.session_state.place_detail_from = "home"
                    go("place_detail")
        st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div style="font-size:17px;font-weight:700;color:#1a2e2e;margin:20px 0 16px;padding-bottom:10px;border-bottom:2px solid #b2dfdb;">📸 Community Posts</div>', unsafe_allow_html=True)
    for place in places:
        render_place_card(place, allow_edit=True, card_key_prefix="home_")
        st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── AUTH ───────────────────────────────────────────────────────────────────────
def show_auth():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="auth_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

    tab = st.session_state.get("auth_tab","login")

    st.markdown(f"""
    <div style="max-width:440px;margin:20px auto;">
      <div style="text-align:center;margin-bottom:20px;">
        <img src="{LOGO_URL}" style="height:56px;margin-bottom:6px;">
        <div style="font-size:22px;font-weight:800;color:#0f766e;">Tourgram</div>
        <div style="font-size:13px;color:#64748b;">Discover & share Nepal's hidden gems 🇳🇵</div>
      </div>
      <div class="auth-tab-row">
        <div class="auth-tab {'active' if tab=='login' else ''}">🔑 Login</div>
        <div class="auth-tab {'active' if tab=='signup' else ''}">✨ Sign Up</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔑  Login", key="switch_login", use_container_width=True):
            st.session_state.auth_tab = "login"; st.rerun()
    with c2:
        if st.button("✨  Sign Up", key="switch_signup", use_container_width=True):
            st.session_state.auth_tab = "signup"; st.rerun()

    st.markdown("<div style='max-width:440px;margin:0 auto;'>", unsafe_allow_html=True)
    if tab == "login":
        st.markdown("### 👋 Welcome back")
        uname = st.text_input("Username", placeholder="your_username", key="l_uname")
        pw = st.text_input("Password", type="password", placeholder="••••••••", key="l_pw")
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Log In →", key="login_go", use_container_width=True):
            user = get_user_by_username(uname.strip())
            if user and user["password_hash"] == hash_pw(pw):
                do_login(user["id"], user["username"])
                st.success("Welcome back!")
                time.sleep(0.4); go("home")
            else:
                st.error("Incorrect username or password.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin-top:10px;font-size:13px;color:#64748b;'>No account? Click <b>Sign Up</b> above.</div>", unsafe_allow_html=True)
    else:
        st.markdown("### 🚀 Create your account")
        nu = st.text_input("Username *", placeholder="e.g. rajan_travels", key="s_uname")
        ne = st.text_input("Email address *", placeholder="you@example.com", key="s_email")
        np1 = st.text_input("Password *", type="password", placeholder="Min 6 characters", key="s_pw1")
        np2 = st.text_input("Confirm password *", type="password", placeholder="Repeat password", key="s_pw2")
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Create Account →", key="signup_go", use_container_width=True):
            errors = []
            if not nu.strip(): errors.append("Username is required.")
            if not ne.strip() or "@" not in ne: errors.append("Valid email is required.")
            if len(np1) < 6: errors.append("Password must be at least 6 characters.")
            if np1 != np2: errors.append("Passwords do not match.")
            if errors:
                for e in errors: st.error(e)
            else:
                if get_user_by_username(nu.strip()): st.error("Username already taken.")
                elif get_user_by_email(ne.strip()): st.error("Email already registered.")
                else:
                    uid = create_user(nu.strip(), ne.strip(), np1)
                    if uid:
                        do_login(uid, nu.strip())
                        st.success("Welcome to Tourgram! 🎉")
                        time.sleep(0.5); go("home")
                    else:
                        st.error("Something went wrong. Try again.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin-top:10px;font-size:13px;color:#64748b;'>Already have an account? Click <b>Login</b> above.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── PROFILE ────────────────────────────────────────────────────────────────────
def show_profile():
    if not st.session_state.logged_in:
        go("auth"); return

    user = get_user_by_id(st.session_state.user_id)
    uname = st.session_state.username
    all_places = get_all_places()
    my_places = [p for p in all_places if p["username"].lstrip("u/") == uname]

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="prof_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

    av_b64 = user.get("avatar_b64","") if user else ""
    av_html = avatar_img(uname, av_b64, 76)

    st.markdown(f"""
    <div class="profile-header">
      {av_html}
      <div style="flex:1;">
        <div style="font-size:22px;font-weight:800;color:#0f766e;">@{uname}</div>
        <div style="font-size:13px;color:#475569;margin-top:3px;">{user.get('bio','No bio yet.') if user else ''}</div>
        <div style="display:flex;gap:28px;margin-top:12px;">
          <div class="profile-stat"><div class="profile-stat-num">{len(my_places)}</div><div class="profile-stat-label">Posts</div></div>
          <div class="profile-stat"><div class="profile-stat-num">✓</div><div class="profile-stat-label">Certified</div></div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    with st.expander("✏️ Edit Profile", expanded=False):
        st.markdown("**Profile Photo**")
        st.caption("Upload a photo from your computer:")
        uploaded = st.file_uploader("Choose photo", type=["jpg","jpeg","png","webp"], key="prof_upload", label_visibility="collapsed")
        new_b64 = av_b64
        if uploaded:
            raw = uploaded.getvalue()
            ext = uploaded.name.rsplit(".",1)[-1].lower()
            mime = "image/jpeg" if ext in ("jpg","jpeg") else f"image/{ext}"
            new_b64 = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
            st.image(uploaded, width=80, caption="Preview")
        elif av_b64 and av_b64.startswith("data:image"):
            st.image(av_b64, width=60, caption="Current photo")
        else:
            st.markdown(avatar_img(uname, "", 60), unsafe_allow_html=True)
            st.caption("Auto-generated avatar (upload a photo above to replace)")

        new_bio = st.text_area("Bio", value=user.get("bio","") if user else "", placeholder="Tell the community about yourself…", key="prof_bio", height=80)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Save Profile", key="save_prof"):
            update_user_profile(st.session_state.user_id, new_b64, new_bio.strip())
            st.success("Profile updated!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="tg-section-title">📸 My Posts ({len(my_places)})</div>', unsafe_allow_html=True)
    if my_places:
        for place in my_places:
            render_place_card(place, allow_edit=True, card_key_prefix="prof_")
            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.info("You haven't posted any places yet. Use 'Post a Place' to get started!")
    st.markdown('</div>', unsafe_allow_html=True)


# ── POST ───────────────────────────────────────────────────────────────────────
def show_post():
    if not st.session_state.logged_in:
        show_auth(); return

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="post_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="title-banner">
      <h2>📷 Share a Place</h2>
      <div style="color:#0d9488;font-size:13px;margin-top:4px;">Your post will appear in the community feed</div>
    </div>""", unsafe_allow_html=True)

    form_col, preview_col = st.columns([3, 2], gap="large")

    if "post_image_b64" not in st.session_state:
        st.session_state.post_image_b64 = ""
    if "post_image_url" not in st.session_state:
        st.session_state.post_image_url = ""

    with form_col:
        st.markdown('<div class="post-step-label">① Photo</div>', unsafe_allow_html=True)
        st.markdown('<div class="post-section-card">', unsafe_allow_html=True)
        photo_mode = st.radio("", ["📁 Upload from computer","🔗 Paste a URL"], horizontal=True, key="post_photo_mode")

        if photo_mode == "📁 Upload from computer":
            uploaded_file = st.file_uploader("Choose image", type=["jpg","jpeg","png","webp"], key="post_upload", label_visibility="collapsed")
            if uploaded_file:
                raw = uploaded_file.getvalue()
                ext = uploaded_file.name.rsplit(".",1)[-1].lower()
                mime = "image/jpeg" if ext in ("jpg","jpeg") else f"image/{ext}"
                st.session_state.post_image_b64 = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
                st.session_state.post_image_url = ""
                st.image(uploaded_file, use_container_width=True)
            else:
                st.session_state.post_image_b64 = ""
        else:
            img_url_input = st.text_input("Image URL", placeholder="https://example.com/photo.jpg", key="post_img_url_input", label_visibility="collapsed")
            if img_url_input.strip():
                st.session_state.post_image_url = img_url_input.strip()
                st.session_state.post_image_b64 = ""
                st.image(img_url_input.strip(), use_container_width=True)
            else:
                st.session_state.post_image_url = ""
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="post-step-label">② Place Details</div>', unsafe_allow_html=True)
        st.markdown('<div class="post-section-card">', unsafe_allow_html=True)
        title = st.text_input("Place name *", placeholder="e.g. Gosaikunda Lake", key="post_title")
        district = st.text_input("District *", placeholder="e.g. Rasuwa", key="post_district")
        caption = st.text_area("Caption", placeholder="What makes this place special?", key="post_caption", height=70)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="post-step-label">③ Traveller Info</div>', unsafe_allow_html=True)
        st.markdown('<div class="post-section-card">', unsafe_allow_html=True)
        history = st.text_area("📜 History & background", placeholder="Tell the story of this place…", key="post_history", height=70)
        budget = st.text_area("💰 Budget tips", placeholder="Entry fees, transport costs…", key="post_budget", height=70)
        safety = st.text_area("🛡️ Safety info", placeholder="Best season, warnings?", key="post_safety", height=70)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="post-step-label">④ Initial Review</div>', unsafe_allow_html=True)
        st.markdown('<div class="post-section-card">', unsafe_allow_html=True)
        star_map = {"⭐⭐⭐⭐⭐ Excellent":5,"⭐⭐⭐⭐ Great":4,"⭐⭐⭐ Good":3,"⭐⭐ Fair":2,"⭐ Poor":1}
        star_choice = st.selectbox("Rating", list(star_map.keys()), key="post_stars")
        star_value = star_map[star_choice]
        review_text = st.text_area("Your experience", placeholder="Share your personal experience…", key="post_review_text", height=70)
        st.markdown("</div>", unsafe_allow_html=True)

        final_image = st.session_state.post_image_b64 or st.session_state.post_image_url or "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Himalaya_annotated.jpg/1280px-Himalaya_annotated.jpg"

        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Publish Post ✓", key="publish_btn", use_container_width=True):
            errors = []
            if not title.strip(): errors.append("Place name is required.")
            if not district.strip(): errors.append("District is required.")
            if errors:
                for e in errors: st.error(e)
            else:
                new_id = "p" + str(uuid.uuid4())[:8]
                insert_place({
                    "id": new_id, "user_id": st.session_state.user_id,
                    "username": f"u/{st.session_state.username}",
                    "title": title.strip(), "district": district.strip(),
                    "image": final_image, "caption": caption.strip(),
                    "history": history.strip() or "No history provided.",
                    "budget": budget.strip() or "No budget info provided.",
                    "safety": safety.strip() or "No safety info provided.",
                    "stars": star_value,
                })
                if review_text.strip():
                    insert_review(new_id, f"@{st.session_state.username}", st.session_state.user_id,
                                  review_text.strip(), star_value, 1)
                st.session_state.post_image_b64 = ""
                st.session_state.post_image_url = ""
                st.success("🎉 Post published!")
                st.balloons()
                time.sleep(0.5); go("home")
        st.markdown('</div>', unsafe_allow_html=True)

    with preview_col:
        st.markdown('<div class="post-step-label">Live Preview</div>', unsafe_allow_html=True)
        preview_title = st.session_state.get("post_title","").strip() or "Place Name"
        preview_district = st.session_state.get("post_district","").strip() or "District"
        preview_caption = st.session_state.get("post_caption","").strip()
        user = get_user_by_id(st.session_state.user_id)
        av_b64 = user.get("avatar_b64","") if user else ""
        preview_img = st.session_state.post_image_b64 or st.session_state.post_image_url or "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Himalaya_annotated.jpg/1280px-Himalaya_annotated.jpg"

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e0f2f1;border-radius:14px;overflow:hidden;box-shadow:0 2px 12px rgba(0,128,128,0.07);">
          <img src="{preview_img}" style="width:100%;height:190px;object-fit:cover;display:block;">
          <div style="padding:14px 16px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
              {avatar_img(st.session_state.username, av_b64, 34)}
              <div>
                <div style="font-size:12px;font-weight:700;color:#0f766e;">@{st.session_state.username}</div>
                <div style="font-size:11px;color:#64748b;">📍 {preview_district}</div>
              </div>
            </div>
            <div style="font-size:15px;font-weight:800;color:#1a2e2e;">{preview_title}</div>
            {"<div style='font-size:12px;color:#475569;font-style:italic;margin-top:5px;padding:6px 10px;background:#f0fdfa;border-radius:6px;border-left:2px solid #14b8a6;'>" + preview_caption + "</div>" if preview_caption else ""}
            <div style="font-size:11px;color:#94a3b8;margin-top:8px;">Fill in the form on the left to update ↗</div>
          </div>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── DISTRICT ───────────────────────────────────────────────────────────────────
def show_district():
    places = get_all_places()
    EMOJIS = {"Kaski":"🏔️","Kathmandu":"🕌","Chitwan":"🦏","Mugu":"🌊"}
    districts = sorted(set(p["district"] for p in places))

    if st.session_state.selected_district:
        d = st.session_state.selected_district
        dist_places = [p for p in places if p["district"] == d]
        st.markdown('<div class="tg-page">', unsafe_allow_html=True)
        st.markdown('<div class="btn-back">', unsafe_allow_html=True)
        if st.button("← Back to Districts", key="dist_inner_back"):
            st.session_state.selected_district = None; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="title-banner">
          <h2>{EMOJIS.get(d,'📍')} {d}</h2>
          <div style="color:#0d9488;font-size:13px;">{len(dist_places)} place{'s' if len(dist_places)!=1 else ''}</div>
        </div>""", unsafe_allow_html=True)
        for place in dist_places:
            render_place_card(place, allow_edit=True, card_key_prefix=f"dist_{d}_")
            st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="dist_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#00796b;margin-top:0;">🗺️ Districts</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#607d8b;font-size:14px;margin-bottom:20px;">Browse tourist spots by district.</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, d in enumerate(districts):
        count = sum(1 for p in places if p["district"] == d)
        with cols[i % 4]:
            st.markdown(f"""
            <div class="tg-district-card">
              <div style="font-size:36px;">{EMOJIS.get(d,'📍')}</div>
              <div style="font-size:15px;font-weight:700;color:#00796b;margin-top:8px;">{d}</div>
              <div style="font-size:12px;color:#607d8b;margin-top:4px;">{count} place{'s' if count!=1 else ''}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Explore {d} →", key=f"dist_{d}"):
                st.session_state.selected_district = d; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── ROUTER ─────────────────────────────────────────────────────────────────────
page = st.session_state.page
if page == "home":          show_home()
elif page == "auth":        show_auth()
elif page == "post":        show_post()
elif page == "district":    show_district()
elif page == "profile":     show_profile()
elif page == "place_detail": show_place_detail()
