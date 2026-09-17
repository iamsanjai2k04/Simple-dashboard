import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Aussie City Match",
    page_icon="🇦🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LIGHT COLOUR DESIGN
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F7FBF9;
}

/* Main page width */
.block-container {
    max-width: 1300px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Main text */
h1 {
    color: #123C35 !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #176B5B !important;
}

p {
    color: #314F49;
    font-size: 16px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EAF7F3;
    border-right: 1px solid #D1E8E1;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #DCEAE6;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(30, 80, 65, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #55756E;
}

[data-testid="stMetricValue"] {
    color: #123C35;
}

/* Charts */
[data-testid="stVegaLiteChart"] {
    background-color: white;
    padding: 12px;
    border-radius: 18px;
    border: 1px solid #DFEBE7;
}

/* Data table */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 16px;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 16px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# Prototype values — verify/source before final submission
# ============================================================

cities = pd.DataFrame({

    "City": [
        "Sydney",
        "Melbourne",
        "Brisbane",
        "Perth",
        "Adelaide",
        "Canberra",
        "Hobart",
        "Darwin"
    ],

    "State": [
        "NSW",
        "VIC",
        "QLD",
        "WA",
        "SA",
        "ACT",
        "TAS",
        "NT"
    ],

    "Latitude": [
        -33.8688,
        -37.8136,
        -27.4698,
        -31.9523,
        -34.9285,
        -35.2809,
        -42.8821,
        -12.4634
    ],

    "Longitude": [
        151.2093,
        144.9631,
        153.0251,
        115.8613,
        138.6007,
        149.1300,
        147.3272,
        130.8456
    ],

    "Summer °C": [
        26, 26, 29, 32,
        29, 28, 22, 32
    ],

    "Winter °C": [
        17, 14, 21, 19,
        16, 12, 12, 31
    ],

    "Sunshine hrs/day": [
        7.2, 6.0, 7.4, 8.8,
        7.6, 7.7, 5.9, 8.5
    ],

    "Rainfall mm": [
        1213, 648, 1149, 731,
        547, 620, 626, 1723
    ]
})


# ============================================================
# TITLE
# ============================================================

st.title("🇦🇺 Aussie City Match")

st.subheader(
    "Find the Australian capital city that fits your lifestyle"
)

st.write(
    "Explore Australia's capital cities through climate, "
    "location and interactive visualisations. Compare cities "
    "and discover which climate is closest to your preferences."
)

st.info(
    "🧭 Use the controls in the sidebar to personalise your journey."
)

st.divider()


# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.title("🇦🇺 Explore Australia")

st.sidebar.write(
    "Choose a city and customise what you want to explore."
)

selected_city = st.sidebar.selectbox(
    "📍 Choose a capital city",
    cities["City"]
)

comparison = st.sidebar.selectbox(
    "📊 Compare cities by",
    [
        "☀️ Sunshine",
        "🔥 Summer temperature",
        "❄️ Winter temperature",
        "🌧️ Annual rainfall"
    ]
)

ideal_temp = st.sidebar.slider(
    "🌡️ Your ideal summer temperature",
    min_value=20,
    max_value=35,
    value=27
)

show_data = st.sidebar.checkbox(
    "📋 Show raw data"
)

st.sidebar.divider()

st.sidebar.caption(
    "36104 · Data Visualisation and Narratives"
)


# ============================================================
# SELECTED CITY
# ============================================================

city = cities[
    cities["City"] == selected_city
].iloc[0]

st.header(
    f"📍 Discover {selected_city}, {city['State']}"
)

st.write(
    f"Here's a quick climate snapshot of **{selected_city}**."
)


# ============================================================
# METRIC CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "☀️ Sunshine",
        f"{city['Sunshine hrs/day']} hrs/day"
    )

with col2:
    st.metric(
        "🔥 Summer",
        f"{city['Summer °C']}°C"
    )

with col3:
    st.metric(
        "❄️ Winter",
        f"{city['Winter °C']}°C"
    )

with col4:
    st.metric(
        "🌧️ Rainfall",
        f"{city['Rainfall mm']:,} mm"
    )


# ============================================================
# CITY MAP
# ============================================================

