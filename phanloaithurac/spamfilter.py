import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB 

#import data
spam_df = pd.read_csv('C:\\Users\\Admin\\Documents\\GitHub\\BTL-TTNT\\phanloaithurac\\spam.csv')

#inspect data
spam_df.groupby('Category').describe()

#turn spam/ham into numerical data, creating a new colume call spam
spam_df['spam'] = spam_df['Category'].apply(lambda x : 1 if x =='spam' else 0)

#create train/text split
x_train, x_test, y_train, y_test = train_test_split(spam_df.Message, spam_df.spam, test_size = 0.25)

#word count
cv = CountVectorizer()
x_train_count = cv.fit_transform(x_train.values)

#train model
model = MultinomialNB()
model.fit(x_train_count, y_train)

#pre-test ham
email_ham = ["hay wanna meet up for the game?"]
email_ham_count = cv.transform(email_ham)
model.predict(email_ham_count)

#pre-test spam
email_spam = ["reward money cfaf fafglick"]
email_spam_count = cv.transform(email_spam)
model.predict(email_spam_count)

#test model
x_test_count = cv.transform(x_test)
model.score(x_test_count, y_test)

def main():
    # print(model.predict(email_ham_count))
    print(model.score(x_test_count, y_test))

if __name__ == "__main__":
    main()
