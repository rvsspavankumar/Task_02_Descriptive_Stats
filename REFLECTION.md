# REFLECTION: Pure Python vs Pandas vs Polars

## Overview

This document compares the three analytical approaches used to compute descriptive
statistics on the 2024 Facebook Political Ads dataset: a pure Python implementation
using only the standard library, a Pandas-based implementation, and a Polars-based
implementation. Each script produces dataset-level summaries, column-by-column
statistics, and grouped analysis by `page_id` and by the `page_id`/`ad_id`
combination.

---

## Producing Identical Results Across Three Approaches

Getting all three scripts to agree numerically required deliberate attention to a few
areas.

**Missing value handling** was the first source of divergence. Pure Python treats
missing values through explicit string matching against a set of tokens (`""`, `"na"`,
`"n/a"`, etc.). Pandas has its own `NaN`-propagation behavior when loading CSVs, and
its `keep_default_na` flag adds several tokens automatically. Polars applies strict
type inference at load time and does not silently coerce empty strings to null in the
same way. To align all three, each script applies the same normalization step:
trimming whitespace and replacing a shared list of tokens with the
language-appropriate null representation.

**Standard deviation** was another subtle difference. Python's `statistics.stdev`
uses Bessel's correction (dividing by n − 1), which matches the default behavior of
both `pandas.Series.std()` and `polars.Series.std()`. Had any of these defaulted to
population standard deviation (dividing by n), the results would have diverged on
every numeric column. Verifying this alignment was essential.

**Type inference** also required care. The Task 2 dataset stores `estimated_spend`,
`estimated_impressions`, and `estimated_audience_size` as clean integers, unlike
Task 1 where `spend` and `impressions` were range-encoded dictionaries. This made
numeric detection straightforward across all three tools, but the pure Python
implementation still needed explicit float-conversion logic since `csv.DictReader`
returns everything as strings.

---

## Developer Experience: Ease and Ergonomics

**Pure Python** demands the most manual effort. Loading CSV data, detecting column
types, computing grouped statistics, and formatting output all require explicit code.
The grouped analysis — partitioning rows into dictionaries keyed by `page_id` and
then running statistical functions on each partition — is particularly verbose. However,
this explicitness is the point: every decision about how to handle an edge case is
visible in the code.

**Pandas** provides a dramatic productivity gain. `groupby().describe()`,
`value_counts()`, `isna().sum()` — these one-liners replace dozens of lines of pure
Python. The main friction points were API changes in Pandas 3.0 (notably
`get_group()` now requiring tuples for single-key groups) and the implicit type
coercion that can silently alter data during loading.

**Polars** sits between the two. Its expression-based API is more explicit than
Pandas — you write `pl.col("x").mean()` instead of relying on method chaining on
DataFrame objects. Polars enforces strict types at load time, which means errors
surface earlier rather than hiding in mixed-type columns. Lazy evaluation is a
powerful feature for larger-than-memory datasets, though for a 250K-row file the
performance difference is negligible. The main learning curve is the expression
syntax, which is different enough from Pandas to require reading documentation rather
than guessing.

---

## Performance

On the 246,745-row dataset, all three approaches complete in a reasonable time.
Pandas and Polars each load the file in under a second. The pure Python
implementation takes noticeably longer because it reads every row into a list of
dictionaries and then iterates multiple times for type inference, missing-value
counting, and statistics computation.

For grouped analysis, the difference becomes more visible. Polars' native groupby
implementation is built on Rust and processes groups significantly faster than
Pandas for large group counts. Pure Python's `defaultdict`-based grouping is the
slowest but remains tractable for this dataset size.

For datasets in the millions of rows, Polars and its lazy evaluation mode would
offer meaningful advantages. For this task's dataset, the choice is driven by
developer preference rather than performance necessity.

---

## AI Code Generation: Observations

When asked to produce descriptive statistics scripts, tools like ChatGPT and Claude
tend to generate Pandas code by default. The code is generally correct for simple
`describe()` and `value_counts()` operations but often misses edge cases:

- AI-generated code frequently omits explicit missing-value normalization, relying
  on Pandas' default `NaN` handling, which may not catch tokens like `"n/a"` or
  empty strings in object columns.
- For Polars, AI tools sometimes produce code using deprecated APIs or Pandas-like
  syntax that does not work with Polars' expression model.
- Pure Python code generated by AI tends to be structurally correct but
  overly simplistic, often skipping type inference and edge-case handling.

The AI-generated code served as a useful starting point for each implementation
but required manual review and correction in every case. The value of AI assistance
was highest for boilerplate (CSV loading, output formatting) and lowest for the
analytical logic that needed to be consistent across all three approaches.

---

## Recommendations for a Junior Analyst

If coaching someone new to data analysis, I would recommend starting with **Pandas**.
It has the largest community, the most tutorials and Stack Overflow answers, and
covers the widest range of use cases. Once someone is comfortable with Pandas, learning
**Polars** as a second tool introduces important concepts (strict typing, lazy
evaluation, expression-based APIs) that improve analytical thinking even when using
Pandas.

The **pure Python** approach should be introduced as an educational exercise — writing
a mean function that handles missing values teaches more about statistics than calling
`.mean()` ever will — but it is not practical as a daily analysis tool.

---

## Key Takeaway

The three approaches produce identical results when care is taken to align missing-value
handling, type inference, and aggregation semantics. The pure Python version teaches the
most about what is actually happening during analysis. Pandas is the most productive for
everyday work. Polars offers the best combination of performance and explicitness for
larger datasets or production systems. Having fluency in all three gives a data analyst
the ability to choose the right tool for each situation.
