# afeez EDA — NHANES (Adults 18–50)
# Variables: Age, Gender, Race1, Weight, Height, Diabetes, BPSysAve, BPDiaAve
# Outcome: Diabetes
# Constraint: Age between 18 and 50 inclusive

library(tidyverse)
library(gtsummary)
library(gt)
library(skimr)

# ---------------------------------------------------------------------------
# 1. Load & prepare data
# ---------------------------------------------------------------------------
df <- readr::read_csv("data/nhanes.csv", na = c("", "NA", "N/A", "."))

# Select requested variables
sel_vars <- c("Age", "Gender", "Race1", "Weight", "Height", "Diabetes", "BPSysAve", "BPDiaAve")
df <- df %>% select(all_of(sel_vars))

# Filter adults 18–50
df <- df %>% filter(Age >= 18, Age <= 50)

# Ensure Diabetes is a factor (clean NA)
df <- df %>% filter(!is.na(Diabetes))
df$Diabetes <- factor(df$Diabetes)

# Factor other categorical
df$Gender <- factor(df$Gender)
df$Race1 <- factor(df$Race1)

cat("Rows after filtering:", nrow(df), "\n")
cat("Outcome levels:\n")
print(table(df$Diabetes))

# ---------------------------------------------------------------------------
# 2. Dataset Overview
# ---------------------------------------------------------------------------
cat("\n--- Glimpse ---\n")
glimpse(df)

cat("\n--- Missingness ---\n")
df %>%
  summarise(across(everything(), ~ sum(is.na(.)))) %>%
  pivot_longer(everything(), names_to = "variable", values_to = "n_missing") %>%
  mutate(pct_missing = round(100 * n_missing / nrow(df), 1)) %>%
  arrange(desc(n_missing)) %>%
  print()

cat("\n--- Skim ---\n")
print(skim(df))

# ---------------------------------------------------------------------------
# 3. Normality Assessment
# ---------------------------------------------------------------------------
num_vars <- setdiff(names(df)[sapply(df, is.numeric)], "Diabetes")

normality <- tibble::tibble()
for (v in num_vars) {
  vals <- na.omit(df[[v]])
  n <- length(vals)
  if (n >= 3 && n <= 5000) {
    pval <- stats::shapiro.test(vals)$p.value
    is_norm <- pval > 0.05
  } else {
    pval <- NA
    is_norm <- FALSE
  }
  normality <- dplyr::bind_rows(normality, tibble::tibble(
    variable = v, n = n, shapiro_p = pval, is_normal = is_norm
  ))
}
cat("\n--- Normality (Shapiro-Wilk) ---\n")
print(normality)

# ---------------------------------------------------------------------------
# 4. Univariate Analysis — Plots
# ---------------------------------------------------------------------------
# Numeric: histogram + boxplot
for (v in num_vars) {
  p_hist <- ggplot(df, aes_string(x = v)) +
    geom_histogram(bins = 30, fill = "steelblue", color = "white", alpha = 0.8) +
    theme_minimal() +
    labs(title = paste("Distribution of", v), x = v, y = "Count")
  
  p_box <- ggplot(df, aes_string(y = v)) +
    geom_boxplot(fill = "steelblue", alpha = 0.6, outlier.color = "red") +
    theme_minimal() +
    labs(title = paste("Boxplot of", v), x = "", y = v)
  
  ggsave(paste0("plots/uni_hist_", v, ".png"), p_hist, width = 6, height = 4, dpi = 150)
  ggsave(paste0("plots/uni_box_", v, ".png"), p_box, width = 6, height = 4, dpi = 150)
}

# Categorical: bar charts
cat_vars <- setdiff(names(df)[sapply(df, function(x) is.factor(x) || is.character(x))], "Diabetes")
for (v in cat_vars) {
  p_bar <- df %>%
    count(.data[[v]]) %>%
    mutate(pct = scales::percent(n / sum(n), accuracy = 0.1)) %>%
    ggplot(aes(x = .data[[v]], y = n, fill = .data[[v]])) +
    geom_col(show.legend = FALSE) +
    geom_text(aes(label = paste0(n, " (", pct, ")")), vjust = -0.3, size = 3) +
    theme_minimal() +
    labs(title = paste("Distribution of", v), x = v, y = "Count")
  
  ggsave(paste0("plots/uni_bar_", v, ".png"), p_bar, width = 6, height = 4, dpi = 150)
}

