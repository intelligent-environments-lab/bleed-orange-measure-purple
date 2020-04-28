# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:54:58 2020

@author: CalvinL2
"""
# import os
# import datetime
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# # %% Nan remover
# p2 = pm_vector[~np.isnan(temp_vector)]
# p2 = p2[~np.isnan(pm_vector)]
# t2 = temp_vector[~np.isnan(temp_vector)]
# t2 =  t2[~np.isnan(pm_vector)]
# pm_vector = p2
# temp_vector = t2

# # %%
# plt.figure()
# t = temp_vector-np.min(temp_vector)
# p = pm_vector-np.min(pm_vector)
# plt.plot(abs((t)/np.max(t)),abs(p/np.max(p)),'.')
# a = np.linspace(0,1,100)
# plt.plot(a,a)



# %% Linear Regression

# #https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
# X = temp_vector ## X usually means our input variables (or independent variables)
# y = pm_vector ## Y usually means our output/dependent variable
# X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# # Note the difference in argument order
# model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
# predictions = model.predict(X)

# # Print out the statistics
# model.summary()

# plt.figure()
# plt.plot(abs(predictions/np.max(predictions)),abs(pm_vector/np.max(pm_vector)),'.')
# a = np.linspace(0,1,100)
# plt.plot(a,a)




#eval
#getattr

def timegraph(files,param='pm25'):
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(1, 1, 1)
    
    for file in files:
        if file.hourly[param] is not None:
            plt.plot_date(file.hourly.time, file.hourly[param], 'o-', xdate=True,
                          label=file.sensorname)

    rolling_data = [file[param] for file in files if file[param] is not None]
    avg = sum(rolling_data)/len(rolling_data)
    avg = avg.rolling(window=48).mean()
    plt.plot_date(avg.index.values, avg,
                  '-k', xdate=True, linewidth=4,
                  label='Rolling Average')
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    # ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    ax.grid()
    plt.legend(loc='upper left')
    fig.autofmt_xdate()
    plt.ylim(0, 70)
    plt.xlim([datetime.date(2020, 3, 17), datetime.date(2020, 4, 8)])    
    plt.title(f'Hourly {param} Values from UT PurpleAirs for Mar 1 to Apr 8')
    plt.ylabel('PM 2.5 (ug/m3)')
    plt.xlabel('Time')
    
    fig.savefig(f'output//march_ut_pa_hourly_{param}.svg')