# TACTIX AI – Football Tactical Intelligence System

## Overview

TACTIX AI is a machine learning based football analytics platform designed to transform raw match data into tactical insights and predictive intelligence. The system analyzes historical football match statistics and engineered tactical features to predict match outcomes, estimate expected goals (xG), and provide interactive analytical dashboards for deeper exploration of team and match performance.

The project is built using the European Soccer Database and combines machine learning, data engineering, and interactive visualization to create a professional football intelligence platform.

---

## Objectives

The primary objectives of TACTIX AI are:

- Predict football match outcomes using historical tactical data
- Estimate expected goals for home and away teams
- Analyze team performance using tactical indicators
- Compare teams using statistical and visual dashboards
- Explore historical matches and dataset trends
- Demonstrate practical applications of machine learning in sports analytics

---

## Core Features

### Match Prediction
Generate predictions for football matches using tactical input metrics such as form, attack strength, and defensive capability.

### Tactical Analysis
Visualize team strengths and weaknesses through radar charts, bar comparisons, and tactical summaries.

### Team Comparison
Compare two teams based on goals scored, attack metrics, defensive strength, and recent form.

### Match Explorer
Select teams and inspect historical matches between them with detailed match statistics.

### Dataset Analytics
Explore goal distributions, feature relationships, form trends, and dataset-wide patterns.

### Model Insights
Understand the machine learning architecture, feature relevance, and statistical behavior of input variables.

### Batch Predictions
Upload CSV datasets and generate predictions for multiple matches simultaneously.

---

## Machine Learning Models Used

TACTIX AI integrates multiple machine learning approaches:

- Logistic Regression
- Random Forest
- XGBoost
- Neural Networks (TensorFlow / Keras)

These models are used for:

- Match outcome prediction
- Expected goals estimation
- Tactical pattern recognition

---

## Dataset

The project uses the [**European Soccer Database**](https://www.kaggle.com/datasets/hugomathien/soccer) , containing historical football match data across multiple European leagues.

Feature engineering was performed to create tactical indicators such as:

- Home form
- Away form
- Attack strength
- Defensive strength
- Goal difference
- Derived comparative metrics

---

## Technology Stack

### Programming Language
- Python

### Data Processing
- Pandas
- NumPy

### Machine Learning
- Scikit-learn
- XGBoost
- TensorFlow / Keras

### Visualization
- Plotly
- Matplotlib

### Web Application
- Streamlit

### Deployment
- Docker
- Streamlit Community Cloud

---

## Project Structure

```text
TACTIX-AI
│
├── Dockerfile
├── requirements.txt
├── README.md
│
├── data
│   └── processed
│       └── match_features.csv
│
├── source
│   ├── engine
│   │   └── tactix_prediction_engine.py
│   ├── features
│   └── models
│
└── frontend
    ├── tactix.py
    └── pages
        ├── 1_Match_Prediction.py
        ├── 2_Tactical_Analysis.py
        ├── 3_Team_Comparison.py
        ├── 4_Match_Explorer.py
        ├── 5_Dataset_Analytics.py
        ├── 6_Model_Insights.py
        └── 7_Batch_Predictions.py

```
## Running the Project Locally 
### Clone the Repo 
```Bash
git clone https://github.com/arvindmatharoo/TACTIX-AI
cd TACTIX-AI
```
### Install the Dependencies 
```Bash
pip install -r requirements.txt
```
### Run app
```Bash
streamlit run frontend/tactix.py
```

## Running with Docker 

### Build Docker Image 
```Bash
docker build -t tactix-ai
```

### Run container 
```Bash
docker run -p 8501:8501 tactix-ai
```


## Live Deployment 
The deployed web application is available at : [LINK](https://tactix-ai.streamlit.app/)

## Use Cases
It can be useful for : 
- Football analysts
- Sports data enthusiasts
- Machine learning portfolio demonstrations
- Tactical performance evaluation
- Educational projects in sports analytics

## Future Enhancements

Potential Future improvements include: 
- Live match data integration
- League standings analytics
- Player-level analytics
- Match momentum visualizations
- Team ranking systems
- Mobile application deployment
- Advanced explainable AI modules

