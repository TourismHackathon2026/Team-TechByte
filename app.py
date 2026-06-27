import streamlit as st
import os
from PIL import Image

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tourgram",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state defaults ────────────────────────────────────────────────────
def init_state():
    defaults = {
        "selected_place": None,
        "votes": {},
        "logged_in": False,
        "username": "",
        "page": "home",
        "posts": [
            {
                "id": "p1", "user": "u/rajan_travels", "title": "Phewa Lake at Sunrise",
                "image": None, "district": "Kaski",
                "history": "Phewa Lake is the second largest lake in Nepal, located in Pokhara. It has been a hub for travellers for centuries.",
                "budget": "Entry free. Boat rides from NPR 500/hr.",
                "safety": "Very safe. Lifeguards present during peak hours.",
                "reviews": [
                    {"text": "Absolutely stunning!", "user": "u/guest", "certified": False},
                    {"text": "Best sunrise I've ever seen.", "user": "u/sara_wanderer", "certified": True},
                ],
            },
            {
                "id": "p2", "user": "u/anita_explorer", "title": "Pashupatinath Temple",
                "image": None, "district": "Kathmandu",
                "history": "One of the most sacred Hindu temples in the world, dating back to the 5th century.",
                "budget": "Foreign nationals: NPR 1000 entry. Locals: free.",
                "safety": "Safe. Follow dress code rules inside.",
                "reviews": [
                    {"text": "Spiritual and peaceful.", "user": "u/deepak_lens", "certified": True},
                    {"text": "Must visit during Shivaratri.", "user": "u/guest", "certified": False},
                ],
            },
            {
                "id": "p3", "user": "u/bikram_hikes", "title": "Annapurna Base Camp",
                "image": None, "district": "Kaski",
                "history": "At 4,130m, ABC is one of the most iconic trekking destinations in the world.",
                "budget": "Trek permits: NPR 3000. Guide recommended.",
                "safety": "Altitude sickness risk. Acclimatise properly.",
                "reviews": [
                    {"text": "Life-changing trek.", "user": "u/bikram_hikes", "certified": True},
                ],
            },
            {
                "id": "p4", "user": "u/sara_wanderer", "title": "Chitwan National Park",
                "image": None, "district": "Chitwan",
                "history": "UNESCO World Heritage Site. Home to one-horned rhinos and Bengal tigers.",
                "budget": "Entry: NPR 1500. Jeep safari: NPR 2500.",
                "safety": "Stay with guides. Do not wander alone.",
                "reviews": [
                    {"text": "Saw a rhino up close!", "user": "u/mina_clicks", "certified": True},
                ],
            },
            {
                "id": "p5", "user": "u/deepak_lens", "title": "Boudhanath Stupa",
                "image": None, "district": "Kathmandu",
                "history": "One of the largest stupas in the world, a centre of Tibetan Buddhism in Nepal.",
                "budget": "Entry: NPR 400 for foreigners.",
                "safety": "Very safe. Busy tourist area.",
                "reviews": [
                    {"text": "Peaceful and majestic.", "user": "u/guest", "certified": False},
                ],
            },
            {
                "id": "p6", "user": "u/mina_clicks", "title": "Rara Lake",
                "image": None, "district": "Mugu",
                "history": "Nepal's largest lake, hidden in the remote Karnali region at 2,990m elevation.",
                "budget": "Flight to Talcha: ~NPR 15,000. Trek + permits extra.",
                "safety": "Remote area. Go with an experienced guide.",
                "reviews": [
                    {"text": "Pure paradise.", "user": "u/rajan_travels", "certified": True},
                ],
            },
        ],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

for post in st.session_state.posts:
    if post["id"] not in st.session_state.votes:
        st.session_state.votes[post["id"]] = {"up": 0, "down": 0}

# ── Logo helper ───────────────────────────────────────────────────────────────
def logo_b64(height=34):
    if os.path.exists("logo.png"):
        import base64
        with open("logo.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<img src="data:image/png;base64,{b64}" style="height:{height}px;border-radius:6px;vertical-align:middle;" />'
    return '📷'

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], [class*="st-"] {
    font-family: 'Inter', sans-serif !important;
}
body, .stApp { background-color: #f0fafa !important; }

/* Hide streamlit default chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }

/* Sidebar — always visible, no collapse */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #b2dfdb !important;
    min-width: 240px !important;
    max-width: 240px !important;
    display: flex !important;
    visibility: visible !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1rem 0.5rem !important;
}
/* Style the collapse/expand toggle button (the ☰ three dash button) */
button[data-testid="collapsedControl"] {
    background: #ffffff !important;
    border: 1.5px solid #b2dfdb !important;
    border-radius: 8px !important;
    color: #00796b !important;
}
button[data-testid="collapsedControl"]:hover {
    background: #e0f2f1 !important;
}
/* Sidebar nav buttons */
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
    padding: 10px 16px !important;
    margin-bottom: 2px !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #e0f2f1 !important;
    border-left-color: #00897b !important;
    color: #00796b !important;
}

