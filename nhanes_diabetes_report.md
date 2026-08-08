# NHANES Diabetes Study — Analysis Report

**Source:** `data/nhanes.csv` (NHANES 2009–2010)
**Subset file:** `nhanes_diabetes_subset.csv`
**Analysis script:** `diabetes_analysis.py`

---

## 1. Study Population

A diabetes-focused analytic subset was created from the full NHANES dataset. Records with a missing `Diabetes` value were dropped.

| Step | Rows |
|---|---:|
| Full NHANES dataset | 20,293 |
| After dropping missing `Diabetes` | **19,460** |

**Outcome variable:** `Diabetes` (Yes / No) — Yes: 1,706 (8.8%); No: 17,754 (91.2%). The outcome is imbalanced.

### Variables in the subset

| Variable in subset | Original NHANES name | Role | Type |
|---|---|---|---|
| Diabetes | Diabetes | Outcome | Categorical (Yes/No) |
| Age | Age | Predictor | Numeric |
| Sex | Gender | Predictor | Categorical (female/male) |
| BMI | BMI | Predictor | Numeric |
| SystolicBP | BPSysAve | Predictor | Numeric |
| DiastolicBP | BPDiaAve | Predictor | Numeric |
| Race | Race1 | Predictor | Categorical (5 levels) |
| AlcoholUse | Alcohol12PlusYr (drank in past 12 months) | Predictor | Categorical (Yes/No) |
| SmokeHistory | Smoke100 (≥100 cigarettes in lifetime) | Predictor | Categorical (Yes/No) |

> `Sex`/`Gender` are both listed in your request; NHANES records sex as `Gender`, so it is retained as `Sex`. `Alcohol12PlusYr` captures alcohol use in the past year, and `Smoke100` captures lifetime smoking history (≥100 cigarettes) — these were chosen as the binary "alcohol use" and "smoking history" indicators.

---

## 2. Normality Assessment (Numeric Variables)

For each numeric predictor, three checks were run: **D'Agostino-Pearson K²** (skew + kurtosis composite), **Anderson-Darling**, and **Shapiro-Wilk** on a 5,000-row subsample (Shapiro is unreliable above n≈5,000). Skewness and excess kurtosis are also reported.

| Variable | n | Mean (SD) | Median (IQR) | Skew | Excess Kurtosis | D'Agostino K² p | Shapiro p (subsample) | Normal? |
|---|---:|---|---|---:|---:|---:|---:|:---:|
| Age | 19,460 | 33.37 (24.37) | 30.00 (11–54) | 0.38 | −1.14 | <0.001 | <0.001 | **No** |
| BMI | 18,005 | 25.65 (7.73) | 24.92 (19.79–30.10) | 0.94 | 1.90 | <0.001 | <0.001 | **No** |
| SystolicBP | 14,860 | 118.07 (18.44) | 115.00 (105–127) | 1.09 | 2.19 | <0.001 | <0.001 | **No** |
| DiastolicBP | 14,860 | 65.60 (15.63) | 67.00 (58–75) | −1.02 | 3.12 | <0.001 | <0.001 | **No** |

**Interpretation:** None of the numeric variables pass normality. All four reject the null of normality at p < 0.001 across all three tests, and the skewness/kurtosis exceed conventional thresholds (|skew| > 1 for SystolicBP and DiastolicBP; BMI is moderately right-skewed). **Therefore non-parametric methods are used in all bivariate comparisons below** (Mann-Whitney U for numeric predictors; chi-squared for categorical). Full machine-readable results: `normality_results.csv`.

---

## 3. Univariate Table

| Variable | Type | n | Missing | Mean (SD) | Median (IQR) | Min–Max | Levels (n, %) |
|---|---|---:|---:|---|---|---|---|
| **Diabetes** (outcome) | Categorical | 19,460 | 0 | — | — | — | No: 17,754 (91.2%); Yes: 1,706 (8.8%) |
| Age | Numeric | 19,460 | 0 | 33.37 (24.37) | 30.00 (11–54) | 1–80 | — |
| BMI | Numeric | 18,005 | 1,455 | 25.65 (7.73) | 24.92 (19.79–30.10) | 12.40–84.87 | — |
| SystolicBP | Numeric | 14,860 | 4,600 | 118.07 (18.44) | 115.00 (105–127) | 74–233 | — |
| DiastolicBP | Numeric | 14,860 | 4,600 | 65.60 (15.63) | 67.00 (58–75) | 0–131 | — |
| Sex | Categorical | 19,460 | 0 | — | — | — | female: 9,785 (50.3%); male: 9,675 (49.7%) |
| Race | Categorical | 19,460 | 0 | — | — | — | White: 7,137 (36.7%); Black: 4,481 (23.0%); Mexican: 3,502 (18.0%); Other: 2,235 (11.5%); Hispanic: 2,105 (10.8%) |
| AlcoholUse | Categorical | 10,298 | 9,162 | — | — | — | Yes: 7,479 (72.6%); No: 2,819 (27.4%) |
| SmokeHistory | Categorical | 11,763 | 7,697 | — | — | — | No: 6,533 (55.5%); Yes: 5,230 (44.5%) |

> **Note on missingness:** `AlcoholUse` and `SmokeHistory` are only asked of adults (≥18), so ~47% and ~40% of the subset are missing respectively — this is structural skip-logic, not data loss. Blood pressure was only measured in the MEC exam (~24% missing).

**Univariate plots:** `plots/uni_*.png` (histogram + KDE and boxplot for each numeric variable; bar chart for each categorical variable and the outcome).

