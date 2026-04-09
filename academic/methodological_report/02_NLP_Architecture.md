# NLP Architecture

## Model Selection

The base model is **BETO** (`dccuchile/bert-base-spanish-wwm-uncased`), a BERT-base model featuring 12 transformer layers and hidden size d=768. It was trained on a 1.5 billion word dataset from Spanish Wikipedia and OPUS project sources, using Whole Word Masking (WWM).

> **Note**: `PlanTL-GOB-ES/roberta-large-bne` (RoBERTa-BNE) was initially planned but proved non-functional due to deprecation issues. The project uses BETO exclusively.

## Domain-Adaptive Pretraining (DAPT)

Following Gururangan et al. (2020), the base model was further pretrained on the filtered mental health corpus to learn domain-specific semantic relations (e.g., "ola" as infection peak, not ocean wave; "confinamiento" with psychological connotations).

### DAPT Attempts

| Attempt | Corpus | Epochs | Outcome |
|---|---|---|---|
| 1 | Full COVID broad (286 MB) | 3 | ❌ Interrupted after 16 min — estimated 648h |
| 2 | 5K sample | 1 | ❌ Test only — abandoned |
| **3 (FINAL)** | MH-strict filtered (15.4 MB) | 1 | ✅ Completed in **8h 49m** |

### Final DAPT Model

- **Path**: `models/beto_dapt_spain_MHstrict_2020-03_2021-03_e1/`
- **Training loss**: 2.3675
- **Total steps**: 17,970
- **Weights**: `model.safetensors` (419 MB)

## Embedding Extraction

From the 2,156 filtered articles, embeddings were extracted using **13 normalized mental health keywords**:

> `salud mental`, `ansiedad`, `depresion`, `estres`, `suicidio`, `soledad`, `miedo`, `psicosis`, `psicologo`, `terapia`, `autolesion`, `trastorno mental`, `psiquiatria`

Orthographic variants (e.g., `estrés`/`estres`, `depresión`/`depresion`) were normalized to canonical forms.

This produced **7,535 keyword occurrences**, each converted to a contextual embedding via mean pooling.

## Layer Extraction Strategies

Two strategies were computed and compared (see Section 4.2.2 of thesis):

| Strategy | Description | Dimensionality |
|---|---|---|
| **Penultimate** | Second-to-last transformer layer | d=768 |
| Last4_concat | Concatenation of final 4 layers | d=3,072 |

**Winner**: Penultimate layer — provides stable, interpretable trajectories with lower noise. Last4_concat captures syntactic detail but introduces severe structural noise for longitudinal tracking.

## Anisotropy Correction

Contextualized embeddings exhibit anisotropy (Ethayarajh, 2019), where vectors cluster in a narrow cone distorting cosine similarity. Two configurations compared:

- **RAW**: Embeddings directly from the model
- **CORRECTED**: Global mean vector subtracted from each embedding (Mu et al., 2017)

**Key finding**: Subspace projections are mathematically invariant under centering (RAW and CORRECTED produce identical subspace trajectories), while centroids are highly sensitive to anisotropic noise.