/* Top navbar area */
.tg-topbar {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #ffffff;
    border-bottom: 1.5px solid #b2dfdb;
    padding: 10px 20px 10px 10px;
    box-shadow: 0 1px 6px rgba(0,128,128,0.07);
    margin-bottom: 0;
}
.tg-brand {
    font-size: 20px;
    font-weight: 700;
    color: #00796b;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
}
.tg-search {
    flex: 1;
    padding: 8px 18px;
    border: 1.5px solid #b2dfdb;
    border-radius: 20px;
    font-size: 14px;
    background: #f0fafa;
    color: #1a2e2e;
    outline: none;
    font-family: 'Inter', sans-serif;
}
.tg-search:focus { border-color: #00897b; background: #fff; }
.tg-userbadge {
    font-size: 13px;
    font-weight: 600;
    color: #00796b;
    white-space: nowrap;
    background: #e0f2f1;
    padding: 5px 12px;
    border-radius: 20px;
}

/* Page content */
.tg-page {
    padding: 8px 28px 60px 28px;
}

/* Section titles */
.tg-section-title {
    font-size: 16px;
    font-weight: 700;
    color: #00796b;
    margin: 24px 0 10px 0;
    letter-spacing: 0.1px;
}

/* Photo card */
.tg-card-photo {
    width: 100%;
    height: 130px;
    background: linear-gradient(135deg, #80cbc4, #4db6ac);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    overflow: hidden;
    margin-bottom: 0;
}
.tg-card-photo img {
    width: 100%;
    height: 130px;
    object-fit: cover;
    border-radius: 10px;
}

/* Detail page */
.tg-detail-photo {
    width: 100%;
    height: 380px;
    background: linear-gradient(135deg, #80cbc4, #4db6ac);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 80px;
    overflow: hidden;
    margin-bottom: 14px;
}
.tg-detail-photo img {
    width: 100%;
    height: 380px;
    object-fit: cover;
    border-radius: 14px;
}
.tg-user-tag {
    font-size: 13px;
    font-weight: 700;
    color: #00796b;
    margin-bottom: 2px;
}
.tg-place-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a2e2e;
    margin: 0 0 14px 0;
}
.tg-info-box {
    background: #ffffff;
    border: 1px solid #e0f2f1;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
}
.tg-info-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #00897b;
    margin-bottom: 6px;
}
.tg-info-text {
    font-size: 14px;
    line-height: 1.7;
    color: #2d4a4a;
}

/* Review badges */
.badge-cert {
    display: inline-block;
    background: #e0f2f1;
    color: #00796b;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 6px;
}
.badge-guest {
    display: inline-block;
    background: #f5f5f5;
    color: #999;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 6px;
}
.review-row {
    padding: 10px 0;
    border-bottom: 1px solid #f0fafa;
}
.review-username {
    font-size: 13px;
    font-weight: 700;
    color: #00796b;
}
.review-text {
    font-size: 14px;
    color: #2d4a4a;
    margin: 4px 0 0 0;
}

/* Feed / post cards */
.tg-feed-card {
    background: #ffffff;
    border: 1px solid #e0f2f1;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: 0 1px 6px rgba(0,128,128,0.06);
}
.tg-feed-meta {
    padding: 10px 14px 4px;
    font-size: 13px;
    font-weight: 700;
    color: #00796b;
}
.tg-feed-photo {
    width: 100%;
    height: 220px;
    background: linear-gradient(135deg, #80cbc4, #4db6ac);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    overflow: hidden;
}
.tg-feed-photo img {
    width: 100%;
    height: 220px;
    object-fit: cover;
}
.tg-feed-footer { padding: 6px 14px 12px; }

/* Vote buttons */
.stButton > button {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

/* Teal primary buttons */
.tg-primary .stButton > button {
    background: #00897b !important;
    color: white !important;
    border: none !important;
    padding: 8px 20px !important;
}
.tg-primary .stButton > button:hover {
    background: #00796b !important;
}

hr { border: none; border-top: 1px solid #e0f2f1; margin: 18px 0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR (native Streamlit — properly toggles) ─────────────────────────────
with st.sidebar:
    st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:4px 8px 16px;border-bottom:1px solid #e0f2f1;">'
                f'<span style="font-size:22px;">{logo_b64(32)}</span>'
                f'<span style="font-size:18px;font-weight:700;color:#00796b;">Tourgram</span></div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🏠  Home", key="nav_home"):
        st.session_state.selected_place = None
        st.session_state["page"] = "home"
        st.rerun()

    if st.button("🗺️  Districts", key="nav_district"):
        st.session_state["page"] = "district"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(f'<div style="padding:6px 16px;font-size:13px;color:#00796b;font-weight:600;">'
                    f'👤 {st.session_state.username} <span style="background:#e0f2f1;padding:2px 7px;border-radius:10px;font-size:11px;">✓ Certified</span></div>',
                    unsafe_allow_html=True)
        if st.button("📷  Post a Place", key="nav_post_in"):
            st.session_state["page"] = "post"
            st.rerun()
        if st.button("🚪  Logout", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state["page"] = "home"
            st.rerun()
    else:
        if st.button("👤  Login / Sign Up", key="nav_login"):
            st.session_state["page"] = "login"
            st.rerun()
        if st.button("📷  Post a Place", key="nav_post_out"):
            st.session_state["page"] = "login"
            st.rerun()

# ── TOP NAVBAR ────────────────────────────────────────────────────────────────
logo_html = logo_b64(32)
user_html = ""
if st.session_state.logged_in:
    user_html = f'<span class="tg-userbadge">👤 {st.session_state.username} ✓</span>'

st.markdown(f"""
<div class="tg-topbar">
    <div class="tg-brand">{logo_html} Tourgram</div>
    <input class="tg-search" type="text" placeholder="🔍  Search places, districts…" />
    {user_html}
</div>
""", unsafe_allow_html=True)


# ── PLACE DETAIL VIEW ─────────────────────────────────────────────────────────
def show_place_detail(post):
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)

    if st.button("← Back", key="back_btn"):
        st.session_state.selected_place = None
        st.rerun()

    st.markdown(f'<div class="tg-user-tag">{post["user"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="tg-place-title">{post["title"]}</div>', unsafe_allow_html=True)

    # Photo
    if post["image"]:
        st.image(post["image"], use_container_width=True)
    else:
        st.markdown('<div class="tg-detail-photo">🏔️</div>', unsafe_allow_html=True)

    # Upvote / Downvote
    vid = post["id"]
    v = st.session_state.votes[vid]
    vc1, vc2, vc3 = st.columns([1.4, 1.6, 6])
    with vc1:
        if st.button(f"▲  Upvote  {v['up']}", key=f"up_{vid}"):
            st.session_state.votes[vid]["up"] += 1
            st.rerun()
    with vc2:
        if st.button(f"▼  Downvote  {v['down']}", key=f"dn_{vid}"):
            st.session_state.votes[vid]["down"] += 1
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Info sections
    for label, key in [("📜 History", "history"), ("💰 Budget", "budget"), ("🛡️ Safety", "safety")]:
        st.markdown(f"""
        <div class="tg-info-box">
            <div class="tg-info-label">{label}</div>
            <div class="tg-info-text">{post[key]}</div>
        </div>""", unsafe_allow_html=True)

    # Reviews
    st.markdown('<div class="tg-info-box">', unsafe_allow_html=True)
    st.markdown('<div class="tg-info-label">⭐ Reviews</div>', unsafe_allow_html=True)
    for r in post["reviews"]:
        badge = '<span class="badge-cert">✓ Certified User</span>' if r["certified"] else '<span class="badge-guest">Guest</span>'
        st.markdown(f"""
        <div class="review-row">
            <span class="review-username">{r['user']}</span>{badge}
            <p class="review-text">{r['text']}</p>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add review
    st.markdown("<br>", unsafe_allow_html=True)
    new_rev = st.text_input("✍️ Write a review", placeholder="Share your experience…", key=f"rev_input_{vid}")
    if st.button("Submit Review", key=f"rev_submit_{vid}"):
        if new_rev.strip():
            certified = st.session_state.logged_in
            reviewer  = f"u/{st.session_state.username}" if st.session_state.logged_in else "u/guest"
            for p in st.session_state.posts:
                if p["id"] == vid:
                    p["reviews"].append({"text": new_rev.strip(), "user": reviewer, "certified": certified})
            st.success("Review submitted!")
            st.rerun()
        else:
            st.warning("Please write something first.")

    if not st.session_state.logged_in:
        st.caption("💡 Log in to show ✓ Certified User badge on your review.")

    st.markdown('</div>', unsafe_allow_html=True)

# ── HOME PAGE ─────────────────────────────────────────────────────────────────
def show_home():
    # If a place is selected, show its detail
    if st.session_state.selected_place:
        for p in st.session_state.posts:
            if p["id"] == st.session_state.selected_place:
                show_place_detail(p)
                return

    st.markdown('<div class="tg-page">', unsafe_allow_html=True)

    sections = [
        ("✨ Recommended for You", st.session_state.posts[:3]),
        ("🔥 Popular",             st.session_state.posts[1:5]),
        ("📍 Must Visit",          st.session_state.posts[2:6]),
        ("⭐ Highest Rated",       st.session_state.posts[3:] + st.session_state.posts[:1]),
    ]

    for sec_title, items in sections:
        st.markdown(f'<div class="tg-section-title">{sec_title}</div>', unsafe_allow_html=True)
        cols = st.columns(len(items))
        for i, post in enumerate(items):
            with cols[i]:
                if post["image"]:
                    st.image(post["image"], use_container_width=True)
                else:
                    st.markdown('<div class="tg-card-photo">🏔️</div>', unsafe_allow_html=True)
                if st.button(post["title"], key=f"card_{sec_title[:3]}_{post['id']}"):
                    st.session_state.selected_place = post["id"]
                    st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)

    # ── Community feed ────────────────────────────────────────────────────────
    st.markdown('<div class="tg-section-title">📸 Community Posts</div>', unsafe_allow_html=True)

    bcol, _ = st.columns([1.5, 5])
    with bcol:
        if st.button("＋  Post a Place", key="feed_post_btn"):
            if not st.session_state.logged_in:
                st.session_state["page"] = "login"
            else:
                st.session_state["page"] = "post"
            st.rerun()

    for post in st.session_state.posts:
        vid = post["id"]
        v   = st.session_state.votes[vid]

        st.markdown('<div class="tg-feed-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="tg-feed-meta">{post["user"]}  ·  {post["district"]}</div>', unsafe_allow_html=True)

        if post["image"]:
            st.image(post["image"], use_container_width=True)
        else:
            st.markdown('<div class="tg-feed-photo">🏔️</div>', unsafe_allow_html=True)

        st.markdown('<div class="tg-feed-footer">', unsafe_allow_html=True)
        fc1, fc2, fc3 = st.columns([1.2, 1.4, 3])
        with fc1:
            if st.button(f"▲  {v['up']}", key=f"f_up_{vid}"):
                st.session_state.votes[vid]["up"] += 1
                st.rerun()
        with fc2:
            if st.button(f"▼  {v['down']}", key=f"f_dn_{vid}"):
                st.session_state.votes[vid]["down"] += 1
                st.rerun()
        with fc3:
            if st.button("View Details →", key=f"f_view_{vid}"):
                st.session_state.selected_place = vid
                st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── POST PAGE ─────────────────────────────────────────────────────────────────
def show_post_page():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    if st.button("← Back to Home", key="post_back"):
        st.session_state["page"] = "home"
        st.rerun()

    st.markdown('<h2 style="color:#00796b;margin-top:10px;">📷 Post a Place</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#555;font-size:14px;margin-bottom:20px;">Share a tourist spot with the Tourgram community.</p>', unsafe_allow_html=True)

    title    = st.text_input("Place Name *", placeholder="e.g. Gosaikunda Lake")
    district = st.text_input("District *",   placeholder="e.g. Rasuwa")
    uploaded = st.file_uploader("Upload a Photo", type=["jpg","jpeg","png","webp"])
    history  = st.text_area("History",    placeholder="Tell us the history of this place…")
    budget   = st.text_area("Budget Tips", placeholder="Entry fees, transport costs, tips…")
    safety   = st.text_area("Safety Info", placeholder="Is it safe? Any warnings?")

    if st.button("Publish Post ✓", key="publish_btn"):
        if not title.strip() or not district.strip():
            st.error("Place name and district are required.")
        else:
            import uuid
            new_id = "p" + str(uuid.uuid4())[:8]
            img    = Image.open(uploaded) if uploaded else None
            st.session_state.posts.insert(0, {
                "id": new_id,
                "user": f"u/{st.session_state.username}",
                "title": title.strip(),
                "image": img,
                "district": district.strip(),
                "history": history.strip() or "No history provided.",
                "budget":  budget.strip()  or "No budget info provided.",
                "safety":  safety.strip()  or "No safety info provided.",
                "reviews": [],
            })
            st.session_state.votes[new_id] = {"up": 0, "down": 0}
            st.success("🎉 Post published!")
            st.session_state["page"] = "home"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
def show_login_page():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    if st.button("← Back", key="login_back"):
        st.session_state["page"] = "home"
        st.rerun()


# ── DISTRICT PAGE ─────────────────────────────────────────────────────────────
def show_district_page():
    st.markdown('<div class="tg-page">', unsafe_allow_html=True)
    if st.button("← Back", key="dist_back"):
        st.session_state["page"] = "home"
        st.rerun()


# ── RENDER ────────────────────────────────────────────────────────────────────
page = st.session_state["page"]
if page == "home":
    show_home()
elif page == "post":
    show_post_page()
elif page == "login":
    show_login_page()
elif page == "district":
    show_district_page()
