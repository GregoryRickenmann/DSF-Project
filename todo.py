# select datasets
# preprocessing
# replace NaN values, check outliers, check duplicates
# time series decomposition (check with ADF)
# ACF/PACF interpretation: AR/MA or ARMA 
# split into train and test before standardization
# rolling CV because you cannot shuffle time series data
# Based on interpretation define features + fit ARIMA model 
# calculate forecasting error (MSE?) and tune hyperparameters
# validate model on validation set

#-->baseline prediction

#preprocess other datasets
#normalize them to correct time scale
#decompose
#multivariate time series prediction via random forest 

#important: split into train, test and validate!