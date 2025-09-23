import streamlit as st

def landing_page():
    # --- Custom CSS for the Final Design ---
    st.markdown("""
    <style>
        /* --- FONT & BASE LAYOUT --- */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
        body { font-family: 'Montserrat', sans-serif; background-color: #F8F9FA; }
        .block-container {
            padding-top: 2rem !important; padding-bottom: 4rem !important;
            padding-left: 4rem !important; padding-right: 4rem !important;
        }

        /* --- HEADER & HERO --- */
        .navbar-brand { font-size: 2.5rem; font-weight: 700; color: #2C3E50; user-select: none; }
        .login-btn { width: 100%; display: flex; justify-content: flex-end; }
        .st-key-login-btn .stButton > button {
            background-color: #24446b !important; color: #fff !important; font-weight: 600 !important;
            border-radius: 18px !important; font-size: 1.1rem !important; padding: 10px 28px !important; border: none !important;
        }
        .st-key-login-btn .stButton > button:hover { background-color: #183356 !important; }
        .hero-heading { font-size: 4.5rem; font-weight: 700; line-height: 1.2; color: #2C3E50 !important; margin-bottom: 1.5rem; }
        .hero-tagline { font-size: 1.2rem; color: #555; margin-bottom: 2.5rem; }
        .st-key-learn-more-btn .stButton > button {
            background-color: #24446b !important; color: #fff !important; font-weight: 700 !important;
            font-size: 1rem !important; padding: 12px 36px !important; border-radius: 28px !important;
            border: none !important; box-shadow: 0 8px 22px rgba(36, 68, 107, 0.4);
        }
        .hero-image img { border-radius: 15px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1); }
        hr { border-top: 1px solid #E0E0E0; margin: 4rem 0; }

        /* --- ABOUT & SERVICES SECTIONS --- */
        .section-title { font-size: 2.8rem; font-weight: 700; color: #2C3E50; text-align: center; margin-bottom: 3rem; }
        .feature-card {
            background: #FFFFFF; border: 1px solid #EAECEE; border-radius: 15px; padding: 2rem;
            text-align: center; height: 100%; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .feature-card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1); }
        .feature-icon { font-size: 3.5rem; color: #24446b; margin-bottom: 1rem; }
        .feature-card h3 { font-size: 1.5rem; font-weight: 700; color: #2C3E50; margin-bottom: 0.5rem; }
        .feature-card p { font-size: 1rem; color: #5D6D7E; line-height: 1.6; }
        .service-card {
            background: linear-gradient(145deg, #ffffff, #f9f9f9); border: 1px solid #EAECEE;
            border-radius: 15px; padding: 2rem; margin-bottom: 1rem; display: flex;
            align-items: center; gap: 1.5rem; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .service-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08); }
        .service-icon { font-size: 2.5rem; color: #24446b; background-color: #EBF5FF; padding: 1rem; border-radius: 50%; }
        .service-card h4 { font-size: 1.2rem; font-weight: 700; color: #2C3E50; margin-bottom: 0.25rem; }
        .service-card p { font-size: 0.95rem; color: #5D6D7E; margin: 0; }
        
        /* --- CTA SECTION --- */
        .cta-container {
            background: linear-gradient(135deg, #24446b, #183356); color: #fff; text-align: center;
            padding: 4rem 2rem; border-radius: 20px; box-shadow: 0 15px 40px rgba(36, 68, 107, 0.3);
        }
        .cta-container h2 { font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 1rem; }
        .cta-container p { font-size: 1.2rem; margin-bottom: 0; opacity: 0.9; }

        /* --- FINAL BUTTON STYLE BASED ON YOUR IMAGE --- */
        .st-key-cta-user-btn button, .st-key-cta-mech-btn button {
            font-size: 1.1rem !important; font-weight: 700 !important;
            padding: 14px 30px !important; border-radius: 12px !important;
            transition: all 0.3s ease !important; margin-top: -1.5rem;
            position: relative; z-index: 1;
            background-color: #fff !important;
            color: #24446b !important;
            border: 2px solid #24446b !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .st-key-cta-user-btn button:hover, .st-key-cta-mech-btn button:hover {
            background-color: #24446b !important; /* Navy Blue hover */
            color: #fff !important;
            border-color: #24446b !important;
            box-shadow: 0 12px 25px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER & HERO SECTION ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="navbar-brand">ONESTOP|MECH</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="login-btn">', unsafe_allow_html=True)
        if st.button("LOGIN / SIGNUP", key="login-btn"):
            st.session_state.update({'show_login': True, 'show_landing': False})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<hr style='border:none; height:1px; background-color:#E0E0E0; margin: 1rem 0 3rem 0;'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.1])
    with col1:
        st.markdown('<h1 class="hero-heading">Ride Further,<br>Worry Less</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-tagline">Find trusted mechanics near you and get quality service with ease. Your one-stop solution for all vehicle needs.</p>', unsafe_allow_html=True)
        if st.button("LEARN MORE", key="learn-more-btn"):
            st.session_state.update({'show_login': True, 'show_landing': False})
            st.rerun()
    with col2:
        st.image("data/OneStopMech_Logo/Capture.png", use_container_width=True)
    
    # --- ABOUT & SERVICES SECTIONS ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Why ONESTOP MECH?</h2>', unsafe_allow_html=True)
    cols = st.columns(4)
    features = [
        ("✅", "Verified Experts", "Every mechanic is vetted for skill and reliability, ensuring top-quality service."),
        ("🔍", "Transparent Pricing", "Receive clear, upfront quotes before any work begins. No hidden fees, no surprises."),
        ("📱", "Ultimate Convenience", "Book services, track repairs, and manage payments all from the comfort of your home."),
        ("🕒", "24/7 Roadside Help", "Get immediate assistance for breakdowns, flat tires, or battery issues, anytime, anywhere.")
    ]
    for i, (icon, title, text) in enumerate(features):
        with cols[i]:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Our Core Services</h2>', unsafe_allow_html=True)
    cols = st.columns(2)
    services = [
        ("🚨", "Emergency Repairs", "Instant connection to nearby mechanics for urgent breakdown assistance."),
        ("⚙️", "Routine Servicing", "Scheduled maintenance to keep your vehicle in peak condition."),
        ("🛠️", "Major Repairs", "Expert handling of complex engine, transmission, and electrical issues."),
        ("✨", "Detailing & Care", "Professional cleaning, polishing, and cosmetic services to make your vehicle shine.")
    ]
    with cols[0]:
        st.markdown(f'<div class="service-card"><div class="service-icon">{services[0][0]}</div><div><h4>{services[0][1]}</h4><p>{services[0][2]}</p></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="service-card"><div class="service-icon">{services[2][0]}</div><div><h4>{services[2][1]}</h4><p>{services[2][2]}</p></div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="service-card"><div class="service-icon">{services[1][0]}</div><div><h4>{services[1][1]}</h4><p>{services[1][2]}</p></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="service-card"><div class="service-icon">{services[3][0]}</div><div><h4>{services[3][1]}</h4><p>{services[3][2]}</p></div></div>', unsafe_allow_html=True)
    
    # --- CTA SECTION ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
        <div class="cta-container">
            <h2>Ready to Experience Hassle-Free Vehicle Care?</h2>
            <p>Join thousands of satisfied vehicle owners. Get started in minutes.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # --- CTA Buttons ---
    _, cta_col1, cta_col2, _ = st.columns([1.5, 1, 1, 1.5])
    with cta_col1:
        if st.button("I'm a Vehicle Owner", key="cta-user-btn", use_container_width=True):
            st.session_state.update({'show_signup': True, 'show_landing': False})
            st.rerun()
    with cta_col2:
        if st.button("I'm a Mechanic", key="cta-mech-btn", use_container_width=True):
            st.session_state.update({'show_signup': True, 'show_landing': False})
            st.rerun()

if __name__ == "__main__":
    landing_page()
