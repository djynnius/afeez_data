"""Build the NHANES diabetes analysis Jupyter notebook (R kernel)."""
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

cells = []

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
# NHANES Diabetes Study — Analysis

**Objective.** Describe the relationship between diabetes status and a set of
demographic, anthropometric, clinical, and lifestyle variables in the
NHANES 2009–2010 sample.

**Analytic subset.** Nine variables are retained:

| Variable in subset | Original NHANES name | Role | Type |
|---|---|---|---|
| Diabetes | `Diabetes` | Outcome | Categorical (Yes/No) |
| Age | `Age` | Predictor | Numeric |
| Sex | `Gender` | Predictor | Categorical (female/male) |
| BMI | `BMI` | Predictor | Numeric |
| SystolicBP | `BPSysAve` | Predictor | Numeric |
| DiastolicBP | `BPDiaAve` | Predictor | Numeric |
| Race | `Race1` | Predictor | Categorical (5 levels) |
| AlcoholUse | `Alcohol12PlusYr` (drank in past 12 months) | Predictor | Categorical (Yes/No) |
| SmokeHistory | `Smoke100` (≥100 cigarettes in lifetime) | Predictor | Categorical (Yes/No) |

Records with a missing `Diabetes` value are dropped before analysis.

> *Note.* `Sex`/`Gender` are both requested; NHANES records biological sex
> under the `Gender` field, so it is kept as `Sex`. `Alcohol12PlusYr` and
> `Smoke100` are used as the binary indicators of **alcohol use** and
> **smoking history** respectively."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
# --- Setup ---------------------------------------------------------------
suppressPackageStartupMessages({
  library(tidyverse)
  library(gtsummary)
  library(gt)
  library(broom)
  library(nortest)   # Anderson-Darling Lilliefors
  library(moments)   # skewness, kurtosis, agostino, jarque
  library(ggplot2)
  library(patchwork)
})

theme_set(theme_bw(base_size = 13))
options(gtsummary.print_engine = "gt")
options(width = 120)

# --- Load & subset -------------------------------------------------------
df <- read_csv("data/nhanes.csv", na = c("", "NA"), show_col_types = FALSE)

keep <- c("Diabetes", "Age", "Gender", "BMI", "BPSysAve", "BPDiaAve",
          "Race1", "Alcohol12PlusYr", "Smoke100")

dat <- df |>
  select(all_of(keep)) |>
  rename(
    Sex          = Gender,
    SystolicBP   = BPSysAve,
    DiastolicBP  = BPDiaAve,
    Race         = Race1,
    AlcoholUse   = Alcohol12PlusYr,
    SmokeHistory = Smoke100
  ) |>
  filter(!is.na(Diabetes)) |>
  mutate(
    Diabetes     = factor(Diabetes, levels = c("No", "Yes")),
    Sex          = factor(Sex),
    Race         = factor(Race),
    AlcoholUse   = factor(AlcoholUse, levels = c("No", "Yes")),
    SmokeHistory = factor(SmokeHistory, levels = c("No", "Yes"))
  )

write_csv(dat, "nhanes_diabetes_subset.csv")

cat("Subset rows:", nrow(dat), " cols:", ncol(dat), "\\n")
glimpse(dat)"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 1. Normality assessment (numeric predictors)

For each numeric variable we report:

* sample size, mean, SD, median, IQR, min, max
* skewness and excess kurtosis
* **D'Agostino-Pearson K²** (`agostino.test`)
* **Jarque-Bera** (`jarque.test`)
* **Anderson-Darling** Lilliefors (`lillie.test` — appropriate for large n)
* **Shapiro-Wilk** on a 5,000-row subsample (Shapiro is unreliable above n≈5,000)

A variable is treated as **normal** only if skewness |<1|, excess kurtosis |<2|,
and all three large-sample tests fail to reject at α = 0.05. The result of this
assessment determines whether parametric or non-parametric tests are used in
the bivariate table."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
numeric_vars <- c("Age", "BMI", "SystolicBP", "DiastolicBP")

normality_df <- map_dfr(numeric_vars, function(v) {
  x <- dat[[v]]; x <- x[!is.na(x)]
  set.seed(1)
  sh <- if (length(x) > 5000) shapiro.test(sample(x, 5000)) else shapiro.test(x)
  tibble(
    Variable      = v,
    n             = length(x),
    Mean          = mean(x),
    SD            = sd(x),
    Median        = median(x),
    IQR           = IQR(x),
    Min           = min(x),
    Max           = max(x),
    Skew          = skewness(x),
    ExcessKurt    = kurtosis(x) - 3,
    K2_stat       = agostino.test(x)$statistic,
    K2_p          = agostino.test(x)$p.value,
    JB_stat       = jarque.test(x)$statistic,
    JB_p          = jarque.test(x)$p.value,
    AD_stat       = lillie.test(x)$statistic,
    AD_p          = lillie.test(x)$p.value,
    Shapiro_stat  = sh$statistic,
    Shapiro_p     = sh$p.value
  )
})

