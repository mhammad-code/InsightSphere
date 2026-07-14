import streamlit as st


def apply_theme():
    """
    Applies an ultra-premium cyberpunk glassmorphic theme.
    Navigation uses real st.button elements (stable HTML) instead of
    st.radio with brittle CSS overrides targeting internal div structure.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Clean up native boilerplate elements */
    #MainMenu, footer, div[data-testid="stDecoration"] { 
        visibility: hidden !important; 
        display: none !important; 
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    /* CORE CANVAS BASE SETUP */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0D1527 0%, #070A12 100%) !important;
        color: #E2E8F0 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* ---------- NEON GLASS CHART CONTAINERS (read-only, animated) ---------- */
    @keyframes chartFadeIn {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .js-plotly-plot {
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        background: linear-gradient(135deg, rgba(17, 24, 42, 0.55) 0%, rgba(10, 15, 28, 0.75) 100%) !important;
        backdrop-filter: blur(14px);
        padding: 10px !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
        transition: transform 0.35s cubic-bezier(0.4,0,0.2,1), border-color 0.35s ease, box-shadow 0.35s ease;
        animation: chartFadeIn 0.5s cubic-bezier(0.22,1,0.36,1) backwards;
    }
    .js-plotly-plot:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 245, 212, 0.35) !important;
        box-shadow: 0 16px 38px rgba(0, 245, 212, 0.15);
    }
    /* Read-only lock badge shown on hover, reinforces charts can't be edited */
    .chart-lock-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.7rem;
        color: #64748B;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 8px;
    }

    /* ---------- LIVE ANIMATED NEON BACKGROUND ---------- */
    @keyframes orbFloat1 {
        0%, 100% { transform: translate(0,0) scale(1); }
        33% { transform: translate(70px,50px) scale(1.15); }
        66% { transform: translate(-40px,90px) scale(0.9); }
    }
    @keyframes orbFloat2 {
        0%, 100% { transform: translate(0,0) scale(1); }
        33% { transform: translate(-60px,-40px) scale(1.1); }
        66% { transform: translate(50px,-80px) scale(0.92); }
    }
    @keyframes orbFloat3 {
        0%, 100% { transform: translate(0,0) scale(1); }
        50% { transform: translate(80px,-60px) scale(1.2); }
    }
    .stApp::before, .stApp::after {
        content: "";
        position: fixed;
        border-radius: 50%;
        filter: blur(70px);
        z-index: 0;
        pointer-events: none;
    }
    .stApp::before {
        width: 460px; height: 460px;
        background: radial-gradient(circle, rgba(0,245,212,0.35), transparent 70%);
        top: -120px; left: -100px;
        animation: orbFloat1 16s ease-in-out infinite;
    }
    .stApp::after {
        width: 420px; height: 420px;
        background: radial-gradient(circle, rgba(123,44,233,0.3), transparent 70%);
        bottom: -100px; right: -80px;
        animation: orbFloat2 20s ease-in-out infinite;
    }
    .neon-orb-3 {
        position: fixed;
        width: 340px; height: 340px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(236,72,153,0.22), transparent 70%);
        filter: blur(65px);
        top: 45%; left: 45%;
        z-index: 0;
        pointer-events: none;
        animation: orbFloat3 24s ease-in-out infinite;
    }
    section.main > div, section[data-testid="stSidebar"] { position: relative; z-index: 1; }

    /* ---------- SIDEBAR TOGGLE: base styling only, icon fixed via JS below ---------- */
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] button,
    div[data-testid="collapsedControl"] button {
        background: rgba(13, 21, 39, 0.7) !important;
        border: 1px solid rgba(0, 245, 212, 0.25) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(8px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[data-testid="stSidebarCollapseButton"]:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    div[data-testid="collapsedControl"] button:hover {
        border-color: #00F5D4 !important;
        box-shadow: 0 0 16px rgba(0, 245, 212, 0.35) !important;
        transform: scale(1.06);
    }

    /* PREMIUM SIDEBAR LAYOUT CONFIG */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090E1A 0%, #050811 100%) !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
        width: 320px !important;
    }

    /* ---------- NAV BUTTONS: colorful, animated, neon-glass ---------- */
    @keyframes navFadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] {
        animation: navFadeIn 0.45s cubic-bezier(0.22,1,0.36,1) backwards;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #C7CEDB !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        box-shadow: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
        transform: translateX(6px) scale(1.02);
        color: #FFFFFF !important;
    }
    /* Cycle each nav item through a distinct neon color on hover/active */
    .nav-btn-idx-0 div[data-testid="stButton"] button:hover { border-color: rgba(0, 245, 212, 0.5) !important; box-shadow: 0 6px 22px rgba(0, 245, 212, 0.22) !important; }
    .nav-btn-idx-1 div[data-testid="stButton"] button:hover { border-color: rgba(139, 92, 246, 0.5) !important; box-shadow: 0 6px 22px rgba(139, 92, 246, 0.22) !important; }
    .nav-btn-idx-2 div[data-testid="stButton"] button:hover { border-color: rgba(236, 72, 153, 0.5) !important; box-shadow: 0 6px 22px rgba(236, 72, 153, 0.22) !important; }
    .nav-btn-idx-3 div[data-testid="stButton"] button:hover { border-color: rgba(249, 115, 22, 0.5) !important; box-shadow: 0 6px 22px rgba(249, 115, 22, 0.22) !important; }

    .nav-btn-idx-0.nav-btn-active div[data-testid="stButton"] button {
        background: linear-gradient(90deg, rgba(0,245,212,0.22), rgba(0,245,212,0.04)) !important;
        border-color: #00F5D4 !important; color: #00F5D4 !important;
        box-shadow: 0 6px 26px rgba(0,245,212,0.3) !important; font-weight: 700 !important;
    }
    .nav-btn-idx-1.nav-btn-active div[data-testid="stButton"] button {
        background: linear-gradient(90deg, rgba(139,92,246,0.22), rgba(139,92,246,0.04)) !important;
        border-color: #8B5CF6 !important; color: #C4B5FD !important;
        box-shadow: 0 6px 26px rgba(139,92,246,0.3) !important; font-weight: 700 !important;
    }
    .nav-btn-idx-2.nav-btn-active div[data-testid="stButton"] button {
        background: linear-gradient(90deg, rgba(236,72,153,0.22), rgba(236,72,153,0.04)) !important;
        border-color: #EC4899 !important; color: #F9A8D4 !important;
        box-shadow: 0 6px 26px rgba(236,72,153,0.3) !important; font-weight: 700 !important;
    }
    .nav-btn-idx-3.nav-btn-active div[data-testid="stButton"] button {
        background: linear-gradient(90deg, rgba(249,115,22,0.22), rgba(249,115,22,0.04)) !important;
        border-color: #F97316 !important; color: #FDBA74 !important;
        box-shadow: 0 6px 26px rgba(249,115,22,0.3) !important; font-weight: 700 !important;
    }

    /* CENTRAL WORKSPACE HEADER BRANDING */
    .central-brand-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 15px 0;
        margin-bottom: 25px;
    }
    .brand-icon-box {
        background: linear-gradient(135deg, rgba(0, 245, 212, 0.1), rgba(123, 44, 233, 0.1));
        border: 1px solid rgba(0, 245, 212, 0.3);
        border-radius: 14px;
        width: 50px;
        height: 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 4px;
        margin-bottom: 12px;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .central-brand-container:hover .brand-icon-box {
        border-color: #7B2CE9;
        box-shadow: 0 0 25px rgba(123, 44, 233, 0.4);
        transform: rotate(180deg) scale(1.05);
    }
    .brand-icon-line {
        width: 20px;
        height: 3px;
        background-color: #00F5D4;
        border-radius: 2px;
    }
    .main-title-header {
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        background: linear-gradient(135deg, #FFFFFF 30%, #00F5D4 70%, #7B2CE9 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 0 !important;
    }
    .brand-sub {
        font-size: 0.75rem !important;
        color: #94A3B8 !important;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 6px !important;
        font-weight: 700;
    }

    /* CYBER GLOW METRIC CARDS */
    .metric-data-card {
        background: linear-gradient(135deg, rgba(17, 24, 42, 0.6) 0%, rgba(10, 15, 28, 0.8) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 2px solid rgba(0, 245, 212, 0.3) !important;
        border-radius: 16px !important;
        padding: 22px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .metric-data-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(135deg, rgba(0, 245, 212, 0.05), transparent);
        opacity: 0; transition: opacity 0.3s ease;
    }
    .metric-data-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 245, 212, 0.4) !important;
        border-top-color: #00F5D4 !important;
        box-shadow: 0 15px 35px rgba(0, 245, 212, 0.1) !important;
    }
    .metric-data-card:hover::before { opacity: 1; }
    .card-metric-label {
        font-size: 0.75rem !important; 
        letter-spacing: 0.1em !important; 
        text-transform: uppercase !important;
        color: #94A3B8 !important; 
        font-weight: 700 !important; 
    }
    .card-metric-primary {
        font-size: 2.1rem !important; 
        font-weight: 800 !important; 
        background: linear-gradient(135deg, #FFFFFF 0%, #E2E8F0 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-top: 8px;
    }
    .card-metric-suffix {
        font-size: 0.75rem !important;
        color: #00F5D4 !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        margin-top: 6px;
    }
    .metric-flex-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
        gap: 18px !important;
        margin-bottom: 25px !important;
    }

    /* HIGH-DYNAMIC NEON DOWNLOAD CARDS */
    .premium-download-card {
        background: rgba(13, 21, 39, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(8px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 15px;
        width: 100%;
    }
    .premium-download-card:hover {
        border-color: rgba(123, 44, 233, 0.4) !important;
        background: rgba(13, 21, 39, 0.65) !important;
        box-shadow: 0 12px 24px rgba(123, 44, 233, 0.1) !important;
        transform: scale(1.01);
    }
    .download-tile-left-content {
        display: flex;
        align-items: center;
        gap: 16px;
        flex: 1;
    }
    .download-tile-icon-frame {
        font-size: 1.4rem;
        background: rgba(255, 255, 255, 0.02);
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.3s ease;
    }
    .premium-download-card:hover .download-tile-icon-frame {
        background: rgba(123, 44, 233, 0.1);
        border-color: rgba(123, 44, 233, 0.4);
    }
    .download-tile-text-fields {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .download-tile-title {
        font-weight: 700;
        font-size: 1rem;
        color: #FFFFFF;
    }
    .download-tile-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    /* PREVENT EXPORT BUTTONS FROM EXPANDING WILDLY */
    div.export-col-wrapper {
        min-width: 160px;
        max-width: 180px;
        flex-shrink: 0;
    }
    div.export-col-wrapper div.stDownloadButton {
        width: 100%;
    }
    div.export-col-wrapper div.stDownloadButton > button {
        background: linear-gradient(135deg, rgba(123, 44, 233, 0.15) 0%, rgba(0, 245, 212, 0.05) 100%) !important;
        color: #00F5D4 !important;
        border: 1px solid rgba(0, 245, 212, 0.3) !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
        text-align: center;
        letter-spacing: 0.03em;
    }
    div.export-col-wrapper div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #7B2CE9 0%, #00F5D4 100%) !important;
        color: #070A12 !important;
        border-color: transparent !important;
        box-shadow: 0 0 20px rgba(0, 245, 212, 0.4) !important;
        transform: translateY(-2px);
    }
    div.export-col-wrapper div.stDownloadButton > button:active {
        transform: translateY(0px);
    }
    </style>
    <div class="neon-orb-3"></div>
    """, unsafe_allow_html=True)


