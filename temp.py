import pandas as pd
import numpy as np
import PyQt5
import matplotlib.pyplot as plt
plt.ion()
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
from keras.models import Sequential
from keras.layers import LSTM,Dropout,Dense
from sklearn.preprocessing import MinMaxScaler

def predict(file,zzz):
    
    file=str(file.get()).replace("/","\\\\")
    df=pd.read_csv(file)
    df.head()
    
    #creating dataframe
    data = df.sort_index(ascending=True, axis=0)
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
    for i in range(0,len(data)):
        new_data['Date'][i] = data['Date'][i]
        new_data['Close'][i] = data['Close'][i]
    
    #setting index
    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)
    
    #creating train and test sets
    dataset = new_data.values
    train = dataset[0:zzz,:]
    valid = dataset[zzz:,:]
    
    #converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    
    x_train, y_train = [], []
    for i in range(60,len(train)):
        x_train.append(scaled_data[i-60:i,0])
        y_train.append(scaled_data[i,0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    
    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)
    
    #predicting 246 values, using past 60 from the train data
    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)
    
    X_test = []
    for i in range(60,inputs.shape[0]):
        X_test.append(inputs[i-60:i,0])
    X_test = np.array(X_test)
    
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    
    print(closing_price)
    rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
    print(rms)
    
    train = new_data[:zzz]
    valid = new_data[zzz:]
    valid['Predictions'] = closing_price
    plt.title("RMS = "+str(rms))
    plt.ylabel('Price')
    plt.plot(train['Close'])
    plt.plot(valid[['Close','Predictions']])
    print(valid['Predictions'])
#predict("C:\\Users\\Mahender Chowdary\\Downloads\\FB.csv",2000)  