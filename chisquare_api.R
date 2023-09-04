library(plumber)

# Define the Chi-Square function
chi_square_test <- function(observed, expected) {
  chi_sq <- sum(((observed - expected)^2) / expected)
  p_value <- 1 - pchisq(chi_sq, df = length(observed) - 1)
  return(list(chi_square = chi_sq, p_value = p_value))
}

# Create a plumber API
pr <- plumber::plumber()

# Define the API endpoint
pr$register(
  "/chisquare",
  methods = "POST",
  function(req, res) {
    data <- req$postBody
    observed <- data$observed
    expected <- data$expected
    
    # Perform the Chi-Square test
    result <- chi_square_test(observed, expected)
    
    # Return the result as JSON
    res$setHeader("Content-Type", "application/json")
    return(toJSON(result))
  }
)

# Run the API
#pr$run(port = 8000)


