import yfinance as yf
import matplotlib.pyplot as plt


moving_average_points = {}
simulation_tracker = {}

# indicators
def get_ma(data, length):
    values = []
    moving_average = []
    for i in range(len(data)):
        values.append(data[i])
        if i < length:
            # moving_average.append(None)
            moving_average.append(0)
        else:
            moving_average.append(sum(values)/len(values))
            values.remove(values[0])
    return moving_average

    
""" Get the history of a specified stock for a specified amount of time.
For the "t" and "interval" arguments, can use:
    'm' = minute
    'd' = day
    'mo' = month
    'y' = year

:param symbl: Ticker symbol
:param t: amount of time to go back. Default "1000m"
:param interval: time between datapoints. Default "1m"
"""
def get_history(symbl: str, t: str="100m", interval: str="1m"):
    data = yf.Ticker(symbl).history(period=t, interval=interval)
    return data["Close"]


"""
Only care about the last few moments of the moving averages
"""
def update(new_data):
    for ma in moving_average_points:
        moving_average_points[ma].remove(moving_average_points[ma][0])
        moving_average_points[ma].append(new_data)
        
        simulation_tracker[ma].append(moving_average_points[ma])


def decision(new_data):
    # Find current points
    ma_25 = moving_average_points['25']
    ma_50 = moving_average_points['50']
    ma_100 = moving_average_points['100']

    # Find trend directions
    # current
    # 25
    # 50
    # 100

    # if data is "in order" - live -> 25 -> 50 -> 100 and all trends are in the same direction
    # check off first indicator

    # if moving averages start criss-crossing before live data goes past 25
    # uncheck everything

    # if first indicator is checked, then live data goes between 25 and 100
    # check off second indicator 

    # if live data goes beyond 100
    # uncheck everything

    # if first and second indicators are checked, then live data breaks through 25 again
    # take position.  Set take-profit to 1.5%, stop-loss to 1.0%


    


def main():
    ma_values = [25, 50, 100]
    tesla_data = get_history("TSLA")
    moving_averages = {}
    for window in ma_values:
        moving_averages[f"{str(window)}"] = get_ma(tesla_data, window)
        simulation_tracker[f"{str(window)}"] = moving_averages[f"{str(window)}"][window]

    time = tesla_data.index
    current_time_index = max(ma_values)

    while current_time_index < len(time):
        current_time = time[current_time_index]
        update(tesla_data[current_time])
        decision(tesla_data[current_time])
        current_time_index += 1
    

if __name__ == "__main__":
    main()



