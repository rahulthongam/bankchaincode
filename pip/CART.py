from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Define the features and target variable
features = [
    ["red", "large"],
    ["green", "small"],
    ["red", "small"],
    ["yellow", "large"],
    ["green", "large"],
    ["orange", "large"],
]
target_variable = ["apple", "lime", "strawberry", "banana", "grape", "orange"]

# Encode features
feature_encoders = [LabelEncoder() for _ in range(len(features[0]))]
encoded_features = np.array([
    [feature_encoders[i].fit_transform([row[i] for row in features])[j]
     for i in range(len(features[0]))]
    for j in range(len(features))
])

# Encode target variable
target_encoder = LabelEncoder()
encoded_target = target_encoder.fit_transform(target_variable)

# Train the DecisionTreeClassifier
clf = DecisionTreeClassifier()
clf.fit(encoded_features, encoded_target)

# Predict the fruit type for a new instance
new_instance = ["red", "large"]
encoded_new_instance = [feature_encoders[i].transform([new_instance[i]])[0] for i in range(len(new_instance))]
predicted_fruit_type = clf.predict([encoded_new_instance])
decoded_predicted_fruit_type = target_encoder.inverse_transform(predicted_fruit_type)

print("Predicted fruit type:", decoded_predicted_fruit_type[0])
