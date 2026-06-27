import streamlit as st
import time

st.set_page_config(
    page_title="Kathmandu",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Teal CSS Override - Customizing the visual interface
teal_css = """
<style>
    /* Premium Light Mode Gradient Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f0fdfa 0%, #ffffff 100%);
        color: #0f172a;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Sidebar: Clean light gray/teal tint */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Modern Teal Glow Banner Header Styling (Light Mode) */
    .title-banner {
        background: linear-gradient(135deg, #ccfbf1 0%, #f0fdfa 100%);
        padding: 35px;
        border-radius: 20px;
        color: #042f2e;
        text-align: center;
        box-shadow: 0 10px 30px rgba(13, 148, 136, 0.1);
        margin-bottom: 30px;
        border: 1px solid #99f6e4;
    }
    .title-banner h1 {
        color: #0f766e !important;
        font-weight: 800;
        margin-bottom: 8px;
        font-size: 3rem;
    }

    /* ---- NEW POST AUTHOR HEADER STYLES ---- */
    .post-author-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
        padding-left: 4px;
    }
    .author-avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #14b8a6;
        box-shadow: 0 2px 8px rgba(20, 184, 166, 0.2);
    }
    .author-name {
        font-weight: 700;
        color: #0f766e;
        font-size: 1.05rem;
        margin: 0;
    }
    .post-meta {
        font-size: 0.78rem;
        color: #64748b;
        margin: 0;
        line-height: 1.2;
    }

    /* Card styling */
    .card-img-container {
        height: 330px;
        border-radius: 16px;
        overflow: hidden;
        position: relative;
        margin-bottom: 15px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    /* Fixed missing image fit style */
    .card-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Rating overlay in light mode */
    .rating-overlay {
        position: absolute;
        bottom: 14px;
        left: 14px;
        background: rgba(255, 255, 255, 0.9);
        color: #0f766e;
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 700;
        backdrop-filter: blur(4px);
        border: 1px solid #99f6e4;
    }
    
    .safety-pill {
        position: absolute;
        top: 14px;
        right: 14px;
        background: rgba(255, 255, 255, 0.9);
        color: #0f766e;
        padding: 6px 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 700;
        border: 1px solid #99f6e4;
    }

    /* Feedback container */
    .feedback-bubble {
        background-color: #f0fdfa;
        padding: 14px 18px;
        border-radius: 14px;
        margin-bottom: 12px;
        border-left: 4px solid #14b8a6;
        color: #0f172a;
    }

    /* Action buttons light overrides */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #0f766e !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: #f0fdfa !important;
        border-color: #14b8a6 !important;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.15) !important;
    }

    /* Premium accent submission button */
    .accent-btn div.stButton > button {
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(13, 148, 136, 0.25) !important;
        width: 100%;
        margin-top: 10px;
    }
    .accent-btn div.stButton > button:hover {
        box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4) !important;
        transform: scale(1.02);
    }
</style>
"""
st.markdown(teal_css, unsafe_allow_html=True)

# PLACES dataset with new 'post_author' and 'author_avatar' keys added
PLACES = [
    {
        "id": "swayambhunath",
        "name": "Swayambhunath Stupa",
        "tagline": "The Ancient Monkey Temple",
        "image": "https://www.distinctdestinations.in/DistinctDestinationsBackEndImg/BlogImage/experiencing-swayambhunath-stupa-the-monkey-temple-of-nepal-L-distinctdestinations.jpg",
        "post_author": "Samir Sharma",
        "author_avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80",
        "description": "Perched atop a hill west of Kathmandu city, Swayambhunath is one of the most sacred Buddhist sites in Nepal. The dome-shaped stupa is painted with the watchful eyes of Buddha. It is universally loved for its spiritual harmony, hundreds of playful monkeys, and panoramic sunset views of the valley.",
        "safety_pct": 96,
        "default_likes": 1240,
        "default_dislikes": 12,
        "default_ratings": [5, 5, 4, 5],
        "default_feedbacks": [
            {"author": "GuideDorje", "comment": "The morning prayers are hypnotic.", "verified": True},
            {"author": "WandererKT", "comment": "Amazing view of the entire valley!", "verified": True},
            {"author": "Guest", "comment": "Keep your sunglasses safe from the monkeys!", "verified": False}
        ]
    },
    {
        "id": "boudhanath",
        "name": "Boudhanath Stupa",
        "tagline": "The Mandala of Light",
        "image": "https://lp-cms-production.imgix.net/2019-06/813869da84003e9ab623499ae2465723-bodhnath-stupa.jpg?w=1200&auto=format",
   
        "post_author": "Pasang Sherpa",
        "author_avatar": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&auto=format&fit=crop&q=80",
        "description": "As one of the largest spherical stupas in the world, Boudhanath dominates the skyline with its massive mandala. It serves as a historic trade hub and a sanctuary of Tibetan Buddhism, surrounded by humming prayer wheels, rooftop cafes, and the rich aroma of butter lamps.",
        "safety_pct": 98,
        "default_likes": 1850,
        "default_dislikes": 8,
        "default_ratings": [5, 5, 5, 4],
        "default_feedbacks": [
            {"author": "Karma_P", "comment": "Peaceful circumambulations (Kora) around sunset.", "verified": True},
            {"author": "ChieTravels", "comment": "Best rooftop cafes in Kathmandu.", "verified": True},
            {"author": "Guest", "comment": "Very safe even for solo night walks.", "verified": False}
        ]
    },
    {
        "id": "pashupatinath",
        "name": "Pashupatinath Temple",
        "tagline": "The Sacred River Sanctuary",
        
        "image": "https://www.travelhimalayan.com/wp-content/uploads/2026/01/Pashupatinath-to-Mount-Kailash-1.webp",
     
        "post_author": "Aayush Bhattarai",
        "author_avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "description": "Stretched along both banks of the sacred Bagmati River, Pashupatinath is Nepal's most revered Hindu temple complex. Dedicated to Lord Shiva, the site is an intricate tapestry of gold-roofed temples, stone shrines, and profound cultural rituals of life, devotion, and transition.",
        "safety_pct": 92,
        "default_likes": 980,
        "default_dislikes": 32,
        "default_ratings": [4, 5, 4, 4],
        "default_feedbacks": [
            {"author": "Aarav_Dev", "comment": "Profound cultural and spiritual experience.", "verified": True},
            {"author": "TravelScribe", "comment": "Visit during Aarati evening prayers.", "verified": True},
            {"author": "Guest", "comment": "Respect the photography rules near the riverbanks.", "verified": False}
        ]
    },
    {
        "id": "ktm_durbar",
        "name": "Kathmandu Durbar Square",
        "tagline": "The Ancient Courtyard of Kings",
        "image": "https://happymountainnepal.com/wp-content/uploads/2025/02/all-you-need-to-know-about-kathmandu-durbar-square19.jpg",
   
        "post_author": "Prerana Shrestha",
        "author_avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
        "description": "Located in the heart of the old city, this UNESCO World Heritage Site is surrounded by spectacular Newari architecture, ancient palaces, and courtyard temples. It is the historic seat of Nepalese royalty and the home of the Kumari, the living goddess.",
        "safety_pct": 89,
        "default_likes": 1120,
        "default_dislikes": 19,
        "default_ratings": [4, 4, 3, 4],
        "default_feedbacks": [
            {"author": "NewarHeritage", "comment": "Intricate wood carvings that are centuries old.", "verified": True},
            {"author": "Shreeya_K", "comment": "Lovely place to sit and people-watch.", "verified": True},
            {"author": "Guest", "comment": "Local tea stalls around here are wonderful.", "verified": False}
        ]
    },
    {
        "id": "patan_durbar",
        "name": "Patan Durbar Square",
        "tagline": "The City of Fine Arts",
        "image": "https://pristinenepal.com/wp-content/uploads/2024/05/patan-durbar-1024x683.webp",
        
        "post_author": "Niranjan Joshi",
        "author_avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "description": "Patan Durbar Square is famous for its artistic heritage. Every corner showcases incredible Newari architecture, stone temples, and bronze monuments. The Patan Museum inside the palace is widely considered one of the best curators of Asian religious art.",
        "safety_pct": 95,
        "default_likes": 1390,
        "default_dislikes": 11,
        "default_ratings": [5, 4, 5, 5],
        "default_feedbacks": [
            {"author": "Art_Lover", "comment": "The Krishna Mandir stone temple is a marvel.", "verified": True},
            {"author": "Rohan99", "comment": "Very clean and highly artistic.", "verified": True},
            {"author": "Guest", "comment": "Excellent local handicraft shops.", "verified": False}
        ]
    },
    {
        "id": "bhaktapur_durbar",
        "name": "Bhaktapur Durbar Square",
        "tagline": "The Museum of Living Culture",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/c9/View_of_Bhaktapur_Durbar_Square.jpg",
     
        "post_author": "Srijana Malla",
        "author_avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&auto=format&fit=crop&q=80",
        "description": "Bhaktapur is a timeless town filled with red clay brick roads, historic courtyards, and massive temples like Nyatapola. Known as the 'City of Devotees', it retains its traditional lifestyle, potters’ squares, and world-famous JuJu Dhau (king curd).",
        "safety_pct": 97,
        "default_likes": 1460,
        "default_dislikes": 14,
        "default_ratings": [5, 5, 5, 4],
        "default_feedbacks": [
            {"author": "JujuEnthusiast", "comment": "Make sure to try the local JuJu Dhau!", "verified": True},
            {"author": "Wander_Lust", "comment": "The 55-window palace is breathtaking.", "verified": True},
            {"author": "Guest", "comment": "Very pedestrian-friendly and peaceful.", "verified": False}
        ]
    },
    {
        "id": "garden_of_dreams",
        "name": "Garden of Dreams",
        "tagline": "The Oasis of Tranquility",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSacINV-fSDNL-IxCLdEivJKfgYAZ1JrZbvkKuCLwIq6d8iTW9V_cQraMU&s=10",
     
        "post_author": "Rohan Raj",
        "author_avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
        "description": "Tucked away near the bustling streets of Thamel, the Garden of Dreams is a neoclassical historical garden. Its beautifully restored pavilions, amphitheater, fountains, and sunken gardens offer a quiet escape from the city’s vibrant energy.",
        "safety_pct": 99,
        "default_likes": 870,
        "default_dislikes": 6,
        "default_ratings": [5, 4, 4, 5],
        "default_feedbacks": [
            {"author": "EscapeArtist", "comment": "Perfect escape from Thamel's chaotic streets.", "verified": True},
            {"author": "Flora_Fan", "comment": "Beautifully manicured gardens.", "verified": True},
            {"author": "Guest", "comment": "Great spot to read a book and have a coffee.", "verified": False}
        ]
    }
]

# Initializing Session States
if "likes" not in st.session_state:
    st.session_state.likes = {p["id"]: p["default_likes"] for p in PLACES}
if "dislikes" not in st.session_state:
    st.session_state.dislikes = {p["id"]: p["default_dislikes"] for p in PLACES}
if "ratings" not in st.session_state:
    st.session_state.ratings = {p["id"]: p["default_ratings"].copy() for p in PLACES}
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = {p["id"]: p["default_feedbacks"].copy() for p in PLACES}
if "voted" not in st.session_state:
    st.session_state.voted = {p["id"]: None for p in PLACES}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Main App Header
st.markdown(
    """
    <div class="title-banner">
        <h1>📍 Kathmandu</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Loop and render each place sequentially
for p in PLACES:
    p_id = p["id"]
    
    # Calculate real-time dynamic star rating
    current_ratings = st.session_state.ratings[p_id]
    avg_rating = sum(current_ratings) / len(current_ratings) if current_ratings else 0.0
    star_display = "★" * int(round(avg_rating)) + "☆" * (5 - int(round(avg_rating)))
    
    # Custom Card Container opening
    st.markdown(f'<div class="place-scroller-card">', unsafe_allow_html=True)
    
    # Side-by-side design layout
    col_visual, col_details = st.columns([1.1, 1.0])
    
    with col_visual:
        # ---- MODIFICATION HERE: Added Profile & Author Header ----
        st.markdown(
            f"""
            <div class="post-author-header">
                <img src="{p['author_avatar']}" class="author-avatar" alt="avatar">
                <div>
                    <p class="author-name">{p['post_author']}</p>
                    <p class="post-meta">Shared a location • Local Guide</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Image block
        st.markdown(
            f"""
            <div class="card-img-container">
                <img src="{p['image']}" alt="{p['name']}">
                
                <div class="rating-overlay">⭐ {avg_rating:.1f}/5 ({len(current_ratings)} ratings)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Upvoting and downvoting metrics
        v_col1, v_col2 = st.columns([1, 1])
        with v_col1:
            if st.button(f"👍 Upvote ({st.session_state.likes[p_id]})", key=f"like_{p_id}", use_container_width=True):
                if st.session_state.voted[p_id] != "like":
                    st.session_state.likes[p_id] += 1
                    if st.session_state.voted[p_id] == "dislike":
                        st.session_state.dislikes[p_id] -= 1
                    st.session_state.voted[p_id] = "like"
                    st.rerun()
                    
        with v_col2:
            if st.button(f"👎 Downvote ({st.session_state.dislikes[p_id]})", key=f"dislike_{p_id}", use_container_width=True):
                if st.session_state.voted[p_id] != "dislike":
                    st.session_state.dislikes[p_id] += 1
                    if st.session_state.voted[p_id] == "like":
                        st.session_state.likes[p_id] -= 1
                    st.session_state.voted[p_id] = "dislike"
                    st.rerun()

        vote_state = st.session_state.voted[p_id]
        if vote_state:
            st.caption(f"✨ Registered Feedback: **{vote_state.upper()}**")

    # Details and review container column
    with col_details:
        st.markdown(f"<h2 style='color:#0f766e; font-weight:800; margin-top:0; margin-bottom: 2px;'>{p['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#115e59; font-size:1.05rem; font-weight:600; font-style:italic; margin-bottom: 12px;'>{p['tagline']}</p>", unsafe_allow_html=True)
        
        # Unhidden, Prominent Vibe Rating Summary Panel
        st.markdown(
            f"""
            <div style='background: rgba(13, 148, 136, 0.08); padding: 14px 18px; border-radius: 12px; border: 1px solid rgba(45, 212, 191, 0.3); margin-bottom: 15px;'>
                <span style='color:#64748b; font-size:0.8rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight:700; display:block;'>Current Vibe Rating</span>
                <span style='color:#fbbf24; font-size:1.8rem; font-weight:800; line-height: 1.2;'>{star_display}</span>
                <span style='color:#0f766e; font-size:1.4rem; font-weight:700; margin-left: 6px;'>{avg_rating:.1f} / 5.0</span>
                <span style='color:#64748b; font-size:0.8rem; display:block; margin-top: 2px;'>Aggregated from {len(current_ratings)} verified travelers</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Expander for Historical / Cultural Information
        with st.expander("📖 Read Description", expanded=False):
            st.write(p["description"])
            
            # Interactive context alert based on safety scores
            if p["safety_pct"] >= 95:
                st.success(f"🔒 Verified Secure Area ({p['safety_pct']}%). Optimal choice for solo exploration.")
            else:
                st.warning(f"⚠️ Heavy Market Area. Safety index at {p['safety_pct']}%. Secure your bags.")

        # Unified Expandable Reviews & Feedback Workspace
        review_count = len(st.session_state.feedbacks[p_id])
        with st.expander(f"💬 Traveler Reviews & Comments ({review_count})", expanded=False):
            
            # Interactive Input Area directly inside the reviews box
            st.markdown("<h4 style='color: #0f766e; font-weight: 700; margin-top: 10px; margin-bottom: 4px;'>Write a Review</h4>", unsafe_allow_html=True)
            
            # User Identity Verification Info
            if st.session_state.logged_in:
                st.markdown(f"<p style='color: #0f766e; font-size:0.85rem; font-weight:600;'>✍️ Posting as: <strong>{st.session_state.username}</strong> <span style='color: #0f766e;'>(✔ Verified)</span></p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #fbbf24; font-size:0.85rem; font-style:italic;'>⚠️ Posting as: <strong>Guest</strong> (Unverified. Log in from the sidebar to claim your badge!)</p>", unsafe_allow_html=True)

            # Borderless interactive submit form
            with st.form(key=f"inline_rating_form_{p_id}", clear_on_submit=True):
                user_rating = st.select_slider(
                    "Set your score:",
                    options=[1, 2, 3, 4, 5],
                    value=5,
                    key=f"star_slider_{p_id}",
                    format_func=lambda x: "★" * x + "☆" * (5 - x)
                )
                
                user_comment = st.text_input(
                    "Share your experience / tip:",
                    placeholder="e.g. Visited at golden hour, beautiful atmosphere...",
                    key=f"comment_{p_id}"
                )
                
                st.markdown('<div class="accent-btn">', unsafe_allow_html=True)
                submit_rating_btn = st.form_submit_button("Post Traveler Review ✈️")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if submit_rating_btn:
                    st.session_state.ratings[p_id].append(user_rating)
                    
                    # Log comments with verification statuses
                    comment_author = st.session_state.username if st.session_state.logged_in else "Guest"
                    is_verified = st.session_state.logged_in
                    
                    if user_comment.strip():
                        st.session_state.feedbacks[p_id].append({
                            "author": comment_author,
                            "comment": user_comment.strip(),
                            "verified": is_verified
                        })
                    st.toast(f"✅ Review posted successfully!")
                    time.sleep(0.4)
                    st.rerun()

            st.markdown("---")
            st.markdown("<h4 style='color: #0f766e; font-weight: 700; margin-bottom: 12px;'>Recent Comments</h4>", unsafe_allow_html=True)
            
            # Render all reviews with conditional traveler verification tags
            for fb in st.session_state.feedbacks[p_id]:
                if fb["verified"]:
                    badge_html = f'<span style="font-size: 0.72rem; color: #0f766e; font-weight: 700;">✔ Verified Traveler ({fb["author"]})</span>'
                else:
                    badge_html = '<span style="font-size: 0.72rem; color: #fbbf24; font-style: italic; font-weight: 600;">⚠ Guest Reviewer (Unverified)</span>'
                
                st.markdown(
                    f"""
                    <div class="feedback-bubble">
                        <span style="font-size: 0.92rem; color: #0f172a;">"{fb['comment']}"</span>
                        <br>
                        <div style="margin-top: 5px;">
                            {badge_html}
                        </div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                        
    # Custom Card Container closing
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #0d9488; font-size: 0.85rem; font-weight:600;'>Tourism Analytics © 2026. Designed for the Bagmati Province Hackathon.</p>", 
    unsafe_allow_html=True
)