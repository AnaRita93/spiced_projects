
"""
WEEK 02:Classification Project with Titatnic Data 

This program will run a set of steps to calculate the survival predictions of Titanic passengers using Classification Models 

For more details on EDA and model selection, please check  the jupyter notebook version of this program (week02_project.ipynb). 

###Step 1: Load Data 
###Step 2: Train-Test Split (df_train and df_test)
###Step 3: Feature Engineering on df_train and df_test 
###Step 4: Train Models (Logistic Reg, Random Forest) + Cross validation 
###Step 5: Make predictions for Titanic Kaggle challenge and save results in a csv file 

"""

# Packages 

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.api import add_constant 
from statsmodels.api import OLS, add_constant
from sklearn.feature_selection import RFE
import statsmodels.api as sm

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import plot_roc_curve, auc, roc_curve
from sklearn.model_selection import cross_val_score

pd.options.mode.chained_assignment = None 

# Functions 

def clean_data(df):
    df['Age'].fillna(df['Age'].mean(), inplace=True)
    df['Age'] = pd.to_numeric(df['Age'])
    df['Age'].fillna(df['Age'].mean(), inplace=True)
    df['Cabin'].fillna('not identified', inplace=True)
    df['Embarked'].dropna(inplace=True)
    df.drop(['PassengerId', 'Ticket', 'Cabin'], inplace=True, axis=1)

def format_family_name(df):
    family = df[['PassengerId','Name', 'SibSp','Parch']]
    family.set_index('PassengerId',inplace=True)
    family['Surname'] = family['Name'].str.split(expand=True, n=2, pat=',')[0]
    family['FirstName'] = family['Name'].str.split(expand=True, n=2, pat=',')[1]
    family['PrefixName'] = family['FirstName'].str.split(expand=True, n=2, pat='.')[0]
    family['FirstName'] = family['FirstName'].str.split(expand=True, n=2, pat='.')[1]
    family.sort_values(by='Surname', inplace=True)
    df = df.merge(family)
    df.drop(['Name','FirstName'], inplace=True, axis=1)

def add_family_size_variable(df):
    df['family_size'] = df['Parch']+df['SibSp']+1 
    df['family_size'].value_counts().sort_index()
    family_size_map = {1: 'alone', 2: 'small', 3: 'small', 4: 'small', 5: 'medium', 6: 'medium', 7: 'large', 
                   8: 'large', 11: 'large'}
    df['family_size_cat'] = df['family_size'].map(family_size_map)


def create_age_groups(df): 
    kbins = KBinsDiscretizer(n_bins=5, encode='onehot-dense', strategy='quantile')
    columns = df[['Age']]
    kbins.fit(columns)
    t = kbins.transform(columns)

    edges = kbins.bin_edges_[0].round(1)
    labels = []
    for i in range(len(edges)-1):
        edge1 = edges[i]
        edge2 = edges[i+1]
        labels.append(f"{edge1}_to_{edge2}")

    df_bins = pd.DataFrame(t, columns=labels)
    df_bins['Age'] = df['Age']
    df = df.merge(df_bins)

def create_pipeline_for_logistic_regression(Xtrain, ytrain):
    categorical_pipe = make_pipeline(OneHotEncoder())
    numeric_pipe = make_pipeline(StandardScaler())

    feature_transform = make_column_transformer(
    
                    (categorical_pipe, ['Sex','Embarked', 'family_size_cat']),
    
                    (numeric_pipe, ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'family_size']) )

    pipeline = make_pipeline(feature_transform, LogisticRegression())
    pipeline.fit(Xtrain, ytrain)
    pipeline[:-1].get_feature_names_out()
    Xtrain_transformed_LogReg = pd.DataFrame(pipeline[:-1].transform(Xtrain),
                     columns=pipeline[:-1].get_feature_names_out(),
                     index=Xtrain.index)

def train_decision_tree(Xtrain,ytrain,Xtest, ytest,tree_depth):
    m_tree = DecisionTreeClassifier(max_depth=tree_depth)  
    m_tree.fit(Xtrain.values, ytrain.values)

    ypred_tree = m_tree.predict(Xtrain.values)
    print(classification_report(ytrain.values, ypred_tree))
    print(f'crossvalidatin for DecisionTree is {cross_val_score(m_tree, Xtrain, ytrain)}')
    print('')
    print('Comparison with test data')
    print("training DecTree accuracy = ",   round(m_tree.score(Xtrain.values, ytrain.values),2))
    print("validation DecTree accuracy = ", round(m_tree.score(Xtest.values, ytest.values), 2))    

def train_logistic_regression(Xtrain,ytrain,Xtest, ytest):
    m = LogisticRegression(class_weight='balanced', multi_class='multinomial', solver='newton-cg')
    m.fit(Xtrain.values, ytrain.values)
    ypred_log = m.predict(Xtrain.values)
    print(classification_report(ytrain.values, ypred_log))
    print(f'crossvalidatin for LogReg is {cross_val_score(m, Xtrain, ytrain)}')
    print('')
    print('Comparison with test data')
    print("training LogReg accuracy = ",   round(m.score(Xtrain.values, ytrain.values),2))
    print("validation LogReg accuracy = ", round(m.score(Xtest.values, ytest.values), 2))

def train_randomforest(Xtrain,ytrain,Xtest, ytest):
    r = RandomForestClassifier(max_depth=tree_dept)
    r.fit(Xtrain.values, ytrain.values)
    ypred_rf = r.predict(Xtrain.values)
    print(classification_report(ytrain.values, ypred_rf))
    print(f'crossvalidatin for RF is {cross_val_score(r, Xtrain, ytrain)}')
    print('')
    print('Comparison with test data:')
    print("training RF accuracy = ",       round(r.score(Xtrain.values, ytrain.values),2))
    print("validation RF accuracy = ",     round(r.score(Xtest.values, ytest.values),2))

# Program execution 

# Load and Inspect Data. Fill Missing values. 
df = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

clean_data(df)
clean_data(test)



# Train-test split the data 
df_train, df_test = train_test_split(df, test_size = 0.2)

# Step 3: Feature Engineering of df train and df_test

# Step 4: Train models -Logistic Regression, Random Forest and print out evaluation and cross validation metrics 
train_logReg(Xtrain.values, ytrain.values)
train_randomForest(Xtrain.values, ytrain.values)


# Step 6: Make predictions and save it into a csv file in Kaggle format 

