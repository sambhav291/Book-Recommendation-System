# %%
import numpy as np
import pandas as pd

# %%
books=pd.read_csv('BX-Books.csv', on_bad_lines='skip', encoding='latin-1', low_memory=False)

# %%
books.head()

# %%
books.rename(columns={'isbn':'ISBN', 'book_title':'Book_Title' , 'book_author':'Book_Author' , 'year_of_publication':'Year_Of_Publication' , 'publisher':'Publisher'}, inplace=True)

# %%
books.head(2)

# %%
users=pd.read_csv('BX-Users.csv', on_bad_lines='skip', encoding='latin-1', low_memory=False)

# %%
users.head(2)

# %%
users.rename(columns={'user_id':'User_ID'},inplace=True)

# %%
users.head(2)


# %%
ratings=pd.read_csv('BX-Book-Ratings.csv', on_bad_lines='skip', encoding='latin-1', low_memory=False)

# %%
ratings.head(2)

# %%
ratings.rename(columns={'user_id':'User_ID','isbn':'ISBN','rating':'Ratings'},inplace=True)

# %%
ratings.head(2)

# %%
books.shape

# %%
ratings.shape

# %%
users.shape

# %%
x=ratings['User_ID'].value_counts()>200

# %%
y=x[x].index

# %%
y

# %%
ratings=ratings[ratings['User_ID'].isin(y)]

# %%
ratings.shape

# %%
ratings.head()


# %%
ratings_with_books=ratings.merge(books, on='ISBN')

# %%
ratings_with_books

# %%
number_rating=ratings_with_books.groupby('Book_Title')['Ratings'].count().reset_index()

# %%
number_rating.rename(columns={'Ratings':'Number_Of_Ratings'},inplace=True)

# %%
final_rating=ratings_with_books.merge(number_rating, on='Book_Title')

# %%
final_rating

# %%
final_rating=final_rating[final_rating['Number_Of_Ratings']>=50]

# %%
final_rating

# %%
final_rating.drop_duplicates(['User_ID','Book_Title'], inplace=True)

# %%
final_rating.shape

# %%
book_pivot=final_rating.pivot_table(columns='User_ID', index='Book_Title', values='Ratings')

# %%
book_pivot.fillna(0,inplace=True)

# %%
book_pivot.shape

# %%
from scipy.sparse import csr_matrix
book_sparse=csr_matrix(book_pivot)

# %%
type(book_sparse)

# %%
from sklearn.neighbors import NearestNeighbors
model=NearestNeighbors(algorithm='brute')

# %%
model.fit(book_sparse)

# %%
distances, suggestions=model.kneighbors(book_pivot.iloc[600,:].values.reshape(1,-1), n_neighbors=6)

# %%
suggestions

# %%
for i in range(len(suggestions)):
    print(book_pivot.index[suggestions[i]])

# %%
book_pivot.index[100]

# %%
np.where(book_pivot.index=='While My Pretty One Sleeps')[0][0]

# %%
# def recommend_book(book_name):
#     book_id=np.where(book_pivot.index==book_name)[0][0]
#     distances, suggestions=model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)
#     for i in range(len(suggestions)):
#         if i==0:
#             print("The suggestions for", book_name, "are:")
#         if not i:
#             print(book_pivot.index[suggestions[i]])
def recommend_book(book_name):
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)
        recommended_books = [book_pivot.index[suggestion] for suggestion in suggestions[0]]
        return recommended_books
    except Exception as e:
        print("Error:", e)  # Print the error for debugging
        return []

# %%
recommend_book('While My Pretty One Sleeps')

# %%



