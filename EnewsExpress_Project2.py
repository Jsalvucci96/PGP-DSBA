# -*- coding: utf-8 -*-
"""Copy of ENews_Express_Learner_Notebook%5BFull_Code_Version%5D.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E83ka5kdTgR4KHG83i7kvRiMW5lQ5cyQ

# Project Business Statistics: E-news Express

**Marks: 60**

## Define Problem Statement and Objectives

An electronic news company called E-news Express wants to increase its number of subscribers and expand its business. The company wants its data science team to analyze visitor data/actions to see how to increase engagement. The executives want to confirm whether or not there has been a decline in new monthly subscribers due to the webpage design. The design company has created a new landing page and the company wants to test the effectiveness of the new page compared to the old page. The data science team has taken a sample of 100 randomly selected users, half which used the old and half which used the new landing page.

The data science team will perform a statistical analysis (at a significance level of 5%) to determine the effectiveness of the new landing page with the following questions in mind:

- Do users spend more time on new landing page compared to old landing page?
-Is the converstion rate higher for the new landing page?
-Does the converted status (whether the visitor subscribed or not) depend on the preferred language?
-Is the time spent on the new page the same for different language users?

## Import all the necessary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
import scipy.stats as stats

"""## Reading the Data into a DataFrame"""

#mounting google colab
from google.colab import drive
drive.mount('/content/drive')

#importing the data frame
data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Business Stats - Week 3/Project 2/abtest.csv')
abtest = data.copy() #copying the dataframe so as not to make changes to the original dataframe

"""## Explore the dataset and extract insights using Exploratory Data Analysis

- Data Overview
  - Viewing the first and last few rows of the dataset
  - Checking the shape of the dataset
  - Getting the statistical summary for the variables
- Check for missing values
- Check for duplicates

###Data Overview
"""

abtest.head() #checking the first 5 rows of data to make sure the dataframe imported properly

"""The dataframe has been loaded properly."""

abtest.tail() #checking the last 5 rows of data

#checking for null values
abtest.isnull().sum()

"""There are no null values in our dataframe."""

abtest.isna().sum()

"""There are also no missing values in our dataframe."""

#checking the shape of the dataframe
abtest.shape

"""There are 100 rows and 6 columns in this data frame."""

#checking datatypes and counts
abtest.info()

"""We can see that each column has 100 non-null values, as we noted previously. No missing value treatments are needed.

There are two continuous data type columns (user_id as an integer type and time_spent_on_the_page as a float data type) and 4 object data type columns (group, landing_page, converted, and language_preferred).
"""

#convert all "object" data types to "category" to reduce amount of space required to store the data

for col in ['group', 'landing_page', 'converted', 'language_preferred']:
  abtest[col] = abtest[col].astype('category')

#check to see if these changes were made properly
abtest.info()

"""The conversions to "Category" data type were executed properly."""

#getting a statistical summary of the dataframe
abtest.describe(include = 'all').T

"""user_id: this column is just a unique identifier for each customer, so we will not get meaningful insights from statistical data of this column.

group: There are two unique values of this column (control and treatment group) with 50 visitors in each group.

landing_page: There are also two unique values of this column (old landing page or new landing page) with 50 visitors in each group.

time_spent_on_page: The average time spent on the page is around 5.4 minutes with a standard deviation of around 2 minutes. The range is from 0.19 minute to almost 11 minutes. Based on the 25th, 50th, and 75th percentiles, this seems to follow a relatively normal distribution.

converted: There are two unique values of this column (yes or no). The most common valule is yes, with 54 (also 54%) of values being yes.

language_preferred: There are 3 unique values, with the highest frequency language being French with 34 visitors preferring French.
"""

#check for duplicates
abtest.duplicated().sum()

"""There are no duplicates in this dataframe.

### Univariate Analysis

We will start with the continuous columns first. Since 'user_id' is just a unique identifier for each visitor, we will start with time_spent_on_the_page.
"""

#plot histogram and boxplot
sns.histplot(x = abtest['time_spent_on_the_page'])
plt.show()
sns.boxplot(x = abtest['time_spent_on_the_page'])
plt.show()

"""Observations: This column appears to have a fairly normal distribution with the most common time spent on page occuring around 5.38 minutes, and the median ocurring very closely around 5.4 (as we saw earlier in our statistical summary). The boxplot also does not show skew in either direction, and no outliers.

We can analyze the 'user_id' column by checking the number of unique values.
"""

abtest['user_id'].nunique()

