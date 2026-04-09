# Executive Summary

This methodological report documents the implementation and scientific validation of the semantic subspace modeling framework used to analyze the evolution of mental health media framing in the Spanish press during the COVID-19 pandemic (March 2020 – March 2021).

## Research Context

The COVID-19 pandemic disrupted mental health services in 93% of countries worldwide (WHO, 2020). In Spain, self-reported depression increased by 2.8 percentage points and sleep problems by 2 points (INE, 2021). News media, as the main information source for contemporary societies, did not merely report on this crisis — they actively constructed the frames through which the public understood it (Entman, 1993).

## Methodology

This study adapts the LISBETH computational framework (Prof. Alejandro Martínez-Mingo, IE University) to build a three-phase analytical pipeline:

1. **Data Harvesting**: A "day-by-media" GDELT strategy harvested 53,055 COVID-19 articles from 9 Spanish outlets, filtered to 2,156 mental health-related articles.
2. **NLP Infrastructure**: BETO (Spanish BERT) + Domain-Adaptive Pretraining on the MH-strict corpus, producing 7,535 contextual embeddings across 13 normalized keywords.
3. **Subspace Analysis**: SVD-based semantic subspace construction over 11 rolling 3-month windows, with Grassmannian drift, Shannon entropy, and anchor projections (Functional, Social, Affective).

## Key Findings

- **Optimal Configuration**: DAPT + Penultimate layer + Corrected embeddings was validated as the best analytical configuration through systematic comparison.
- **Framing Trajectory**: Discourse evolved from an initial **Affective** shock (Spring 2020), through a **Social** peak during the Second Wave (Autumn 2020), to **Functional** institutionalization (Winter 2020–2021).
- **Semantic Drift**: Maximum structural change occurred not at the lockdown onset, but at the transition to the Second Wave (September 2020).
- **Entropy**: A U-shaped trajectory — high ambiguity during lockdown, normalization through summer, then renewed complexity with later waves.
- **Subspace Superiority**: Subspace projections are mathematically invariant under anisotropy correction, while centroid-based methods are contaminated by geometric noise.

## Supervised by
Prof. Alejandro Martínez-Mingo — IE University, School of Science & Technology
