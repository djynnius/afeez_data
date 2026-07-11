library(gtsummary)
library(dplyr)

# Simple test dataframe
df2 <- structure(list(
  Age = c(34, 26, 49, 35, 42, 45, 28, 19),
  Diabetes = factor(c("No","No","No","No","Yes","No","No","No"))
), class = "data.frame", row.names = c(NA, -8L))

# Test formula with quoted string RHS
f <- as.formula('Age ~ "t.test"')
cat("RHS class:", class(f[[3]]), "\n")

tryCatch({
  tbl2 <- df2 %>% 
    tbl_summary(by = Diabetes) %>%
    add_p(test = list(f))
  print(tbl2)
  cat("SUCCESS\n")
}, error = function(e) { 
  cat("ERROR:", e$message, "\n") 
})
