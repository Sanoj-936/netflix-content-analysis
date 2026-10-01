"""Netflix Content Analysis - Interactive Streamlit Dashboard

An end-to-end data analytics web application visualizing Netflix's global content
catalog, historical growth, genre dynamics, content ratings, runtime distributions,
and business strategy insights.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Netflix Content Analysis | EDA Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Relative directory resolution
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "netflix_titles.csv"


@st.cache_data
def load_and_prepare_data(file_path: Path) -> pd.DataFrame:
    """Load and preprocess the Netflix titles dataset."""
    if not file_path.exists():
        # Fallback search if current working directory varies
        alt_path = Path("data/netflix_titles.csv")
        if alt_path.exists():
            file_path = alt_path
        else:
            raise FileNotFoundError(f"Dataset not found at {file_path}")

    df = pd.read_csv(file_path)

    # Impute missing values matching the project's analytical workflow
    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Not Rated")

    # Clean and parse date_added
    df["date_added"] = df["date_added"].astype(str).str.strip()
    df["date_added_clean"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added_clean"].dt.year
    df["month_added"] = df["date_added_clean"].dt.month_name()

    # Extract numeric duration
    df["duration_numeric"] = df["duration"].str.extract(r"(\d+)").astype(float)

    return df


# Load data
try:
    df_raw = load_and_prepare_data(DATA_PATH)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
    width=160,
)
st.sidebar.title("Catalog Filters")

# Content Type filter
content_types = ["All"] + sorted(df_raw["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Content Type", content_types, index=0)

# Release Year slider
min_year = int(df_raw["release_year"].min())
max_year = int(df_raw["release_year"].max())
selected_years = st.sidebar.slider(
    "Release Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
)

# Genres list
all_genres = sorted(
    df_raw["listed_in"]
    .str.split(", ")
    .explode()
    .dropna()
    .unique()
    .tolist()
)
selected_genres = st.sidebar.multiselect(
    "Filter by Genre (matches any)",
    options=all_genres,
    default=[],
)

# Rating filter
all_ratings = sorted(df_raw["rating"].dropna().unique().tolist())
selected_ratings = st.sidebar.multiselect(
    "Filter by Rating",
    options=all_ratings,
    default=[],
)

# Title search filter
search_term = st.sidebar.text_input("Search Title or Cast", "").strip().lower()

# Apply filters
filtered_df = df_raw.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= selected_years[0])
    & (filtered_df["release_year"] <= selected_years[1])
]

if selected_genres:
    pattern = "|".join([r"\b" + g + r"\b" for g in selected_genres])
    filtered_df = filtered_df[filtered_df["listed_in"].str.contains(pattern, regex=True, na=False)]

if selected_ratings:
    filtered_df = filtered_df[filtered_df["rating"].isin(selected_ratings)]

if search_term:
    filtered_df = filtered_df[
        filtered_df["title"].str.lower().str.contains(search_term, na=False)
        | filtered_df["cast"].str.lower().str.contains(search_term, na=False)
        | filtered_df["director"].str.lower().str.contains(search_term, na=False)
    ]

# ----------------- MAIN DASHBOARD HEADER -----------------
st.title("🎬 Netflix Content Analysis & Strategy Dashboard")
st.markdown(
    """
    An exploratory and strategic business intelligence analysis of **8,800+ Netflix titles**.
    Uncover historical content growth patterns, global distribution, genre concentration, 
    and feature duration dynamics.
    """
)

# KPI Cards
total_filtered = len(filtered_df)
total_movies = int((filtered_df["type"] == "Movie").sum())
total_tv = int((filtered_df["type"] == "TV Show").sum())
pct_movies = round((total_movies / total_filtered * 100), 1) if total_filtered > 0 else 0
pct_tv = round((total_tv / total_filtered * 100), 1) if total_filtered > 0 else 0

countries_series = (
    filtered_df[filtered_df["country"] != "Unknown"]["country"]
    .str.split(", ")
    .explode()
)
unique_countries = int(countries_series.nunique())

genres_series = filtered_df["listed_in"].str.split(", ").explode()
unique_genres = int(genres_series.nunique())

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Titles", f"{total_filtered:,}")
with col2:
    st.metric("Movies", f"{total_movies:,} ({pct_movies}%)")
with col3:
    st.metric("TV Shows", f"{total_tv:,} ({pct_tv}%)")
with col4:
    st.metric("Active Countries", f"{unique_countries:,}")
with col5:
    st.metric("Unique Genres", f"{unique_genres:,}")

st.markdown("---")

# ----------------- DASHBOARD TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📊 Content Distribution",
        "📈 Growth Trends",
        "🌍 Country Analysis",
        "🎭 Genre Dynamics",
        "⏱️ Duration & Ratings",
        "🔍 Data Explorer & Insights",
    ]
)

# TAB 1: Content Distribution
with tab1:
    st.subheader("Content Type & Portfolio Distribution")
    col_a, col_b = st.columns(2)

    with col_a:
        type_counts = filtered_df["type"].value_counts().reset_index()
        type_counts.columns = ["Content Type", "Count"]
        fig_type = px.pie(
            type_counts,
            values="Count",
            names="Content Type",
            title="Movies vs TV Shows Ratio",
            color="Content Type",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#221F1F"},
            hole=0.45,
        )
        fig_type.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_type, use_container_width=True)

    with col_b:
        rating_counts = (
            filtered_df["rating"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        rating_counts.columns = ["Rating", "Count"]
        fig_rating = px.bar(
            rating_counts,
            x="Rating",
            y="Count",
            title="Top 10 Content Ratings",
            color="Count",
            color_continuous_scale="Reds",
        )
        fig_rating.update_layout(xaxis_title="Rating Category", yaxis_title="Number of Titles")
        st.plotly_chart(fig_rating, use_container_width=True)

    st.info(
        "💡 **Key Observation**: Movies represent approximately ~70% of the entire Netflix catalog, "
        "highlighting an entertainment strategy built on standalone, high-volume film releases."
    )

# TAB 2: Growth Trends
with tab2:
    st.subheader("Historical Addition Trends (Over Years)")

    growth_df = (
        filtered_df.dropna(subset=["year_added"])
        .groupby(["year_added", "type"])
        .size()
        .reset_index(name="Count")
    )

    if not growth_df.empty:
        fig_growth = px.line(
            growth_df,
            x="year_added",
            y="Count",
            color="type",
            markers=True,
            title="Annual Content Growth on Netflix by Type",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#000000"},
        )
        fig_growth.update_layout(
            xaxis_title="Year Added to Netflix",
            yaxis_title="Number of Titles Added",
            hovermode="x unified",
        )
        st.plotly_chart(fig_growth, use_container_width=True)

        # Monthly seasonality heatmap / bar chart
        monthly_df = (
            filtered_df.dropna(subset=["month_added"])
            .groupby(["month_added", "type"])
            .size()
            .reset_index(name="Count")
        )
        months_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        monthly_df["month_added"] = pd.Categorical(
            monthly_df["month_added"], categories=months_order, ordered=True
        )
        monthly_df = monthly_df.sort_values("month_added")

        fig_month = px.bar(
            monthly_df,
            x="month_added",
            y="Count",
            color="type",
            barmode="group",
            title="Seasonality: Titles Added by Month",
            color_discrete_map={"Movie": "#E50914", "TV Show": "#564D4D"},
        )
        fig_month.update_layout(xaxis_title="Month", yaxis_title="Titles Added")
        st.plotly_chart(fig_month, use_container_width=True)
    else:
        st.warning("No date added data available for selected filters.")

    st.info(
        "💡 **Growth Insight**: Content acquisitions expanded exponentially post-2016, "
        "reaching a peak in 2019 before stabilizing around 2020 due to production cycles."
    )

# TAB 3: Country Analysis
with tab3:
    st.subheader("Top Content-Producing Countries")

    valid_countries = filtered_df[filtered_df["country"] != "Unknown"]
    country_counts = (
        valid_countries["country"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(15)
        .reset_index()
    )
    country_counts.columns = ["Country", "Titles"]

    fig_country = px.bar(
        country_counts,
        x="Titles",
        y="Country",
        orientation="h",
        title="Top 15 Countries by Production Volume",
        color="Titles",
        color_continuous_scale="Reds",
    )
    fig_country.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_country, use_container_width=True)

    st.info(
        "💡 **Geographic Insight**: While the United States leads aggregate production by a wide margin, "
        "India and the United Kingdom follow as major content powerhouses, indicating strong regional investment."
    )

# TAB 4: Genre Dynamics
with tab4:
    st.subheader("Top Genre Distribution")

    genre_counts = (
        filtered_df["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(15)
        .reset_index()
    )
    genre_counts.columns = ["Genre", "Number of Titles"]

    fig_genres = px.bar(
        genre_counts,
        x="Number of Titles",
        y="Genre",
        orientation="h",
        title="Top 15 Genres on Netflix",
        color="Number of Titles",
        color_continuous_scale="Viridis",
    )
    fig_genres.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_genres, use_container_width=True)

    st.info(
        "💡 **Genre Insight**: 'International Movies', 'Dramas', and 'Comedies' form the backbone "
        "of Netflix catalog hours, appealing to universal and multilingual subscriber demographics."
    )

# TAB 5: Duration & Ratings
with tab5:
    st.subheader("Movie Run-Time & TV Show Seasonality")
    col_dur1, col_dur2 = st.columns(2)

    movies_df = filtered_df[filtered_df["type"] == "Movie"]
    tv_df = filtered_df[filtered_df["type"] == "TV Show"]

    with col_dur1:
        if not movies_df.empty:
            fig_hist = px.histogram(
                movies_df,
                x="duration_numeric",
                nbins=35,
                title="Movie Duration Distribution (Minutes)",
                color_discrete_sequence=["#E50914"],
            )
            fig_hist.update_layout(
                xaxis_title="Duration (Minutes)",
                yaxis_title="Frequency",
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            dur_mean = movies_df["duration_numeric"].mean()
            dur_median = movies_df["duration_numeric"].median()
            st.caption(
                f"Average Movie Duration: **{dur_mean:.1f} min** | "
                f"Median: **{dur_median:.1f} min** | "
                f"Range: **{movies_df['duration_numeric'].min():.0f} - {movies_df['duration_numeric'].max():.0f} min**"
            )

    with col_dur2:
        if not tv_df.empty:
            season_counts = (
                tv_df["duration_numeric"]
                .value_counts()
                .head(8)
                .reset_index()
            )
            season_counts.columns = ["Seasons", "TV Shows"]
            season_counts["Seasons"] = season_counts["Seasons"].astype(str) + " Season(s)"

            fig_seasons = px.bar(
                season_counts,
                x="Seasons",
                y="TV Shows",
                title="TV Show Seasons Distribution",
                color_discrete_sequence=["#221F1F"],
            )
            fig_seasons.update_layout(xaxis_title="Season Count", yaxis_title="Number of Shows")
            st.plotly_chart(fig_seasons, use_container_width=True)

            one_season_pct = (
                (tv_df["duration_numeric"] == 1).sum() / len(tv_df) * 100
            ) if len(tv_df) > 0 else 0
            st.caption(f"**{one_season_pct:.1f}%** of TV Shows conclude after Season 1.")

# TAB 6: Data Explorer & Insights
with tab6:
    st.subheader("Data Explorer & Export")

    # Display dataset preview
    st.dataframe(
        filtered_df[
            [
                "title",
                "type",
                "director",
                "country",
                "release_year",
                "rating",
                "duration",
                "listed_in",
            ]
        ],
        use_container_width=True,
        height=380,
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="netflix_filtered_analysis.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.subheader("📌 Key Strategic Insights & Recommendations")
    st.markdown(
        """
        1. **Rapid Scaling & Strategy Shift**: Netflix experienced aggressive library expansion between 2016 and 2019, followed by a pivot toward higher-quality original programming and curated additions.
        2. **Standalone Content Dominance**: Movies dominate (~70%) over series, showing customer appetite for quick-consumption evening entertainment alongside serialized binge content.
        3. **Internationalization Opportunity**: International Movies & TV Shows are top-ranking genres. Continuing to localize investments outside the US (e.g. Asia-Pacific, Latin America, EMEA) directly fuels subscriber acquisition.
        4. **Standardized Runtime**: Feature film runtimes peak tightly between 80–120 minutes, indicating viewers favor standard film lengths over 2.5h+ epics.
        5. **Series Longevity**: A vast majority of series consist of 1–2 seasons. Netflix can focus on multi-season retention drivers to maximize lifetime customer value.
        """
    )

# Footer
st.markdown("---")
st.markdown(
    "<center><small>Netflix Content Analysis Portfolio Project | Built with Python, Pandas & Streamlit</small></center>",
    unsafe_allow_html=True,
)
