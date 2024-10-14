Instagram Reach Prediction Model 
This project aims to predict Instagram post reach based on a variety of features related to user 
activity, engagement, and profile metrics. The dataset includes features such as likes, comments, 
hashtags, and user bios, which have been processed and used to train different machine learning 
models. 
Project Structure 
INSTAGRAM_REACH_ANALYSIS:FOOD_BLOGGERS/ 
             Dataset_Creation_Report.pdf 
             Jupyter_Notebook_Report.pdf 
      data 
            Food_bloggers.csv 
            Instagram_data.csv     
     src 
            Food_bloggers.py         
            web_scraping.py        
            csv_convertor.py             
     README.md                         
      requirements.txt                 
Key Features of the Project 
1. Data Preprocessing: Cleaning missing values, removing unnecessary features, and scaling 
data for model training. 
2. Feature Engineering: Scaling numerical features, handling categorical features, and applying 
PCA for dimensionality reduction. 
3. Model Training: Multiple models were trained and tuned, including Random Forest, Linear 
Regression, Support Vector Machine (SVM), and Gradient Boosting. 
4. Hyperparameter Tuning: Grid search was used to optimize the parameters of the Random 
Forest and Gradient Boosting models. 
5. Model Evaluation: Models were evaluated using metrics such as MAE, MSE, RMSE, and R² to 
compare performance. 
Dependencies 
Install the required dependencies using: 
            pip install -r requirements.txt 
The project requires the following Python libraries: 
• pandas 
• numpy 
• scikit-learn 
• matplotlib 
• seaborn 
Data Preprocessing 
The dataset includes the following features: 
• Numerical: Likes, comments, followers count, engagement rate, etc. 
• Categorical: Hashtags, post content, etc. 
• Target: total_reach_estimated, representing the Instagram post reach. 
Steps: 
1. Missing values were handled using SimpleImputer (median strategy). 
2. Feature scaling was applied using StandardScaler. 
3. Dimensionality reduction was achieved via PCA, reducing the data to the most important 
components. 
Feature Engineering 
Unnecessary features such as post date, username, and post URL were removed. The remaining 
features were imputed, scaled, and prepared for model training. 
Model Training 
The following models were trained: 
1. Random Forest: Ensemble model tuned via grid search. 
2. Linear Regression: Baseline regression model. 
3. Support Vector Machine (SVM): A model with an RBF kernel. 
4. Gradient Boosting: Ensemble model that performed well in certain cases. 
Models were evaluated using: 
• MAE (Mean Absolute Error) 
• MSE (Mean Squared Error) 
• RMSE (Root Mean Squared Error) 
• R² Score 
Model Evaluation 
The best models were evaluated on the test dataset, and their performance was compared: 
• Random Forest: Achieved strong results with the lowest error rates. 
• Gradient Boosting: Performed comparably to Random Forest. 
• SVM and Linear Regression: Served as baseline models, but were outperformed by 
ensemble methods. 
Visualizations 
Key visualizations included: 
1. Model Comparison: RMSE comparison across all models using a box plot. 
2. Actual vs. Predicted Scatter Plot: Comparison of actual and predicted values for each model. 
3. Bar Charts for Evaluation Metrics: Bar charts showing MAE, RMSE, and R² scores for all 
models. 
Conclusion 
Random Forest and Gradient Boosting models showed the best performance for predicting Instagram 
reach. This project highlights the effectiveness of ensemble methods and the importance of 
hyperparameter tuning.