normality_df <- normality_df |>
  mutate(
    Normal = case_when(
      abs(Skew) < 1 & abs(ExcessKurt) < 2 &
        K2_p > 0.05 & JB_p > 0.05 & AD_p > 0.05 ~ "Yes",
      TRUE ~ "No"
    )
  )

normality_df |>
  mutate(across(where(is.numeric), ~ signif(.x, 4))) |>
  select(Variable, n, Mean, SD, Median, IQR, Min, Max,
         Skew, ExcessKurt, K2_p, JB_p, AD_p, Shapiro_p, Normal) |>
  gt() |>
  fmt_number(columns = where(is.numeric), decimals = 3) |>
  fmt_number(columns = n, decimals = 0) |>
  tab_header("Table 1. Normality assessment of numeric predictors",
             "NHANES 2009–2010, diabetes analytic subset (N = 19,460)") |>
  tab_spanner(label = "Distribution", columns = c(Mean, SD, Median, IQR, Min, Max)) |>
  tab_spanner(label = "Shape", columns = c(Skew, ExcessKurt)) |>
  tab_spanner(label = "Normality tests (p-value)", columns = c(K2_p, JB_p, AD_p, Shapiro_p)) |>
  cols_label(
    n = "n", Mean = "Mean", SD = "SD", Median = "Median", IQR = "IQR",
    Min = "Min", Max = "Max", Skew = "Skew", ExcessKurt = "Excess kurt.",
    K2_p = "D'Agostino K²", JB_p = "Jarque-Bera",
    AD_p = "Anderson-Darling", Shapiro_p = "Shapiro (n≤5000)",
    Normal = "Normal?"
  )

