# -*- coding: utf-8 -*-
"""App Rating Prediction by Rahul Kuzhuppillil.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1465FdOSmkpBEkyNMQpcdANxzNHkDHEdh
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#importing all necessary  libraries

df= pd.read_csv(r"/content/drive/MyDrive/Colab Notebooks/googleplaystore.csv")

df.describe(include='all')

df.drop_duplicates(inplace=True)
#removed all the duplicates as part of data cleaning to increase accuracy

from google.colab import drive
drive.mount('/content/drive')

df.isna().sum()
#2)Checking for null values in the data and displaying null values for each column.

df.dropna(subset = ['Content Rating','Type','Android Ver','Current Ver'], axis = 0, inplace = True)
#3)Dropping records with nulls from columns - 'Content Rating','Type','Android Ver','Current Ver'
df["Rating"].fillna(df["Rating"].mode()[0],axis=0,inplace = True)
#Replaced nulls from Rating column with "mode of rating" which is 4.4

df["Size-Numeric"] = df["Size"].str.extract("(\d+\.?\d*)").astype("float")
df.loc[df["Size"].str.contains("M"),"Size-Numeric"] *=1000
# 4.1 Extracted the numeric value from the column using expression pattern, extract method and Multiplied the value by 1,000  for size mentioned in Mb

df.drop("Size",axis =1,inplace = True)
#dropping the Size column

df.rename(columns={"Size-Numeric":"Size"}, inplace = True)
#renaming the new column to original

df.isnull().sum()
#the Size column generated 1525 null values which were originally as string "varies with size"

df["Size"].fillna(df["Size"].mode()[0], axis =0, inplace = True)
#Replace null with mode of strings which is 11000.0 kb

df["Reviews"] = df["Reviews"].astype("int")
#4.2) Reviews is a numeric field that is loaded as a string field, Converted it to integer

df["Installs"] = df["Installs"].str.replace("+","",regex = True).str.replace(",","",regex = True)
#4.3) Removed symbols from Installs column

df["Installs"] = df["Installs"].astype("int")
#4.3) Installs column converted to integer

df["Price"] = df["Price"].str.replace("$","",regex = True)
# 4.4) Price field is a string and has $ symbol. Removed ‘$’ sign

df["Price"] = df["Price"].astype("float")
# 4.4) Converted Price field to float.

(df['Rating'] >=1).value_counts()

(df['Rating'] <= 5 ).value_counts()
#all 10346 values in the rating field are within the specified range of >=1 and <=5

df['Rating'].mean()
#5.1) average rating is 4.2 with the range and all the value falls within the range, nothing to be dropped.

(df['Reviews'] > df['Installs']).sum()
#there are 11 records where review is greater than installs

df.drop(df[df['Reviews']>df['Installs']].index,axis =0, inplace=True)
#5.2) All the 11 records where the number of reviews greater than number of installs are dropped.

df['Type'].describe()

df["Type"].value_counts()

((df["Type"] == "Free") & (df['Price']>0)).value_counts()
#5.3) All 9579 free app are priced 0, so there is nothing to drop

def turkey_IQR(col):
    Q1 = np.percentile(col, 25)
    Q3 = np.percentile(col, 75)
    IQR = Q3 - Q1
    print("Q1 =",Q1)
    print("Q3 =",Q3)
    print("IQR =",IQR)
    upperf = Q3+1.5*IQR
    lowerf = Q1-1.5*IQR
    print("Lower Fence =",lowerf)
    print("Upper Fence =",upperf)
    upper = np.where(col>upperf)
    lower = np.where(col<lowerf)
    print("Upper Outliers :",upper)
    print("Lower Outliers :",lower)

#function to calculate turkey's fence, IQR etc

df["Price"].describe()

(df["Price"] > 0).value_counts()
#7.8% values of price are outliers

df["Price"].unique()

turkey_IQR(df["Price"])

plt.figure(figsize=(6,3))
sns.boxplot(x=df["Price"])
plt.title("Boxplot for price")
plt.xlabel("Price Range")
plt.show()
#5) boxplot of price

"""Univariate analysis of Price:
1) Price range: 0 to 400.
2) Majority of dataset: '0'.
3) Tukey's fences calculation: Q1, Q3, IQR, lower, and upper fences all '0' due to dataset majority.
4) Standard method for identifying outliers: Values below threshold are potential outliers.
5) Understanding further requirements is necessary to identify outliers. Extremely high price could be considered an outlier with a defined threshold.
6) Potential outliers: Sorted unique high prices - 400.0, 399.99, 379.99, 299.99, 200.0, 154.99, 109.99, 89.99, 79.99, 74.99, 46.99, 33.99, 30.99, 29.99, 28.99, 25.99.
7) Outliers account for approximately 7.8% of the data.
"""

df["Reviews"].describe()

df["Reviews"].nunique()

np.sort(df["Reviews"].unique())

turkey_IQR(df["Reviews"])

(df["Reviews"] > 116878.0).value_counts()

df[df["Reviews"] > 116878.0]["Reviews"].value_counts()

df[df["Reviews"] > 116878.0]
#data of apps with rating higher than 116878. The values seems reasonable because they are less than the number of installs

plt.figure(figsize=(6, 3))
sns.boxplot(x=df["Reviews"])
plt.title("Boxplot for Review")
plt.show()
#box plot of Reviews

"""Univariate analysis of Review:
1) Review has 5998 unique values, ranging from 0 to 78158306.
2) Out of the total apps, 1866 (18.04%) have extremely high review values compared to the majority. This is determined based on IQR values and an upper fence value of 116878. The three highest ratings are 69119316, 78128208, and 78158306 respectively. Currently, 18.04% of the data are considered outliers.
3) The high rating values appear reasonable as they are lower than the number of installs.
4) The data might require normalization.
"""

df["Rating"].describe()

turkey_IQR(df["Rating"])

df["Rating"].value_counts()

plt.figure(figsize=(6,4))
plt.hist(df["Rating"])
plt.xlabel("Ratings")
plt.ylabel("Frequency")
plt.title("Histogram of Ratings")
plt.show()
#5) Histogram of Ratings

"""Univariate analysis: Histogram of Rating:
1) The majority of the ratings are higher, with the highest count observed at 4.4 (2487 counts). Other significant counts include 4.3 (1016), 4.5 (976), 4.2 (887), and 4.6 (768).
2) The bin ranging from 4.2 to 4.6 has the highest count according to the histogram, indicating it as the majority range.
3) There are fewer counts towards the left side of the histogram.
"""

df["Size"].describe()
#size of app is in kb

np.sort(df["Size"].unique())

(df["Size"].value_counts())

turkey_IQR(df["Size"])

plt.figure(figsize=(6,4))
plt.hist(df["Size"])
plt.xlabel("Size")
plt.ylabel("Frequency")
plt.title("Histogram of Size")
plt.show()
#5) Histogram of Size

"""Univariate analysis: Histogram of Rating:
1) The size field consists of 454 unique values, ranging from 8.5 to 100,000 kb.
2) The histogram reveals that there is a higher number of apps with smaller sizes, and fewer apps towards the right side of the graph.
3) The majority of the apps fall within the bin range of 10,000 to 20,000.

