import streamlit as st
import uuid

st.set_page_config(
    page_title="Tourgram",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLACES = [
    {
        "id": "p1", "user": "u/rajan_travels", "title": "Phewa Lake",
        "district": "Kaski",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Phewa_lake.jpg/1280px-Phewa_lake.jpg",
        "history": "Phewa Lake is the second largest lake in Nepal, located in Pokhara. It has been a hub for travellers for centuries, with the iconic Tal Barahi Temple sitting on a small island at its centre.",
        "budget": "Entry free. Boat rides from NPR 500/hr. Rowboats available for self-rowing.",
        "safety": "Very safe. Lifeguards present during peak hours. Avoid during heavy rain season.",
        "reviews": [
            {"text": "Absolutely stunning at sunrise!", "user": "u/guest", "certified": False},
            {"text": "Best sunrise I've ever seen. The reflection of Machhapuchhre is unreal.", "user": "u/sara_wanderer", "certified": True},
        ],
    },
    {
        "id": "p2", "user": "u/anita_explorer", "title": "Pashupatinath Temple",
        "district": "Kathmandu",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Pashupatinath_temple.jpg/1280px-Pashupatinath_temple.jpg",
        "history": "One of the most sacred Hindu temples in the world, dating back to the 5th century. Dedicated to Lord Shiva, it sits on the banks of the Bagmati River.",
        "budget": "Foreign nationals: NPR 1000 entry. Locals: free. Best visited early morning.",
        "safety": "Safe. Follow dress code rules inside. Non-Hindus cannot enter the main temple.",
        "reviews": [
            {"text": "Spiritual and deeply peaceful experience.", "user": "u/deepak_lens", "certified": True},
            {"text": "Must visit during Shivaratri — incredible atmosphere.", "user": "u/guest", "certified": False},
        ],
    },
    {
        "id": "p3", "user": "u/bikram_hikes", "title": "Annapurna Base Camp",
        "district": "Kaski",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Annapurna_Base_Camp.jpg/1280px-Annapurna_Base_Camp.jpg",
        "history": "At 4,130m, ABC is one of the most iconic trekking destinations in the world. Surrounded by peaks over 7,000m, it offers a 360° amphitheatre of the Himalayas.",
        "budget": "Trek permits: NPR 3000. Guide recommended: NPR 2500/day. 7–12 day round trip.",
        "safety": "Altitude sickness risk. Acclimatise properly. Do not rush the ascent.",
        "reviews": [
            {"text": "Life-changing trek. Nothing prepares you for that view.", "user": "u/bikram_hikes", "certified": True},
        ],
    },
    {
        "id": "p4", "user": "u/sara_wanderer", "title": "Chitwan National Park",
        "district": "Chitwan",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/One_horned_rhino_chitwan.jpg/1280px-One_horned_rhino_chitwan.jpg",
        "history": "UNESCO World Heritage Site. Home to one-horned rhinos and Bengal tigers. One of the best wildlife parks in Asia, established in 1973.",
        "budget": "Entry: NPR 1500. Jeep safari: NPR 2500. Elephant breeding centre: NPR 500.",
        "safety": "Stay with guides at all times. Do not wander alone near the jungle edges.",
        "reviews": [
            {"text": "Saw a rhino up close — absolutely incredible!", "user": "u/mina_clicks", "certified": True},
        ],
    },
    {
        "id": "p5", "user": "u/deepak_lens", "title": "Boudhanath Stupa",
        "district": "Kathmandu",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Boudha_stupa.jpg/1280px-Boudha_stupa.jpg",
        "history": "One of the largest stupas in the world and a centre of Tibetan Buddhism in Nepal. The all-seeing eyes of Buddha watch over the valley from every angle.",
        "budget": "Entry: NPR 400 for foreigners. Best visited at dawn or dusk for the butter lamp ceremony.",
        "safety": "Very safe. Busy tourist area. Watch out for pickpockets in crowd.",
        "reviews": [
            {"text": "Peaceful and majestic. The evening kora is magical.", "user": "u/guest", "certified": False},
        ],
    },
    {
        "id": "p6", "user": "u/mina_clicks", "title": "Rara Lake",
        "district": "Mugu",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Rara_Lake.jpg/1280px-Rara_Lake.jpg",
        "history": "Nepal's largest lake, hidden in the remote Karnali region at 2,990m elevation. Crystal-clear blue waters surrounded by dense forests — one of Nepal's best-kept secrets.",
        "budget": "Flight to Talcha: ~NPR 15,000. Trek + permits extra. Very limited accommodation nearby.",
        "safety": "Remote area. Go with an experienced guide. Very limited phone signal.",
        "reviews": [
            {"text": "Pure paradise. Worth every rupee and every step.", "user": "u/rajan_travels", "certified": True},
        ],
    },
]

SECTIONS = [
    ("✨ Recommended for You", ["p1","p2","p3"]),
    ("🔥 Popular Right Now",   ["p2","p3","p4","p5"]),
    ("📍 Must Visit",          ["p3","p4","p5","p6"]),
    ("⭐ Highest Rated",       ["p4","p5","p6","p1"]),
]

def init():
    defaults = {
        "page": "home",
        "selected_place": None,
        "logged_in": False,
        "username": "",
        "posts": [dict(p) for p in PLACES],
        "votes": {p["id"]: {"up": 0, "down": 0} for p in PLACES},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

for p in st.session_state.posts:
    if p["id"] not in st.session_state.votes:
        st.session_state.votes[p["id"]] = {"up": 0, "down": 0}

def go(page, place=None):
    st.session_state.page = page
    st.session_state.selected_place = place
    st.rerun()

def post_by_id(pid):
    return next((p for p in st.session_state.posts if p["id"] == pid), None)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp, body { background: #f0fafa !important; }

#MainMenu, footer, header { visibility: hidden !important; }
div[data-testid="stDecoration"],
div[data-testid="stToolbar"] { display: none !important; }

/* ── PERMANENTLY LOCK THE SIDEBAR OPEN ── */
/* Hide every button that could collapse the sidebar */
button[data-testid="collapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] button[kind="header"],
.st-emotion-cache-1rs6os,
.st-emotion-cache-czk5ss {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* Sidebar always visible, no transform */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 2px solid #b2dfdb !important;
    min-width: 230px !important;
    max-width: 230px !important;
    transform: none !important;
    transition: none !important;
}
section[data-testid="stSidebar"] > div {
    background: #ffffff !important;
    padding: 0 !important;
    transform: none !important;
}
section[data-testid="stSidebar"] .block-container { padding: 0 !important; }
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 8px 8px 0 !important;
    color: #1a2e2e !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 11px 18px !important;
    margin-bottom: 2px !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #e0f2f1 !important;
    border-left-color: #00897b !important;
    color: #00796b !important;
}

.block-container { padding: 0 !important; max-width: 100% !important; }

/* Topbar */
.tg-topbar {
    display: flex; align-items: center; gap: 12px;
    background: #ffffff; border-bottom: 1.5px solid #b2dfdb;
    padding: 13px 28px;
    box-shadow: 0 1px 6px rgba(0,128,128,0.08);
}
.tg-brand { font-size: 20px; font-weight: 700; color: #00796b; flex: 1; }
.tg-userbadge {
    font-size: 13px; font-weight: 600; color: #00796b;
    background: #e0f2f1; padding: 5px 14px; border-radius: 20px;
}

.tg-page { padding: 12px 28px 60px; }
.tg-section-title { font-size: 16px; font-weight: 700; color: #00796b; margin: 22px 0 12px; }

.tg-card-img { width: 100%; height: 130px; object-fit: cover; border-radius: 10px 10px 0 0; display: block; }
.tg-card-wrap {
    background: #fff; border: 1px solid #e0f2f1; border-radius: 12px;
    overflow: hidden; box-shadow: 0 1px 6px rgba(0,128,128,0.06); margin-bottom: 4px;
}

/* Feed cards */
.tg-feed-card {
    background: #fff; border: 1px solid #e0f2f1; border-radius: 14px;
    overflow: hidden; margin-bottom: 20px;
    box-shadow: 0 1px 6px rgba(0,128,128,0.06);
}
.tg-feed-meta { padding: 10px 14px 4px; font-size: 13px; font-weight: 700; color: #00796b; }
.tg-feed-title { padding: 4px 14px 8px; font-size: 15px; font-weight: 600; color: #1a2e2e; }

/* Community posts subheader */
.tg-community-header {
    font-size: 18px; font-weight: 700; color: #1a2e2e;
    margin: 32px 0 16px; padding-bottom: 10px;
    border-bottom: 2px solid #b2dfdb;
}

/* Detail */
.tg-detail-img { width:100%; height:360px; object-fit:cover; border-radius:14px; display:block; margin-bottom:14px; }
.tg-user-tag { font-size:13px; font-weight:700; color:#00796b; margin-bottom:4px; }
.tg-place-title { font-size:26px; font-weight:700; color:#1a2e2e; margin:0 0 14px; }
.tg-info-box { background:#fff; border:1px solid #e0f2f1; border-radius:10px; padding:14px 18px; margin-bottom:12px; }
.tg-info-label { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#00897b; margin-bottom:6px; }
.tg-info-text { font-size:14px; line-height:1.75; color:#2d4a4a; }
.badge-cert { background:#e0f2f1; color:#00796b; font-size:10px; font-weight:700; padding:2px 8px; border-radius:10px; margin-left:6px; }
.badge-guest { background:#f5f5f5; color:#999; font-size:10px; font-weight:600; padding:2px 8px; border-radius:10px; margin-left:6px; }
.review-row { padding:10px 0; border-bottom:1px solid #f0fafa; }
.review-username { font-size:13px; font-weight:700; color:#00796b; }
.review-text { font-size:14px; color:#2d4a4a; margin:4px 0 0; }

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    transition: all .15s !important;
}
.btn-primary .stButton > button {
    background: #00897b !important; color: #fff !important; border: none !important;
}
.btn-primary .stButton > button:hover { background: #006960 !important; }
.btn-back .stButton > button {
    background: #fff !important; border: 1px solid #b2dfdb !important; color: #00796b !important;
}
.vote-up .stButton > button {
    background: #e0f2f1 !important; border: 1px solid #80cbc4 !important; color: #00796b !important;
}
.vote-dn .stButton > button {
    background: #fff0f0 !important; border: 1px solid #ffcdd2 !important; color: #c62828 !important;
}

.tg-login-box {
    max-width: 420px; margin: 40px auto;
    background: #fff; border: 1px solid #e0f2f1;
    border-radius: 16px; padding: 32px 28px;
    box-shadow: 0 2px 16px rgba(0,128,128,0.08);
}
.tg-district-card {
    background:#fff; border:1px solid #e0f2f1; border-radius:12px;
    padding:20px 16px; text-align:center;
    box-shadow:0 1px 6px rgba(0,128,128,0.06); margin-bottom:4px;
}

hr { border:none; border-top:1px solid #e0f2f1; margin:18px 0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;padding:18px 18px 14px;border-bottom:1px solid #e0f2f1;">
        <span style="font-size:22px;">📷</span>
        <span style="font-size:18px;font-weight:700;color:#00796b;">Tourgram</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(f"""
        <div style="padding:10px 18px 12px;border-bottom:1px solid #e0f2f1;font-size:13px;color:#00796b;font-weight:600;">
            👤 {st.session_state.username}
            <span style="background:#e0f2f1;padding:2px 7px;border-radius:10px;font-size:11px;margin-left:6px;">✓ Certified</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if st.button("🏠  Home",             key="nav_home"): go("home")
    if st.button("🗺️  Districts",        key="nav_dist"): go("district")
    if st.button("📷  Post a Place",     key="nav_post"): go("post" if st.session_state.logged_in else "login")

    if st.session_state.logged_in:
        if st.button("🚪  Logout", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            go("home")
    else:
        if st.button("👤  Login / Sign Up", key="nav_login"): go("login")

    st.markdown("""
    <div style="margin-top:40px;padding:0 18px;font-size:12px;color:#90a4ae;">
        Discover Nepal's hidden gems 🇳🇵
    </div>
    """, unsafe_allow_html=True)

# ── TOPBAR ─────────────────────────────────────────────────────────────────────
user_html = f'<span class="tg-userbadge">👤 {st.session_state.username} ✓</span>' if st.session_state.logged_in else ""
st.markdown(f"""
<div class="tg-topbar">
    <div class="tg-brand">📷 Tourgram</div>
    {user_html}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DETAIL VIEW
# ══════════════════════════════════════════════════════════════════════════════
def show_detail(post):
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)

    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="back_detail"):
        st.session_state.selected_place = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="tg-user-tag">{post["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tg-place-title">{post["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<img class="tg-detail-img" src="{post["image"]}" />', unsafe_allow_html=True)

    vid = post["id"]
    v   = st.session_state.votes[vid]
    c1, c2, c3 = st.columns([1.4, 1.6, 5])
    with c1:
        st.markdown('<div class="vote-up">', unsafe_allow_html=True)
        if st.button(f"▲  Upvote  {v['up']}", key=f"up_{vid}"):
            st.session_state.votes[vid]["up"] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="vote-dn">', unsafe_allow_html=True)
        if st.button(f"▼  Downvote  {v['down']}", key=f"dn_{vid}"):
            st.session_state.votes[vid]["down"] += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<span style="font-size:13px;color:#607d8b;line-height:2.6;display:block;">📍 {post["district"]}</span>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    for label, key in [("📜 History","history"),("💰 Budget","budget"),("🛡️ Safety","safety")]:
        st.markdown(f"""
        <div class="tg-info-box">
            <div class="tg-info-label">{label}</div>
            <div class="tg-info-text">{post[key]}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="tg-info-box"><div class="tg-info-label">⭐ Reviews</div>', unsafe_allow_html=True)
    for r in post["reviews"]:
        badge = '<span class="badge-cert">✓ Certified</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
        st.markdown(f"""
        <div class="review-row">
            <span class="review-username">{r['user']}</span>{badge}
            <p class="review-text">{r['text']}</p>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    new_rev = st.text_input("✍️ Write a review", placeholder="Share your experience…", key=f"rev_{vid}")
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Submit Review", key=f"rev_sub_{vid}"):
        if new_rev.strip():
            reviewer = f"u/{st.session_state.username}" if st.session_state.logged_in else "u/guest"
            for p in st.session_state.posts:
                if p["id"] == vid:
                    p["reviews"].append({"text": new_rev.strip(), "user": reviewer, "certified": st.session_state.logged_in})
            st.success("Review submitted!"); st.rerun()
        else:
            st.warning("Please write something first.")
    st.markdown('</div>', unsafe_allow_html=True)
    if not st.session_state.logged_in:
        st.caption("💡 Log in to earn a ✓ Certified badge on your review.")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
def show_home():
    if st.session_state.selected_place:
        post = post_by_id(st.session_state.selected_place)
        if post:
            show_detail(post); return

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    by_id = {p["id"]: p for p in st.session_state.posts}

    # ── Curated sections ──
    for sec_title, ids in SECTIONS:
        st.markdown(f'<div class="tg-section-title">{sec_title}</div>', unsafe_allow_html=True)
        items = [by_id[i] for i in ids if i in by_id]
        cols  = st.columns(len(items))
        for i, post in enumerate(items):
            with cols[i]:
                st.markdown(f'<div class="tg-card-wrap"><img class="tg-card-img" src="{post["image"]}" /></div>', unsafe_allow_html=True)
                if st.button(post["title"], key=f"card_{sec_title[:3]}_{post['id']}"):
                    st.session_state.selected_place = post["id"]; st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)

    # ── Community Posts subheader ──
    st.markdown('<div class="tg-community-header">📸 Community Posts</div>', unsafe_allow_html=True)

    for post in st.session_state.posts:
        vid = post["id"]
        v   = st.session_state.votes[vid]
        st.markdown(f"""
        <div class="tg-feed-card">
            <div class="tg-feed-meta">{post['user']}  ·  {post['district']}</div>
            <img src="{post['image']}" style="width:100%;height:240px;object-fit:cover;display:block;" />
            <div class="tg-feed-title">{post['title']}</div>
        </div>""", unsafe_allow_html=True)

        fc1, fc2, fc3 = st.columns([1.2, 1.4, 3])
        with fc1:
            st.markdown('<div class="vote-up">', unsafe_allow_html=True)
            if st.button(f"▲  {v['up']}", key=f"f_up_{vid}"):
                st.session_state.votes[vid]["up"] += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with fc2:
            st.markdown('<div class="vote-dn">', unsafe_allow_html=True)
            if st.button(f"▼  {v['down']}", key=f"f_dn_{vid}"):
                st.session_state.votes[vid]["down"] += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with fc3:
            st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
            if st.button("View Details →", key=f"f_view_{vid}"):
                st.session_state.selected_place = vid; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:6px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="login_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="tg-login-box">
        <div style="font-size:22px;font-weight:700;color:#00796b;margin-bottom:4px;">👤 Login / Sign Up</div>
        <div style="font-size:14px;color:#607d8b;margin-bottom:8px;">Join Tourgram to post places and earn your Certified badge.</div>
    </div>
    """, unsafe_allow_html=True)

    uname = st.text_input("Username", placeholder="e.g. rajan_travels", key="login_uname")
    st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Login / Sign Up →", key="login_submit"):
        if uname.strip():
            st.session_state.logged_in = True
            st.session_state.username  = uname.strip()
            go("home")
        else:
            st.error("Please enter a username.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Any username works — this is a demo 🇳🇵")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# POST
# ══════════════════════════════════════════════════════════════════════════════
def show_post():
    if not st.session_state.logged_in:
        show_login(); return

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="post_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h2 style="color:#00796b;margin-top:10px;">📷 Post a Place</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#607d8b;font-size:14px;margin-bottom:16px;">Share a tourist spot with the Tourgram community.</p>', unsafe_allow_html=True)

    title    = st.text_input("Place Name *",  placeholder="e.g. Gosaikunda Lake")
    district = st.text_input("District *",    placeholder="e.g. Rasuwa")
    image    = st.text_input("Image URL",     placeholder="https://...")
    history  = st.text_area("History",        placeholder="Tell us the history of this place…")
    budget   = st.text_area("Budget Tips",    placeholder="Entry fees, transport costs…")
    safety   = st.text_area("Safety Info",    placeholder="Is it safe? Any warnings?")

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("Publish Post ✓", key="publish_btn"):
        if not title.strip() or not district.strip():
            st.error("Place name and district are required.")
        else:
            new_id = "p" + str(uuid.uuid4())[:8]
            st.session_state.posts.insert(0, {
                "id": new_id,
                "user": f"u/{st.session_state.username}",
                "title": title.strip(), "district": district.strip(),
                "image": image.strip() or "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Boudha_stupa.jpg/1280px-Boudha_stupa.jpg",
                "history": history.strip() or "No history provided.",
                "budget":  budget.strip()  or "No budget info provided.",
                "safety":  safety.strip()  or "No safety info provided.",
                "reviews": [],
            })
            st.session_state.votes[new_id] = {"up": 0, "down": 0}
            st.success("🎉 Post published!")
            go("home")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DISTRICT
# ══════════════════════════════════════════════════════════════════════════════
def show_district():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    st.markdown('<div class="btn-back">', unsafe_allow_html=True)
    if st.button("← Back", key="dist_back"): go("home")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h2 style="color:#00796b;margin-top:0;">🗺️ Districts</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#607d8b;font-size:14px;margin-bottom:20px;">Browse tourist spots by district.</p>', unsafe_allow_html=True)

    EMOJIS = {"Kaski":"🏔️","Kathmandu":"🕌","Chitwan":"🦏","Mugu":"🌊"}
    districts = sorted(set(p["district"] for p in st.session_state.posts))
    cols = st.columns(4)
    for i, d in enumerate(districts):
        count = sum(1 for p in st.session_state.posts if p["district"] == d)
        with cols[i % 4]:
            st.markdown(f"""
            <div class="tg-district-card">
                <div style="font-size:36px;">{EMOJIS.get(d,'📍')}</div>
                <div style="font-size:15px;font-weight:700;color:#00796b;margin-top:8px;">{d}</div>
                <div style="font-size:12px;color:#607d8b;margin-top:4px;">{count} place{'s' if count!=1 else ''}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<p style="font-size:13px;color:#90a4ae;margin-top:32px;text-align:center;">More district content coming from your team 🇳🇵</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── ROUTER ─────────────────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "home":     show_home()
elif page == "login":    show_login()
elif page == "post":     show_post()
elif page == "district": show_district()
