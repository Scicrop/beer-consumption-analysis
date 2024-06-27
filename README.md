# Beer Consumption Analysis

This repository contains an analysis and predictive model for beer consumption in São Paulo, Brazil. The analysis leverages demographic, climatic, and event data to understand and predict beer consumption patterns.

## Overview

This project aims to predict beer consumption using a variety of factors, including:
- Demographic data
- Climatic conditions
- Events and holidays

The main objective is to provide a robust model that can predict beer consumption based on these variables.

## Dataset

The dataset used in this analysis includes the following features:
- **Date**: The date of the observation.
- **Average Temperature (C)**: The average temperature on the given day.
- **Minimum Temperature (C)**: The minimum temperature on the given day.
- **Maximum Temperature (C)**: The maximum temperature on the given day.
- **Precipitation (mm)**: The amount of rainfall on the given day.
- **Weekend**: Whether the day is a weekend (1) or not (0).
- **Beer Consumption (liters)**: The total beer consumption in liters.
- **Holiday Name**: The name of the holiday if the day is a holiday.
- **Is Holiday**: Whether the day is a holiday (1) or not (0).
- **Has Match**: Whether there was a sports match on the given day (1) or not (0).
- **Match Type**: The type of match if there was a match.
- **Is Corinthians, Is São Paulo, etc.**: Indicators for specific football teams.

## Tools and Libraries

- **Python**: Programming language used for the analysis.
- **Pandas**: Data manipulation and analysis library.
- **NumPy**: Library for numerical computations.
- **Matplotlib**: Plotting and visualization library.
- **Seaborn**: Statistical data visualization library.
- **Scikit-learn**: Machine learning library used for training and evaluation of models.

## Methodology

### Data Preparation

The data was cleaned and prepared by:
1. Loading the data from CSV files.
2. Handling missing values.
3. Converting columns to appropriate data types.
4. Creating dummy variables for categorical features.

### Exploratory Data Analysis (EDA)

EDA was performed to understand the relationships between the variables and beer consumption. Visualizations were created using Matplotlib and Seaborn.

### Feature Importance

Feature importance was analyzed using mutual information regression to determine which features had the most significant impact on beer consumption.

### Model Training

Several machine learning models were trained and evaluated, including:
- Linear Regression
- Decision Tree
- Random Forest
- Gradient Boosting

The Random Forest model was chosen for its balance of performance and interpretability.

### Evaluation

The models were evaluated using metrics such as Mean Squared Error (MSE) and R-squared. Visualizations were created to show the accuracy and error distribution of the predictions.

## Usage

### Running the Analysis

To run the analysis, clone this repository and execute the notebook:

```bash
git clone https://github.com/yourusername/beer-consumption-analysis.git
cd beer-consumption-analysis
jupyter notebook beer_sp_br_consumption.ipynb
```