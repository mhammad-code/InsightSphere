import streamlit as st


def apply_theme(dark_mode=False):
    if dark_mode:
        base = "#15121F"
        text = "#F5F3FF"
        muted = "#C4BEDF"
        glass_border = "rgba(255, 255, 255, 0.18)"
    else:
        base = "#FAF8FF"
        text = "#241F3D"
        muted = "#6A6285"
        glass_border = "rgba(255, 255, 255, 0.85)"

    # Bold, saturated multicolor palette
    violet = "#8B5CF6"
    pink   = "#EC4899"
    teal   = "#14B8A6"
    orange = "#F97316"
    blue   = "#3B82F6"
    lime   = "#84CC16"

    ease = "cubic-bezier(0.22, 1, 0.36, 1)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

    :root {{
        --base: {base}; --text: {text}; --muted: {muted}; --glass-border: {glass_border};
        --violet: {violet}; --pink: {pink}; --teal: {teal};
        --orange: {orange}; --blue: {blue}; --lime: {lime};
        --ease: {ease};
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    div[data-testid="stDecoration"] {{visibility: hidden;}}

    .stApp {{
        background: var(--base);
        color: var(--text);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow-x: hidden;
    }}

    /* Vivid multi-color mesh -- five large saturated blobs in motion */
    .mesh-blob {{
        position: fixed;
        border-radius: 50%;
        filter: blur(85px);
        z-index: 0;
        pointer-events: none;
    }}
    .mesh-1 {{ width: 480px; height: 480px; background: var(--violet); opacity: 0.55; top: -140px; left: -100px; animation: floatA 15s ease-in-out infinite; }}
    .mesh-2 {{ width: 440px; height: 440px; background: var(--pink);   opacity: 0.45; top: 10%; right: -140px; animation: floatB 19s ease-in-out infinite; }}
    .mesh-3 {{ width: 420px; height: 420px; background: var(--teal);  opacity: 0.45; bottom: -120px; left: 8%; animation: floatC 22s ease-in-out infinite; }}
    .mesh-4 {{ width: 360px; height: 360px; background: var(--orange);opacity: 0.35; bottom: 5%; right: 12%; animation: floatA 18s ease-in-out infinite reverse; }}
    .mesh-5 {{ width: 320px; height: 320px; background: var(--blue);  opacity: 0.35; top: 45%; left: 40%; animation: floatB 24s ease-in-out infinite; }}

    @keyframes floatA {{
        0%, 100% {{ transform: translate(0,0) scale(1); }}
        33% {{ transform: translate(90px,70px) scale(1.2); }}
        66% {{ transform: translate(-50px,110px) scale(0.85); }}
    }}
    @keyframes floatB {{
        0%, 100% {{ transform: translate(0,0) scale(1); }}
        33% {{ transform: translate(-80px,-60px) scale(1.15); }}
        66% {{ transform: translate(60px,-100px) scale(0.9); }}
    }}
    @keyframes floatC {{
        0%, 100% {{ transform: translate(0,0) scale(1); }}
        50% {{ transform: translate(100px,-70px) scale(1.25); }}
    }}

    section.main > div {{ position: relative; z-index: 1; }}
    section[data-testid="stSidebar"] {{ position: relative; z-index: 1; }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(16px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    div[data-testid="stElementContainer"] {{ animation: fadeUp 0.55s var(--ease) backwards; }}

    h1, h2 {{
        font-family: 'Poppins', sans-serif !important;
        font-weight: 800 !important;
        color: var(--text) !important;
    }}

    h3 {{
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 3px !important;
        text-transform: uppercase;
        font-weight: 700 !important;
        background: linear-gradient(90deg, var(--violet), var(--pink), var(--orange));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 8px !important;
    }}
    h3::after {{
        content: "";
        display: block;
        width: 0%;
        height: 3px;
        margin-top: 10px;
        background: linear-gradient(90deg, var(--violet), var(--pink), var(--orange), var(--teal));
        border-radius: 3px;
        animation: growLine 0.9s var(--ease) 0.15s forwards;
    }}
    @keyframes growLine {{ to {{ width: 100%; }} }}

    .stCaption, [data-testid="stCaptionContainer"] {{ color: var(--muted) !important; }}
    hr {{ border-color: var(--glass-border) !important; margin: 1.6rem 0 !important; }}

    section[data-testid="stSidebar"] {{
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(22px);
        border-right: 1px solid var(--glass-border);
    }}
    section[data-testid="stSidebar"] h2 {{
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.8rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 700 !important;
        background: linear-gradient(90deg, var(--violet), var(--teal));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* Each glass card gets a distinct tint + colored glow, cycling through the palette */
    .glass-card {{
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        padding: 20px 22px;
        transition: transform 0.35s var(--ease), box-shadow 0.35s var(--ease);
    }}
    .glass-card:nth-of-type(6n+1) {{ background: linear-gradient(135deg, rgba(139,92,246,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--violet); }}
    .glass-card:nth-of-type(6n+2) {{ background: linear-gradient(135deg, rgba(236,72,153,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--pink); }}
    .glass-card:nth-of-type(6n+3) {{ background: linear-gradient(135deg, rgba(20,184,166,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--teal); }}
    .glass-card:nth-of-type(6n+4) {{ background: linear-gradient(135deg, rgba(249,115,22,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--orange); }}
    .glass-card:nth-of-type(6n+5) {{ background: linear-gradient(135deg, rgba(59,130,246,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--blue); }}
    .glass-card:nth-of-type(6n+6) {{ background: linear-gradient(135deg, rgba(132,204,22,0.18), rgba(255,255,255,0.55)); border-left: 4px solid var(--lime); }}

    .glass-card:hover {{
        transform: translateY(-7px) scale(1.015);
        box-shadow: 0 18px 40px rgba(139, 92, 246, 0.3);
    }}

    .metric-label {{
        font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase;
        color: var(--muted); margin-bottom: 6px; font-weight: 600;
    }}
    .metric-value {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.75rem; font-weight: 700; color: var(--text);
    }}

    .stButton button, .stDownloadButton button, .stFormSubmitButton button {{
        background: linear-gradient(90deg, var(--violet), var(--pink)) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.3rem !important;
        box-shadow: 0 6px 18px rgba(139, 92, 246, 0.3);
        transition: all 0.32s var(--ease) !important;
    }}
    .stButton button:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover {{
        background: linear-gradient(90deg, var(--pink), var(--orange)) !important;
        box-shadow: 0 10px 28px rgba(236, 72, 153, 0.45);
        transform: translateY(-3px) scale(1.03);
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background: linear-gradient(135deg, rgba(139,92,246,0.10), rgba(20,184,166,0.10)) !important;
        backdrop-filter: blur(14px);
        border: 2px dashed var(--violet) !important;
        border-radius: 18px !important;
        transition: all 0.32s var(--ease);
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: var(--pink) !important;
        transform: translateY(-2px);
    }}

    [data-testid="stExpander"] {{
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px;
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid var(--glass-border) !important;
        border-radius: 14px;
        font-family: 'IBM Plex Mono', monospace !important;
    }}

    [data-baseweb="tag"] {{
        background: linear-gradient(90deg, var(--violet), var(--teal)) !important;
        color: #fff !important;
        font-weight: 600 !important;
    }}

    [data-testid="stChatMessage"] {{
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        transition: transform 0.3s var(--ease);
    }}
    [data-testid="stChatMessage"]:hover {{ transform: translateX(4px); }}

    [data-testid="stAlert"] {{ border-radius: 14px !important; backdrop-filter: blur(10px); }}

    .js-plotly-plot {{
        border: 1px solid var(--glass-border);
        border-radius: 18px;
        padding: 8px;
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(14px);
        transition: transform 0.4s var(--ease), box-shadow 0.4s var(--ease);
    }}
    .js-plotly-plot:hover {{
        transform: translateY(-5px);
        box-shadow: 0 18px 36px rgba(139, 92, 246, 0.25);
    }}
    </style>
    <div class="mesh-blob mesh-1"></div>
    <div class="mesh-blob mesh-2"></div>
    <div class="mesh-blob mesh-3"></div>
    <div class="mesh-blob mesh-4"></div>
    <div class="mesh-blob mesh-5"></div>
    """, unsafe_allow_html=True)


def custom_metric(label, value):
    st.markdown(f"""
    <div class="glass-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_intro():
    st.markdown("""
    <style>
    @keyframes logoPop {
        0% { opacity: 0; transform: scale(0.7) translateY(20px); filter: blur(6px); }
        60% { opacity: 1; transform: scale(1.04) translateY(0); filter: blur(0); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes slideFade {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes lineGrow { from { width: 0%; } to { width: 160px; } }
    @keyframes dotBounce {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-12px) scale(1.2); }
    }
    .intro-wrap { text-align: center; padding: 50px 20px 30px 20px; }
    .intro-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--violet), var(--pink), var(--orange), var(--teal), var(--violet));
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: logoPop 0.9s cubic-bezier(0.22, 1, 0.36, 1) backwards, gradientShift 6s ease infinite;
    }
    .intro-line {
        height: 4px; width: 160px; margin: 14px auto 18px auto;
        background: linear-gradient(90deg, var(--violet), var(--pink), var(--orange), var(--teal));
        border-radius: 3px;
        animation: lineGrow 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.5s backwards;
    }
    .intro-sub {
        font-family: 'Inter', sans-serif;
        color: var(--muted);
        font-size: 1.05rem;
        font-weight: 500;
        animation: slideFade 0.8s ease 0.65s backwards;
    }
    .intro-dots { margin-top: 22px; animation: slideFade 0.8s ease 0.85s backwards; }
    .intro-dots span {
        display: inline-block;
        width: 11px; height: 11px;
        margin: 0 6px;
        border-radius: 50%;
        animation: dotBounce 1s ease-in-out infinite;
    }
    .intro-dots span:nth-child(1) { background: var(--violet); animation-delay: 0s; }
    .intro-dots span:nth-child(2) { background: var(--pink); animation-delay: 0.15s; }
    .intro-dots span:nth-child(3) { background: var(--orange); animation-delay: 0.3s; }
    </style>
    <div class="intro-wrap">
        <div class="intro-title">InsightSphere</div>
        <div class="intro-line"></div>
        <div class="intro-sub">Turning raw business data into clear decisions</div>
        <div class="intro-dots"><span></span><span></span><span></span></div>
    </div>
    """, unsafe_allow_html=True)