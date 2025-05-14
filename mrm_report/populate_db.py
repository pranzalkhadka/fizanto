from agno.vectordb.lancedb import LanceDb
from agno.embedder.fastembed import FastEmbedEmbedder
from agno.agent import Agent, AgentKnowledge
import os

os.makedirs("tmp_app/lancedb", exist_ok=True)

knowledge_base = AgentKnowledge(
    vector_db=LanceDb(
        uri="tmp_app/lancedb",
        table_name="data_memory",
        embedder=FastEmbedEmbedder(id="BAAI/bge-small-en-v1.5")
    )
)

analysis_data = [
    """
    Credit Risk Model Documentation
Date: May 14, 2024
Version: 1.0

1. Introduction
Default risk, the likelihood that a borrower fails to repay a loan, is a critical concern for financial institutions managing a $500M consumer lending portfolio. This credit risk model predicts 12-month loan default probabilities using LightGBM, a gradient boosting framework, to support loan approval decisions. The model prioritizes recall (0.8296 at a 0.1 threshold) to minimize financial losses from undetected defaults, achieving an AUC-ROC of 0.9448 and 93 percent accuracy on a 300,000-record dataset. Validation in Q1 2025 ensures compliance with SR 11-7 and OCC 2011-12, focusing on conceptual soundness, fairness, and governance. The model integrates applicant background (e.g., income, registration duration) and credit history (e.g., bureau records) to assess creditworthiness, aligning with regulatory expectations for high-risk models.

2. Dataset
The dataset comprises 300,000 loan application records merged across eight data sources: application data (loan and applicant details), bureau (credit history), bureau balance (monthly credit updates), previous applications, POS cash balance, credit card balance, instalment payments, and aggregated features. Only 8 percent of records indicate defaults (label ‘1’), reflecting a 1:10 imbalanced ratio. The dataset includes 122 features, such as:
- EXT_SOURCE_2: External credit score (high values reduce default risk).
- AMT_INCOME_TOTAL: Client income (key for repayment ability).
- DAYS_REGISTRATION: Days since registration change (indicates stability).
- AMT_ANNUITY: Loan annuity amount.
- REGION_POPULATION_RELATIVE: Regional population density.
Data quality issues, including missing values (up to 30 percent in accommodation features) and high feature correlations, necessitated extensive preprocessing.

3. Evaluation Metrics
Given the imbalanced dataset, recall and AUC-ROC are primary metrics. Recall (0.8296) ensures over 80 percent of defaults are detected, minimizing losses from false negatives, which cost $10,000 per missed default on average. AUC-ROC (0.9448) measures discriminatory power, ensuring balanced performance. Precision (0.65 at 0.1 threshold) is secondary, as false positives (rejected viable applicants) have lower financial impact ($2,000 per case). Threshold optimization used a cost-benefit analysis, setting 0.1 to maximize recall while maintaining acceptable precision.

4. Data Preprocessing
4.1 Missing Values
Missing values were significant, particularly in accommodation features (e.g., WALLSMATERIAL_MODE, 30% missing). Rows with >10% missing values, missing labels, or undocumented columns were removed, reducing the dataset by 5%. Mean imputation was applied to numerical features with <10% missingness (e.g., AMT_ANNUITY).

4.2 Feature Distribution
Numerical features (e.g., AMT_ANNUITY, living area) exhibited skewness (skew > 1.5). A robust scaler standardized features, handling outliers (e.g., income > $1M). L2 normalization ensured consistent scales, improving LightGBM convergence.

4.3 Feature Correlation
High correlations (phi-k > 0.7) were observed, e.g., between CNT_CHILDREN and CNT_FAM_MEMBERS. Correlated features were evaluated using variance inflation factor (VIF > 5), removing 10 redundant features (e.g., CNT_FAM_MEMBERS) to reduce multicollinearity.

4.4 Joining Data Sources
Eight tables were merged using SK_ID_CURR (loan ID) via left outer joins, with application data as the primary table. Aggregation used mean values for numerical features (e.g., credit card balance) and mode for categorical features, ensuring consistency.

4.5 One-Hot Encoding
Categorical features (e.g., NAME_CONTRACT_TYPE, ORGANIZATION_TYPE) were one-hot encoded using pandas’ get_dummies(), adding 50 binary columns. LightGBM’s native categorical handling was tested but not used for consistency across model comparisons.

4.6 Stratified Train-Test Split
An 80/20 train-test split maintained the 2:8 default-to-non-default ratio using stratified sampling, ensuring representative test performance.

5. Model Development
LightGBM was selected after evaluating Logistic Regression, Random Forest, and DeepFM. It achieved the best balance of recall (0.8296), AUC-ROC (0.9448), and training efficiency (2 hours vs. 10 hours for DeepFM).

5.1 Logistic Regression
Logistic Regression underperformed (recall: 0.3116, AUC-ROC: 0.85). Hyperparameter tuning (C: 0.01–100) selected C=100, indicating underfitting. Key features included EXT_SOURCE_2 and AMT_INCOME_TOTAL.

5.2 Random Forest
Random Forest achieved a high AUC-ROC (0.9836) but lower recall (0.7907). Tuned hyperparameters: max_depth=40, min_sample_split=0.78, n_estimators=20. High AUC was inflated by imbalanced data, increasing false positives.

5.3 LightGBM
LightGBM used leaf-wise tree growth and second-order gradient optimization. Bayesian optimization tuned max_depth=7, learning_rate=0.05, subsample=0.8 over 100 iterations. K-fold cross-validation (5 folds) and early stopping prevented overfitting. Results: AUC-ROC=0.9448, recall=0.8296, accuracy=0.93. Top features: AMT_INCOME_TOTAL, EXT_SOURCE_2, DAYS_REGISTRATION.

5.4 DeepFM
DeepFM, combining factorization machines and a neural network, achieved recall=0.8326 but AUC-ROC=0.8492. Using a 0.5 threshold and cross-entropy loss, it was computationally intensive (10 hours training).

6. Validation Methodology
Validation followed SR 11-7 guidelines, combining qualitative and quantitative methods. An independent team conducted:
- **Qualitative Review**: Assessed LightGBM’s documentation, assumptions (e.g., feature independence), and governance.
- **Quantitative Testing**: K-fold CV (5 folds), backtesting on 20% test set, and fairness checks. Results:

For Fold 1 :-
	AUC-ROC :- 0.9450
	Recall :- 0.8300
	Accuracy :-0.932
	
For Fold 2 :-
	AUC-ROC :- 0.9445
	Recall :- 0.8290
	Accuracy :-0.931
 
- **Fairness Analysis**: Evaluated bias in low-income (<$30,000) and regional (rural vs. urban) applicants, finding 5 percent higher false positives in low-income groups.
- **Stress Testing**: Simulated a 20 percent income drop and 2 percent interest rate hike, reducing recall to 0.75.

7. Governance Framework
The model is governed by the MRM Committee, comprising risk, data science, and compliance teams. Key processes:
- **Approval**: Model approved on 12/15/2024 after independent review.
- **Independent Validation**: Conducted by a third-party team in Q1 2025, ensuring no conflicts of interest.
- **Monitoring**: Quarterly reviews track AUC-ROC, recall, and fairness metrics. Drift detection monitors input distributions (e.g., AMT_INCOME_TOTAL shifts >10%).

8. Stress Testing
Stress tests simulated economic downturns:
- **Scenario 1: Recession**: 20 percent income drop reduced recall to 0.75, AUC-ROC to 0.90.
- **Scenario 2: Rate Hike**: 2 percent interest rate increase lowered recall to 0.78.
Recommendations include retraining with stressed data by Q3 2025.

9. Fairness Analyses
Fairness checks assessed bias across income and region:
- **Low-Income Applicants**: 5 percent higher false positives, mitigated by adjusting EXT_SOURCE_2 weights.
- **Rural vs. Urban**: No significant bias (p-value > 0.05 in chi-square test).
Mitigation strategies include fairness constraints in retraining.

10. Monitoring Plans
Continuous monitoring tracks:
- **Performance Metrics**: AUC-ROC, recall, precision (threshold=0.1).
- **Input Drift**: Kolmogorov-Smirnov tests detect shifts in EXT_SOURCE_2, AMT_INCOME_TOTAL.
- **Retraining Triggers**: Recall drop below 0.80 or drift p-value < 0.01.
Dashboards visualize metrics, updated weekly.

11. Validation Logs
- **K-Fold CV Logs**: 5 folds, 100 iterations, average runtime 30 minutes.
- **Hyperparameter Tuning**: Bayesian optimization logs (max_depth, learning_rate).
- **Backtesting**: Out-of-time testing on 2024 Q4 data, recall=0.82.
- **Fairness Logs**: Demographic bias tests, mitigation steps.

12. Feature-Level Analyses
For each of 122 features, we provide:
- **Description**: E.g., EXT_SOURCE_2 (external credit score, range 0–1).
- **Importance**: SHAP values (e.g., EXT_SOURCE_2: 0.25).
- **Distribution**: Skewness, missingness (e.g., 5% missing for AMT_ANNUITY).
- **Role**: E.g., AMT_INCOME_TOTAL indicates repayment capacity.

Example:
| Feature             | SHAP Value | Missingness | Skewness | Role                              |
| EXT_SOURCE_2      | 0.25       | 2%          | 0.3      | Higher scores reduce default risk |
| AMT_INCOME_TOTAL  | 0.20       | 1%          | 1.8      | Indicates repayment capacity      |

13. Conclusion
The LightGBM model effectively predicts defaults (recall=0.8296, AUC-ROC=0.9448) despite imbalanced, high-dimensional data. Limitations include suboptimal one-hot encoding and economic sensitivity. Recommendations:
- Optimize categorical feature handling by Q3 2025.
- Enhance monitoring for economic downturns.
- Retrain with fairness constraints for low-income applicants.

14. References
- SR 11-7: Guidance on Model Risk Management, Federal Reserve, 2011.
- OCC 2011-12: Sound Practices for Model Risk Management.
- Chen et al. (2013). Logistic Regression for P2P Lending.
- Xu et al. (2021). XGBoost for Loan Repayment Analysis.
"""
]

