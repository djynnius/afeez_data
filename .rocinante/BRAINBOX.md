# BRAINBOX
## Goals
- Explore `data/nhanes.csv` (20,293 rows, 78 cols)
- Conduct diabetes study: subset, normality, uni/bivariate analysis
## State
- `nhanes_report.md`: General data summary created
- `nhanes_diabetes_subset.csv`: 19,460 rows × 9 cols (Diabetes not missing)
- `nhanes_diabetes_report.md`: Full analysis write-up
- `diabetes_analysis.py`: Reproducible script (9236 bytes)
- `plots/`: 17 PNGs (uni_*.png, biv_*.png)
- Tables: `normality_results.csv`, `univariate_table.csv`, `bivariate_table.csv`
## Decisions
- Proxy vars: `Alcohol12PlusYr` (alcohol), `Smoke100` (smoke), `Gender` (sex)
- Stats: Mann-Whitney U for numeric (non-normal per normality tests)
- Filtering: Dropped 833 rows where `Diabetes` missing
## Gotchas
- `ModuleNotFoundError: No module named 'scipy'` (resolved via install)
- `ModuleNotFoundError: No module named 'seaborn'` (resolved via install)
- Seaborn `FutureWarning`: Passing `palette` without assigning `hue` (line 213)
- High missingness in source: 69/78 vars (e.g., HeadCirc 97.66% missing)
## Next steps
- Interpret risk factors (BMI p=6.02e-274, Age significant)
- Incorporate survey weights (`WTINT2YR`, `WTMEC2YR`) for population estimates
- Build multivariate logistic regression model
