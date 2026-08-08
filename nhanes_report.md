# NHANES Dataset Report

**Source file:** `data/nhanes.csv`
**Survey cycle:** 2009–2010

---

## 1. Overview

| Metric | Value |
|---|---:|
| Observations (rows) | 20,293 |
| Variables (columns) | 78 |
| Numeric variables | 50 |
| Categorical variables | 28 |
| Variables with no missingness | 9 |
| Variables with some missingness | 69 |

Missing values were detected as empty cells or the literal string `NA` (R-style encoding). A variable was classified as **numeric** if more than 90% of its non-missing values parsed as numbers; otherwise **categorical**.

> **Note on high missingness:** Much of the missingness is *structural* — it reflects the NHANES skip-logic rather than data loss. Variables such as `nPregnancies`, `PregnantNow`, and `Age1stBaby` only apply to females who have been pregnant; `Length` and `HeadCirc` apply to infants; `BMICatUnder20yrs` applies to respondents under 20. These should not be treated as data-quality failures.

---

## 2. Variable Type Classification

### Numeric variables (50)

`ID`, `SurveyYr`, `Age`, `AgeMonths`, `HHIncomeMid`, `Poverty`, `HomeRooms`, `Weight`, `Length`, `HeadCirc`, `Height`, `BMI`, `Pulse`, `BPSysAve`, `BPDiaAve`, `BPSys1`, `BPDia1`, `BPSys2`, `BPDia2`, `BPSys3`, `BPDia3`, `Testosterone`, `DirectChol`, `TotChol`, `UrineVol1`, `UrineFlow1`, `UrineVol2`, `UrineFlow2`, `DiabetesAge`, `DaysPhysHlthBad`, `DaysMentHlthBad`, `nPregnancies`, `nBabies`, `Age1stBaby`, `SleepHrsNight`, `PhysActiveDays`, `TVHrsDayChild`, `CompHrsDayChild`, `AlcoholDay`, `AlcoholYear`, `SmokeAge`, `AgeFirstMarij`, `AgeRegMarij`, `SexAge`, `SexNumPartnLife`, `SexNumPartYear`, `WTINT2YR`, `WTMEC2YR`, `SDMVPSU`, `SDMVSTRA`

### Categorical variables (28)

`Gender`, `Race1`, `Race3`, `Education`, `MaritalStatus`, `HHIncome`, `HomeOwn`, `Work`, `BMICatUnder20yrs`, `BMI_WHO`, `Diabetes`, `HealthGen`, `LittleInterest`, `Depressed`, `SleepTrouble`, `PhysActive`, `TVHrsDay`, `CompHrsDay`, `Alcohol12PlusYr`, `SmokeNow`, `Smoke100`, `Marijuana`, `RegularMarij`, `HardDrugs`, `SexEver`, `SameSex`, `SexOrientation`, `PregnantNow`

> **Caveat:** `ID` and `SurveyYr` are technically numeric-typed but function as identifiers/labels. If reclassified as categorical, the split becomes **48 numeric / 30 categorical**.

---

## 3. Variables with No Missingness (9)

`ID`, `SurveyYr`, `Gender`, `Age`, `Race1`, `WTINT2YR`, `WTMEC2YR`, `SDMVPSU`, `SDMVSTRA`

These are the survey design and core demographic variables — complete for all 20,293 respondents.

---

## 4. Missingness Report

Sorted by percentage missing (high to low). 69 of 78 variables have at least one missing value.

