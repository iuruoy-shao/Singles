import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import r2_score

def find_n():
    n = 2
    max_score = 0
    for i in range(1,5):
        knn = KNeighborsRegressor(n_neighbors=i).fit(X_train,y_train)
        y_pred = knn.predict(X_test)
        r2 = r2_score(y_test,y_pred)
        if r2 > max_score:
            max_score = r2
            n = i
    print("n: \t",n)
    return n

def knn():
    knn = KNeighborsRegressor(n_neighbors=find_n()).fit(X_train,y_train)
    y_pred = knn.predict(X_test)
    r2 = r2_score(y_test,y_pred)
    print("r2: \t",r2)
    return y_pred

def plot(y_test,y_pred):
    fig, ax = plt.subplots()
    plt.scatter(y_test,y_pred)
    plt.xlabel('Views')
    plt.ylabel('Predicted Views')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim((0,3000000000))
    plt.ylim((0,3000000000))
    ax.set_box_aspect(1)
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('data.csv', names=['track_title','artist','release_year','popularity','artist_popularity',
                                    'artist_followers','artist_genres','views','days_since_release'])

    X = data[['popularity','artist_popularity','artist_followers','days_since_release']]
    y = data[['views']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)
    plot(y_test,knn())

# def find_depth():
#     depth = 0
#     max_score = 0
#     for i in range(1,5):
#         dt = DecisionTreeRegressor(max_depth=i).fit(X_train,y_train)
#         y_pred = dt.predict(X_test)
#         r2 = r2_score(y_test,y_pred)
#         if r2 > max_score:
#             max_score = r2
#             depth = i
#     print("depth: \t",depth)
#     return depth

# def dt():
#     dt = DecisionTreeRegressor(max_depth=find_depth()).fit(X_train,y_train)
#     y_pred = dt.predict(X_test)
#     r2 = r2_score(y_test,y_pred)
#     print("r2: \t",r2)

#     return y_pred