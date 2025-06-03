import ast
import re
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
file = open('Musical_Instruments_5.json')
reviews = []
start = time.time()
print('Step 1 (formatting)...')
for x in file.readlines():
    reviews.append(x.replace('\n', ''))
print('...done')
print('Step 2 (evaluating)...')
for x in range(0, len(reviews)):
    try:
        reviews[x] = ast.literal_eval(reviews[x][:-30]+'}')
    except:
        pass
print('...done')
all_reviews = []
labels = []
print('Step 3 (organising)...')
for x in reviews:
    try:
        if x["overall"] >= 3:
            all_reviews.append(re.sub('[^A-Za-z]+', ' ', x["reviewText"]))
            labels.append(1)
        else:
            all_reviews.append(re.sub('[^A-Za-z]+', ' ', x["reviewText"]))
            labels.append(0)
    except:
        pass
print('...done')
print('Step 4 (TFIDF)...')
tfidf = TfidfVectorizer(max_features=2500, max_df=0.8)
tfidf_reviews = tfidf.fit_transform(all_reviews).toarray()
all_reviews = tfidf_reviews
print('...done')
print('Step 5 (training model)...')
lr = LogisticRegression()
# Train and test data split: 80%
lr.fit(X=all_reviews[:int(len(all_reviews)/5*4)], y=labels[:int(len(labels)/5*4)])
print('...done')
total = 0
correct = 0
positive_correct = 0
negative_correct = 0
positive_incorrect = 0
negative_incorrect = 0
print('Step 6 (accuracy score)...')
for val in range(int(len(all_reviews)/5*4+1), len(all_reviews)):
    if lr.predict([all_reviews[val]])[0] and labels[val]:
        correct += 1
        positive_correct += 1
    if not lr.predict([all_reviews[val]])[0] and not labels[val]:
        correct += 1
        negative_correct += 1
    if not lr.predict([all_reviews[val]])[0] and labels[val]:
        negative_incorrect += 1
    if lr.predict([all_reviews[val]])[0] and not labels[val]:
        positive_incorrect += 1
    total += 1
print('...done')
print('Model had a total accuracy of', str(round(correct/total*100, 2)) + '%.')
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.bar(['Positive Correct', 'Negative Correct', 'Positive Incorrect', 'Negative Incorrect'], [positive_correct, negative_correct, positive_incorrect, negative_incorrect])
end = time.time()
print('Process finished in', round(end-start, 2), 'seconds.')
plt.show()