All the columns, including Price, Reviews, Rating, and Size, exhibit outliers.
"""

(df["Price"] >= 200).value_counts()

df[df["Price"] >=200]
#6.1) details of apps with high price, price greater than 200.

"""6.1.1)App with price above 200:
1) Apps with prices above 200 raise suspicion as they all share the same name, "I'm Rich," which suggests they may be scam apps intended to deceive and defraud customers.
2) The app "EP Cook Book" is priced at 200 but has no downloads or ratings. This app seems inappropriate to include as it is excessively expensive for a cookbook, and its categorization as "Medical" is also incorrect.
3) It is recommended to remove these app data, as promoting such applications goes against ethical considerations.
"""

df.drop(df[df["Price"] >=200].index,axis =0,inplace = True)
#6.1.2)All 18 apps with price greater than 200 is dropped.

(df["Reviews"] >2000000).value_counts()
#6.2) there are 408 apps that has reviews greater than 2million - contributes to 4% of the current dataset

df.drop(df[df["Reviews"] >2000000].index,axis =0,inplace = True)
#6.2) Dropping 4% of the high review apps to avoid skewing

turkey_IQR(df["Installs"])

plt.figure(figsize=(6, 3))
sns.boxplot(x=df["Installs"])
plt.title("Boxplot for Installs")
plt.show()
#box plot of Reviews

#6.3.1) Finding out the different percentiles – 10, 25, 50, 70, 90, 95, 99.
print("10th Percentile =", np.percentile(df["Installs"], 10))
print("25th Percentile =", np.percentile(df["Installs"], 25))
print("50th Percentile =", np.percentile(df["Installs"], 50))
print("70th Percentile =", np.percentile(df["Installs"], 70))
print("90th Percentile =", np.percentile(df["Installs"], 90))
print("95th Percentile =", np.percentile(df["Installs"], 95))
print("99th Percentile =", np.percentile(df["Installs"], 99))

"""6.3.2) Finding the cuttoff threshold for installs.
In addition to the above:
IQR = 999000.0
Upper Fence = 2498500.0

