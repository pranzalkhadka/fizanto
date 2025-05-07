# Lending Club Credit Risk Model Summary

## Model Overview
- **Model Type**: Gradient Boosting Classifier
- **Purpose**: Predict probability of loan default for credit decisioning
- **Target Variable**: Binary (Default/Non-Default)
- **Primary Use Case**: Automated credit risk assessment for personal loans
- **Data Size**: 300 samples

## Model Architecture
- **Algorithm**: Gradient Boosting Decision Trees
- **Implementation**: scikit-learn GradientBoostingClassifier
- **Key Parameters**:
  - n_estimators: 100
  - max_depth: 5
  - learning_rate: 0.1
  - min_samples_split: 200
  - random_state: 42

## Features Used

### Numeric Features
- Log-transformed Annual Income
- Log-transformed Loan Amount
- Debt-to-Income Ratio
- FICO Score

### Categorical Features
- Term (36/60 months)
- Grade (A-G)
- Home Ownership (RENT/MORTGAGE/OWN)
- Loan Purpose
- FICO Category (Very Poor/Fair/Good/Very Good/Excellent)
- DTI Category (Very Low/Low/Moderate/High/Very High)

## Feature Engineering
1. **Log Transformations**:
   - Applied to annual_income to handle income distribution skew
   - Applied to loan_amount to normalize loan size distribution

2. **Categorical Binning**:
   - FICO scores binned into risk categories
   - DTI ratios binned into risk levels

3. **Feature Scaling**:
   - Standard scaling applied to all numeric features
   - One-hot encoding for categorical features

## Data Processing
- Missing values handled in employment length
- Invalid records removed (DTI > 150, income ≤ 0, loan amount ≤ 0)
- 80/20 train-test split with random_state=42

## Model Training
- Training samples: 240 (80%)
- Test samples: 60 (20%)
- Features after one-hot encoding: Numeric (4) + Categorical one-hot features
- Target: loan_status (Default=1, Fully Paid=0)

## Model Validation
- Random split validation (no time-based validation due to data limitations)
- Performance evaluated on held-out test set
- Feature importance analysis performed

## Implementation Requirements
- Python 3.8+
- Required packages:
  * pandas
  * numpy
  * scikit-learn
  * matplotlib
  * seaborn

## Usage Notes
1. Data Preprocessing:
   - Apply same transformations as training
   - Use saved scaler for numeric features
   - Maintain same one-hot encoding structure

2. Model Input:
   - Expects features in same order as training
   - Numeric features must be scaled
   - Categorical features must be one-hot encoded

3. Model Output:
   - Probability of default (0-1)
   - Binary prediction (Default/Non-Default)

## Limitations
1. Small sample size (300 records)
2. Limited to approved loans only
3. No temporal validation due to data constraints
4. Binary classification may oversimplify risk
5. Limited feature set compared to full lending data

## Future Improvements
1. Increase training data size
2. Add additional relevant features
3. Implement temporal validation
4. Consider ordinal encoding for grades
5. Explore model interpretability tools

## Version Information
- Model Version: 1.0
- Last Updated: February 2025
- Status: Development
