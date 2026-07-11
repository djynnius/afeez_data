# Refresher


Data 
- Numeric
    + Continuous
    + Count (Discrete)
- Categorical
    + Binary vs Non Binary
    + Nominal vs Ordinal


### Analysis progression

```mermaid
flowchart LR

A[Recieve Data] --> B[Exploratory Analysis] --> C[Hypothesis Testing] --> D[Machine Learning]

```

### Receive Data 
- Get a reson 
- understand the data (get a data dictionary / codebook)
- Explore for observations (rows) and variables (columns)
- Explore for missingness

### Exploratory analysis

Common reference to data types because count/discrete data is often treated as ordinal categorical
- Continuous
- Categorical

##### Summaries

- Continuous 
    1. Distribution (with histogram)
        + Normal 
        + Not normal 
    2. Five number summary (including range and inter quartile range) 
        + Minimum
        + Q1 (First quartile)
        + Median (Q2)
        + Q3 (Third quartile)
        + Maximum
    3. Report center and spread (based on distribution)
    4. Visualize - Boxplot

- Categorical 
    1. Frequencies 
    2. Proportions (Percentages)
    3. Visualize - Bar chart

**Formulae** 

$Range = Maximum - Minimum$

$IQR = Q3 - Q1$

IQR = Inter quartile range


$Percentage = Proportion * 100$


### Probability Theory

1. $0 <= P(X) <= 1$
2. $\sum{P(X_i)} = 1$
3. Compliment rule: $P(X) = 1 - P(X_c)$
4. Addition rule 
    + Independence: $P(A \cup{B}) = P(A) + P(B) $
    + Not independent $P(A \cup{B}) = P(A) + P(B) - P(A \cap{B})$
5. Multiplication rule
    + Independence: $(A\cap{B}) = P(A) * P(B)$
    + Non independent:  $(A\cap{B}) = P(A|B) * P(B)$


### Contingency tables 

||$A$|$A_c$|
|-|-|-|
|**$B$**|a|b|
|**$B_c$**|c|d|

**Probabilty types**

$Total = N = a + b + c + d$

- Marginal Probabilities
    + $P(A) = \frac{(a + c)}{N}$
    + $P(A_c) = \frac{(b + d)}{N}$
    + $P(B) = \frac{(a + b)}{N}$
    + $P(B_c) = \frac{(c + d)}{N}$

- Joint probabilities 
    + $P(A\cap{B}) = \frac{a}{N}$
    + $P(B\cap{A_c}) = \frac{b}{N}$
    + $P(A\cap{B_c}) = \frac{c}{N}$
    + $P(A_c\cap{B_c}) = \frac{d}{N}$

- Conditional probabilites
    + $P(A|B) = \frac{a}{(a+b)}$
    + $P(A|B_c) = \frac{c}{(c+d)}$
    + $P(A_c|B) = \frac{b}{(a+b)}$
    + $P(A_c|B_c) = \frac{d}{(c+d)}$
    + $P(B|A) = \frac{a}{(a+c)}$
    + $P(B|A_c) = \frac{b}{(b+d)}$
    + $P(B_c|A) = \frac{c}{(a+c)}$
    + $P(B_c|A_c) = \frac{d}{(b+d)}$



##### Bi variate analysis 

- Continuous vs Continuous
    1. Correlation 
        + Positive
        + Negative 
        + No 
    2. Visualize - scatterplot
- Categorical vs Categorical 
    1. Frequencies and Proportion of contingency table
    2. Visualize - grouped bar charts
    3. Visualize marginal probibilities using stacked bar charts
- Continuous vs Categorical
    1. Numeric summaries (center and spread) by each level in the categorical
    2. Visualize: Grouped boxplots

> When correlation is very high usually >= -0.8 or <= -0.8 we say the variables are *colinear* (perfectly correlated)


**Selecting tests/analysis**

|Situation | Distribution | Test | 
|----------|--------------|------|
|Center    | Normal      | Mean |
|Center    | Not Normal      | Median |
|Spread    | Normal      | Standard Deviation |
|Spread    | Not Normal      | Inter quartile range |
|Continuous vs Continuous    | Normal      | Pearsons correlation coefficient |
|Continuous vs Continuous    | Not Normal      | Spearmans correlation coefficient |