"""As we noted when viewing the statistical summary, there are 100 different user id's, representing 100 different webpage visitors.

Now we can analyze the categorical columns by looking at the countplot and value counts of each.
"""

#Group column - countplot
sns.countplot(x = abtest['group']);
abtest['group'].value_counts()

"""Observations: There are two values for this column (control, treatment) each with 50 counts."""

#Landing_page column - countplot
sns.countplot(x = abtest['landing_page']);
abtest['landing_page'].value_counts()

"""Observations: Just like the group column, there are two values for the landing_page column (new and old), each with 50 counts."""

#converted column - countplot
sns.countplot(x = abtest['converted']);
abtest['converted'].value_counts()

"""Observations: There are also two values for the converted column: yes and no ("yes" the user has subscribed or "no" they have not). Yes has slightly more counts (54) and no has slightly less (46)."""

#language_preferred column - countplot
sns.countplot(x = abtest['language_preferred']);
abtest['language_preferred'].value_counts()

"""Observations: This column has three values, each with similar counts, but English with slightly less (32) compared to French and Spanish (34 each).

### Bivariate Analysis

We can start with time_spent_on_the_page with other columns.

Note: We will not do a correlation chart (heatmap) since time_spent_on_the_page is the only continuous variable we are analyzing.
"""

#time spent versus group
sns.barplot(data = abtest, x = 'group', y = 'time_spent_on_the_page')
plt.show()
sns.boxplot(data = abtest, x = 'group', y = 'time_spent_on_the_page')
plt.show()
#compare the mean values of these two groups
abtest.groupby(['group'])['time_spent_on_the_page'].mean()

"""Observations: We can see that the treatment group has a higher mean value. However based on the box plot, we can see that the control group has a higher range of values, ranging from almost 0 minutes to 10 minutes, while the treatment group ranges from around 3 minutes to 9.5 minutes.

**Note:** The analysis below for time spent versus landing page should give the same insight as the graph above because the control group used the existing landing page, and the treatment group used the new landing page.
"""

#time spent versus landing page
sns.barplot(data = abtest, x = 'landing_page', y = 'time_spent_on_the_page')
plt.show()
sns.boxplot(data = abtest, x = 'landing_page', y = 'time_spent_on_the_page')
plt.show()
abtest.groupby(['landing_page'])['time_spent_on_the_page'].mean()

"""Observations: The boxplot and bargraph for these two columns is the same (but flipped) as the graphs above for the group column."""

#time spent versus converted columns
sns.barplot(data = abtest, x = 'converted', y = 'time_spent_on_the_page')
plt.show()
sns.boxplot(data = abtest, x = 'converted', y = 'time_spent_on_the_page')
plt.show()
abtest.groupby(['converted'])['time_spent_on_the_page'].mean()

"""Observations: There is a notable difference in time spent on the page between those who subscribed (converted) to the site and those who did not (not converted). The mean of time spent for those who were converted is around 6.6 and the mean of time spent for those who were not converted was around 4. We can see this difference in the boxplot as well, where the 75th percentile of time spent for the not converted group is lower than the 25th percentile for the converted group."""

#time spent versus language preferred
sns.barplot(data=abtest, x='language_preferred', y='time_spent_on_the_page')
plt.show()
sns.boxplot(data=abtest, x='language_preferred', y='time_spent_on_the_page')
plt.show()

"""Observations: There doesn't appear to be a very large difference in means and medians of time spent between the 3 different languages. However, Spanish has a smaller range of times spent (2 to 9 minutes) than the other two.

Let's split the languages by old and new landing page to see if we can get any more information.
"""

#group by old and new landing page using "hue"
sns.catplot(data = abtest, x = 'language_preferred', y = 'time_spent_on_the_page', hue = 'landing_page', kind = 'bar')
plt.show()

"""Observation: The graph shows us that overall, the time spent on the new landing page is higher in every language than on the old landing page. English has the highest time spent, followed by French and Spanish on the new landing page, while Spanish had the highest time spent on the old landing page.

Now we can look at the relationship between the landing page and whether the visitor subscribed or not.
"""

#landing page versus converted

#creating a groupby variable to plot as a graph
landing_page_plot = abtest.groupby(['landing_page', 'converted']).size().reset_index().pivot(columns = 'landing_page', index = 'converted', values = 0)

landing_page_plot.plot(kind = 'bar', stacked = True)
plt.show()

"""Observation: As we noted before, there are slightly more visitors that subscribed (converted) than did not (not converted). The graph shows that for those that visited the old landing page, there is a larger number of visitors who did not convert. Likewise, for those that visited the new landing page, there is a larger number of visitors who did convert.

## 1. Do the users spend more time on the new landing page than the existing landing page?

### Perform Visual Analysis
"""

