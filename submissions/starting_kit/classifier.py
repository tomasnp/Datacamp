from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

columns = ['match_id', 'competition_season', 'match_date', 'player_1', 'player_2', 'player_3', 'player_4', 'player_5', 
 'player_6', 'player_7', 'player_8', 'player_9', 'player_10', 'player_11', 'player_12', 'player_13', 'player_14', 
 'player_15', 'player_16', 'player_17', 'player_18', 'player_19', 'player_20', 'player_21', 'player_22', 'player_1_position', 
 'player_2_position', 'player_3_position', 'player_4_position', 'player_5_position', 'player_6_position', 'player_7_position', 
 'player_8_position', 'player_9_position', 'player_10_position', 'player_11_position', 'player_12_position', 'player_13_position', 
 'player_14_position', 'player_15_position', 'player_16_position', 'player_17_position', 'player_18_position', 'player_19_position', 
 'player_20_position', 'player_21_position', 'player_22_position', 'player_1_goals', 'player_2_goals', 'player_3_goals', 'player_4_goals', 
 'player_5_goals', 'player_6_goals', 'player_7_goals', 'player_8_goals', 'player_9_goals', 'player_10_goals', 'player_11_goals', 'player_12_goals', 
 'player_13_goals', 'player_14_goals', 'player_15_goals', 'player_16_goals', 'player_17_goals', 'player_18_goals', 'player_19_goals', 'player_20_goals', 
 'player_21_goals', 'player_22_goals', 'player_1_assists', 'player_2_assists', 'player_3_assists', 'player_4_assists', 'player_5_assists', 'player_6_assists', 
 'player_7_assists', 'player_8_assists', 'player_9_assists', 'player_10_assists', 'player_11_assists', 'player_12_assists', 'player_13_assists',
 'player_14_assists', 'player_15_assists', 'player_16_assists', 'player_17_assists', 'player_18_assists', 'player_19_assists', 'player_20_assists', 
 'player_21_assists', 'player_22_assists', 'player_1_keypass', 'player_2_keypass', 'player_3_keypass', 'player_4_keypass', 'player_5_keypass', 
 'player_6_keypass', 'player_7_keypass', 'player_8_keypass', 'player_9_keypass', 'player_10_keypass', 'player_11_keypass', 'player_12_keypass', 
 'player_13_keypass', 'player_14_keypass', 'player_15_keypass', 'player_16_keypass', 'player_17_keypass', 'player_18_keypass', 'player_19_keypass', 
 'player_20_keypass', 'player_21_keypass', 'player_22_keypass', 'player_1_obv', 'player_2_obv', 'player_3_obv', 'player_4_obv', 'player_5_obv', 
 'player_6_obv', 'player_7_obv', 'player_8_obv', 'player_9_obv', 'player_10_obv', 'player_11_obv', 'player_12_obv', 'player_13_obv', 'player_14_obv', 'player_15_obv', 
 'player_16_obv', 'player_17_obv', 'player_18_obv', 'player_19_obv', 'player_20_obv', 'player_21_obv', 'player_22_obv', 'player_1_diff_xT', 'player_2_diff_xT', 'player_3_diff_xT', 
 'player_4_diff_xT', 'player_5_diff_xT', 'player_6_diff_xT', 'player_7_diff_xT', 'player_8_diff_xT', 'player_9_diff_xT', 'player_10_diff_xT', 'player_11_diff_xT', 'player_12_diff_xT', 
 'player_13_diff_xT', 'player_14_diff_xT', 'player_15_diff_xT', 'player_16_diff_xT', 'player_17_diff_xT', 'player_18_diff_xT', 'player_19_diff_xT', 'player_20_diff_xT', 'player_21_diff_xT', 
 'player_22_diff_xT']


class Classifier(BaseEstimator):
    """
    This is the classifier class. It should be able to take in the training data
    and return predictions. The methods to implement are `fit` and `predict`.
    """

    def __init__(self) -> None:
        super().__init__()
        self.model = RandomForestClassifier(**{'n_estimators': 61,
                                               'max_depth': 13,
                                               'min_samples_split': 26,
                                               'min_samples_leaf': 18,
                                               'max_features': None})

    def preprocess(self, X):
        """
        This method should preprocess the data. You can use the `pandas` library
        to clean, transform, or scale the data.

        Parameters
        ----------
        X : numpy array
            The data to preprocess.

        Returns
        -------
        X : numpy array
            The preprocessed data.
        """
        X = pd.DataFrame(X, columns=columns)
        X.drop(columns=["match_id", "competition_season",
               "match_date"], inplace=True, errors="ignore")
        X.fillna(0, inplace=True)

        # Drop categorical columns
        
        for col in X.columns:
            try:
                X[col] = pd.to_numeric(X[col]).astype(int)

            except ValueError:
                pass
        
        X = X.select_dtypes(exclude=["object"])

        return X.values

    def fit(self, X, y):
        """
        This method should fit the model to the training data.

        Parameters
        ----------
        X : numpy array
            The training data.

        y : numpy array
            The target variable.
        """
        X = self.preprocess(X)
        self.model.fit(X, y)

    def predict(self, X):
        """
        This method should make predictions on the test data.

        Parameters
        ----------
        X : numpy array
            The test data.

        Returns
        -------
        y : numpy array
            The predictions.
        """
        X = self.preprocess(X)
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        This method should make probability predictions on the test data.

        Parameters
        ----------
        X : numpy array
            The test data.

        Returns
        -------
        y : pandas DataFrame
            The probability predictions.
        """
        X = self.preprocess(X)
        return self.model.predict_proba(X)
