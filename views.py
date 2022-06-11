from django.http import HttpResponseRedirect, Http404
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as py
from django.shortcuts import render, get_object_or_404

def index(request):
    return render(request, 'index.html')

def prediction(request, state, date):
    new_input = [[state, date]]

    data_path = 'GlobalTemp1970up.csv'
    tempData = pd.read_csv(data_path)

    isState = tempData['State']==state

    tempDataState = tempData[isState]

    feature_cols = 'AverageTemperature'

    X = tempDataState[['dt']]

    X = X.apply(pd.to_numeric,errors='coerce')
    X.fillna(0,inplace=True)


    y = tempDataState[['AverageTemperature']]

    linear = linear_model.LinearRegression()
    #linear.fit(X.reshape(-1, 1), y)
    linear.fit(X,y)
    slope = linear.coef_
    intercept = linear.intercept_

    prediction = round(float(date * slope + intercept), 2)

    data_path2= 'GlobalTemp1970DownFinal.csv'
    tempData2 = pd.read_csv(data_path2)

    state2 = state
    date2 = 19600101


    isState2 = tempData2['State']== 'Texas'

    tempDataState2 = tempData2[isState2]

    X2 = tempDataState2[['dt']]

    X2 = X2.apply(pd.to_numeric,errors='coerce')
    X2.fillna(0,inplace=True)


    y2 = tempDataState2[['AverageTemperature']]

    linear2 = linear_model.LinearRegression()
    #linear.fit(X.reshape(-1, 1), y)
    linear2.fit(X2,y2)
    slope2 = linear2.coef_
    intercept2 = linear2.intercept_

    date1900 = 19000101
    date1970 = 19700101
    date2020 = 20200101

    dif00to70 = (date1970*slope2 + intercept2) - (date1900 * slope2 + intercept2)

    dif70to20 = (date2020*slope+intercept) - (date1970 * slope + intercept)

    tempPredict = (date*slope+intercept)
    dif20toPred = tempPredict - (date2020*slope+intercept)


    print("The increase of temperature in",state,"from 1900 to 1970 was",dif00to70[0][0],"degrees Fahrenheit")
    print("The increase of temperature in",state,"from 1970 to 2020 was",dif70to20[0][0],"degrees Fahrenheit")
    print("The temperature in",state,"in the selected year will be",tempPredict[0][0],"degrees Fahrenheit")
    print("The increase of temperature in",state,"from 2020 to the selected year will be",dif20toPred[0][0],"degrees Fahrenheit")

    diff1 = round(dif00to70[0][0],2)
    diff2 = round(dif70to20[0][0],2)
    diff3 = round(tempPredict[0][0],2)
    diff4 = round(dif20toPred[0][0],2)

    dt = int(str(date)[:4])


    context = {
        'prediction': prediction,
        'state': state,
        'diff1': diff1,
        'diff2': diff2,
        'diff3': diff3,
        'diff4': diff4,
        'date': dt
    }
    return render(request, 'prediction.html', context)