# analysis_data = [
#     """Credit Risk Model Documentation

# 1. Introduction
# Default risk represents the possibility that a borrower fails to meet debt repayment obligations. Accurately predicting default risk enables financial institutions to minimize financial losses. This project developed a credit risk model to predict 12-month loan default probabilities using machine learning, leveraging applicant background and credit history data to support loan approval decisions. The model prioritizes recall to reduce losses from missed defaults, achieving over 80% default detection with 98% overall accuracy.

# 2. Dataset
# The dataset comprises 300,000 loan application records merged across eight data sources, including application details (loan and applicant information) and credit history (e.g., bureau and credit card balances). Only 8% of records indicate defaults (label ‘1’), reflecting a highly imbalanced dataset. Features include 122 variables, such as EXT_SOURCE_2 (external credit score), AMT_INCOME_TOTAL (client income), DAYS_REGISTRATION (days since registration change), and living region population. Extensive preprocessing was required to aggregate records and address data quality issues.

# 3. Evaluation Metrics
# Due to the imbalanced dataset (1:10 default-to-non-default ratio), recall and AUC-ROC were selected as primary evaluation metrics. Recall was prioritized to minimize financial losses from undetected defaults, as misclassifying a default case incurs greater costs than rejecting a viable applicant. AUC-ROC assesses the model’s ability to distinguish defaults from non-defaults, ensuring balanced performance without overly sacrificing precision through threshold adjustments.

