import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Materiality & PCAP Prototype",
    page_icon="🌱",
    layout="centered",
)

# ---------------------------------------------------------
# LOGO AT TOP
# ---------------------------------------------------------
LOGO_URL = "https://thedataleaf.com/wp-content/uploads/2025/09/Untitled-design-10-1.png"

# Center the logo
col_logo = st.columns([1, 2, 1])
with col_logo[1]:
    st.image(LOGO_URL, width=200)

st.title("AI Materiality & PCAP Scoring Prototype")
st.write(
    "This prototype demonstrates how company profile data,sector, geography, and size"
    "can be used to infer material ESG/climate topics, emission scopes, and a PCAP-style "
    "risk score. It also auto-generates a narrative to support materiality assessments."
)

st.markdown("---")

# ---------------------------------------------------------
# 1. INPUT SECTION — COMPANY PROFILE
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
    help="Approximate scale based on revenue, assets or headcount.",
)

st.markdown("---")

# ---------------------------------------------------------
# 2. LOGIC — INFER MATERIAL SCOPES & TOPICS
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
        topics.update(["Regulatory Compliance (EU)", "Supply Chain Due Diligence"])
    elif geography == "Asia":
        topics.update(["Supply Chain Risk", "Physical Climate Risk"])
    elif geography == "Global":
        topics.update(["Cross-Jurisdictional Compliance", "Multi-Region Supply Chains"])

    # --- Size modifiers ---
    if company_size == "Large":
        topics.update(["Governance & Oversight", "Supply Chain Management", "Internal Controls"])
    elif company_size == "Medium":
        topics.update(["Growth & Scaling Risk"])

    return sorted(scopes), sorted(topics)


# ---------------------------------------------------------
# 3. PCAP-STYLE RISK SCORING LOGIC
# ---------------------------------------------------------
def compute_pcap_score(sector, geography, company_size):
    sector_risk = {
        "Manufacturing": 8,
        "Software": 4,
        "Retail": 6,
        "Transportation": 9,
        "Energy": 10,
        "Financial Services": 7,
    }

    geography_risk = {
        "Canada": 4,
        "United States": 3,
        "Europe": 4,
        "Asia": 3,
        "Global": 5,
    }

    size_multiplier = {
        "Small": 0.8,
        "Medium": 1.0,
        "Large": 1.2,
    }

    base_score = sector_risk[sector] + geography_risk[geography]
    scaled_score = base_score * size_multiplier[company_size]

    final_score = int(min(scaled_score * 5, 100))

    if final_score < 35:
        band = "Low"
    elif final_score < 70:
        band = "Medium"
    else:
        band = "High"

    return final_score, band


# ---------------------------------------------------------
# 4. RUN ANALYSIS
# ---------------------------------------------------------
if st.button("Generate Materiality Profile"):

    scopes, topics = infer_scopes_and_topics(sector, geography, company_size)
    score, score_band = compute_pcap_score(sector, geography, company_size)

    # --- Score Display ---
    st.header("2. PCAP-style Risk Scoring")

    col_score, col_band = st.columns([2, 1])

    with col_score:
        st.metric("PCAP Risk Score", f"{score} / 100")
        st.progress(score)

    with col_band:
        st.subheader("Risk Band")
        st.markdown(f"### {score_band}")

    # --- Material Outputs ---
    st.header("3. Predicted Material Scopes & ESG Topics")

    st.subheader("Likely Material Emission Scopes")
    st.write(", ".join(scopes))

    st.subheader("Key ESG and Climate Topics")
    st.write(", ".join(topics))

    # --- Narrative ---
    st.header("4. AI-Generated Narrative (Prototype)")

    narrative = (
        f"A {company_size.lower()} {sector.lower()} company in {geography} "
        f"has a **{score_band.lower()} PCAP-style risk score** of **{score}/100**. "
        f"Material emission scopes likely include {', '.join(scopes)}. "
        f"Key ESG and climate topics relevant to this profile include: {', '.join(topics)}. "
        "This provides a structured starting point for materiality assessment, prioritization, "
        "and disclosure planning."
    )

    st.write(narrative)

    st.caption(
        "Prototype only — logic and mappings would be refined with ESGTree taxonomies, "
        "frameworks, and client datasets in production."
    )

else:
    st.info("Select company details above, then click **Generate Materiality Profile** to begin.")