#we look again at the  graph for the amount of time spent on the new page versus the old page
sns.boxplot(x = abtest['landing_page'], y = abtest['time_spent_on_the_page'])
plt.show()

"""Observations: As noted before, though visitors spend more time on the new landing page overall. We will do an analysis to determine if this difference is statistically significant.

### Step 1: Define the null and alternate hypotheses

Null hypothesis: The mean amount of time visitors spend on the new landing page and on the old landing page is equal.

Alternative hypothesis: The mean amount of time visitors spend on the new landing page is greater than the mean amount of time visitors spend on the old landing page.

This is a one-tailed test since the alternative hypothesis is that one of the means is greater than the other (as opposed to just "different than").

### Step 2: Select Appropriate test

Since we are comparing the sample means from two independent populations, when the standard deviations are unknown, we use the 2-sample independent t-test.

Let's check to see if the assumptions for the 2-sample independent t-test are satisfied:

-Continuous data: Yes, the time spent on the page data is continuous

-Normally-distributed populations - the sample sizes for each landing page (50 each) are greater than 30. Central Limit Theorem states that the distribution of the sample means is normal.

-Equal/Unequal population standard deviations? - As the standard deviations are unknown, we will check whether they are equal or unequal with an F-test below (see step 5)

-Random sampling from the population - we were informed in the problem statement that the samples collected is a random sample

### Step 3: Decide the significance level

The significance level is 0.05.

### Step 4: Collect and prepare data
"""

#create a data frame and array for time spent on new landing page
time_new_page = abtest[abtest['landing_page']=='new']['time_spent_on_the_page']
time_new_page_arr = np.array(time_new_page)

#create data frame and array for time spent on old landing page
time_old_page = abtest[abtest['landing_page']=='old']['time_spent_on_the_page']
time_old_page_arr = np.array(time_old_page)

"""### Step 5a: F-test

Now that we have collected and prepared our data, we should perform an F-test to determine if the standard deviation from the two samples can be considered equal or unequal.

We will use this information when we later calculate the p-value for the original problem.

We have already determined based on the parameters for the t-test, that the assumptions for the F-test are also met: continuous data, normally-distributed populations, independent populations, and random sampling from the population.
"""

#first let's calculate the standard deviation of the two groups

print("STD for Old page: ",time_old_page.std())
print("STD for New page: ",time_new_page.std())

"""Observations: The standard deviation for the old landing page is 2.6 and the standard deviation for the new landing page is 1.8.

We can continue with an F-test to determine whether these standard deviations are sufficiently different enough that we can include an "equal_var=False" parameter to our T-test.
"""

#import required function
from scipy.stats import f

#user-defined function to perform F-test
def f_test(x,y):
  x = np.array(x)
  y = np.array(y)
  test_stat = np.var(x, ddof=1)/np.var(y,ddof=1) #calculate F test stat
  dfn = x.size-1 #set dof numerator
  dfd = y.size-1 #set dof denominator
  p = (1-f.cdf(test_stat, dfn, dfd)) #p-value of F test stat
  return(print("The p_value is {}" .format(round(p,8))))

#perform F-test
f_test(time_old_page, time_new_page) #the old landing page array will be used as "x" and placed in the numerator of the equation since it's variance is larger

"""For an F-test, the null hypothesis is that the the two samples have an equal variance. As the p-value is much smaller than the level of significance (0.05), the null hypothesis can be rejected. Therefore, we can assume the two samples have an unequal variance.

We can now move forward with calculating the p-value.

###Step 5b: Calculate the p-value
"""

#import required function
from scipy.stats import ttest_ind

#find p-value
test_stat, p_value = ttest_ind(time_new_page_arr, time_old_page_arr, equal_var = False, alternative="greater")
#we make sure that we placed the new page array before the old page array since our operator is "greater"

print("The p-value is ", p_value)

"""### Step 6: Compare the p-value with $\alpha$"""

if p_value < 0.05:
  print("We reject the null hypothesis")
else:
  print("We fail to reject the null hypothesis")

"""### Step 7:  Draw inference

As the p-value is less than the level of significance (0.05), we have enough evidence to reject the null hypothesis. We have enough evidence to support the claim that users spend longer on the new landing page than on the old landing page.

**A similar approach can be followed to answer the other questions.**

## 2. Is the conversion rate (the proportion of users who visit the landing page and get converted) for the new page greater than the conversion rate for the old page?

###Visual Analysis
"""

