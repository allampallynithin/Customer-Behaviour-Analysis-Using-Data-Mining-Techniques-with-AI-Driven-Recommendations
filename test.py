import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataset = pd.read_csv("Dataset/Dataset.csv")
dataset['Product_Category_Preference'] = dataset['Product_Category_Preference'].str.lower()
dataset = dataset.drop_duplicates(subset='Product_Category_Preference')

vectorizer = CountVectorizer()
vectorized = vectorizer.fit_transform(dataset['Product_Category_Preference'])
similarities = cosine_similarity(vectorized)

df = pd.DataFrame(similarities, columns=dataset['Product_Category_Preference'], index=dataset['Product_Category_Preference']).reset_index()
input_book = 'electronics'

df[input_book] = pd.to_numeric(df[input_book])
data = df.nlargest(11,input_book)
print(data)
print(type(data))

recommendations = pd.DataFrame(df.nlargest(11,input_book)['Product_Category_Preference'])
recommendations = recommendations[recommendations['Product_Category_Preference']!=input_book]
print(recommendations)
