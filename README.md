# 🎬 Netflix Content Analysis & Strategy Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Data Analytics portfolio project exploring **8,807 titles** on Netflix. This repository features an in-depth Exploratory Data Analysis (EDA) notebook and an interactive **Streamlit Web Application** designed to uncover content strategy patterns, growth trajectories, international diversification, and catalog composition.

---

## 🚀 Live Demo

> 🌐 **Live Web Application:** [Open Netflix Content Analysis Dashboard](https://share.streamlit.io) *(Deployment instructions below)*

---

## 📌 Project Overview

With thousands of movies and television shows available globally, streaming platforms rely heavily on data-informed acquisition and production strategies. This project investigates the Netflix catalog to answer key business and operational questions:

- **Portfolio Composition:** What is the balance between standalone feature films and episodic series?
- **Growth Over Time:** When did Netflix experience its most aggressive library expansion, and how did market competition and production cycles impact post-2019 additions?
- **Global Strategy:** Which countries produce the highest volume of content, and where are emerging regional growth markets?
- **Genre & Audience Targeting:** Which genres dominate catalog hours, and how is content distributed across maturity ratings?
- **Viewer Habits & Runtime:** What is the ideal runtime for Netflix films, and how long do TV series typically sustain user engagement?

The project couples rigorous Jupyter Notebook data cleaning and statistical exploration with an interactive, multi-dimensional **Streamlit dashboard**.

---

## 🖼️ Dashboard Preview

![Netflix Content Analysis Dashboard](assets/dashboard.png)

---

## 🎯 Key Features

- **Executive KPI Scorecard:** Instant high-level metrics for total titles, movie/TV split, active production countries, unique genres, and peak acquisition years.
- **Dynamic Multi-Parameter Filtering:** Real-time filtering by content type (Movies/TV Shows), release year range, genre tags, maturity rating, and free-text search (title, director, cast).
- **Interactive Visualizations (Plotly):**
  - Donut and bar charts for Movies vs. TV Shows ratio.
  - Time series area/line charts tracking yearly catalog additions (2008–2021).
  - Monthly acquisition seasonality tracking.
  - Horizontal bar charts for top 15 producing nations and top 15 genres.
  - Runtime distribution histograms with mean and median runtime metrics.
  - TV series season longevity distributions.
- **Data Explorer & CSV Export:** Searchable, paginated data table with one-click filtered dataset export.
- **Reproducible Data Pipeline:** Clean `src/data_processing.py` module for portable loading, cleaning, and metric computation.

---

## 📊 Key Analytical Insights

| Analytical Focus | Finding | Strategic Implication |
|---|---|---|
| **Content Distribution** | **69.6% Movies** (6,131 titles) vs. **30.4% TV Shows** (2,676 titles) | Movies provide broad, standalone viewing variety; TV shows drive long-term subscriber retention and binge viewing. |
| **Expansion Peak** | Exponential growth began in **2016**, reaching an all-time peak of **2,016 additions in 2019** | Post-2019 moderation reflects industry-wide shift toward curated Originals and production delays during 2020. |
| **Geographic Footprint** | **United States (3,689 titles)**, **India (1,046 titles)**, and **United Kingdom (804 titles)** lead output | Significant diversification into India, UK, Canada, France, and South Korea underscores aggressive international localization. |
| **Genre Dominance** | **International Movies (2,752)**, **Dramas (2,427)**, and **Comedies (1,674)** top the catalog | Non-English and local-language productions are critical growth drivers for global subscriber acquisition. |
| **Movie Runtime** | Distribution peaks tightly between **80 and 120 minutes** (Average: ~99.6 min) | Viewers strongly favor standard 90–100 minute feature lengths over extended 2.5h+ runtimes. |
| **Series Longevity** | Over **67% of TV shows conclude after Season 1**; <10% exceed 3 seasons | Single-season investments minimize sunk costs for underperforming titles while identifying break-out franchises. |

---

## 📈 Visualizations from EDA

| Content Growth | Movies vs. TV Shows | Top Genres |
|:---:|:---:|:---:|
| ![Growth](images/netflix_growth.png) | ![Type](images/movies_vs_tvshows.png) | ![Genres](images/top_genres.png) |

| Top Countries | Content Ratings | Movie Durations |
|:---:|:---:|:---:|
| ![Countries](images/top_countries.png) | ![Ratings](images/rating_distribution.png) | ![Duration](images/movie_duration.png) |

---

## 📁 Dataset Details

- **Dataset:** Netflix Movies and TV Shows Dataset (scraped via Flixable)
- **Observations:** 8,807 records
- **Attributes:** 12 raw features

| Column | Type | Description | Cleaning Applied |
|---|---|---|---|
| `show_id` | String | Unique record identifier (`s1`, `s2`, ...) | Primary key |
| `type` | String | Format: `Movie` or `TV Show` | Categorical verification |
| `title` | String | Title of the production | Cleaned string formatting |
| `director` | String | Director name(s) | 2,634 missing values imputed as `'Unknown'` |
| `cast` | String | Leading cast members (comma-separated) | 825 missing values imputed as `'Unknown'` |
| `country` | String | Country/countries of production | 831 missing values imputed as `'Unknown'` |
| `date_added` | String | Date title was added to Netflix | Stripped whitespace, parsed to `datetime64` |
| `release_year` | Integer | Original release year (1925 – 2021) | Validated integer range |
| `rating` | String | Maturity rating code (`TV-MA`, `TV-14`, `R`, etc.) | 4 missing values imputed as `'Not Rated'` |
| `duration` | String | Duration in minutes or seasons | Parsed to numeric `duration_numeric` |
| `listed_in` | String | Associated genre categories | Unnested via string splitting |
| `description` | String | Editorial summary synopsis | Text reference |

---

## 🛠️ Tech Stack

- **Core Language:** Python 3.11
- **Data Manipulation & Analysis:** Pandas, NumPy
- **Data Visualization:** Plotly Express, Plotly Graph Objects, Matplotlib, Seaborn
- **Web Application Framework:** Streamlit
- **Notebook Environment:** Jupyter Notebook / IPython
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```text
netflix-content-analysis/
│
├── assets/
│   ├── dashboard.png                 # Full dashboard preview for README
│   └── dashboard_overview.png        # High-res analytics summary banner
│
├── data/
│   └── netflix_titles.csv            # 8,807-record raw Netflix dataset (3.4 MB)
│
├── images/                           # Generated EDA chart exports
│   ├── movie_duration.png
│   ├── movies_vs_tvshows.png
│   ├── netflix_growth.png
│   ├── rating_distribution.png
│   ├── top_countries.png
│   ├── top_director.png
│   └── top_genres.png
│
├── notebooks/
│   └── netflix_analysis.ipynb        # In-depth Exploratory Data Analysis notebook
│
├── src/
│   ├── __init__.py
│   └── data_processing.py            # Modular, reusable ETL & analytics functions
│
├── .gitignore                        # Git ignore patterns (.venv, pycache, etc.)
├── .python-version                   # Python runtime pinning (3.11)
├── app.py                            # Interactive Streamlit Web Application
├── LICENSE                           # MIT License
├── README.md                         # Comprehensive portfolio documentation
└── requirements.txt                  # Pinned project dependencies
```

---

## 💻 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR_USERNAME>/netflix-content-analysis.git
cd netflix-content-analysis
```

### 2. Create and Activate a Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

### 5. Run the Jupyter Notebook (Optional)
```bash
jupyter notebook notebooks/netflix_analysis.ipynb
```

---

## ☁️ Deployment Guide

### Deploying to Streamlit Community Cloud (Free)

1. Fork or push this repository to your personal GitHub account.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New app"**.
4. Configure the deployment settings:
   - **Repository:** `<YOUR_USERNAME>/netflix-content-analysis`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**.
6. Streamlit Community Cloud will automatically detect `requirements.txt` and `.python-version`, install dependencies, and launch your live dashboard in 1–2 minutes.

---

## 🔮 Future Improvements

- [ ] **Sentiment Analysis:** Apply NLP (VADER / TextBlob / RoBERTa) to editorial descriptions to evaluate thematic tones across genres.
- [ ] **External Rating Integration:** Enrich the dataset with IMDb and Rotten Tomatoes audience and critic scores via OMDb API.
- [ ] **Content Recommendation Engine:** Build a content-based filtering system using TF-IDF and cosine similarity on cast, director, and genre attributes.
- [ ] **Actor Co-occurrence Networks:** Visualize frequent cast collaboration networks using network graphs.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

---

## 👨‍💻 Author

**Vijay Saroj**  
B.Tech (ECE), Indian Institute of Technology (ISM) Dhanbad  
- **GitHub:** [@vijaysaroj](https://github.com)
- **Role:** Data Analyst / Data Scientist
