
import math

import pandas
import numpy

def mark_onoff(series, on_threshold, off_threshold, initial=None, on_state=1, off_state=0):
    #print(series)

    if initial is None:
        state = off_state
    else:
        state = initial

    times = []
    events = []
    
    values = []
    value_times = []
    
    #value_times.append(0.0)
    #values.append(0 if state == off_state else 1)

    for idx, data in zip(series.index, series):
        if state is None:
            state = on_state if data > on_threshold else off_state
            times.append(idx)
            events.append(state)
        elif state == off_state and data > on_threshold:
            state = on_state
            times.append(idx)
            events.append(state)          
        elif state == on_state and data < off_threshold:
            state = off_state
            times.append(idx)
            events.append(state)
        else:
            pass
        
        value_times.append(idx)
        values.append(0 if state == off_state else 1)
    
    s = 1 if series.iloc[-1] > off_threshold else 0
    t = series.index[-1]
    print('last', s, t)
    value_times.append(t)
    values.append(s)
    times.append(t)
    events.append(s)

    #values.append(0 if state == off_state else 1)

    sparse = pandas.Series(events, index=times)
    dense = pandas.Series(values, index=value_times)
    return sparse, dense
    
def matplotlib_time(pandas_time):
    import matplotlib.dates as mdates
    val = mdates.date2num(pandas_time)
    return val


def join_events(series):
    starts = series[series == 1]
    ends = series[series == 0]
    
    df = pandas.DataFrame({
        'start': starts.index,
        'end': ends.index,
    })
    return df

def merge_consecutive(df, col='class'):
    
    # Group where consequtive values are the same
    groups = df.groupby((df[col].shift() != df[col]).cumsum())
    
    dist = df.reset_index()['index'].diff().iloc[-1]
    
    outs = []
    for idx, g in groups:
        #print('fff')
        start, end = g.index[0], (g.index[-1] + dist)
        val = g[col].iloc[0]
        
        outs.append({
            'start': start,
            'end': end,
            col: val,
        })
        
        #print(idx, val, g.index[0], g.index[-1])

    df = pandas.DataFrame.from_records(outs)
    return df


def map_linear(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    if leftSpan == 0.0:
        valueScaled = 0.0
    else:
        valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def constrain(value, lower, upper):

    if value > upper:
        value = upper
    if value < lower:
        value = lower

    return value
    

def next_power_of_2(x):
    return 2**(math.ceil(math.log(x, 2)))



