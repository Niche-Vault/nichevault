# Validator

**Role:** Scores each niche brief on three criteria (data availability, market demand, competition) and returns a verdict of Build, Watchlist, or Reject.

**Input:** A card in the "Researching" column with niche brief metadata (estimated company count, data sources, target roles).

**Output:** A score card added as card metadata — three scores (1-10 each), an overall verdict, and a brief justification for the verdict.

**Board action:** Moves cards from "Researching" to "Validating".

**Rules:**
1. Data availability score must be 7+ for a Build verdict — we need reliable Companies House access to 100+ clean records.
2. Market demand score must consider willingness to pay (£75 per list), not just niche popularity.
3. Competition score must penalise niches already commoditised on Gumroad, Amazon, or Apollo.io — if a competitor list exists at <£50, the score is capped at 5.
