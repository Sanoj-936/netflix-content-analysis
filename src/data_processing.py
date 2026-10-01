"""Data processing and feature extraction module for Netflix Content Analysis.

Provides portable, reproducible functions to load, clean, and aggregate
the Netflix titles dataset.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "netflix_titles.csv"


def load_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Load the Netflix dataset from a relative, portable path.

    Parameters
    ----------
    filepath : Optional[Path]
        Custom path to netflix_titles.csv. Defaults to project data directory.

    Returns
    -------
    pd.DataFrame
        Loaded raw DataFrame.
    """
    path = filepath if filepath is not None else DEFAULT_DATA_PATH
    if not Path(path).exists():
        # Fallback to local data folder if running from different working directory
        alternative = Path("data/netflix_titles.csv")
        if alternative.exists():
            path = alternative
        else:
            raise FileNotFoundError(f"Netflix dataset not found at {path} or {alternative}")
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Netflix dataset matching the exploratory analysis.

    - Fills missing directors, cast, and country with 'Unknown'
    - Fills missing ratings with 'Not Rated'
    - Standardizes date_added to datetime and extracts year_added and month_added
    - Parses duration into numeric values for Movies (minutes) and TV Shows (seasons)

    Parameters
    ----------
    df : pd.DataFrame
        Raw Netflix DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with extracted analysis columns.
    """
    clean_df = df.copy()

    # Impute categorical missing values
    clean_df['director'] = clean_df['director'].fillna('Unknown')
    clean_df['cast'] = clean_df['cast'].fillna('Unknown')
    clean_df['country'] = clean_df['country'].fillna('Unknown')
    clean_df['rating'] = clean_df['rating'].fillna('Not Rated')

    # Parse date_added
    clean_df['date_added'] = clean_df['date_added'].astype(str).str.strip()
    clean_df['date_added_clean'] = pd.to_datetime(clean_df['date_added'], errors='coerce')
    clean_df['year_added'] = clean_df['date_added_clean'].dt.year

    # Movie duration in minutes
    clean_df['duration_num'] = clean_df['duration'].str.extract(r'(\d+)').astype(float)
    clean_df['duration_type'] = np.where(
        clean_df['type'] == 'Movie', 'Minutes', 'Seasons'
    )

    return clean_df


def get_summary_metrics(df: pd.DataFrame) -> dict:
    """Compute high-level summary KPIs for the Netflix catalog.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned Netflix DataFrame.

    Returns
    -------
    dict
        Dictionary of key metrics.
    """
    total_titles = len(df)
    total_movies = int((df['type'] == 'Movie').sum())
    total_tv_shows = int((df['type'] == 'TV Show').sum())
    pct_movies = round((total_movies / total_titles) * 100, 1) if total_titles > 0 else 0
    pct_tv = round((total_tv_shows / total_titles) * 100, 1) if total_titles > 0 else 0

    countries_series = df[df['country'] != 'Unknown']['country'].str.split(', ').explode()
    unique_countries = int(countries_series.nunique())

    genres_series = df['listed_in'].str.split(', ').explode()
    unique_genres = int(genres_series.nunique())

    min_year = int(df['release_year'].min()) if not df.empty else 0
    max_year = int(df['release_year'].max()) if not df.empty else 0

    return {
        "total_titles": total_titles,
        "total_movies": total_movies,
        "total_tv_shows": total_tv_shows,
        "pct_movies": pct_movies,
        "pct_tv": pct_tv,
        "unique_countries": unique_countries,
        "unique_genres": unique_genres,
        "release_year_range": f"{min_year} - {max_year}"
    }


def get_top_genres(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Extract top N genres by title count."""
    genres = df['listed_in'].str.split(', ').explode()
    return genres.value_counts().head(n)


def get_top_countries(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Extract top N content-producing countries excluding 'Unknown'."""
    countries = df[df['country'] != 'Unknown']['country'].str.split(', ').explode()
    return countries.value_counts().head(n)


def get_top_directors(df: pd.DataFrame, n: int = 10) -> pd.Series:
    """Extract top N directors by title count excluding 'Unknown'."""
    directors = df[df['director'] != 'Unknown']['director']
    return directors.value_counts().head(n)


def get_yearly_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Compute content additions by year grouped by content type."""
    growth = (
        df.dropna(subset=['year_added'])
        .groupby(['year_added', 'type'])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )
    growth['Total'] = growth.sum(axis=1)
    return growth
