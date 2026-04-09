# Data Engineering

## Data Source

The primary data source is **GDELT** (Global Database of Events, Language, and Tone), a massive open-source database monitoring worldwide news in over 100 languages. GDELT identifies actors, locations, themes, and emotions every 15 minutes.

## Harvesting Strategy

A **"day-by-media"** harvesting strategy was employed. Unlike bulk scraping, this micro approach iterates through each day and each media outlet individually, circumventing API rate limits and achieving near-100% completeness. The strategy also implements automatic fallback mechanisms and "soft 404" protocols.

- **Period**: March 2020 – March 2021 (13 months)
- **Outlets**: 9 Spanish publishers (see Appendix B in thesis)
- **Country filter**: Spain (`sourceCountry:SP`)
- **COVID-19 keywords**: `covid`, `coronavirus`, `pandemia`
- **Harvesting time**: ~5 hours per month

## Two-Stage Filtering

### Stage 1 — COVID-19 Broad Filter
Applied using 3 COVID-19 keywords, yielding **53,055 unique articles**.

### Stage 2 — Mental Health Strict Filter
A narrower filter using mental health-specific keywords. An initial broad keyword list produced excessive noise (e.g., "agotamiento" in sports articles). A strict version was developed focusing only on directly relevant terms:

> `salud mental`, `ansiedad`, `depresion`, `estrés`, `suicidio`, `psicologo`, `terapia`, `autolesion`, `trastorno mental`, `psiquiatra`, `psiquiatria`, `bienestar emocional`, `salud emocional`

This reduced the corpus to **2,156 unique articles** (4.1% of the COVID-19 corpus).

## Filter Script Evolution

| Version | Script | Notes |
|---|---|---|
| v1 | `filter_mh.py` | ❌ Broke — didn't parse CSV structure |
| v2 | `filter_mh_csv.py` | Worked but used broad keywords, too many false positives |
| v3 | `filter_mh_csv_v2.py` | Strict keywords + COVID co-occurrence |
| **v4 (FINAL)** | `filter_mh_csv_v2_cli.py` | Added `--month`/`--year` CLI args for production |

## Operational Adjustments

- **La Vanguardia**: Temporarily paused between May–July 2020 due to harvesting instability. Resumed in August 2020. This introduces a temporal gap for this publisher but does not affect overall corpus trends.
- **Data Cleaning**: Minimal, given the robustness of the GDELT extraction process.

## Output

- **Raw data**: `data/raw/spain_covid_broad_{YYYY-MM}.csv` (13 monthly files)
- **Filtered data**: `data/interim/filters/mh_v2_strict_covidOK/` (13 monthly filtered CSVs)
- **Merged dataset**: `spain_covidMHstrict_2020-03_2021-03_ALL.csv` (15.4 MB, used for DAPT)
