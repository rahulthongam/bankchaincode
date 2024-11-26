import numpy as np
from collections import defaultdict

# Step 1: Prepare a simple dataset (training data)
data = [
    ('spam', 'buy cheap amazon products now'),
    ('ham', 'how are you doing today'),
    ('spam', 'cheap watches on sale'),
    ('ham', 'let us meet up tomorrow'),
    ('spam', 'win a million dollars now'),
    ('ham', 'can you call me back later'),
]

# Step 2: Define Naive Bayes Classifier class
class NaiveBayesClassifier:
    def __init__(self):
        self.word_probs = defaultdict(lambda: defaultdict(float))  # Word probabilities for each class
        self.class_probs = defaultdict(float)  # Class probabilities
        self.vocab = set()  # Vocabulary

    def train(self, dataset):
        # Count occurrences of words and classes
        class_word_counts = defaultdict(lambda: defaultdict(int))  # Count of words per class
        class_counts = defaultdict(int)  # Count of each class

        # Iterate over the dataset and calculate word and class counts
        for label, text in dataset:
            words = text.split()  # Split text into words
            class_counts[label] += 1  # Increment class count
            for word in words:
                self.vocab.add(word)  # Add word to vocabulary
                class_word_counts[label][word] += 1  # Increment word count for this class

        # Calculate class probabilities P(C) - Probability of each class
        total_samples = sum(class_counts.values())  # Total number of samples
        for label, count in class_counts.items():
            self.class_probs[label] = count / total_samples  # P(C)

        # Calculate word probabilities P(w|C) - Conditional probability of a word given a class
        for label, words in class_word_counts.items():
            total_words = sum(words.values())  # Total words in the current class
            for word in self.vocab:
                # Laplace smoothing: add 1 to each word count to avoid zero probabilities for unseen words
                self.word_probs[label][word] = (words[word] + 1) / (total_words + len(self.vocab))

    def predict(self, text):
        words = text.split()  # Split text into words
        class_scores = {}  # Dictionary to store the score for each class

        # For each class, calculate the log of the posterior probability P(C|w1, w2, ..., wn)
        for label in self.class_probs:
            # Start with the log of class probability P(C)
            class_scores[label] = np.log(self.class_probs[label])

            for word in words:
                if word in self.vocab:
                    # Add log(P(w|C)) to the class score
                    class_scores[label] += np.log(self.word_probs[label].get(word, 1 / len(self.vocab)))  # Laplace smoothing

        # Return the class with the highest score (the one with the highest posterior probability)
        return max(class_scores, key=class_scores.get)

# Step 3: Train the classifier
classifier = NaiveBayesClassifier()
classifier.train(data)

# Step 4: Classify new examples
test_texts = [
    'cheap watches available',
    'how are you',
    'call me now to win',
]

for text in test_texts:
    prediction = classifier.predict(text)
    print(f'Text: "{text}" => Predicted class: {prediction}')
