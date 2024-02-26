from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error 
import numpy as np


def RegressionTree(_test_df):
    # Split the data into train and test sets
    train_x, test_x, train_y, test_y = train_test_split(_test_df.drop('Total Time', axis=1), _test_df['Total Time'], test_size=0.3, random_state=42)
    # Define cross-validation strategy (e.g., KFold with 5 folds)
    kf = KFold(n_splits=10, shuffle=True, random_state=42)
    
    
    # Create Decision Tree Regressor
    model_RT = DecisionTreeRegressor()

    # Perform cross-validation on the train data
    mse_train_RT = -cross_val_score(model_RT, train_x, train_y, cv=kf, scoring='neg_mean_squared_error')

    # Calculate average MSE
    avg_mse_train_RT = np.mean(mse_train_RT)
    print('avg_mse_train_RT : ', avg_mse_train_RT)
    
    # Fit the model to the train data
    model_RT.fit(train_x, train_y)

    # Predict on the test data
    pred_test_RT = model_RT.predict(test_x)

    # Calculate MSE on the test data
    print('mean_squared_error : ', mean_squared_error(test_y, pred_test_RT))
    
    return model_RT

def predict(_model, _x_df):
    pred_y = _model.predict(_x_df)
    return pred_y