The cutoff threshold for installs is set at the upper fence value of 2,498,500.0 using Tukey's fence method.
"""

(df["Installs"] > 2498500.0).value_counts()
#2188 records will be dropped.

df.drop(df[df["Installs"] > 2498500.0].index, inplace=True)
#6.3.2dropping values by consider upper fence value as threshold. 27.84% of the current data will be dropped.

#Q)7.1.1 scatter plot/joinplot for Rating vs. Price

sns.jointplot(x=df["Rating"], y=df["Price"])
plt.title("                                                  Jointplot: Rating vz. Price")
plt.show()

"""Q)7.1.1 What pattern do you observe? Does rating increase with price?

Scatterplot/joinplot observation of Rating vz Price:

From the scatterplot and the bin plot from jointplot we can see that,
1) Apps with ratings around 4.3-4.4 tend to have the highest prices, ranging from approximately 0 to 158. Additionally, this rating bin (4.3-4.4) contains the largest number of apps.
2) The majority of apps are priced between 0 and 10, while the remaining apps are dispersed between 10 and 40. There are only a few apps (around 6) priced above 40.

Conclusion: Although there is a trend suggesting that higher-rated apps may have higher prices in some cases, it's important to note that when comparing the price ranges of 4.4 and 5.0 ratings, the apps with a rating of 4.4 tend to have higher prices. Therefore, it is not necessary to conclude that apps with higher ratings are always more expensive. Thus, the observation indicates that rating does not necessarily increase with price.
"""

#Q)7.2.1 scatter plot/joinplot for Rating vs. Size

sns.jointplot(x=df["Rating"], y=df["Size"])
plt.title("                                                  Jointplot: Rating vz. Size")
plt.show()

"""Q)7.2.1 Are heavier apps rated better?

Scatterplot/joinplot observation of Rating vz Size:

From the scatterplot and the bin plot from jointplot we can see that,
1) The majority of apps fall into the size range of 0-10,000 kb, while the remaining apps are dispersed between 10,000-100,000 kb. The count of apps reduces as the size increases, indicating that there are fewer apps with larger sizes compared to smaller ones.
2) Apps with ratings of 4.3-4.4 have the highest count, and they exhibit a wide range of app sizes, spanning from 0-100,000 kb. This rating bin (4.3-4.4) contains the largest number of apps.

