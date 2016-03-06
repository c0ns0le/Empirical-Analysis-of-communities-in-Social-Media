import urllib
import pandas as pd
import numpy as np


# define URLs
test_data_url = "https://dl.dropboxusercontent.com/u/8082731/datasets/UMICH-SI650/testdata.txt"
train_data_url = "https://dl.dropboxusercontent.com/u/8082731/datasets/UMICH-SI650/training.txt"

# define local file names
test_data_file_name = 'test_data.csv'
train_data_file_name = 'train_data.csv'

# download files using urlib
test_data_f = urllib.urlretrieve(test_data_url, test_data_file_name)
train_data_f = urllib.urlretrieve(train_data_url, train_data_file_name)

#Loading data into data frames for processing


test_data_df = pd.read_csv(test_data_file_name, header=None, delimiter="\t", quoting=3)
test_data_df.columns = ["Text"]
train_data_df = pd.read_csv(train_data_file_name, header=None, delimiter="\t", quoting=3)
train_data_df.columns = ["Sentiment","Text"]
print(train_data_df.shape)
print(test_data_df.shape)
print(train_data_df.head())
print(test_data_df.head())
print(train_data_df.Sentiment.value_counts())
print( np.mean([len(s.split(" ")) for s in train_data_df.Text]))