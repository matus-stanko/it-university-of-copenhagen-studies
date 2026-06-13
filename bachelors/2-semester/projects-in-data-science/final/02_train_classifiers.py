import os
import sys
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import pickle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load data
data = pd.read_csv("final/features/features_training.csv")

# Create binary label indicating cancerous or not
data["cancerous"] = data["diagnostic"].isin(["MEL", "SCC", "BCC"])
# Remove unnecessary colum
features = data.drop(columns=["patient_id", "diagnostic", "cancerous"])
target = data["cancerous"]


# Define cross-validation strategy based on patient_id
group_kfold = GroupKFold(n_splits=5)

# Initialize logistic regression model
model = LogisticRegression(max_iter=1000000)

# Perform cross-validation
accuracies = []
f1_scores = []
recalls = []
precisions = []
for train_index, test_index in group_kfold.split(features, target, data["patient_id"]):
    X_train, X_test = features.iloc[train_index], features.iloc[test_index]
    y_train, y_test = target.iloc[train_index], target.iloc[test_index]

    # Train the model
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    # Calculate F1 score
    f1 = f1_score(y_test, y_pred)
    f1_scores.append(f1)

    # Calculate recall
    recall = recall_score(y_test, y_pred)
    recalls.append(recall)

    # Calculate precision
    precision = precision_score(y_test, y_pred)
    precisions.append(precision)


# Calculate average accuracy
average_accuracy = sum(accuracies) / len(accuracies)
average_f1 = sum(f1_scores) / len(f1_scores)
average_recall = sum(recalls) / len(recalls)
average_precision = sum(precisions) / len(precisions)
print("Average Accuracy:", average_accuracy)
print("Average F1 Score:", average_f1)
print("Average Recall:", average_recall)
print("Average Precision:", average_precision)

# Save the trained classifier using pickle with .sav file extension
with open("logistic_regression_classifier.sav", "wb") as file:
    pickle.dump(model, file)