# 4. Data Pre-processing
# 4.1 Missing Values
# Significant missing values were observed, particularly in applicant accommodation features. To address this, rows with over 10% missing values, missing target labels, or undocumented columns were removed to improve model accuracy.

# 4.2 Feature Distribution
# Numerical features, such as AMT_ANNUITY and living area, exhibited skewness. Standardization (using a robust scaler to handle outliers) and L2 normalization were applied to enhance model convergence.

# 4.3 Feature Correlation
# High correlations were detected among features, such as number of children and family members. Correlated features were evaluated for removal to reduce redundancy and improve model performance.

# 4.4 Joining Data Sources
# Data sources were merged using the SK_ID_CURR column (loan ID) via left outer joins, with the application data as the primary source, ensuring all relevant loan and credit history information was integrated.

# 4.5 One-Hot Encoding
# Categorical features were one-hot encoded using pandas’ get_dummies() function to convert non-numerical data into a numerical format suitable for model training, except for LightGBM, which natively handles categorical data.

# 4.6 Aggregation
# Remaining features were aggregated by calculating mean values using pandas’ agg() function, ensuring consistency across training data and preserving common patterns.

# 4.7 Stratified Train-Test Splitting
# The dataset was split into 80% training and 20% testing sets using stratified sampling to maintain the 2:8 default-to-non-default ratio, addressing the imbalance in the test set.