# ---------------------------------------------------------------------------
# 5. Bivariate Analysis — gtsummary Table
# ---------------------------------------------------------------------------
build_stat_list <- function(data, outcome) {
  num_vars <- setdiff(names(data)[sapply(data, is.numeric)], outcome)
  lst <- list()
  for (v in num_vars) {
    vals <- na.omit(data[[v]])
    n <- length(vals)
    if (n >= 3 && n <= 5000) {
      is_norm <- stats::shapiro.test(vals)$p.value > 0.05
    } else {
      is_norm <- FALSE
    }
    lst[[v]] <- if (is_norm) "{mean} ({sd})" else "{median} ({p25}, {p75})"
  }
  lst
}

build_test_list <- function(data, outcome) {
  num_vars <- setdiff(names(data)[sapply(data, is.numeric)], outcome)
  cat_vars <- setdiff(names(data)[sapply(data, function(x) is.factor(x) || is.character(x))], outcome)
  lst <- list()
  n_out <- nlevels(data[[outcome]])
  for (v in num_vars) {
    vals <- na.omit(data[[v]])
    n <- length(vals)
    if (n >= 3 && n <= 5000) {
      is_norm <- stats::shapiro.test(vals)$p.value > 0.05
    } else {
      is_norm <- FALSE
    }
    test_name <- if (is_norm) {
      if (n_out == 2) "t.test" else "aov"
    } else {
      if (n_out == 2) "wilcox.test" else "kruskal.test"
    }
    # as.formula with quoted RHS so broom.helpers sees a character literal
    lst[[v]] <- as.formula(paste0(v, ' ~ "', test_name, '"'))
  }
  for (v in cat_vars) {
    tab <- table(data[[v]], data[[outcome]], useNA = "ifany")
    if (any(stats::chisq.test(tab)$expected < 5, na.rm = TRUE)) {
      test_name <- "fisher.test"
    } else {
      test_name <- "chisq.test"
    }
    lst[[v]] <- as.formula(paste0(v, ' ~ "', test_name, '"'))
  }
  lst
}

stat_list <- build_stat_list(df, "Diabetes")
test_forms <- build_test_list(df, "Diabetes")

bivariate_tbl <- df %>%
  tbl_summary(
    by = "Diabetes",
    statistic = stat_list,
    missing = "ifany",
    missing_text = "Missing"
  ) %>%
  add_overall() %>%
  add_p(test = test_forms) %>%
  bold_labels()

print(bivariate_tbl)

# Save as HTML
bivariate_tbl %>% as_gt() %>% gt::gtsave("bivariate_table.html")

# ---------------------------------------------------------------------------
# 6. Bivariate Plots
# ---------------------------------------------------------------------------
# Numeric: violin + boxplot + jitter
for (v in num_vars) {
  p <- ggplot(df, aes(x = Diabetes, y = .data[[v]], fill = Diabetes)) +
    geom_violin(alpha = 0.5, trim = FALSE) +
    geom_boxplot(width = 0.15, alpha = 0.8, outlier.shape = NA) +
    geom_jitter(width = 0.2, alpha = 0.3, size = 0.8) +
    ggplot2::scale_fill_brewer(palette = "Set2") +
    theme_minimal() +
    labs(title = paste("Distribution of", v, "by Diabetes"),
         x = "Diabetes", y = v)
  
  ggsave(paste0("plots/biv_", v, "_vs_Diabetes.png"), p, width = 7, height = 5, dpi = 150)
}

# Categorical: stacked proportion bars
for (v in cat_vars) {
  p <- df %>%
    dplyr::count(Diabetes, .data[[v]]) %>%
    dplyr::group_by(Diabetes) %>%
    dplyr::mutate(prop = n / sum(n)) %>%
    ggplot(aes(x = Diabetes, y = prop, fill = .data[[v]])) +
    geom_col(position = "fill", color = "white") +
    ggplot2::scale_fill_brewer(palette = "Set2") +
    theme_minimal() +
    labs(title = paste("Proportion of", v, "by Diabetes"),
         x = "Diabetes", y = "Proportion", fill = v)
  
  ggsave(paste0("plots/biv_", v, "_vs_Diabetes.png"), p, width = 7, height = 5, dpi = 150)
}

cat("\n--- Analysis Complete ---\n")
cat("Plots saved to 'plots/' directory\n")
cat("Bivariate table saved to 'bivariate_table.html'\n")
