import os
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

import rampwf as rw

# Specify the name of the problem
problem_title = "Team Football Challenge"

# Specify target variable name
_prediction_label_names = [-1, 0, 1]

# Specify the type of prediction
Predictions = rw.prediction_types.make_multiclass(
    label_names=_prediction_label_names)

# Specify the type of problem
workflow = rw.workflows.Classifier()

# Specify the score type
score_types = [
    rw.score_types.BalancedAccuracy(name="bal_acc",
                                    precision=3,
                                    adjusted=False),
    rw.score_types.Accuracy(name="acc", precision=3),
]

# ====================


def get_cv(X, y):
    """
    Return the cross-validation split.

    Parameters
    ----------
    X : pandas DataFrame
        The training data.

    y : pandas Series
        The target variable.

    Returns
    -------
    cv : a cross-validation split
    """
    cv = StratifiedShuffleSplit(n_splits=3, random_state=0, test_size=0.2)
    return cv.split(X, y)


# ====================
_target_column_name = "match_outcome"


def _read_data(path, f_name):
    """
    Load the data from the CSV file.

    Parameters
    ----------
    path : str
        The path to the data folder.

    f_name : str
        The name of the CSV file.

    Returns
    -------
    X : pandas DataFrame
        The training data.

    y : pandas Series
        The target variable.
    """
    data = pd.read_csv(os.path.join(path, 'data', f_name))
    y = data[_target_column_name]
    X = data.drop(_target_column_name, axis=1)
    return X.values, y

# ====================


def get_train_data(path='.'):
    """
    Load the training data.

    Parameters
    ----------
    path : str
        The path to the data folder.

    Returns
    -------
    X : pandas DataFrame
        The training data.

    y : pandas Series
        The target variable.
    """
    f_name = "train.csv"
    return _read_data(path, f_name)


def get_test_data(path='.'):
    """
    Load the test data.

    Parameters
    ----------
    path : str
        The path to the data folder.

    Returns
    -------
    X : pandas DataFrame
        The test data.

    y : None
        The target variable is not available.
    """
    f_name = "test.csv"
    return _read_data(path, f_name)
