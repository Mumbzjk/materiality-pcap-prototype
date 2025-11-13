import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Materiality & PCAP Prototype",
    page_icon="https://thedataleaf.com/wp-content/uploads/2025/09/Untitled-design-10-1.png",
    layout="centered",
)

# ---------------------------------------------------------
# LOGO HEADER
# ---------------------------------------------------------
LOGO_URL = "https://thedataleaf.com/wp-content/uploads/2025/09/Untitled-design-10-1.png"

col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    st.image(LOGO_URL, width=200)

st.title("AI Materiality & PCAP Scoring Prototype")

st.write(
    "This prototype demonstrates how basic company profile data (sector, geography, size) "
    "can infer likely material ESG/climate topics, emission scopes, and a **PCAP-style 1–5 exposure score**. "
    "It also generates a short narrative to support early-stage materiality assessments. "
)

st.markdown("---")

# ---------------------------------------------------------
# 1. INPUT SECTION
# ---------------------------------------------------------
st.header("1. Company Profile")

col1, col2 = st.columns(2)

with col1:
    sector = st.selectbox(
        "Select Sector",
        [
            "Manufacturing",
            "Software",
            "Retail",
            "Transportation",
            "Energy",
            "Financial Services",
        ],
    )

with col2:
    geography = st.selectbox(
        "Select Geography",
        ["Canada", "United States", "Europe", "Asia", "Global"],
    )

company_size = st.selectbox(
    "Company Size",
    ["Small", "Medium", "Large"],
    help="Size is a proxy for scale, asset intensity, and governance expectations.",
)

st.markdown("---")

# ---------------------------------------------------------
# 2. SCOPES + TOPICS INFERENCE
# ---------------------------------------------------------
def infer_scopes_and_topics(sector, geography, company_size):
    scopes = set()
    topics = set()

    # --- Sector-driven logic ---
    if sector == "Manufacturing":
        scopes.update(["Scope 1", "Scope 2", "Scope 3 (Upstream Supply Chain)"])
        topics.update(["Energy Use", "Emissions", "Waste", "Water", "Worker Safety"])

    elif sector == "Software":
        scopes.update(["Scope 2", "Scope 3 (Business Travel, Cloud Services)"])
        topics.update(["Data Security", "Privacy", "Workforce Wellbeing", "Diversity & Inclusion"])

    elif sector == "Retail":
        scopes.update(["Scope 2", "Scope 3 (Purchased Goods, Logistics, Use Phase)"])
        topics.update(["Supply Chain Impacts", "Packaging & Waste", "Labour Practices"])

    elif sector == "Transportation":
        scopes.update(["Scope 1 (Fuel)", "Scope 2", "Scope 3 (Logistics & Upstream Fuel)"])
        topics.update(["Fuel Efficiency", "Emissions", "Safety", "Logistics Resilience"])

    elif sector == "Energy":
        scopes.update(["Scope 1", "Scope 2", "Scope 3 (Use of Sold Products)"])
        topics.update(["Transition Risk", "Physical Climate Risk", "Community Impact", "Biodiversity"])

    elif sector == "Financial Services":
        scopes.update(["Financed Emissions", "Operational Scope 2"])
        topics.update(["Financed Emissions", "Portfolio Alignment", "Risk Management", "Governance"])


    # --- Geography modifiers ---
    if geography == "Canada":
        topics.update(["Climate Policy Risk", "Carbon Pricing Exposure"])
    elif geography == "Europe":
        topics.update(["Regulatory Compliance (EU/CSRD)", "Supply Chain Due Diligence"])
    elif geography == "Asia":
        topics.update(["Supply Chain Risk", "Physical Climate Risk"])
    elif geography == "Global":
        topics.update(["Cross-Jurisdictional Compliance", "Multi-Region Supply Chains"])

    # --- Size modifiers ---
    if company_size == "Large":
        topics.update(["Governance & Oversight", "Supply Chain Management", "Internal Controls"])
    elif company_size == "Medium":
        topics.update(["Growth & Scaling Risk"])

    # --- Framework readiness signals ---
    topics.update(["ISSB / SASB Alignment Potential"])

    return sorted(scopes), sorted(topics)

# ---------------------------------------------------------
# 3. PCAP SCORING (1–5 MODEL)
# ---------------------------------------------------------
def compute_pcap_score(sector, geography, company_size):

    # Base sector risk (1–5 anchor)
    sector_weight = {
        "Manufacturing": 4,
        "Software": 2,
        "Retail": 3,
        "Transportation": 4,
        "Energy": 5,
        "Financial Services": 3,
    }

    # Geography modifiers (0–1 additive)
    geography_weight = {
        "Canada": 1,
        "United States": 0.5,
        "Europe": 1,
        "Asia": 0.5,
        "Global": 1.5,
    }

    # Size multiplier (smallest → largest)
    size_mult = {
        "Small": 0.9,
        "Medium": 1.0,
        "Large": 1.2,
    }

    # Raw score logic:
    raw_score = (sector_weight[sector] + geography_weight[geography]) * size_mult[company_size]

    # Normalize to 1–5
    final = min(max(round(raw_score), 1), 5)

    # Band naming
    band_map = {
        1: "Low",
        2: "Low–Medium",
        3: "Medium",
        4: "Medium–High",
        5: "High",
    }

    band = band_map[final]
    return final, band

# ---------------------------------------------------------
# 4. RUN ANALYSIS
# ---------------------------------------------------------
if st.button("Generate Materiality Profile"):

    scopes, topics = infer_scopes_and_topics(sector, geography, company_size)
    score_5, band = compute_pcap_score(sector, geography, company_size)

    # --- PCAP Score Display ---
    st.header("2. PCAP Exposure Score (1–5)")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.metric("PCAP Score", f"{score_5} / 5")
    with col_right:
        st.subheader("Exposure Level")
        st.markdown(f"### {band}")

    # --- Scopes & Topics ---
    st.header("3. Predicted Material Emission Scopes & ESG Topics")

    st.subheader("Likely Material Emission Scopes")
    st.write(", ".join(scopes))

    st.subheader("Key ESG and Climate Topics")
    st.write(", ".join(topics))

    # --- Narrative ---
    st.header("4. AI-Generated Narrative (Prototype)")

    narrative = (
        f"This company — a {company_size.lower()} {sector.lower()} organization operating in {geography} — "
        f"receives a **PCAP exposure score of {score_5}/5 ({band})**. "
        f"Based on profile-level indicators, material emission scopes likely include {', '.join(scopes)}. "
        f"Relevant ESG and climate topics include: {', '.join(topics)}. "
        "This provides a structured, pre-materiality view before deeper data collection. "
        "In a full implementation, this logic would draw on sector taxonomies, ISSB/SASB mappings, "
        "and historical ESGTree assessments to refine scoring and recommendations."
    )

    st.write(narrative)

    st.caption("Prototype only — logic evolves with ESGTree data, frameworks, and AI models.")

else:
    st.info("Select company details above, then click **Generate Materiality Profile**.")
