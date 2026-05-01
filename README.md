# Task_02_Descriptive_Stats

## Descriptive Statistics with Pure Python, Pandas, and Polars

## Project Overview

This project extends Task 1 by adding **Polars** as a third analytical approach and
introducing **grouped analysis** to the descriptive statistics workflow. All three
implementations analyze the same Facebook political advertising dataset from the
2024 U.S. Presidential election and produce identical statistical summaries at both
the dataset level and grouped levels.

The three approaches demonstrate different tradeoffs in data analysis:

- **Pure Python**: maximum transparency, every computation is explicit
- **Pandas**: industry-standard productivity and ecosystem support
- **Polars**: strict typing, expression-based API, and high performance

---

## Dataset

The dataset contains Facebook advertisements referencing U.S. presidential candidates
during the 2024 election cycle.

Each row represents an individual ad purchase and includes metadata such as:

- anonymized page identifier and ad identifier
- ad creation date
- estimated audience size, impressions, and spend (as exact integers)
- message type indicators (advocacy, issue, attack, image, CTA)
- topic indicators (economy, health, immigration, etc.)
- delivery by region and demographic distribution (as structured text)

**Dataset size:** 246,745 rows × 41 columns

### Dataset Source

Google Drive link:
https://drive.google.com/file/d/1UPo11lH2Mlk2cnLtjv8P9XqlKitms-gp/view?usp=sharing

### Important

The dataset **is not included in this repository**. Download the CSV file from the
link above and place it in the project directory with the following filename:

```
2024_fb_ads_president_scored_anon.csv
```

---

## Project Structure

```
Task_02_Descriptive_Stats/
├── pure_python_stats.py      # Standard library only
├── pandas_stats.py           # Pandas implementation
├── polars_stats.py           # Polars implementation
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── FINDINGS.md               # Narrative analysis of the data
├── REFLECTION.md             # Comparison of the three approaches
└── .gitignore                # Python + data file exclusions
```

---

## Scripts

### pure_python_stats.py

Implements descriptive statistics using **only Python's standard library** (`csv`,
`math`, `collections`, `statistics`).

Features:

- CSV loading with `csv.DictReader`
- Missing value detection using configurable token set
- Dynamic column type inference (numeric, date, categorical, identifier, range text, list text)
- Manual computation of count, mean, min, max, median, standard deviation
- Categorical frequency analysis (unique count, mode, top 5)
- **Grouped analysis** by `page_id` and by `page_id` + `ad_id`
- Accepts any CSV file as a command-line argument

### pandas_stats.py

Performs the same analysis using **Pandas**.

Features:

- `DataFrame.describe()` for numeric and categorical summaries
- `isna().sum()` for missing value analysis
- `value_counts()` and `nunique()` for categorical columns
- `groupby('page_id')` and `groupby(['page_id', 'ad_id'])` with aggregation
- Dynamic type inference matching the pure Python logic
- Accepts any CSV file as a command-line argument

### polars_stats.py

Performs the same analysis using **Polars**.

Features:

- `DataFrame.describe()` for structural summary
- Expression-based column analysis with strict typing
- `group_by('page_id')` and `group_by(['page_id', 'ad_id'])` with aggregation
- Handles the same missing value tokens as the other two scripts
- Accepts any CSV file as a command-line argument

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Place the dataset

Download the dataset from the link above and place it in the project directory:

```
2024_fb_ads_president_scored_anon.csv
```

### 3. Run Pure Python analysis

```bash
python3 pure_python_stats.py 2024_fb_ads_president_scored_anon.csv
```

### 4. Run Pandas analysis

```bash
python3 pandas_stats.py 2024_fb_ads_president_scored_anon.csv
```

### 5. Run Polars analysis

```bash
python3 polars_stats.py 2024_fb_ads_president_scored_anon.csv
```

Each script accepts the CSV file path as its first command-line argument,
so you can point them at any well-formed CSV file.

---

## Summary of Findings

Analysis reveals several key patterns in the dataset:

- **High data quality**: Only 1 column (`bylines`) has any missing values (0.41%).
  All numeric fields are cleanly formatted integers.
- **Concentrated advertising activity**: The top 5 page identifiers account for
  roughly 46% of all advertisements, with the largest single page producing
  55,503 ads (22.5% of the dataset).
- **Right-skewed spending**: Mean spend per ad is $1,061 vs. median of $49,
  indicating many small-budget ads and a few very high-budget ones.
- **Mobilization-focused messaging**: Advocacy and CTA message types dominate,
  appearing in over 50% of ads from the largest advertiser.
- **Policy emphasis**: Economy, health, and social/cultural issues are the
  most frequently tagged topics across the dataset.

A detailed narrative analysis is in [FINDINGS.md](FINDINGS.md).

---

## Comparison of Analytical Approaches

All three implementations produce consistent descriptive statistics when care
is taken to align missing-value handling, type inference, and standard deviation
semantics (sample vs. population).

Key observations:

- Pure Python required the most code but made every analytical decision explicit.
- Pandas offered the greatest productivity with built-in operations for all
  common tasks.
- Polars enforced stricter typing and provided an expression-based API that
  prevents many common Pandas pitfalls.

A detailed comparison is in [REFLECTION.md](REFLECTION.md).

---

## Requirements

```
pandas
polars
matplotlib
seaborn
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Author

Revanth venkata Shesha Sai Pavan Kumar Vudutha  
Master's in Information Systems  
Syracuse University