Conclusion: Although heavier apps are more common in higher ratings, it's important to note that lighter apps are also prevalent in the majority. The presence of heavier apps is relatively less compared to lighter apps in higher ratings. While the majority of heavier apps receive better ratings, not all of them do; some have average ratings. Therefore, it is not appropriate to conclude that heavier apps are consistently rated better than lighter apps. This is because there are more lighter apps with higher ratings than heavier apps with high ratings.
"""

#Q)7.3 scatter plot/joinplot for Rating vs. Reviews

sns.jointplot(x=df["Rating"], y=df["Reviews"])
plt.title("                                                  Jointplot: Rating vz. Reviews")
plt.show()

"""Q) 7.3.1 Does more review mean a better rating always?

Scatterplot/joinplot observation of Rating vz Reviews:

From the scatterplot and the bin plot from jointplot we can see that,
1) Apps with 0 reviews are uniformly distributed across the rating range of 1 to 5, indicating that there is no specific correlation between the absence of reviews and the app's rating.
2) While the majority of apps with higher reviews tend to have higher ratings, it is important to note that apps with 0 reviews also have higher ratings. In fact, the count of apps with 0 reviews and higher ratings is greater than the count of apps with high reviews and higher ratings.

Conclusion: It is evident that having more reviews generally contributes to a better rating, but this relationship is not true in all cases. There are instances where apps with fewer reviews still manage to receive better ratings in greater numbers. Therefore, while more reviews typically aid in achieving a higher rating, it is not a guarantee. Other factors may influence the rating of an app.
"""

#7.4) boxplot for Rating vs. Content Rating (sorted)
plt.figure(figsize=(5,2))
sorted_categories = df.groupby("Content Rating")["Rating"].median().sort_values(ascending=False).index
sns.boxplot(x=df["Rating"],y=df["Content Rating"],order =sorted_categories)
plt.title("Boxplot for Rating vs. Content Rating (Sorted in descending)")
plt.show()

"""7.4.1. Is there any difference in the ratings? Are some types liked better?
1) There are notable differences in ratings across all content categories. Ranking the categories based on the median, we have: Adult only 18+ > Everyone > Everyone 10+ > Teen > Unrated > Mature 17+.

