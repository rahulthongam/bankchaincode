import numpy as np  # Fix for np issue
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.svm import SVC

# Generating synthetic data with make_blobs
X, Y = make_blobs(n_samples=500, centers=2, random_state=0, cluster_std=0.40)

# Plotting the scatter of synthetic data
plt.scatter(X[:, 0], X[:, 1], c=Y, s=50, cmap='spring')
plt.show()

# Creating linspace between -1 to 3.5
xfit = np.linspace(-1, 3.5)  # Fixed np import issue

# Plotting scatter and decision boundaries
plt.scatter(X[:, 0], X[:, 1], c=Y, s=50, cmap='spring')
for m, b, d in [(1, 0.65, 0.33), (0.5, 1.6, 0.55), (-0.2, 2.9, 0.2)]:
    yfit = m * xfit + b
    plt.plot(xfit, yfit, '-k')
    plt.fill_between(xfit, yfit - d, yfit + d, edgecolor='none', color='#AAAAAA', alpha=0.4)

plt.xlim(-1, 3.5)
plt.show()

# Reading the CSV file (fix for invalid escape sequence)
x = pd.read_csv(r"C:\Users\bikas\Desktop\DM&ML302\Practical\cancer.csv")  # Adjust the file path appropriately
a = np.array(x)
y = a[:, 2]  # Labels are in the third column (index 2)

# Extracting two features
x = np.column_stack((x["malignant"], x["benign"]))  # Ensure correct column names

# Printing the shapes
print(x.shape, y)

# Support Vector Classifier
clf = SVC(kernel='linear')

# Fitting the model
clf.fit(x, y)

# Making predictions
print(clf.predict([[120, 990]]))  # Prediction 1
print(clf.predict([[85, 550]]))   # Prediction 2
