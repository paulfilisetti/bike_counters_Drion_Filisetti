import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error
import xgboost as xgb

def train_and_evaluate(X: pd.DataFrame, y: pd.Series) -> xgb.XGBRegressor:
    """Train and evaluate the model using time series cross-validation."""
    model = xgb.XGBRegressor(
        n_estimators=300,
        learning_rate=0.13,
        max_depth=7,
        subsample=1,
        min_child_weight=3,
        random_state=0
    )

    tscv = TimeSeriesSplit(n_splits=5)
    scores = []

    for train_indices, test_indices in tscv.split(X):
        X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
        y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = root_mean_squared_error(y_test, y_pred)
        scores.append(rmse)
        print(f"Fold RMSE: {rmse:.4f}")

    print(f"\nAverage RMSE: {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")

    # Train final model on all data
    model.fit(X, y)
    
    # Print feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nTop 10 important features:")
    print(feature_importance.head(10))
    
    return model