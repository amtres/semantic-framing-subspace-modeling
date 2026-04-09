# Sociological Interpretation

The quantitative results presented in the preceding sections support a coherent sociological interpretation: **media framing of mental health during the COVID-19 pandemic was a highly dynamic, iterative narrative** — not a static categorization.

## From Emotional Shock to Institutional Response

The data reveals a clear trajectory from acute emotional crisis to structural institutionalization:

1. **The Shock Phase (Spring 2020)**: With high semantic entropy and overwhelming Affective projections, the initial lockdown discourse was reactionary. Mental health was framed as an acute, individualized emotional trauma — fear, anxiety — caused by COVID-19 as an unprecedented threat to individual well-being.

2. **The Social Peak (Autumn 2020)**: During the Second Wave, the Social dimension reached its all-time maximum. This was driven by the abrupt end of summer relief: media attention turned entirely to social consequences, community friction, localized lockdowns, and the breakdown of social norms. As normalization was interrupted, the public showed high levels of collective anxiety.

3. **Institutionalization (Late 2020 – Early 2021)**: With the Second and Third Waves, the Functional dimension became predominant. The discourse can be characterized by the **institutionalization of mental health**: it was increasingly treated as a public health issue requiring medical and governmental responses — vaccine rollouts, systemic protocols, sustained public health management.

## Implications for Media Practice

These findings have practical relevance for media practice and health communication:

- **Affective-crisis framing** dominated the early pandemic, potentially aggravating collective anxiety through the media's amplification of emotional reactions.
- The transition to **functional framing** in later periods demonstrates that sustained institutional reporting can shift the public agenda toward solutions and resources.
- The **regression during the Second Wave** shows that framing evolution is not linear — it responds dynamically to sociopolitical reality.

## Evidence for the Hypotheses

| Hypothesis | Evidence | Status |
|---|---|---|
| **H1** (Framing Dynamics) | Clear evolution: Affective → Social → Functional | ✅ Supported |
| **H2** (Semantic Drift) | Maximum drift at Second Wave onset (September 2020), not lockdown start | ✅ Partially qualified |
| **H3** (Entropy Reduction) | U-shaped trajectory: high → low → rise again | ✅ Supported |
| **H4** (DAPT Sensitivity) | DAPT provides better geometric space while preserving narrative trends | ✅ Supported |

## Methodological Contributions

Beyond the sociological insights, the framework contributes to computational literature on semantic framing:

1. **Centroid limitations**: Mean vectors are not only vulnerable to anisotropic noise but are also blind to the stability of the semantic space they represent. This exposes the risks of longitudinal inferences based on centroids alone.

2. **Subspace invariance**: Semantic subspaces produced through SVD are geometrically invariant under anisotropy correction — they capture the same structural narrative regardless of geometric preprocessing.

3. **Layer selection**: The penultimate layer of a domain-adapted model (DAPT) is the most reliable, efficient, and geometrically pure strategy for longitudinal NLP research in media studies.

## Limitations

- Results hold for the Spanish newspaper corpus gathered in this specific period. Exact trajectories may differ for other cultures, languages, or social media.
- Anchor dimensions (Affective, Social, Functional) are proxies capturing macro-frames but may miss more granular micro-frames.
- The analysis covers only until early 2021 — post-vaccination framing remains unexplored.
- The methodology was validated by Hamilton et al. (2016) on centuries of historical data; whether the same regularities apply at a one-year timescale is an open question.
