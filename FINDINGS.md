# Findings: Facebook Political Ads Dataset (2024 U.S. Presidential Election)

## Dataset Scope

This analysis examines a dataset of 246,745 Facebook political advertisement records
with 41 variables. Compared to the Task 1 dataset, this version introduces several
structural changes: column names have been reorganized (e.g., `illuminating_topic_economy`
is now `economy_topic_illuminating`), the `page_name` field has been removed in favor of
anonymized `page_id` hashes, and the range-encoded `spend` and `impressions` fields have
been replaced with clean numeric columns (`estimated_spend`, `estimated_impressions`).
Two new columns have been added: `freefair_illuminating` and `fraud_illuminating`. The
dataset also now includes `delivery_by_region` and `demographic_distribution` as
structured text fields.

---

## Data Quality and Completeness

The dataset shows very high completeness. Only one field has measurable missingness:

- **bylines**: 1,009 missing values (0.41%)

All other columns are fully populated with no missing values. The removal of
`ad_delivery_stop_time` (which had 0.87% missing in Task 1) and the replacement of
range-encoded spend and impression fields with clean integers has improved data quality
relative to the Task 1 dataset. This makes the dataset highly suitable for both
descriptive and grouped statistical analysis.

---

## Spending and Reach Patterns

With `estimated_spend` now available as exact integers, spending analysis is
straightforward:

- **Mean spending per ad**: $1,061
- **Median spending per ad**: $49
- **Maximum single-ad spend**: $474,999

The median of $49 indicates that the majority of advertisements fall into the lowest
spending brackets. The mean being roughly 20 times the median reflects a heavily
right-skewed distribution: a small number of high-budget ads pull the average
significantly upward. This pattern is consistent with digital advertising norms, where
campaigns run many small-budget ads for targeted audiences alongside fewer large-budget
ads for broad reach.

Impression data tells a similar story:

- **Mean impressions per ad**: approximately 57,000
- **Median impressions per ad**: approximately 7,000

Again, the gap between mean and median indicates that most ads achieve modest reach
while a smaller set of ads generate very high visibility.

---

## Concentration of Activity by Page

Grouped analysis by `page_id` reveals that advertising activity is highly concentrated.
The top five page identifiers account for the following ad counts:

1. Page `4d66f5...` — 55,503 ads
2. Page `e33420...` — 23,988 ads
3. Page `4ade40...` — 14,822 ads
4. Page `330b2f...` — 10,461 ads
5. Page `ec8ac6...` — 9,851 ads

The top page alone accounts for approximately 22.5% of all advertisements in the
dataset. The top five pages together represent roughly 46% of the total. With 4,475
unique pages in the dataset, this concentration confirms that a small number of
campaign entities dominate the platform's political advertising landscape.

Within the top page, the mean spend per ad is $1,492 with a standard deviation of
$6,281, indicating wide variation in spending strategy even within a single
campaign's output.

---

## Message Strategy Patterns

The binary message-type indicators reveal clear strategic preferences:

- **Advocacy messaging**: present in roughly 55% of ads from the top page
- **Call-to-action (CTA)**: present in roughly 50% of ads
- **Issue messaging**: present in roughly 39% of ads
- **Attack messaging**: present in roughly 27% of ads
- **Image-based messaging**: present in roughly 21% of ads

These patterns suggest that campaigns prioritize mobilization (advocacy + CTA) over
informational or negative messaging. Attack ads, while present, represent a smaller
fraction than advocacy-oriented content.

---

## Topic Distribution

Aggregating the topic indicator columns across the full dataset, the most
frequently addressed topics are:

1. **Economy** — the most prevalent policy topic
2. **Health**
3. **Social and cultural issues**
4. **Women's issues**
5. **Immigration**

These patterns align with major policy themes of the 2024 election cycle. The
new `freefair_illuminating` and `fraud_illuminating` columns introduce indicators
for election integrity narratives, though their prevalence across the dataset
appears low compared to the core policy topics.

---

## Grouped Analysis: Page-Level Variation

Examining grouped statistics by `page_id` reveals notable differences in
advertising strategies across campaign entities:

- The largest advertiser has a high proportion of advocacy and CTA messages,
  suggesting a mobilization-focused strategy.
- Smaller advertisers show more variation in topic emphasis, with some
  concentrating heavily on a single issue (e.g., immigration or health).
- Spending distribution varies substantially across pages: some pages
  maintain a consistently low spend per ad (suggesting micro-targeted
  campaigns), while others show high variance indicating a mix of small
  and large-budget ads.

The `page_id` + `ad_id` grouped analysis confirms that most ad IDs map to
single rows, indicating that each ad purchase is recorded as a unique entry.
However, some ad IDs appear with multiple rows, which may represent
re-runs of the same ad creative or platform-level deduplication artifacts.

---

## Structural Differences from Task 1

Several changes between the Task 1 and Task 2 datasets are worth noting:

- **Column renaming**: The naming convention shifted from prefix-style
  (`illuminating_topic_economy`) to suffix-style (`economy_topic_illuminating`),
  requiring code updates for any hardcoded column references.
- **Numeric fields**: `estimated_spend` and `estimated_impressions` are now
  clean integers rather than range-encoded dictionaries, enabling direct
  arithmetic analysis.
- **Removed columns**: `page_name`, `ad_delivery_start_time`, and
  `ad_delivery_stop_time` are no longer present. The loss of `page_name`
  means identifying specific campaigns requires an external lookup table.
- **New columns**: `delivery_by_region` and `demographic_distribution` provide
  structured geographic and demographic breakdowns, though they are stored as
  string representations of dictionaries and require parsing for analysis.
  `freefair_illuminating` and `fraud_illuminating` are new binary indicators.

These changes demonstrate why building generalized, schema-agnostic analysis
code is important: scripts hardcoded to the Task 1 schema would fail on this
dataset without modification.

---

## Conclusion

The Task 2 dataset improves on Task 1 by providing cleaner numeric fields and
additional analytical dimensions. The core patterns observed in Task 1 remain
consistent: advertising activity is heavily concentrated among a few major
campaign entities, spending follows a long-tailed distribution, and messaging
strategies emphasize mobilization over information. The availability of exact
spend and impression figures enables more precise analysis than was possible
with the range-encoded fields in Task 1.
