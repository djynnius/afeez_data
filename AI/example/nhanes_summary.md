# NHANES Dataset Summary Report

Dataset: `data/nhanes.csv` | Date: 2026-05-23

---

## Overview

This dataset contains **20,293 rows** and **78 columns** from the U.S. National Health and Nutrition Examination Survey (NHANES), combining the **2009–2010** and **2011–2012** survey cycles. It is a nationally representative, cross-sectional survey designed to assess the health and nutritional status of the U.S. civilian noninstitutionalized population.

---

## Demographic Profile

| Attribute | Summary |
|-----------|---------|
| **Survey cycles** | 10,537 (`2009_10`) and 9,756 (`2011_12`) |
| **Gender** | Near balanced: 10,212 female, 10,081 male |
| **Age range** | 0–80 years (mean ≈ 32). Covers infants through older adults. |
| **Race / Ethnicity (Race1)** | White (7,393), Black (4,640), Mexican (3,739), Hispanic (2,209), Other (2,312) |

---

## Content Areas

The 78 variables fall into roughly 14 domains:

1. **Identifiers & Survey Design**
   - `ID`, `SurveyYr`
   - Survey weights: `WTINT2YR`, `WTMEC2YR`
   - Design variables: `SDMVPSU`, `SDMVSTRA`

2. **Demographics**
   - `Gender`, `Age`, `AgeMonths`, `Race1`, `Race3`, `MaritalStatus`

3. **Socioeconomics**
   - `Education`, `HHIncome` / `HHIncomeMid`, `Poverty` (income-to-poverty ratio)
   - `HomeOwn`, `HomeRooms`, `Work` (employment status)

4. **Anthropometrics**
   - `Weight`, `Height`, `Length` (infants), `HeadCirc`
   - `BMI`, `BMICatUnder20yrs`, `BMI_WHO`

5. **Vital Signs**
   - `Pulse`
   - Blood pressure: raw triplicates (`BPSys1-3` / `BPDia1-3`) and averages (`BPSysAve` / `BPDiaAve`)

6. **Laboratory Measurements**
   - `Testosterone`, `DirectChol`, `TotChol`
   - Urine volume (`UrineVol1/2`) and flow rate (`UrineFlow1/2`)

7. **Chronic Conditions**
   - `Diabetes`, `DiabetesAge`, self-rated `HealthGen`

8. **Physical & Mental Health**
   - `DaysPhysHlthBad`, `DaysMentHlthBad`
   - Depression screeners: `LittleInterest`, `Depressed`

9. **Reproductive Health (females)**
   - `PregnantNow`, `nPregnancies`, `nBabies`, `Age1stBaby`

10. **Sleep**
    - `SleepHrsNight`, `SleepTrouble`

11. **Physical Activity & Sedentary Behavior**
    - `PhysActive`, `PhysActiveDays`, `TVHrsDay`, `CompHrsDay`
    - Child-specific variants: `TVHrsDayChild`, `CompHrsDayChild`

12. **Alcohol Use**
    - `Alcohol12PlusYr`, `AlcoholDay`, `AlcoholYear`

13. **Tobacco & Drug Use**
    - Smoking: `SmokeNow`, `Smoke100`, `SmokeAge`
    - Other substances: `Marijuana`, `RegularMarij`, `HardDrugs`, `AgeFirstMarij`, `AgeRegMarij`

14. **Sexual Behavior**
    - `SexEver`, `SexAge`, `SexNumPartnLife`, `SexNumPartYear`
    - `SameSex`, `SexOrientation`

---

## Key Data Properties

### Age-Conditional Missingness (By Design)
Many variables contain `NA` because NHANES skips questions based on age:

- **Infants** have `Length` and `HeadCirc` but no blood pressure, substance use, or sexual behavior data.
- **Children** have child-specific screen time questions (`TVHrsDayChild`) instead of adult versions.
- **Adolescents** & **adults** are asked detailed questions about alcohol, tobacco, drugs, and sexual behavior.
- **Older adults** are eligible for most adult modules.

### Raw + Derived Variables
Several domains provide both raw measurements and processed summaries:

- Three blood pressure readings → `BPSysAve` / `BPDiaAve`
- Raw BMI → categorical WHO classifications (`BMI_WHO`)

### Survey Weights
Two key weights are included:

| Weight | Description |
|--------|-------------|
| `WTINT2YR` | Interview weight (for questions asked in the interview) |
| `WTMEC2YR` | MEC (Mobile Exam Center) weight (for physical exam / lab data) |

**Important:** Any analysis meant to generalize to the full U.S. population must use these weights, along with `SDMVPSU` (PSU) and `SDMVSTRA` (strata), to account for NHANES' complex survey design. Unweighted analyses produce biased estimates.

---

## Recommendations for Analysis

1. **Always use survey weights** (`WTINT2YR` or `WTMEC2YR` depending on the variables) along with PSU (`SDMVPSU`) and strata (`SDMVSTRA`) variables when computing population estimates, confidence intervals, or regression models.
2. **Filter by age eligibility** before analyzing any variable. Check the NHANES documentation for the minimum age at which each question is asked.
3. **Handle missing data carefully.** Given the high proportion of structural missingness (by design), distinguish between "not measured" and "refused/don't know" where possible.
4. **Subset by survey cycle** if analyzing across years. The `SurveyYr` column distinguishes `2009_10` from `2011_12`.

---

## Source

U.S. National Health and Nutrition Examination Survey (NHANES)  
[https://www.cdc.gov/nchs/nhanes/](https://www.cdc.gov/nchs/nhanes/)