def render_central_brand():
    st.markdown("""
    <div class="central-brand-container">
        <div class="brand-icon-box">
            <div class="brand-icon-line"></div>
            <div class="brand-icon-line"></div>
            <div class="brand-icon-line"></div>
        </div>
        <h2 class="main-title-header">InsightSphere</h2>
        <div class="brand-sub">Simple Business Insights</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_nav(nav_options, nav_icons):
    """
    Stable button-based sidebar navigation. Replaces the previous
    st.radio + brittle CSS approach, which broke because it depended
    on Streamlit's internal (and undocumented) DOM structure.
    """
    if "clean_route" not in st.session_state:
        st.session_state["clean_route"] = nav_options[0]

    st.sidebar.markdown(
        "<p style='font-size:0.7rem; letter-spacing:1.5px; text-transform:uppercase; "
        "color:#64748B; font-weight:800; margin: 10px 0 15px 8px;'>Workspace Navigation</p>",
        unsafe_allow_html=True
    )

    for idx, (label, icon) in enumerate(zip(nav_options, nav_icons)):
        is_active = st.session_state["clean_route"] == label
        color_class = f"nav-btn-idx-{idx % 4}"
        active_class = "nav-btn-active" if is_active else ""
        st.sidebar.markdown(f'<div class="{color_class} {active_class}">', unsafe_allow_html=True)
        if st.sidebar.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state["clean_route"] = label
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    return st.session_state["clean_route"]


def render_metric_grid(kpis):
    cards = []
    for name, value in kpis.items():
        is_currency = any(x in name.lower() for x in ["revenue", "value", "price"])
        suffix_text = "Currency: PKR" if is_currency else ""

        if isinstance(value, float):
            display_value = f"{value:,.2f}"
        elif isinstance(value, int):
            display_value = f"{value:,}"
        else:
            display_value = str(value)

        suffix_html = f'<div class="card-metric-suffix">{suffix_text}</div>' if suffix_text else ""

        cards.append(
            f'<div class="metric-data-card">'
            f'<div class="card-metric-label">{name}</div>'
            f'<div class="card-metric-primary">{display_value}</div>'
            f'{suffix_html}'
            f'</div>'
        )
    st.markdown('<div class="metric-flex-grid">' + "".join(cards) + '</div>', unsafe_allow_html=True)


def fix_sidebar_icon():
    """
    Forces the sidebar toggle icon to a cyan hamburger, regardless of which
    exact CSS selector this Streamlit version uses internally.

    Uses st.components.v1.html because scripts injected via st.markdown()
    do not reliably execute in Streamlit (a known browser/React limitation
    with innerHTML) -- components.html runs in a real iframe with working
    <script> execution, and reaches into the parent page via window.parent.
    """
    import streamlit.components.v1 as components
    components.html("""
    <script>
    function fixIcon() {
        const doc = window.parent.document;
        // Find any button whose aria-label mentions "sidebar" -- this works
        // regardless of the exact data-testid Streamlit uses internally.
        const buttons = doc.querySelectorAll('button');
        buttons.forEach(btn => {
            const label = (btn.getAttribute('aria-label') || '').toLowerCase();
            const isSidebarBtn = label.includes('sidebar');
            if (isSidebarBtn && !btn.dataset.iconFixed) {
                btn.dataset.iconFixed = "true";
                btn.style.background = 'rgba(13, 21, 39, 0.85)';
                btn.style.border = '1px solid rgba(0, 245, 212, 0.4)';
                btn.style.borderRadius = '10px';
                btn.style.width = '38px';
                btn.style.height = '38px';
                btn.style.display = 'flex';
                btn.style.alignItems = 'center';
                btn.style.justifyContent = 'center';

                const svg = btn.querySelector('svg');
                if (svg) svg.style.display = 'none';

                let span = btn.querySelector('.hamburger-icon-fix');
                if (!span) {
                    span = doc.createElement('span');
                    span.className = 'hamburger-icon-fix';
                    span.textContent = '☰';
                    span.style.color = '#00F5D4';
                    span.style.fontSize = '19px';
                    span.style.fontWeight = 'bold';
                    span.style.lineHeight = '1';
                    btn.appendChild(span);
                }
            }
        });
    }
    fixIcon();
    setInterval(fixIcon, 1500);
    </script>
    """, height=0, width=0)


def custom_metric(label, value, suffix=""):
    suffix_html = f'<div class="card-metric-suffix">{suffix}</div>' if suffix else ""
    st.markdown(
        f'<div class="metric-data-card">'
        f'<div class="card-metric-label">{label}</div>'
        f'<div class="card-metric-primary">{value}</div>'
        f'{suffix_html}'
        f'</div>',
        unsafe_allow_html=True
    )