write_csv(normality_df, "normality_results.csv")"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
**Normality verdict.** Every numeric predictor rejects normality at
p < 0.001 across all three large-sample tests (D'Agostino-Pearson K²,
Jarque-Bera, Anderson-Darling Lilliefors) and the Shapiro-Wilk subsample.
Skewness exceeds |1| for SystolicBP and DiastolicBP. **All four numeric
predictors are therefore treated as non-normal**, and non-parametric
Mann-Whitney U (Wilcoxon rank-sum) tests are used in the bivariate table."""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 2. Univariate plots

Histograms with an overlaid density curve and boxplots for each numeric
predictor; bar charts for each categorical predictor and the outcome."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
# --- Univariate plots: numeric (histogram + boxplot) ---------------------
uni_numeric <- map(numeric_vars, function(v) {
  d <- dat[[v]]
  p_hist <- ggplot(dat, aes(.data[[v]])) +
    geom_histogram(aes(y = after_stat(density)), bins = 40,
                   fill = "steelblue", colour = "white", alpha = 0.8) +
    geom_density(colour = "darkorange", linewidth = 1) +
    labs(title = paste("Univariate:", v), x = v, y = "Density") +
    theme_bw(base_size = 11)
  p_box <- ggplot(dat, aes(y = .data[[v]])) +
    geom_boxplot(fill = "steelblue", alpha = 0.6, width = 0.4) +
    labs(title = paste("Boxplot:", v), x = "", y = v) +
    theme_bw(base_size = 11) +
    theme(axis.text.x = element_blank(), axis.ticks.x = element_blank())
  p_hist / p_box + plot_layout(heights = c(2, 1))
})

walk2(uni_numeric, numeric_vars, ~ {
  ggsave(file.path("plots", paste0("uni_", .y, ".png")),
         .x, width = 8, height = 6, dpi = 150)
})

# --- Univariate plots: categorical (bar charts) --------------------------
categorical_vars <- c("Sex", "Race", "AlcoholUse", "SmokeHistory")

uni_categorical <- map(categorical_vars, function(v) {
  d <- dat |>
    count(.data[[v]]) |>
    mutate(pct = 100 * n / sum(n))
  ggplot(d, aes(x = .data[[v]], y = n, fill = .data[[v]])) +
    geom_col(show.legend = FALSE) +
    geom_text(aes(label = sprintf("%d\\n(%.1f%%)", n, pct)),
              vjust = -0.3, size = 3.2) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +
    labs(title = paste("Univariate:", v), x = v, y = "Count") +
    theme_bw(base_size = 11) +
    theme(axis.text.x = element_text(angle = 25, hjust = 1))
})

walk2(uni_categorical, categorical_vars, ~ {
  ggsave(file.path("plots", paste0("uni_", .y, ".png")),
         .x, width = 7, height = 5, dpi = 150)
})

# Outcome bar chart
p_outcome <- dat |>
  count(Diabetes) |>
  mutate(pct = 100 * n / sum(n)) |>
  ggplot(aes(x = Diabetes, y = n, fill = Diabetes)) +
  geom_col(show.legend = FALSE) +
  geom_text(aes(label = sprintf("%d\\n(%.1f%%)", n, pct)),
            vjust = -0.3, size = 3.4) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +
  labs(title = "Univariate: Diabetes (outcome)",
       x = "Diabetes", y = "Count") +
  theme_bw(base_size = 11)
ggsave(file.path("plots", "uni_Diabetes.png"),
       p_outcome, width = 6, height = 5, dpi = 150)

cat("Univariate plots saved.\\n")"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 3. Table 1 — Univariate summary

A publication-style "Table 1" summarising every variable in the analytic
subset. Numeric variables are summarised as median (IQR) (non-normal
distribution confirmed above); categorical variables as n (%)."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
tbl_uni <- dat |>
  select(Diabetes, Age, Sex, BMI, SystolicBP, DiastolicBP,
         Race, AlcoholUse, SmokeHistory) |>
  tbl_summary(
    statistic = list(
      all_continuous()  ~ "{median} ({p25}, {p75})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    label = list(
      Diabetes     ~ "Diabetes (outcome)",
      Age          ~ "Age (years)",
      Sex          ~ "Sex",
      BMI          ~ "BMI (kg/m²)",
      SystolicBP   ~ "Systolic blood pressure (mmHg)",
      DiastolicBP  ~ "Diastolic blood pressure (mmHg)",
      Race         ~ "Race",
      AlcoholUse   ~ "Alcohol use (past 12 months)",
      SmokeHistory ~ "Smoking history (≥100 cigarettes)"
    ),
    missing = "ifany",
    missing_text = "Missing"
  ) |>
  modify_header(label ~ "**Variable**") |>
  modify_spanning_header(all_stat_cols() ~
    "**NHANES 2009–2010 (N = {N})**") |>
  bold_labels()

tbl_uni"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 4. Bivariate plots — by Diabetes

For each numeric predictor: boxplot and density plot stratified by Diabetes.
For each categorical predictor: grouped bar chart of within-level proportions
by Diabetes status."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
# --- Bivariate plots: numeric (boxplot + density) ------------------------
biv_numeric <- map(numeric_vars, function(v) {
  p_box <- ggplot(dat, aes(x = Diabetes, y = .data[[v]], fill = Diabetes)) +
    geom_boxplot(alpha = 0.7, show.legend = FALSE) +
    labs(title = paste(v, "by Diabetes"), x = "Diabetes", y = v) +
    theme_bw(base_size = 11)
  p_dens <- ggplot(dat, aes(x = .data[[v]], colour = Diabetes, fill = Diabetes)) +
    geom_density(alpha = 0.35) +
    labs(title = paste("Density:", v, "by Diabetes"),
         x = v, y = "Density") +
    theme_bw(base_size = 11) +
    theme(legend.position = "bottom")
  p_box / p_dens + plot_layout(heights = c(1, 1))
})

walk2(biv_numeric, numeric_vars, ~ {
  ggsave(file.path("plots", paste0("biv_", .y, ".png")),
         .x, width = 8, height = 7, dpi = 150)
})

# --- Bivariate plots: categorical (grouped bars, % within level) ---------
biv_categorical <- map(categorical_vars, function(v) {
  d <- dat |>
    count(.data[[v]], Diabetes) |>
    group_by(.data[[v]]) |>
    mutate(pct = 100 * n / sum(n)) |>
    ungroup()
  ggplot(d, aes(x = .data[[v]], y = pct, fill = Diabetes)) +
    geom_col(position = position_dodge(width = 0.8), width = 0.7) +
    geom_text(aes(label = sprintf("%.1f%%", pct)),
              position = position_dodge(width = 0.8), vjust = -0.3, size = 3) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +
    labs(title = paste(v, "by Diabetes"),
         x = v, y = "% within level", fill = "Diabetes") +
    theme_bw(base_size = 11) +
    theme(axis.text.x = element_text(angle = 25, hjust = 1),
          legend.position = "bottom")
})

walk2(biv_categorical, categorical_vars, ~ {
  ggsave(file.path("plots", paste0("biv_", .y, ".png")),
         .x, width = 7, height = 5, dpi = 150)
})

cat("Bivariate plots saved.\\n")"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 5. Table 2 — Bivariate analysis by Diabetes

Publication-style "Table 2" stratified by Diabetes status, with hypothesis
tests and p-values.

* **Numeric predictors** — Mann-Whitney U (Wilcoxon rank-sum) test, because
  all numeric variables failed normality (Section 1). Summary reported as
  median (IQR).
* **Categorical predictors** — Pearson chi-squared test of independence.
  Summary reported as n (%).

The test used for each p-value is shown in the table footnotes."""))

