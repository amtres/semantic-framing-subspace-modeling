# Introduction — Semantic Framing of Mental Health During COVID-19

## Background and Motivation

The COVID-19 crisis sparked a massive public discussion on psychological distress, ranging from prevalent conditions such as anxiety and depression to experiences such as loneliness and emotional fatigue. Beyond the risk of infection, the pandemic impacted daily routines, social relationships, educational institutions, work, and access to mental health services. According to the World Health Organization, the pandemic disrupted or canceled essential mental health services in 93% of countries (WHO, 2020).

In Spain, the prevalence of self-reported low interest or pleasure in activities increased by 3.3 points, feelings of depression by 2.8 points, and sleeping problems by 2 points (INE, 2021). These figures configure a social reality that news media have been documenting, interpreting, and constructing simultaneously.

The news media constitute the main sources of information for contemporary societies. Their frames of reference determine what we consider important, the responses that seem appropriate, and what we understand as urgent (Entman, 1993). By foregrounding some words and emotional inflections while backgrounding others, the media's editorial agenda shapes the reader's agenda.

This suggests that the way media represents mental health is not merely descriptive — it is fundamentally consequential. Evidence indicates that coverage may influence social stigma associated with mental disorders, attitudes toward help-seeking behaviors, and adoption of high-risk behaviors such as suicidal intentions (Gunnell & Biddle, 2020; Gunnell, Appleby et al., 2020).

## Research Question

> How did Spanish news media frame mental health during the COVID-19 pandemic, and how did the meanings, emotions, and narrative relevance of key mental health concepts evolve over time?

## Objectives

1. Build a corpus of Spanish news articles during the COVID-19 pandemic and filter articles containing mental health-related vocabulary.
2. Obtain contextual embeddings for mental health constructs for each time period and represent them as semantic subspaces.
3. Measure diachronic changes through: semantic drift, valence-adjusted framing (emotional orientation), and salience/centrality.
4. Explain temporal patterns by relating results to major pandemic stages.

## Hypotheses

- **H1 (Framing Dynamics)**: The framing of mental health varies significantly over time, moving towards functional and social framing as pandemic management becomes more institutional.
- **H2 (Semantic Drift)**: The rate of semantic drift is higher at pandemic turning points (lockdown onset, New Normal transition, Second Wave onset).
- **H3 (Entropy Reduction)**: Semantic entropy follows a U-shaped trajectory, decreasing as discourse normalizes but increasing again with later pandemic waves.
- **H4 (DAPT Sensitivity)**: The DAPT model provides a different geometrical arrangement of the latent space with more sensitivity but retains the same temporal trends.

## Contributions

- A structured, time-indexed dataset containing mental health lexicon during COVID-19, enabling semantic analysis.
- Framing operationalization based on semantic subspace modeling, representing discourse periods as semantic structures rather than single-word meanings.
- A multidimensional measurement framework studying the evolution of semantic drift, emotional valence projection, and salience indicators.
- Empirical visualizations offering interpretable representations of framing dynamics throughout the pandemic.

## Scope and Assumptions

This study focuses on news articles written in Spanish, related to the COVID-19 pandemic and mental health discourse. The time scope spans **March 2020 to March 2021**, and content is restricted to articles retrieved through keyword-based search targeting mental health-related language.

**Assumptions:**
1. Contextual language models capture enough semantic information to approximate meaning change over time.
2. Time windows provide a reasonable approximation for diachronic analysis of social discourse.
3. Keyword-based filtering provides a practical approximation for capturing mental health-related discourse.

This thesis does not assume any causal relationship between media coverage and mental health outcomes; rather, it provides a mapping of how discourse in news media evolved during the pandemic.

## Theoretical Framework

This project draws from three intersecting theoretical traditions:

- **Framing Theory** (Entman, 1993; Fillmore, 1982): Meaning is not simply activated by keywords but assembled from structured background knowledge.
- **Cognitive Similarity** (Tversky, 1977): Human similarity judgements are asymmetric, violate triangle inequality, and depend on context — properties that single-point vector representations cannot capture.
- **Conceptual Subspaces** (Martínez-Mingo et al., 2023): Quantum-inspired projections on distributional semantic spaces account for context-dependent meaning, asymmetry, and diagnosticity effects.

## Pipeline Overview

The computational methodology adapts the LISBETH framework (Martínez-Mingo) into a three-phase pipeline:

```
Phase 1: Data Harvesting    → GDELT API → 53,055 COVID articles → 2,156 MH-filtered articles
Phase 2: NLP Infrastructure → BETO + DAPT → 7,535 contextual embeddings
Phase 3: Subspace Analysis  → SVD decomposition → Grassmannian drift, entropy, anchor projections
```

For full methodology details, see the methodological reports in `academic/methodological_report/`.
