import numpy as np
import pandas as pd
#import math
#import random
#from numpy.linalg import *
from sklearn.impute  import SimpleImputer
from calculate_glass_binary_bayesian import calculate_accuracy, calculate_accuracy_naive
#from sklearn.preprocessing import Binarizer
#from sklearn import datasets

################################################################################################################################################
#load data
data = pd.read_excel("data/generated_binary_data.xlsx", index_col=None, header=None)
data = data.transpose()

#data = data.drop(data.columns[[0]], axis=1) 
#print (data)

#read Data
#data = pd.read_csv("glass3.data", names = ['Index', 'RI', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Potassium', 'Calcium', 'Barium', 'Iron','class'])
#data = data.drop('Index',axis=1)
#print "Original data:", data

print ("Original data shape:", data.shape)
#print data
np.seterr(divide = 'ignore') 
np.seterr(all = 'ignore') 

################################################################################################################################################
#check if missing value (cleaning)
missing_values = ["n/a", "na", "--","?", " ","NA"]
data = data.replace(missing_values, np.nan)
feat_miss = data.columns[data.isnull().any()]
if feat_miss.size == 0:
    print ("Data is clean")
else:
    print ("Missing data shape before:", feat_miss.shape)
    imputer = SimpleImputer(copy=True, fill_value=None, missing_values=np.nan, strategy='calculate_iris', verbose=0)
    data[feat_miss] = imputer.fit_transform(data[feat_miss])
    feat_miss = data.columns[data.isnull().any()]
    print ("Missing data shape after:", feat_miss.shape)

################################################################################################################################################
cols = ['RI', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Potassium', 'Calcium', 'Barium', 'Iron','class']
#binarization
def get_binary(dataset):
    
    features = dataset.shape[1]
    #print (features)    
    dataset = dataset.iloc[:,:]
    datacol = np.array(dataset.iloc[1:,-1])
    datacol = np.reshape(datacol,(datacol.shape[0],1))
    dataset =  dataset.iloc[1:,:features-1].values 
    #dataset.astype(float) 
    '''
    meanValue = np.reshape(np.mean(dataset,axis=0), (1, features-1))
    #print (meanValue)          
    
    dataset[dataset < meanValue] = 0.0
    dataset[dataset > meanValue] = 1.0
    '''
    #print (dataset)
       
    dataset = np.reshape(dataset,(dataset.shape[0], dataset.shape[1]))
    
    dataset = np.concatenate((dataset, datacol), axis = 1)
    #print (datacol.shape, dataset.shape)
    np.random.shuffle(dataset)
    dataset = pd.DataFrame(dataset, columns = cols)
    return dataset

data = data.iloc[:, 1:].values
data = pd.DataFrame(data, columns = cols)
data = get_binary(data)  #bluff, conversion
print ("Shape after shuffling", data)

################################################################################################################################################
#removed head and index and convert to numpy array
data = data.iloc[:, :].values    #np.random.shuffle(data)     print data.size
#print "Cleaned data:", data [175,:]
print ("Cleaned data shape:", data.shape)

################################################################################################################################################
#data Training
features = np.size(data,1)-1 # 149  #column    [all columns except last one as it has predicted class]
#print features
samples = np.size(data,0)  #row

################################################################################################################################################
#class finding
totalClass = data[:, features]
totalClass = (np.sort(np.unique(np.array(totalClass))))
totalClass = np.reshape(totalClass,[totalClass.size,1]) #convert to (*,1) array
print ("classes: ", totalClass)

################################################################################################################################################
fold = 5
foldSize = (int)(((float)(samples)/fold))
print ("fold Size: ", foldSize)

################################################################################################################################################
#pure test data
data_test = data[:(samples-fold*foldSize),:]

################################################################################################################################################
splitArray = np.split(data[:(fold*foldSize),:], fold)
print ("Each split size: ", splitArray[0].shape)
print ("Total split: ", len(splitArray))

################################################################################################################################################
#call method
print ("For fold starts for optimal bayesian")
accuracy = []
for i in range(fold-1):    
    
    training_idx = []    
    
    test_idx = splitArray[i]
    for j in range(len(splitArray)):
        if j !=i:
            training_idx.append(splitArray[i])
            
    training_idx = np.array(np.concatenate((training_idx), axis=0))
    #print training_idx, training_idx.shape   

    data_train, data_cv_test = training_idx, test_idx
    #print "Train data Set: ", data_train.shape    
    #print "CV Test data Set: ", data_cv_test.shape   
  
    print ("For fold starts: ", (i+1))
    accuracyVal = calculate_accuracy(data_train,features,data_cv_test,totalClass,foldSize)
    accuracy.append(accuracyVal)
    print ("For fold ends ")

################################################################################################################################################
#call method
print ("For fold starts for naive bayesian")
accuracy2 = []
for i in range(fold-1):    
    
    training_idx = []    
    
    test_idx = splitArray[i]
    for j in range(len(splitArray)):
        if j !=i:
            training_idx.append(splitArray[i])
            
    training_idx = np.array(np.concatenate((training_idx), axis=0))
    #print training_idx, training_idx.shape   

    data_train, data_cv_test = training_idx, test_idx
    #print "Train data Set: ", data_train.shape    
    #print "CV Test data Set: ", data_cv_test.shape   
  
    print ("For fold starts: ", (i+1))
    accuracyVal = calculate_accuracy_naive(data_train,features,data_cv_test,totalClass,foldSize)
    accuracy2.append(accuracyVal)
    print ("For fold ends ")

################################################################################################################################################
print ("Average Cross Validation Accuracy for bayesian: ", sum(accuracy) / len(accuracy))

################################################################################################################################################
print ("Average Cross Validation Accuracy for naive bayes: ", sum(accuracy2) / len(accuracy2))
