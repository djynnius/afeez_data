"""
NHANES diabetes study analysis.

- Subset: Diabetes, Age, Gender, BMI, BPSysAve, BPDiaAve, Race1,
          Alcohol12PlusYr (alcohol use), Smoke100 (smoking history)
- Drop rows where Diabetes is missing.
- Normality tests for numeric variables.
- Univariate summary table.
- Bivariate table by Diabetes with hypothesis tests.
- Univariate plots + bivariate plots by Diabetes.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
OUT = "plots"
os.makedirs(OUT, exist_ok=True)

# ---- Load & subset ----
df = pd.read_csv("data/nhanes.csv", na_values=["NA", ""])

rename = {
    "BPSysAve": "SystolicBP",
    "BPDiaAve": "DiastolicBP",
    "Race1": "Race",
    "Alcohol12PlusYr": "AlcoholUse",
    "Smoke100": "SmokeHistory",
    "Gender": "Sex",
}
keep = ["Diabetes", "Age", "Gender", "BMI", "BPSysAve", "BPDiaAve",
        "Race1", "Alcohol12PlusYr", "Smoke100"]
sub = df[keep].rename(columns=rename).copy()
sub = sub.dropna(subset=["Diabetes"]).reset_index(drop=True)
sub["Diabetes"] = sub["Diabetes"].astype(str)
sub.to_csv("nhanes_diabetes_subset.csv", index=False)
print(f"Subset rows: {len(sub)}  cols: {list(sub.columns)}")

numeric = ["Age", "BMI", "SystolicBP", "DiastolicBP"]
categorical = ["Sex", "Race", "AlcoholUse", "SmokeHistory"]
outcome = "Diabetes"

# ---- Normality tests ----
print("\n=== NORMALITY (numeric) ===")
normality_rows = []
for v in numeric:
    s = sub[v].dropna()
    # Shapiro is unreliable for n>5000; use D'Agostino-Pearson K^2 (normality of skew+kurt)
    # and Anderson-Darling. Report both. Also report skew/kurtosis.
    skew = stats.skew(s, bias=False)
    kurt = stats.kurtosis(s, fisher=True, bias=False)
    # D'Agostino-Pearson
    try:
        k2_stat, k2_p = stats.normaltest(s)
    except Exception:
        k2_stat, k2_p = np.nan, np.nan
    # Anderson-Darling
    try:
        ad = stats.anderson(s, dist="norm")
        ad_stat = ad.statistic
        # p-value approximation from Anderson
        ad_p = ad.significance_level[list(ad.critical_values).index(
            min(ad.critical_values, key=lambda cv: abs(cv - ad_stat)))] / 100.0
    except Exception:
        ad_stat, ad_p = np.nan, np.nan
    # Shapiro on a random subsample of 5000 for reference
    try:
        sample = s.sample(min(5000, len(s)), random_state=1)
        sh_stat, sh_p = stats.shapiro(sample)
    except Exception:
        sh_stat, sh_p = np.nan, np.nan
    normality_rows.append({
        "Variable": v, "n": len(s),
        "Mean": s.mean(), "SD": s.std(),
        "Median": s.median(), "IQR": s.quantile(.75) - s.quantile(.25),
        "Skew": skew, "ExcessKurtosis": kurt,
        "DagostinoK2_stat": k2_stat, "DagostinoK2_p": k2_p,
        "AndersonDarling_stat": ad_stat,
        "ShapiroW_stat (n<=5000 subsample)": sh_stat,
        "ShapiroW_p (n<=5000 subsample)": sh_p,
    })
    print(f"{v}: skew={skew:.3f} kurt={kurt:.3f} "
          f"K2_p={k2_p:.3g} AD_stat={ad_stat:.2f} Shapiro_p={sh_p:.3g}")
norm_df = pd.DataFrame(normality_rows)
norm_df.to_csv("normality_results.csv", index=False)

# Interpretation of normality
def is_normal(row):
    # treat as normal if skew abs<1, |excess kurt|<2, and K2 p>0.05
    return (abs(row["Skew"]) < 1 and abs(row["ExcessKurtosis"]) < 2
            and row["DagostinoK2_p"] > 0.05)
norm_df["Normal?"] = norm_df.apply(
    lambda r: "Yes" if is_normal(r) else "No", axis=1)
print("\nNormality call:")
print(norm_df[["Variable", "Skew", "ExcessKurtosis",
               "DagostinoK2_p", "Normal?"]].to_string(index=False))

# ---- Univariate table ----
print("\n=== UNIVARIATE TABLE ===")
uni_rows = []
for v in numeric:
    s = sub[v].dropna()
    uni_rows.append({
        "Variable": v, "Type": "Numeric",
        "n": len(s), "Missing": sub[v].isna().sum(),
        "Mean (SD)": f"{s.mean():.2f} ({s.std():.2f})",
        "Median (IQR)": f"{s.median():.2f} "
                         f"({s.quantile(.25):.2f}-{s.quantile(.75):.2f})",
        "Min-Max": f"{s.min():.2f}-{s.max():.2f}",
        "Normal?": norm_df.loc[norm_df['Variable'] == v, "Normal?"].values[0],
        "Levels": "",
    })
for v in categorical:
    s = sub[v].dropna()
    levels = s.value_counts()
    lev_str = "; ".join([f"{k}: {cnt} ({100*cnt/len(s):.1f}%)" for k, cnt in levels.items()])
    uni_rows.append({
        "Variable": v, "Type": "Categorical",
        "n": len(s), "Missing": sub[v].isna().sum(),
        "Mean (SD)": "", "Median (IQR)": "", "Min-Max": "",
        "Normal?": "", "Levels": lev_str,
    })
# Outcome row
s = sub[outcome]
lev_str = "; ".join([f"{k}: {cnt} ({100*cnt/len(s):.1f}%)"
                    for k, cnt in s.value_counts().items()])
uni_rows.insert(0, {
    "Variable": outcome, "Type": "Categorical (outcome)",
    "n": len(s), "Missing": 0,
    "Mean (SD)": "", "Median (IQR)": "", "Min-Max": "",
    "Normal?": "", "Levels": lev_str,
})
uni_df = pd.DataFrame(uni_rows)
uni_df.to_csv("univariate_table.csv", index=False)
print(uni_df.to_string(index=False))

# ---- Bivariate table by Diabetes ----
print("\n=== BIVARIATE TABLE by Diabetes ===")
groups = {g: sub[sub[outcome] == g] for g in sorted(sub[outcome].unique())}
bi_rows = []
for v in numeric:
    normal = norm_df.loc[norm_df['Variable'] == v, "Normal?"].values[0] == "Yes"
    data = {g: groups[g][v].dropna() for g in groups}
    if normal:
        # t-test (assume unequal var = Welch)
        keys = list(data.keys())
        stat, p = stats.ttest_ind(data[keys[0]], data[keys[1]],
                                  equal_var=False)
        test_name = "Welch's two-sample t-test"
        summary = " | ".join(
            [f"{g}: {data[g].mean():.2f} ({data[g].std():.2f})"
             for g in data])
    else:
        keys = list(data.keys())
        stat, p = stats.mannwhitneyu(data[keys[0]], data[keys[1]],
                                      alternative="two-sided")
        test_name = "Mann-Whitney U (Wilcoxon rank-sum)"
        summary = " | ".join(
            [f"{g}: {data[g].median():.2f} "
             f"[{data[g].quantile(.25):.2f}-{data[g].quantile(.75):.2f}]"
             for g in data])
    bi_rows.append({
        "Variable": v, "Type": "Numeric",
        "Summary (No | Yes)": summary,
        "Test": test_name, "Statistic": stat, "p-value": p,
    })
for v in categorical:
    ct = pd.crosstab(sub[v], sub[outcome])
    chi2, p, dof, exp = stats.chi2_contingency(ct)
    test_name = "Chi-squared test of independence"
    # summary: level: n(%) within each Diabetes group
    cols = list(ct.columns)
    parts = []
    for level in ct.index:
        parts.append(f"{level}: " + " | ".join(
            [f"{ct.loc[level, c]} ({100*ct.loc[level, c]/ct[c].sum():.1f}%)"
             for c in cols]))
    summary = " ; ".join(parts)
    bi_rows.append({
        "Variable": v, "Type": "Categorical",
        "Summary (No | Yes)": summary,
        "Test": test_name, "Statistic": chi2, "p-value": p,
    })
bi_df = pd.DataFrame(bi_rows)
bi_df.to_csv("bivariate_table.csv", index=False)
print(bi_df[["Variable", "Type", "Test", "Statistic",
             "p-value"]].to_string(index=False))
print("\nFull summaries saved to bivariate_table.csv")

# ---- Univariate plots ----
print("\n=== PLOTS ===")
# Histograms + boxplots for numeric, barplots for categorical
for v in numeric:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(sub[v].dropna(), kde=True, ax=axes[0], color="steelblue")
    axes[0].set_title(f"Univariate: {v} (histogram + KDE)")
    axes[0].set_xlabel(v)
    sns.boxplot(x=sub[v].dropna(), ax=axes[1], color="steelblue")
    axes[1].set_title(f"Univariate: {v} (boxplot)")
    axes[1].set_xlabel(v)
    plt.tight_layout()
    plt.savefig(f"{OUT}/uni_{v}.png", dpi=120)
    plt.close()

for v in categorical + [outcome]:
    fig, ax = plt.subplots(figsize=(8, 4))
    order = sub[v].value_counts().index
    sns.countplot(x=sub[v], order=order, ax=ax, palette="Set2")
    ax.set_title(f"Univariate: {v} (counts)")
    ax.set_xlabel(v)
    ax.set_ylabel("Count")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(f"{OUT}/uni_{v}.png", dpi=120)
    plt.close()

# ---- Bivariate plots by Diabetes ----
for v in numeric:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.boxplot(x=outcome, y=v, data=sub, ax=axes[0], palette="Set2")
    axes[0].set_title(f"{v} by Diabetes (boxplot)")
    sns.kdeplot(data=sub, x=v, hue=outcome, common_norm=False, ax=axes[1])
    axes[1].set_title(f"{v} by Diabetes (density)")
    plt.tight_layout()
    plt.savefig(f"{OUT}/biv_{v}.png", dpi=120)
    plt.close()

for v in categorical:
    fig, ax = plt.subplots(figsize=(8, 4))
    ct = pd.crosstab(sub[v], sub[outcome], normalize="index") * 100
    ct.plot(kind="bar", stacked=False, ax=ax, colormap="Set2")
    ax.set_title(f"{v} by Diabetes (proportion within {v} level, %)")
    ax.set_xlabel(v)
    ax.set_ylabel("% within level")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Diabetes")
    plt.tight_layout()
    plt.savefig(f"{OUT}/biv_{v}.png", dpi=120)
    plt.close()

print("Plots written to", OUT)
print("Done.")