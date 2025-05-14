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
    """Credit Risk Model Documentation

1. Introduction
Default risk represents the possibility that a borrower fails to meet debt repayment obligations. Accurately predicting default risk enables financial institutions to minimize financial losses. This project developed a credit risk model to predict 12-month loan default probabilities using machine learning, leveraging applicant background and credit history data to support loan approval decisions. The model prioritizes recall to reduce losses from missed defaults, achieving over 80% default detection with 98% overall accuracy.

2. Dataset
The dataset comprises 300,000 loan application records merged across eight data sources, including application details (loan and applicant information) and credit history (e.g., bureau and credit card balances). Only 8% of records indicate defaults (label ‘1’), reflecting a highly imbalanced dataset. Features include 122 variables, such as EXT_SOURCE_2 (external credit score), AMT_INCOME_TOTAL (client income), DAYS_REGISTRATION (days since registration change), and living region population. Extensive preprocessing was required to aggregate records and address data quality issues.

3. Evaluation Metrics
Due to the imbalanced dataset (1:10 default-to-non-default ratio), recall and AUC-ROC were selected as primary evaluation metrics. Recall was prioritized to minimize financial losses from undetected defaults, as misclassifying a default case incurs greater costs than rejecting a viable applicant. AUC-ROC assesses the model’s ability to distinguish defaults from non-defaults, ensuring balanced performance without overly sacrificing precision through threshold adjustments.

4. Data Pre-processing
4.1 Missing Values
Significant missing values were observed, particularly in applicant accommodation features. To address this, rows with over 10% missing values, missing target labels, or undocumented columns were removed to improve model accuracy.

4.2 Feature Distribution
Numerical features, such as AMT_ANNUITY and living area, exhibited skewness. Standardization (using a robust scaler to handle outliers) and L2 normalization were applied to enhance model convergence.

4.3 Feature Correlation
High correlations were detected among features, such as number of children and family members. Correlated features were evaluated for removal to reduce redundancy and improve model performance.

4.4 Joining Data Sources
Data sources were merged using the SK_ID_CURR column (loan ID) via left outer joins, with the application data as the primary source, ensuring all relevant loan and credit history information was integrated.

4.5 One-Hot Encoding
Categorical features were one-hot encoded using pandas’ get_dummies() function to convert non-numerical data into a numerical format suitable for model training, except for LightGBM, which natively handles categorical data.

4.6 Aggregation
Remaining features were aggregated by calculating mean values using pandas’ agg() function, ensuring consistency across training data and preserving common patterns.

4.7 Stratified Train-Test Splitting
The dataset was split into 80% training and 20% testing sets using stratified sampling to maintain the 2:8 default-to-non-default ratio, addressing the imbalance in the test set.

5. Models
The project evaluated four models: Logistic Regression, Random Forest, LightGBM, and DeepFM. LightGBM was selected as the best model due to its high recall (0.8296), strong AUC-ROC (0.9448), and faster training time compared to DeepFM.

5.1 Logistic Regression
Logistic Regression, a binary classification model using a sigmoid function, underperformed with a recall of 0.3116 and AUC-ROC of 0.85. Hyperparameter tuning (C from 0.01 to 100) indicated under-fitting, with the best C at 100, suggesting no regularization was needed.

5.2 Random Forest
Random Forest, an ensemble of decision trees using bagging, achieved the highest AUC-ROC (0.9836) but a lower recall (0.7907). Hyperparameters were tuned: max_depth=40, min_sample_split=0.78, n_estimators=20. Its high AUC was attributed to imbalanced data, inflating false positives. Key features included EXT_SOURCE_2, DAYS_REGISTRATION, AMT_INCOME_TOTAL, and DAYS_ID_PUBLISH.

5.3 LightGBM
LightGBM, a gradient boosting model with leaf-wise tree growth and second-order gradient optimization, excelled with an AUC-ROC of 0.9448, recall of 0.8296 (at a 0.1 threshold), and 93% accuracy. K-fold cross-validation and Bayesian optimization tuned hyperparameters (e.g., max_depth, subsample, learning rate). Early stopping prevented overfitting. Key features included AMT_INCOME_TOTAL and living region population, aligning with intuitive creditworthiness factors.

5.4 DeepFM
DeepFM, combining factorization machines and a neural network for feature interactions, achieved a recall of 0.8326 but a lower AUC-ROC (0.8492). Using a 0.5 threshold and cross-entropy loss, it was computationally intensive and less effective than LightGBM for this task.

6. Conclusion
The credit risk model, leveraging LightGBM, effectively predicts loan defaults, achieving a recall of 0.8296 and AUC-ROC of 0.9448 despite challenges from imbalanced and high-dimensional data. Key features like higher income, longer registration duration, and comprehensive documentation reduce default likelihood, offering actionable insights for creditworthiness assessment. Limitations include suboptimal feature engineering, as uniform one-hot encoding was applied despite LightGBM’s native categorical feature support, and potential performance degradation in economic downturns. Future improvements include optimizing categorical feature handling and enhancing monitoring for economic shifts to ensure robust performance."""
]


for text in analysis_data:
    knowledge_base.load_text(text)

print("Knowledge base populated with credit risk model documentation.")