pd.crosstab(abtest['landing_page'], abtest['converted']).plot(kind='bar', stacked=True)
plt.legend()
plt.show()

"""Observations: From this bar graph we can infer that the new landing page has a larger proportion of converted users than the old landing page. But we need to perform a statistical analysis to confirm that this is true.

###Step 1: Define Null and Alternative Hypothesis

**Null Hypothesis:** The conversion rate for the new page is greater than the conversion rate for the old page.

**Alternative Hypothesis:** The conversion rate for the new page is greater than the conversion rate for the old page.

The is another one-tailed test for comparing sample proportions, since the alternative hypothesis is that one of the proportions is greater than the other (as opposed to just "different than").

### Choose Appropriate Test

As this is a test of equality of proportion (conversion rate) between two samples, we choose the 2-sample z-test for proportions.

The assumptions of this test are satisfied:
- Binomially distributed population - The visitor either subscribes or they do not
-Independent populations - yes
- Random sampling from the popuation - Yes, we are informed that the collected sample is a random sample.
- The binomial distribution can be approximated to a normal distribution -
See below for calculation to check whether np and n(1-p) are greater than or equal to 10, where n is equal to the sample size and p is equal to the sample proportion.
"""

#create contingency table to get numbers for calculations
#we will use the number of "yes"s and the total number of visitors (50) for both the new and old landing page for our calculations

contingency_table = pd.crosstab(abtest['landing_page'], abtest['converted'], margins=True)
contingency_table

"""**New:**

np1 = 50 * 33/50 = 33 > 10

n(1-p1) = 50 * (50-33)/50 = 17 > 10


**Old:**

np2 = 50 * 21/50 = 21 > 10

n(1-p2) = 50 * (50-21)/50 = 29 > 10

**Conclusion:**

Since np1, np2, n(1-p1), and n(1-p2) are all greater than 10, we can approximate the binomial distribution to a normal distribution.

All Z-test assumptions are satisfied.

### Step 3: Decide Significance Level

The significance level will be 0.05.

### Step 4: Collect and Prepare Data
"""

#create array of counts of converted users
converted_count = np.array([33, 21])

#create array of sample sizes (total users for each landing page)
sample_sizes = np.array([50, 50])

"""###Step 5: Calculate the p-value"""

#import the required function
from statsmodels.stats.proportion import proportions_ztest

test_stat, p_value = proportions_ztest(converted_count, sample_sizes, alternative='larger')
#note that in the converted_count and sample_sizes arrays, the respective value for the new page was listed first and we can therefore use the 'larger' alternative parameter

print("The p-value is ", p_value)

"""###Step 6: Compare p-value with level of significance (0.05)"""

if p_value < 0.05:
  print("We reject the null hypothesis")
else:
  print("We fail to reject the null hypothesis")

"""###Step 7: Draw Inference

As the p-value is less than the level of significance, we reject the null hypothesis. We have enough evidence to claim that the conversion rate for visitors using the new landing page is higher than the conversion rate for visitors using the old landing page.

## 3. Is the conversion and preferred language are independent or related?

###Visual Analysis
"""

pd.crosstab(abtest['converted'], abtest['language_preferred']).plot(kind='bar', stacked=True)
plt.legend()
plt.show()

"""Observations:

The proportion of colors representing different languages vary slightly, but not to a notable degree. It appears there is slightly less English preference among the not converted group. There also appears to there is slightly more English preference among the converted group.  We will perform a statistical analysis to see if the difference is significant enough that these variables are considered dependent.

###Step 1: Define null and alternative hypotheses

**Null hypothesis:** Conversion and preferred language are independent.

**Alternative hypothesis:** Conversion and preferred language are not independent.

###Step 2: Select Appropriate Test

As this problem is a test of independence for two categorical cariables, we can use the Chi-Square Test of Independence.

The assumptions for this test are satisfied:

-Both language preferred and converted status are categorical variables

-The expected value of the number of sample observations in each level of the variable is at least 5

-The problem statement confirms simple random sampling from the population.

###Step 3: Decide the significance level

The significance level is 0.05.

###Step 4: Collect and prepare data
"""

#create a contingency table to compare the two columns and their proportions
contingency_table = pd.crosstab(abtest['converted'], abtest['language_preferred'])
contingency_table

"""###Step 5: Calculate the p-value"""

#import required function
from scipy.stats import chi2_contingency

chi, p_value, dof, expected = chi2_contingency(contingency_table)
print("The p-value is", p_value)

