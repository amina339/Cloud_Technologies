from collections import Counter, defaultdict
from itertools import chain


class NaiveBayesClassifier:

    def __init__(self):
        self.prediction = None
        self.class_priors = None
        self.vocabulary = None
        self.class_word_counts = None
        self.word_probs = None
        self.classes = None

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        self.classes = list(set(y))
        total_docs = len(y)
        self.class_priors = {}
        self.word_probs = defaultdict(lambda: defaultdict(float))
        self.class_word_counts = {}
        self.vocabulary = set()

        class_counts = Counter(y)
        self.class_priors = {cls: count / total_docs for cls, count in class_counts.items()}

        class_texts = {cls: [] for cls in self.classes}
        for text, label in zip(X, y):
            class_texts[label].append(text)

        class_word_freqs = {}
        for cls in self.classes:
            all_words = list(chain.from_iterable([text.split() for text in class_texts[cls]]))
            self.vocabulary.update(all_words)
            class_word_freqs[cls] = Counter(all_words)
            self.class_word_counts[cls] = len(all_words)

        vocab_size = len(self.vocabulary)

        for word in self.vocabulary:
            for cls in self.classes:
                word_count = class_word_freqs[cls][word]
                self.word_probs[word][cls] = (word_count + 1) / (self.class_word_counts[cls] + vocab_size)
        return self.word_probs

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        res = []
        for sentence in X:
            default_value = sum(self.class_priors.values())
            prob = {key: default_value for key in self.classes}
            for word in sentence.split():
                if word in self.word_probs.keys():
                    for cls in self.classes:
                        prob[cls] += self.word_probs[word][cls]
            res.append(max(prob, key=prob.get))

        self.prediction = res
        return self.prediction

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        y_pred = self.predict(X_test)
        cm = 0
        others = 0

        for true, pred in zip(y_test, y_pred):
            if true == pred:
                cm += 1
            else:
                others += 1

        mean_accuracy = cm / (others + cm)
        return mean_accuracy
