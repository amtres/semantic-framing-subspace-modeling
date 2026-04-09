# LISBETH — COVID-19 & Mental Health Media Framing in Spain

## Computational Analysis of Media Representation through Dynamic Semantic Subspaces

> **Final Degree Project (TFG) — 4th Year**
>
> This project adapts the [LISBETH framework](https://github.com/original-repo) (originally developed by Prof. Alejandro Martínez-Mingo at UNED for a Master's programme) to a new research domain: **the evolution of mental health framing in Spanish mainstream press during the COVID-19 pandemic (2020–2021).**

---

## About This Project

This repository is a **fork and adaptation** of the LISBETH ("Laboratorio") system — a computational research pipeline for analysing the semantic evolution of concepts in news media. The original system was designed to study how the Peruvian mobile wallet *Yape* was represented in press over time. This fork repurposes the entire pipeline for a different research question:

> **How did Spanish newspapers frame mental health during the COVID-19 pandemic, and how did that framing evolve over time?**

The system combines **Transformer-based NLP** (Domain-Adaptive Pretraining + contextual embeddings) with **Sociological Framing Theory** to quantitatively track how abstract concepts like *anxiety*, *depression*, *isolation*, or *therapy* shift in meaning across time windows in the press.

### Key Adaptations in This Fork

| Aspect | Original (LISBETH) | This Project (TFG) |
|---|---|---|
| **Research target** | "Yape" (Peruvian fintech brand) | COVID-19 × Mental Health framing |
| **Country & press** | Peru (El Comercio, Gestión, etc.) | Spain (El País, El Mundo, ABC, La Vanguardia, etc.) |
| **Keywords** | `Yape`, `Yapear` | `salud mental`, `ansiedad`, `depresión`, `suicidio`, `estrés`, `terapia`, etc. |
| **Anchor dimensions** | Financial, Community, Security | **Functional** (clinical services, treatment), **Social** (isolation, family, domestic violence), **Affective** (anxiety, fear, depression, trauma) |
| **Time span** | 2019–2023 | March 2020 – March 2021 (COVID-19 first wave and aftermath) |
| **Language models** | Spanish: RoBERTa-BNE, BETO | Same (language-agnostic architecture) |

---

## How It Works

The system is orchestrated through a single master CLI: `pipeline_manager.py`.

### Phase 1 — Data Harvesting (Granular Collector)

*Resilient news collection infrastructure.*

- **"Day × Media" strategy**: Unlike traditional scrapers that make bulk queries, LISBETH iterates **day by day** and **outlet by outlet**. This bypasses GDELT's return cap (max 250 records) and ensures near-complete historical coverage.
- **Hybrid sources**: GDELT (primary), Google News (backup), RSS (real-time).
- **Resilience**:
  - Handles "Soft 404s" and JS-rendered (client-side) content through domain-specific CSS selectors (`src/news_harvester/domains.py`).
  - Automatic fallback to `trafilatura` for clean text extraction.

### Phase 2 — NLP Infrastructure

*Transforming text into calibrated mathematical tensors.*

#### 2.1 Model Management
The system supports any Hugging Face model, optimised for monolingual Spanish models:
- **`PlanTL-GOB-ES/roberta-large-bne`**: SOTA model trained by Spain's National Library.
- **`dccuchile/bert-base-spanish-wwm-uncased`** (BETO): Robust and lightweight alternative.

#### 2.2 DAPT (Domain-Adaptive Pretraining)
Before extracting embeddings, the base model is fine-tuned (**DAPT**) on the corpus collected in Phase 1.
- **Why**: A generic model may not capture domain-specific semantics. For instance, the evolving connotations of "confinamiento" (lockdown) or "ERTE" (furlough scheme) in Spanish COVID-19 discourse.
- **Parameters**:
  - MLM (Masked Language Modeling): Words from the collected corpus are randomly masked, and the model learns to predict them.
  - Epochs: Configurable (default 3).

#### 2.3 Contextual Embedding Extraction
For each mention of a target keyword (e.g., "salud mental"):
1. **Tokenisation**: The keyword is located in the sentence. If fragmented into sub-tokens, **Mean Pooling** is applied to produce a single vector.
2. **Layer Strategy**: Hidden activations are extracted.
   - **`penultimate`**: The second-to-last layer (best for general geometric representations).
   - **`last4_concat`**: Concatenation of the last 4 layers (4096 dims for RoBERTa-large), capturing deep syntactic and semantic nuances.

### Phase 3 — Subspace Analysis (The "Mathematical Laboratory")

*Where the sociological insights emerge.*

#### 3.1 Dual Anisotropy Correction
Language models suffer from **anisotropy**: all vectors tend to occupy a narrow cone in space, distorting cosine distances.
LISBETH implements a strict comparison protocol:
1. **RAW**: Embeddings as-is from the model.
2. **CORRECTED**: The **Global Mean Vector** (μ_global) of the entire corpus is computed and subtracted from each embedding (v' = v − μ_global). This "centres" the point cloud and reveals the true internal semantic structure.

#### 3.2 Dynamic Subspaces
Embeddings are grouped into **Sliding Windows** (e.g., quarterly) and **SVD (Singular Value Decomposition)** is applied to find the principal axes of meaning in each period.

#### 3.3 Metrics
- **Semantic Drift**: Grassmannian distance between subspace at time *t* and time *t+1*. Measures how much meaning has changed.
- **Entropy**: Dispersion of singular values. High entropy = diffuse / polysemous meaning.
- **Anchor Projection**: Theoretical vectors are defined (e.g., "therapy", "isolation", "anxiety") and the system mathematically measures how close the target concept moves towards each anchor across time.

In this project, three anchor dimensions are used:

| Dimension | Description | Example anchors |
|---|---|---|
| **Functional** | Clinical services, treatment access, work–life burden | *psicólogo, terapia, ERTE, teletrabajo, tratamiento* |
| **Social** | Relationships, isolation, community support, domestic violence | *aislamiento, familia, violencia, duelo, solidaridad* |
| **Affective** | Emotional states and psychological symptoms | *ansiedad, depresión, miedo, trauma, suicidio* |

### Phase 4 — Automated Reports
Generates Jupyter Notebooks and visualisations (heatmaps, time series) that visually compare RAW vs CORRECTED conditions to validate findings.

---

## Execution Guide

The script `pipeline_manager.py` is the single entry point.

### 0. Initial Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify the media list
cat data/metadata/media_lists/media_list.csv
# name,domain,type
# elpais,elpais.com,national
# elmundo,elmundo.es,national
# ...
```

### 1. Download Models

Pre-download models to avoid latency or network errors during processing.

```bash
python pipeline_manager.py phase2 download-models \
    --models "dccuchile/bert-base-spanish-wwm-uncased" "PlanTL-GOB-ES/roberta-large-bne"
```

### 2. Phase 1: Harvesting

**Key Parameters**:
- `--keyword`: Words to track.
- `--media-list`: Path to the media CSV. If omitted, searches all of GDELT (less exhaustive).
- `--country`: GDELT country code (default: SP for Spain in this project).

```bash
# Spain — COVID & Mental Health
python pipeline_manager.py phase1 \
    --keyword "salud mental" "ansiedad" "depresión" "suicidio" \
    --from 2020-03-01 --to 2021-03-31 \
    --country SP \
    --media-list data/metadata/media_lists/media_list.csv \
    --output data/raw/spain_covid_mh.csv
```

### 3. Phase 2: NLP Processing

#### Step 3.1: DAPT (Optional but Recommended)
Fine-tune the base model on your data.

```bash
python pipeline_manager.py phase2 dapt \
    --data data/interim/datasets/spain_covidMHstrict_2020-03_2021-03_ALL.txt \
    --output models/roberta-adapted-covid-mh \
    --model "PlanTL-GOB-ES/roberta-large-bne" \
    --epochs 3
```

#### Step 3.2: Embedding Extraction
Generate the vector dataset.

```bash
python pipeline_manager.py phase2 extract \
    --data_dir data/raw \
    --output data/interim/embeddings/embeddings_covid_mh.parquet \
    --model "PlanTL-GOB-ES/roberta-large-bne" \
    --dapt_model models/roberta-adapted-covid-mh \
    --keywords "salud mental" "ansiedad" "depresión"
```

### 4. Phase 3: Subspace Analysis

Run the full metric computation. Supports dynamic model and anchor configuration.

```bash
python pipeline_manager.py phase3 \
    --input data/interim/embeddings/embeddings_covid_mh.parquet \
    --output-dir results/phase3_covid_mh \
    --baseline-model "PlanTL-GOB-ES/roberta-large-bne" \
    --dapt-model models/roberta-adapted-covid-mh \
    --anchors data/metadata/anchors/dimensiones_ancla_mh_es_covid_FSA.json \
    --window-months 3
```

### 5. Phase 4: Report Generation

Generate the final deliverables.

```bash
python pipeline_manager.py phase4 \
    --input results/phase3_covid_mh/phase3_results.csv \
    --output_dir results/final_report
```

---

## 📂 Repository Structure

```
LISBETH/
├── academic/                   # Academic reports and methodological notebooks
│   ├── INTRO_TFM.md            # Theoretical introduction (original study)
│   └── model_comparison/       # Model comparison reports
├── configs/                    # Pipeline configuration files
│   └── tfg_phase1_plan.yml     # Phase 1 harvesting plan for this TFG
├── data/                       # Data (Gitignored except metadata)
│   ├── metadata/
│   │   ├── anchors/            # Anchor dimension definitions (JSON)
│   │   ├── keywords/           # Keyword lists (COVID, mental health, etc.)
│   │   └── media_lists/        # Spanish media outlet catalogues
│   ├── interim/
│   │   ├── datasets/           # Harvested corpora
│   │   └── embeddings/         # Extracted embeddings
│   └── raw/                    # Raw harvested news articles
├── models/                     # Trained/adapted models (Gitignored)
├── notebooks/                  # Interactive demos, EDA, and analysis
├── results/                    # Phase 3 & 4 outputs
├── scripts/                    # Utility scripts
├── tools/                      # Diagnostic tools
├── src/                        # Source Code
│   ├── news_harvester/         # Scraping logic (domains, selectors)
│   ├── nlp/                    # DAPT, embedding extraction, anchors
│   ├── subspace_analysis/      # Mathematics (SVD, Grassmann, Procrustes)
│   ├── reporting/              # Report generation logic
│   └── visualization/          # Plotting and visualisation utilities
├── pipeline_manager.py         # Master CLI
├── pyproject.toml              # Project metadata
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Data Storage & Backups

- This project was cloned from the original LISBETH repository and published to a **private GitHub repository** to avoid losing progress.
- All project files are pushed and version-controlled **except the large COVID broad dataset** outputs.
- The **MH-strict dataset** is stored in this repository:
  - `data/interim/datasets/spain_covidMHstrict_2020-03_2021-03_ALL.txt`
- The **COVID broad (ALL) dataset** is **not pushed to GitHub** (large files). It is backed up as a ZIP in **Google Drive** (TFG data backup folder).
- Large harvesting outputs are ignored via `.gitignore` to prevent GitHub push issues (>100 MB).

---

## Credits

- **LISBETH Framework**: Originally developed by [Prof. Alejandro Martínez-Mingo](https://www.uned.es) — Master's in Behavioural and Health Sciences Methodology, UNED.
- **This Adaptation (TFG)**: Applies the LISBETH pipeline to the study of COVID-19 and mental health media framing in Spanish press.

---

**LISBETH v2.0 · Adapted for TFG · April 2026**
