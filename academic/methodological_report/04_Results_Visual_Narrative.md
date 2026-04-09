# Results — Visual Narrative

The application of the semantic subspace pipeline over the Spanish COVID-19 mental health corpus (March 2020 – March 2021) reveals clear, interpretable patterns in the evolution of media framing.

## Optimal Configuration

Through systematic validation (see thesis Section 4.2), the following configuration was selected:

> **Winner: DAPT + Penultimate Layer + Corrected Embeddings**

This configuration provides:
- **Parsimony**: Low entropy and intrinsic dimensionality (k ≈ 45–55), capturing semantic core without syntactic noise
- **Temporal stability**: Tight clustering of data points throughout the year
- **Geometric robustness**: Mathematically invariant under anisotropy correction

## Semantic Drift

The Grassmannian distance between consecutive windows reveals that structural change is **not monotonic**:

- **Lowest drift**: March → April 2020 (lockdown onset — discourse was uniformly emotional)
- **Maximum drift**: September 2020 — end of "New Normal" and beginning of Second Wave
- **Secondary peak**: November 2020 — autumn turbulence

This partly qualifies H2: the most dramatic shifts in meaning appear not at the lockdown start, but when society was obliged to return from summer to harsh pandemic conditions.

## Shannon Entropy

A clear **U-shaped pattern** confirmating H3:

- **Peak entropy**: Spring 2020 (National Lockdown) — high semantic ambiguity
- **Minimum**: September 2020 — discourse normalization during summer
- **Rise**: October 2020 – January 2021 — new complexity from Second/Third Waves, vaccine discourse

## Anchor Projections (Subspace)

Three distinct evolutionary phases emerge across the semantic dimensions:

### Affective Dimension (Crisis & Emotion)
- **Maximum** during National Lockdown (March–June 2020): emotionally charged coverage (fear, panic, trauma)
- Massive drop in summer 2020
- Volatile peaks during autumn/winter: "pandemic fatigue" and emotional response to later waves

### Social Dimension (Isolation & Community)
- **Most significant structural change** in the entire dataset
- Relatively important during first confinement
- Lowest during summer 2020 (partial return to public life)
- **Extraordinary peak** September–November 2020: Second Wave, return to school/work, selective confinements, social tension

### Functional Dimension (Institutions & Healthcare)
- **U-shaped trajectory**
- High during initial State of Alarm (hospital collapses, emergency response)
- Dip during "New Normal" summer
- Steady climb October 2020 → early 2021: vaccine rollouts, systemic protocols, sustained public health management

## Semantic Trajectory

The Functional-Affective trajectory plot reveals a clear **rotational pattern**:
- Early windows (March–May 2020): High-Affective, Low-Functional quadrant
- Progressive migration toward High-Functional, Low-Affective region
- Loops during Second Wave show the sensitivity of the subspace method to real-world events
- The shift in media framing is not one-directional but a **dynamic social process**

## Temporal Narrative Epochs

| Phase | Period | Dominant Frame | Characteristics |
|---|---|---|---|
| **Shock** | Spring 2020 | Affective | High entropy, reactionary discourse, mental health as acute individualized trauma |
| **Social Peak** | Autumn 2020 | Social | Second Wave, community friction, localized lockdowns, social tension |
| **Institutionalization** | Late 2020–Early 2021 | Functional | Chronic crisis management, vaccine discourse, systematic protocols |