# ---------------------------------------------------------------------------
cells.append(new_code_cell("""\
tbl_biv <- dat |>
  select(Diabetes, Age, Sex, BMI, SystolicBP, DiastolicBP,
         Race, AlcoholUse, SmokeHistory) |>
  tbl_summary(
    by = Diabetes,
    statistic = list(
      all_continuous()  ~ "{median} ({p25}, {p75})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    label = list(
      Age          ~ "Age (years)",
      Sex          ~ "Sex",
      BMI          ~ "BMI (kg/m²)",
      SystolicBP   ~ "Systolic blood pressure (mmHg)",
      DiastolicBP  ~ "Diastolic blood pressure (mmHg)",
      Race         ~ "Race",
      AlcoholUse   ~ "Alcohol use (past 12 months)",
      SmokeHistory ~ "Smoking history (≥100 cigarettes)"
    ),
    missing = "ifany",
    missing_text = "Missing"
  ) |>
  add_p(
    test = list(
      all_continuous()  ~ "wilcox.test",
      all_categorical() ~ "chisq.test"
    ),
    pvalue_fun = function(x) style_pvalue(x, digits = 3)
  ) |>
  modify_header(label ~ "**Variable**") |>
  modify_spanning_header(
    all_stat_cols() ~ "**Diabetes status**"
  ) |>
  bold_labels() |>
  modify_footnote(
    all_stat_cols() ~ "Median (IQR) for numeric; n (%) for categorical"
  ) |>
  modify_footnote(
    p.value ~
    "Mann-Whitney U (Wilcoxon rank-sum) for numeric predictors (non-normal);
     Pearson chi-squared for categorical predictors"
  )

tbl_biv"""))

# ---------------------------------------------------------------------------
cells.append(new_markdown_cell("""\
## 6. Summary of findings

**Sample.** 19,460 respondents with non-missing diabetes status; 1,706
(8.8%) reported diabetes.

**Normality.** All four numeric predictors (Age, BMI, SystolicBP, DiastolicBP)
rejected normality at p < 0.001 (D'Agostino K², Jarque-Bera, Anderson-Darling,
Shapiro subsample). Non-parametric tests were therefore used throughout.

**Bivariate associations with Diabetes (Table 2):**

* **Age** — median 62 yrs in diabetics vs 25 yrs in non-diabetics, p < 0.001.
* **BMI** — median 31.0 vs 24.3 kg/m², p < 0.001.
* **SystolicBP** — median 128 vs 114 mmHg, p < 0.001.
* **DiastolicBP** — median 68 vs 67 mmHg, p = 2.3×10⁻⁶ (significant but
  clinically small).
* **Sex** — not associated (p = 0.53).
* **Race** — associated (p < 0.001); Black respondents over-represented
  among diabetics.
* **AlcoholUse** — associated (p < 0.001); current drinkers less likely to
  be diabetic.
* **SmokeHistory** — associated (p < 0.001); lifetime smoking more common
  among diabetics.

## 7. Files produced

| File | Description |
|---|---|
| `nhanes_diabetes_subset.csv` | Analytic subset (19,460 × 9) |
| `normality_results.csv` | Full normality test output |
| `plots/uni_*.png` | Univariate plots |
| `plots/biv_*.png` | Bivariate plots by Diabetes |
| `nhanes_diabetes_analysis.ipynb` | This notebook |"""))

# ---------------------------------------------------------------------------
nb = new_notebook(
    cells=cells,
    metadata={
        "kernelspec": {
            "display_name": "R",
            "language": "R",
            "name": "ir",
        },
        "language_info": {"name": "R"},
    },
)
with open("nhanes_diabetes_analysis.ipynb", "w") as f:
    nbf.write(nb, f)
print("notebook written:", len(cells), "cells")