| # | Variable | Missing Count | % Missing |
|---:|---|---:|---:|
| 1 | HeadCirc | 19,819 | 97.66% |
| 2 | DiabetesAge | 18,856 | 92.92% |
| 3 | AgeRegMarij | 18,473 | 91.03% |
| 4 | TVHrsDayChild | 18,065 | 89.02% |
| 5 | CompHrsDayChild | 18,065 | 89.02% |
| 6 | Length | 18,008 | 88.74% |
| 7 | PregnantNow | 17,680 | 87.12% |
| 8 | UrineFlow2 | 17,596 | 86.71% |
| 9 | UrineVol2 | 17,585 | 86.66% |
| 10 | Age1stBaby | 17,135 | 84.44% |
| 11 | BMICatUnder20yrs | 16,938 | 83.47% |
| 12 | RegularMarij | 16,581 | 81.71% |
| 13 | AgeFirstMarij | 16,579 | 81.70% |
| 14 | nBabies | 16,354 | 80.59% |
| 15 | nPregnancies | 16,091 | 79.29% |
| 16 | SmokeAge | 15,244 | 75.12% |
| 17 | SmokeNow | 15,060 | 74.21% |
| 18 | Testosterone | 13,467 | 66.36% |
| 19 | SexOrientation | 13,446 | 66.26% |
| 20 | AlcoholDay | 13,300 | 65.54% |
| 21 | SexNumPartYear | 13,253 | 65.31% |
| 22 | Marijuana | 13,221 | 65.15% |
| 23 | PhysActiveDays | 12,918 | 63.66% |
| 24 | SexAge | 12,157 | 59.91% |
| 25 | SexNumPartnLife | 11,761 | 57.96% |
| 26 | SameSex | 11,657 | 57.44% |
| 27 | SexEver | 11,655 | 57.43% |
| 28 | HardDrugs | 11,652 | 57.42% |
| 29 | AlcoholYear | 11,462 | 56.48% |
| 30 | TVHrsDay | 11,228 | 55.33% |
| 31 | CompHrsDay | 11,219 | 55.29% |
| 32 | Race3 | 10,537 | 51.92% |
| 33 | Alcohol12PlusYr | 9,990 | 49.23% |
| 34 | LittleInterest | 9,785 | 48.22% |
| 35 | Depressed | 9,779 | 48.19% |
| 36 | AgeMonths | 9,555 | 47.09% |
| 37 | Education | 8,535 | 42.06% |
| 38 | MaritalStatus | 8,526 | 42.01% |
| 39 | Smoke100 | 8,522 | 41.99% |
| 40 | DaysMentHlthBad | 7,867 | 38.77% |
| 41 | DaysPhysHlthBad | 7,862 | 38.74% |
| 42 | HealthGen | 7,844 | 38.65% |
| 43 | SleepHrsNight | 7,261 | 35.78% |
| 44 | SleepTrouble | 7,235 | 35.65% |
| 45 | Work | 7,233 | 35.64% |
| 46 | PhysActive | 6,015 | 29.64% |
| 47 | BPSys1 | 6,008 | 29.61% |
| 48 | BPDia1 | 6,008 | 29.61% |
| 49 | BPSys2 | 5,812 | 28.64% |
| 50 | BPDia2 | 5,812 | 28.64% |
| 51 | BPSys3 | 5,788 | 28.52% |
| 52 | BPDia3 | 5,788 | 28.52% |
| 53 | UrineFlow1 | 5,603 | 27.61% |
| 54 | TotChol | 5,459 | 26.90% |
| 55 | DirectChol | 5,458 | 26.90% |
| 56 | BPSysAve | 5,426 | 26.74% |
| 57 | BPDiaAve | 5,426 | 26.74% |
| 58 | Pulse | 5,397 | 26.60% |
| 59 | UrineVol1 | 4,210 | 20.75% |
| 60 | BMI_WHO | 2,346 | 11.56% |
| 61 | BMI | 2,279 | 11.23% |
| 62 | Height | 2,258 | 11.13% |
| 63 | HHIncome | 2,076 | 10.23% |
| 64 | HHIncomeMid | 2,076 | 10.23% |
| 65 | Poverty | 1,836 | 9.05% |
| 66 | Weight | 888 | 4.38% |
| 67 | Diabetes | 833 | 4.10% |
| 68 | HomeRooms | 145 | 0.71% |
| 69 | HomeOwn | 137 | 0.68% |

---

## 5. Key Observations

1. **Survey design variables are complete.** `ID`, `SurveyYr`, `Gender`, `Age`, `Race1`, and the weighting/stratification fields (`WTINT2YR`, `WTMEC2YR`, `SDMVPSU`, `SDMVSTRA`) have no missingness — these should be used as the backbone of any analysis.
2. **Most missingness is structural, not random.** The highest-missingness variables (>80%) are tied to specific subpopulations (infants, pregnant women, marijuana users, sexually active respondents). They should be analyzed within their eligible subpopulation, not imputed across the full sample.
3. **Measurement variables cluster around 25–30% missing.** Blood pressure, cholesterol, pulse, and urine measures — the NHANES MEC exam components — are missing for roughly a quarter of respondents, typically those who did not complete the clinical examination.
4. **Core demographics and socioeconomic fields are 90%+ complete.** `Weight`, `Diabetes`, `HomeRooms`, `HomeOwn`, `Poverty`, and `HHIncome` are well-populated and suitable for broad descriptive analysis.