2) "Adult only 18+" content category stands out as it is more favored compared to other content types. It has a higher median rating and a smaller interquartile range (IQR) when compared to the "Everyone" category.
"""

#7.5) boxplot for Ratings vs. Category (sorted)
plt.figure(figsize=(10,7))
sorted_categories2 = df.groupby("Category")["Rating"].median().sort_values(ascending=False).index
sns.boxplot(x=df["Rating"],y=df["Category"], order =sorted_categories2)
plt.title("Boxplot for Rating vs. Category (Sorted in descending)")
plt.show()

sorted_genr = df.groupby("Genres")["Rating"].median().sort_values(ascending=False).index
print("Genres sorted based on rating in Descending order:- \n\n", sorted_genr)

"""7.5.1) Which genre has the best ratings?
1) The genre "Comics;Creativity and Board;Pretend Play" has the highest ratings among the genres considered. It showcases consistently positive ratings across various metrics.
2) From the boxplot, it is evident that the category "ART and DESIGN" has the best ratings. It demonstrates higher values in the upper quartiles compared to other genres and boasts the highest maximum rating value, indicating its strong performance.
"""

#8)copy of the dataframe
inp1 = df.copy()

#8.1) log transformation applied to Reviews & Installs to reduce the skew for linear regression model
inp1["Reviews"]=np.log1p(inp1["Reviews"])
inp1["Installs"]=np.log1p(inp1["Installs"])

#boxplot of before and after comparison
plt.figure(figsize=(10,.5))
sns.boxplot(x=df["Reviews"])
plt.title("Before log tranformation")
plt.figure(figsize=(10,.5))
sns.boxplot(x=df["Installs"])
plt.show()
print("--------------------------------------------------------------------------------------------------------------")
plt.figure(figsize=(10,.5))
sns.boxplot(x=inp1["Reviews"])
plt.title("After log tranformation")
plt.figure(figsize=(10,.5))
sns.boxplot(x=inp1["Installs"])
plt.show()

#8.2) Dropping columns App, Last Updated, Current Ver, and Android Ver. These variables are not useful for model.
inp1.drop(["App","Last Updated","Android Ver","Current Ver","Type"],axis =1, inplace =True)

#8.3) Performing one-hot encoding : Getting dummy columns for Category, Genres, and Content Rating to inp2 dataframe
inp2 = pd.get_dummies(inp1)

inp2.head()

x =inp2.drop(["Rating"],axis =1)
y =inp2["Rating"]
#inputs for alternate method

#9) Train test split  and apply 70-30 split. Name the new dataframes df_train and df_test.
#x_train, y_test = train_test_split(inp2, test_size=0.3, random_state=100)
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=100)

#9)Separate the dataframes into X_train, y_train, X_test, and y_test.
#x_train = df_train.drop(["Rating"],axis =1)
#x_test = df_test.drop(["Rating"],axis =1)
#y_train = df_train["Rating"]
#y_test = df_test["Rating"]
#splitting the data into training and testing sets for both the input features (x) and the corresponding target variable (y).

#11) Model Building - Using linear regression model
model = LinearRegression()
model.fit(x_train,y_train)
#training the model on train set

pred_train = model.predict(x_train)
#using x train set for model prediction, this value is required for calculating R2 score

#11) Report the R2 on the train set
print ("R2 on train set:", r2_score(y_train,pred_train))
#The R2 score on train set is poor 0.11. The model fit is poor, so we can expect model performance also to be poor

#12) Make predictions on test set
#pred_test = model.predict(x_test)
#using x test set for model prediction

#12) R2 of prediction model
print ("R2 on test set:",r2_score(y_test,pred_test))
#Poor R2 score of 0.07.

"""Final Observations:
The R2 score of the training set is 0.116, indicating that approximately 11.65% of the variance in the target variable can be explained by the predictor variables in the model. This suggests a relatively weak relationship between the predictor variables and the target variable in the training data.

Similarly, the R2 score of the test set is 0.072, indicating that approximately 7.21% of the variance in the target variable can be explained by the predictor variables in the model when applied to unseen test data.

These results suggest that the model's performance on the test data is consistent with its performance on the training data, but still reflects a relatively weak predictive ability.

Considering the correlation coefficients between the predictor variables and the target variable, none of the variables show a strong correlation. Therefore, it would be more appropriate to consider either using a different dataset or exploring alternative modeling techniques and evaluation metrics.

Additionally, the correlation coefficient values for the target variable "Rating" are provided below:

Correlation coefficients for target variable "Rating":
1.000000 -0.028403 -0.119659 0.028496 0.002698 0.028610 0.004383 0.017988 0.047664 0.009433 ... 0.004496 0.006606 -0.080340 -0.025298 -0.001833 -0.006362 0.004496 -0.045823 0.010178 0.007054
"""

sns.heatmap(inp2.corr())
plt.show()
#heatmap after one hot encoding

sns.heatmap(df.corr(), cmap="coolwarm", annot=True)
plt.show()

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

rf_regressor = RandomForestRegressor(max_depth=3, random_state=42)
rf_regressor.fit(x_train, y_train)

knn_regressor = KNeighborsRegressor()
knn_regressor.fit(x_train, y_train)

rf_y_pred = rf_regressor.predict(x_test)
knn_y_pred = knn_regressor.predict(x_test)

rf_y_pred = rf_regressor.predict(x_test)
knn_y_pred = knn_regressor.predict(x_test)

rf_r2 = r2_score(y_test, rf_y_pred)
knn_r2 = r2_score(y_test, knn_y_pred)

print("Random Forest R2 on test set:", rf_r2)
print("K Neighbors R2 on test set:", knn_r2)

