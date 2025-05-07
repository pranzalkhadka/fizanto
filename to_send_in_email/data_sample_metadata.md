# Data Transformation Documentation

This document details the transformations applied to convert the raw Lending Club data into the golden dataset used for model training.

## Dataset Overview

- Raw Dataset: `lending_club_raw_data.csv` (300 samples)
- Golden Dataset: `lending_club_golden_data.csv` (300 samples)

## Transformations Applied

### 1. FICO Score Categorization
```python
# Convert numeric FICO scores to risk categories
df['fico_category'] = pd.cut(
    df['fico_score'], 
    bins=[0, 580, 670, 740, 800, 850],
    labels=['Very Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
)
```
Rationale:
- Industry-standard FICO score ranges
- Makes risk levels more interpretable
- Helps identify non-linear relationships

### 2. Debt-to-Income (DTI) Bucketing
```python
# Convert continuous DTI to risk buckets
df['dti_category'] = pd.cut(
    df['dti'],
    bins=[0, 10, 20, 30, 40, float('inf')],
    labels=['Very Low', 'Low', 'Moderate', 'High', 'Very High']
)
```
Rationale:
- Standard industry thresholds for DTI risk assessment
- Captures risk levels more effectively than raw ratios
- Aligns with underwriting guidelines

### 3. Log Transformations
```python
# Apply log transformation to handle skewed distributions
df['log_income'] = np.log1p(df['annual_income'])
df['log_loan_amount'] = np.log1p(df['loan_amount'])
```
Rationale:
- Normalizes heavily skewed financial data
- Reduces impact of outliers
- Improves model performance with normalized distributions

## Data Quality Checks

### Raw Data Validation
- No missing values in critical fields (FICO, DTI)
- All loan amounts > 0
- All annual incomes > 0
- DTI ratios <= 150%

### Golden Data Validation
- All categorical features properly encoded
- No missing values in engineered features
- Log transformations successfully applied
- Categories match expected distributions

## Feature Distributions

### Raw Features
- FICO Scores: Range 580-850, mean ~700
- DTI: Range 0-150%, mean ~25%
- Annual Income: Range $20k-$300k
- Loan Amount: Range $1k-$40k

### Engineered Features
- FICO Categories: 5 risk levels
- DTI Categories: 5 risk levels
- Log Income: Normalized distribution
- Log Loan Amount: Normalized distribution

## Usage Notes

### For Model Training
- Use golden dataset features
- Categorical features require one-hot encoding
- Numeric features should be scaled
- Target variable: loan_status (Default/Fully Paid)

### For Inference
1. Apply same transformations to new data:
   - FICO categorization
   - DTI bucketing
   - Log transformations
2. Validate transformed features match training distributions
3. Scale numeric features using training scaler

## Monitoring Considerations

### Data Drift Monitoring
- Track raw feature distributions
- Monitor category proportions
- Alert on significant distribution shifts

### Data Quality Monitoring
- Validate transformation outputs
- Check for unexpected categories
- Monitor missing value patterns

## Version Control

- Transformation code version: 1.0
- Last updated: February 2025
- Changes tracked in Git repository

## Dependencies

- Python 3.8+
- pandas
- numpy
- scikit-learn (for scaling)

## Contact

For questions about data transformations:
- Data Engineering Team
- Model Development Team