---

## 4. Bivariate Table — by Diabetes (Outcome)

For each predictor, the table reports a summary stratified by Diabetes status (No | Yes) and a hypothesis test with p-value. Test choice follows from the normality assessment: **Mann-Whitney U (Wilcoxon rank-sum)** for numeric predictors (non-normal), **chi-squared test of independence** for categorical predictors.

| Variable | Type | Summary (No \| Yes) | Test | Statistic | p-value |
|---|---|---|---|---:|---:|
| Age | Numeric | No: 25.00 [10–49] \| Yes: 62.00 [52–72] | Mann-Whitney U | 4,906,789 | <0.001 |
| BMI | Numeric | No: 24.30 [19.20–29.33] \| Yes: 31.00 [27.03–36.12] | Mann-Whitney U | 6,208,710 | <0.001 |
| SystolicBP | Numeric | No: 114.00 [105–125] \| Yes: 128.00 [116–141] | Mann-Whitney U | 6,367,393 | <0.001 |
| DiastolicBP | Numeric | No: 67.00 [58–75] \| Yes: 68.00 [60–77] | Mann-Whitney U | 9,847,530 | 2.3×10⁻⁶ |
| Sex | Categorical | female: 8,940 (50.4%) \| 845 (49.5%); male: 8,814 (49.6%) \| 861 (50.5%) | Chi-squared | 0.39 | 0.532 |
| Race | Categorical | Black: 3,980 (22.4%) \| 501 (29.4%); Hispanic: 1,924 (10.8%) \| 181 (10.6%); Mexican: 3,238 (18.2%) \| 264 (15.5%); Other: 2,064 (11.6%) \| 171 (10.0%); White: 6,548 (36.9%) \| 589 (34.5%) | Chi-squared | 45.16 | 3.7×10⁻⁹ |
| AlcoholUse | Categorical | No: 2,297 (26.1%) \| 522 (35.2%); Yes: 6,519 (73.9%) \| 960 (64.8%) | Chi-squared | 53.18 | 3.0×10⁻¹³ |
| SmokeHistory | Categorical | No: 5,713 (56.6%) \| 820 (49.2%); Yes: 4,382 (43.4%) \| 848 (50.8%) | Chi-squared | 31.72 | 1.8×10⁻⁸ |

> **Tests used:** For numeric predictors, the **Mann-Whitney U (Wilcoxon rank-sum) test** was used because all numeric variables failed normality (Section 2), so the parametric two-sample t-test is inappropriate. For categorical predictors, the **Pearson chi-squared test of independence** was used to compare the distribution of each predictor across Diabetes groups. A p-value < 0.05 is considered statistically significant.

### Interpretation of bivariate results

- **Age** — strongly associated with Diabetes (p < 0.001). Median age is dramatically higher in diabetics (62 vs 25 years), reflecting the well-known age gradient.
- **BMI** — strongly associated (p < 0.001). Diabetics have a markedly higher median BMI (31.0 vs 24.3 kg/m²), crossing into the obese range.
- **SystolicBP** — strongly associated (p < 0.001). Median systolic pressure is 14 mmHg higher in diabetics (128 vs 114).
- **DiastolicBP** — statistically significant but clinically modest (p = 2.3×10⁻⁶); median differs by only 1 mmHg (68 vs 67).
- **Sex** — not associated with Diabetes (p = 0.53); prevalence is essentially identical in males and females.
- **Race** — significantly associated (p = 3.7×10⁻⁹). Black respondents have a disproportionately high share of diabetes cases (29.4% of diabetics vs 22.4% of non-diabetics), while Mexican and White respondents are under-represented among diabetics.
- **AlcoholUse** — significantly associated (p = 3.0×10⁻¹³). Current alcohol users are *less* likely to have diabetes (64.8% of diabetics vs 73.9% of non-diabetics report drinking).
- **SmokeHistory** — significantly associated (p = 1.8×10⁻⁸). A lifetime smoking history is more common among diabetics (50.8% vs 43.4%).

**Bivariate plots:** `plots/biv_*.png` (boxplot + density by Diabetes for numeric predictors; grouped bar chart of within-level proportions for categorical predictors).

---

## 5. Files Produced

| File | Description |
|---|---|
| `nhanes_diabetes_subset.csv` | Analytic subset (19,460 rows × 9 cols) |
| `normality_results.csv` | Full normality test output |
| `univariate_table.csv` | Univariate summary table |
| `bivariate_table.csv` | Bivariate table with tests |
| `diabetes_analysis.py` | Reproducible analysis script |
| `plots/uni_*.png` | Univariate plots (9 figures) |
| `plots/biv_*.png` | Bivariate plots by Diabetes (8 figures) |

---

## 6. Limitations

1. **Cross-sectional design.** Diabetes is self-reported; no HbA1c or fasting glucose confirmation. Direction of causality cannot be inferred — associations only.
2. **Imbalanced outcome.** Only 8.8% are diabetics; any future multivariable modelling should consider this class imbalance.
3. **Structural missingness in lifestyle variables.** `AlcoholUse` and `SmokeHistory` are only collected for adults, reducing the available sample for any adjusted analysis that includes them.
4. **No multiple-testing adjustment** in the bivariate table. Eight tests are reported; a Bonferroni-corrected threshold would be 0.05/8 = 0.00625 — under that threshold, DiastolicBP (p = 2.3×10⁻⁶) remains significant, and Sex remains non-significant, with all others remaining highly significant.