st.header("🗺️ Where is it?")

st.write(
    f"See where **{selected_city}** is located in Australia."
)

selected_map = pd.DataFrame({
    "lat": [city["Latitude"]],
    "lon": [city["Longitude"]]
})

st.map(
    selected_map,
    zoom=4,
    use_container_width=True
)


# ============================================================
# CITY COMPARISON
# ============================================================

st.header("📊 Compare Australia's capitals")

st.write(
    "Change the comparison option in the sidebar "
    "to explore different patterns."
)

if comparison == "☀️ Sunshine":

    selected_column = "Sunshine hrs/day"
    chart_title = "Typical daily sunshine"

elif comparison == "🔥 Summer temperature":

    selected_column = "Summer °C"
    chart_title = "Typical summer maximum temperature"

elif comparison == "❄️ Winter temperature":

    selected_column = "Winter °C"
    chart_title = "Typical winter maximum temperature"

else:

    selected_column = "Rainfall mm"
    chart_title = "Approximate annual rainfall"


chart_data = (
    cities[
        ["City", selected_column]
    ]
    .sort_values(
        selected_column,
        ascending=False
    )
    .set_index("City")
)

st.subheader(chart_title)

st.bar_chart(
    chart_data,
    use_container_width=True
)


# ============================================================
# TEMPERATURE COMPARISON
# ============================================================

st.header("🌤️ Summer vs Winter")

st.write(
    "Australia has very different climates from north to south. "
    "Compare typical summer and winter temperatures."
)

temperature_data = (
    cities[
        [
            "City",
            "Summer °C",
            "Winter °C"
        ]
    ]
    .set_index("City")
)

st.bar_chart(
    temperature_data,
    use_container_width=True
)


# ============================================================
# UNIQUE CITY MATCH FEATURE
# ============================================================

st.header("🧳 Find your climate match")

st.write(
    "Choose your ideal summer temperature using the slider "
    "in the sidebar. We'll find the closest capital city."
)

match_data = cities.copy()

match_data["Difference"] = abs(
    match_data["Summer °C"] - ideal_temp
)

closest = match_data.loc[
    match_data["Difference"].idxmin()
]

st.success(
    f"🌿 Your ideal summer temperature is **{ideal_temp}°C**. "
    f"The closest match in this small comparison is "
    f"**{closest['City']}, {closest['State']}**, "
    f"with a typical summer maximum of approximately "
    f"**{closest['Summer °C']}°C**."
)


# ============================================================
# SUNSHINE VS RAINFALL
# ============================================================

st.header("☀️ Sunshine & Rain")

st.write(
    "Explore the relationship between sunshine and rainfall "
    "across Australian capital cities."
)

sun_rain = cities[
    [
        "City",
        "Sunshine hrs/day",
        "Rainfall mm"
    ]
]

st.scatter_chart(
    sun_rain,
    x="Sunshine hrs/day",
    y="Rainfall mm",
    size=100,
    use_container_width=True
)


# ============================================================
# ALL CAPITALS MAP
# ============================================================

st.header("🌏 Eight capitals, one country")

st.write(
    "From tropical Darwin to cool Hobart, Australia's "
    "capital cities span a huge geographic area."
)

all_locations = cities[
    [
        "City",
        "Latitude",
        "Longitude"
    ]
].rename(
    columns={
        "Latitude": "lat",
        "Longitude": "lon"
    }
)

st.map(
    all_locations,
    zoom=3,
    use_container_width=True
)


# ============================================================
# RAW DATA CHECKBOX
# ============================================================

if show_data:

    st.header("🔍 Explore the data")

    st.write(
        "This table contains the values used "
        "to create the dashboard."
    )

    st.dataframe(
        cities,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FINAL SECTION
# ============================================================

st.divider()

st.header("💡 What can we learn?")

st.write(
    """
    Australia is not one climate. Its capital cities range
    from tropical conditions in the north to much cooler
    conditions in the south.

    **Aussie City Match** lets users interact with these
    differences instead of simply reading a static table.
    """
)

st.caption(
    "🇦🇺 Aussie City Match | "
    "36104 · Data Visualisation and Narratives"
)
