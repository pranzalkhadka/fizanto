# Lending Club Data Preprocessing Steps

## 1. Data Cleaning

### Missing Value Treatment
```python
# Employment Length
if employment_length is null:
    fill with mode of employment_length
    flag_employment_length_imputed = 1

# Debt-to-Income
if dti is null and (stated_monthly_income is not null and total_monthly_debt is not null):
    dti = (total_monthly_debt / stated_monthly_income) * 100
else if dti is null:
    remove record

# FICO Score
if fico_score is null:
    remove record  # Critical feature, cannot impute
```

### Invalid Value Handling
```python
# Remove invalid DTI
remove if dti > 150

# Remove invalid income
remove if annual_income <= 0 or annual_income > 5000000

# Remove invalid loan amounts
remove if loan_amount <= 0 or loan_amount > 40000
```

## 2. Feature Engineering

### Credit Score Processing
```python
def process_fico_score(score):
    # Convert to ranges for privacy
    if score < 580:
        return 'Very Poor'
    elif score < 670:
        return 'Fair'
    elif score < 740:
        return 'Good'
    elif score < 800:
        return 'Very Good'
    else:
        return 'Excellent'
```

### Employment Length Categorization
```python
def categorize_employment(length):
    if length < 1:
        return 'Less than 1 year'
    elif length < 3:
        return '1-3 years'
    elif length < 5:
        return '3-5 years'
    elif length < 10:
        return '5-10 years'
    else:
        return '10+ years'
```

### Debt-to-Income Ratio Bucketing
```python
def bucket_dti(dti):
    if dti < 10:
        return 'Very Low'
    elif dti < 20:
        return 'Low'
    elif dti < 30:
        return 'Moderate'
    elif dti < 40:
        return 'High'
    else:
        return 'Very High'
```

### Purpose Category Consolidation
```python
purpose_mapping = {
    'debt_consolidation': 'Debt Consolidation',
    'credit_card': 'Debt Consolidation',
    'home_improvement': 'Home Improvement',
    'house': 'Home Improvement',
    'major_purchase': 'Major Purchase',
    'car': 'Major Purchase',
    'medical': 'Medical',
    'moving': 'Other',
    'vacation': 'Other',
    'wedding': 'Other',
    'small_business': 'Business',
    'other': 'Other'
}
```

## 3. Feature Transformations

### Numeric Features
```python
# Log transformation for skewed features
features_to_log = ['annual_income', 'loan_amount', 'total_credit_lines']

# Standard scaling
numeric_features = [
    'annual_income',
    'loan_amount',
    'dti',
    'total_credit_lines',
    'revolving_balance',
    'revolving_utilization'
]

scaler = StandardScaler()
X[numeric_features] = scaler.fit_transform(X[numeric_features])
```

### Categorical Features
```python
# One-hot encoding
categorical_features = [
    'term',
    'grade',
    'home_ownership',
    'purpose_category',
    'employment_length_category',
    'fico_category'
]

X = pd.get_dummies(X, columns=categorical_features, drop_first=True)
```

## 4. Target Variable Creation
```python
def create_default_target(status):
    default_statuses = [
        'Charged Off',
        'Default',
        'Late (31-120 days)',
        'Late (>120 days)'
    ]
    return 1 if status in default_statuses else 0
```

## 5. Data Validation Checks

### Pre-processing Checks
```python
def validate_input_data(df):
    assert df['annual_income'].min() > 0
    assert df['loan_amount'].min() > 0
    assert df['dti'].between(0, 150).all()
    assert not df['fico_score'].isnull().any()
```

### Post-processing Checks
```python
def validate_processed_data(df):
    # Check for nulls
    assert not df.isnull().any().any()
    
    # Check for infinite values
    assert not np.isinf(df.select_dtypes(include=np.number)).any().any()
    
    # Check feature ranges
    assert df[numeric_features].between(-5, 5).all().all()  # After scaling
```

## 6. Data Splitting Strategy

```python
def split_data(X, y):
    # Time-based split
    train_cutoff = '2017-12-31'
    val_cutoff = '2018-06-30'
    
    X_train = X[X['issue_date'] <= train_cutoff]
    X_val = X[(X['issue_date'] > train_cutoff) & (X['issue_date'] <= val_cutoff)]
    X_test = X[X['issue_date'] > val_cutoff]
    
    # Get corresponding target values
    y_train = y[X_train.index]
    y_val = y[X_val.index]
    y_test = y[X_test.index]
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)
```

## 7. Feature Storage

```python
# Save preprocessing artifacts
preprocessing_artifacts = {
    'scaler': scaler,
    'purpose_mapping': purpose_mapping,
    'categorical_features': categorical_features,
    'numeric_features': numeric_features
}

joblib.dump(preprocessing_artifacts, 'preprocessing_artifacts.joblib')
```

## Important Notes

1. All preprocessing steps must be applied consistently between training and inference
2. Preprocessing artifacts must be versioned with the model
3. Any changes to preprocessing steps require model retraining
4. Monitor feature distributions post-preprocessing for drift
5. Validate preprocessing output before model training