"""###Step 6: Compare the p-value with the level of significance"""

if p_value < 0.05:
  print("We reject the null hypothesis")
else:
  print("We fail to reject the null hypothesis")

"""###Step 7: Draw inference

As the p-value is higher than the level of significance, we fail to reject the null hypothesis. We do not have enough evidence to claim that conversion and language preference are dependent.

## 4. Is the time spent on the new page same for the different language users?

###Visual Analysis
"""

#create a data frame that just includes the new landing page

new_only = abtest[abtest['landing_page']=='new']
new_only.head() #checking the new data frame

#visualize different language preferences and time spent on the new page with a boxplot
sns.boxplot(x=new_only['language_preferred'], y=new_only['time_spent_on_the_page'])
plt.show()

#printing the means of time spent on the page for the 3 different languages
new_only.groupby(['language_preferred'])['time_spent_on_the_page'].mean()

"""Observations: The Spanish and French means are more similar to each other (smaller) than to the English mean (a little higher). The English and French medians are the furthest apart according to the boxplot. English has the highest range of values, French has the second highest and Spanish has the lowest range.

###Step 1: Define the null and alternative hypotheses

**Null Hypothesis:** The time spent on the new page for the different languages are all the same.

**Alternative Hypothesis:** The time spent on the new page for the different language are not all the same (i.e, there is at least one that differs).

###Step 2: Select Appropriate Test

Since we are comparing sample means from 3 (more than 2) independent populations, based on one factor (language), we will use the one-way ANOVA test.

We will first test if the assumptions are satisfied:

- The populations are normally distributed - we will test with Shapiro Wilk's test

- Population variances are equal - we will test with the Levene test

- The samples are independent simple random samples - we already know this is true from the problem statement.
"""

#Shapiro-Wilk's test to test for normal distribution

#import required function
from scipy import stats

w, p_value = stats.shapiro(new_only['time_spent_on_the_page'])
print("The p-value is ", p_value)

"""The null hypothesis for the Shapiro-Wilk's test is that the time spent on the new page follows a normal distribution. Because the p-value is large, we fail to reject the null hypothesis that the repsonse follows a normal distribution."""

#Levene's test

#import the required function
from scipy.stats import levene

#create variables for the time_spent_on_the_page values of each language to enter into the function
English = new_only['time_spent_on_the_page'][new_only['language_preferred']=='English']
Spanish = new_only['time_spent_on_the_page'][new_only['language_preferred']=='Spanish']
French = new_only['time_spent_on_the_page'][new_only['language_preferred']=='French']

stat, p_value = levene(English, Spanish, French)
print("The p-value is ", p_value)

"""The null hypothesis for the Levene's test is homogeneity of variances in regards to the time spent on the new landing page between different languages. As the p-value is large, we fail to reject the null hypothesis of homogeneity of variances.

**Conclusion:** Now that we have confirmed that the time spent on the page follows a normal distribution and that there is a homogenity of variances between the three languages, We can confirm that the assumptions for the ANOVA test are satisfied.

###Step 3: Decide the significance level

The significance level is 0.05.

###Step 4: Collect and Prepare Data

We have already subsetted our data frame into time spent on the new page by each of the languages.

###Step 5: Calculate the p-value
"""

#import required function
from scipy.stats import f_oneway

test_stat, p_value = f_oneway(English, Spanish, French) #using the subsetted dataframe we used in the levene's test
print("The p-value is ", p_value)

"""###Step 6: Compare the p-value to the level of significance"""

if p_value < 0.05:
  print("We reject the null hypothesis")
else:
  print("We fail to reject the null hypothesis")

"""###Step 7: Draw Inference

Since the p-value is larger than the level of significance (0.05), we fail to reject the null hypothesis that the time spent on the new page between different languages is the same. We do not have enough evidence to claim that the amount of time spent on one or more languages is significantly different than the others.

## Conclusion and Business Recommendations

We can now accurately answer the original objective questions for the company and offer recommendations:

- Do the users spend more time on the new landing page than on the existing landing page? Yes.

- Is the conversion rate for the new page greater than the conversion rate for the old page? Yes.

- Does the converted status depend on the preferred language? No.

- Is the time spent on the new page the same for the different language users? No.

Based on these questions, we can recommend that the company use the new landing page instead of the old to increase time spent on the page and likelihood of a user subscribing. We can also recommend that the company continue to utilize the webpage in English, Spanish and French as there is not one or more languages that differ from the others in terms of time spent on the new page.

___
"""