# 5. Models
# The project evaluated four models: Logistic Regression, Random Forest, LightGBM, and DeepFM. LightGBM was selected as the best model due to its high recall (0.8296), strong AUC-ROC (0.9448), and faster training time compared to DeepFM.

# 5.1 Logistic Regression
# Logistic Regression, a binary classification model using a sigmoid function, underperformed with a recall of 0.3116 and AUC-ROC of 0.85. Hyperparameter tuning (C from 0.01 to 100) indicated under-fitting, with the best C at 100, suggesting no regularization was needed.

# 5.2 Random Forest
# Random Forest, an ensemble of decision trees using bagging, achieved the highest AUC-ROC (0.9836) but a lower recall (0.7907). Hyperparameters were tuned: max_depth=40, min_sample_split=0.78, n_estimators=20. Its high AUC was attributed to imbalanced data, inflating false positives. Key features included EXT_SOURCE_2, DAYS_REGISTRATION, AMT_INCOME_TOTAL, and DAYS_ID_PUBLISH.

# 5.3 LightGBM
# LightGBM, a gradient boosting model with leaf-wise tree growth and second-order gradient optimization, excelled with an AUC-ROC of 0.9448, recall of 0.8296 (at a 0.1 threshold), and 93% accuracy. K-fold cross-validation and Bayesian optimization tuned hyperparameters (e.g., max_depth, subsample, learning rate). Early stopping prevented overfitting. Key features included AMT_INCOME_TOTAL and living region population, aligning with intuitive creditworthiness factors.

# 5.4 DeepFM
# DeepFM, combining factorization machines and a neural network for feature interactions, achieved a recall of 0.8326 but a lower AUC-ROC (0.8492). Using a 0.5 threshold and cross-entropy loss, it was computationally intensive and less effective than LightGBM for this task.

# 6. Conclusion
# The credit risk model, leveraging LightGBM, effectively predicts loan defaults, achieving a recall of 0.8296 and AUC-ROC of 0.9448 despite challenges from imbalanced and high-dimensional data. Key features like higher income, longer registration duration, and comprehensive documentation reduce default likelihood, offering actionable insights for creditworthiness assessment. Limitations include suboptimal feature engineering, as uniform one-hot encoding was applied despite LightGBM’s native categorical feature support, and potential performance degradation in economic downturns. Future improvements include optimizing categorical feature handling and enhancing monitoring for economic shifts to ensure robust performance."""
# ]


for text in analysis_data:
    knowledge_base.load_text(text)

print("Knowledge base populated with credit risk model documentation.")