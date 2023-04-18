'''raman_pulse_plot.py

A script to find the width of the pulses generated in the Raman pulse scan by 
the Arduino MKR Vidor'''


import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import matplotlib.ticker as ticker


fig, axs = plt.subplots(4, 5, sharey=True)
fig1, ax1 = plt.subplots(1, figsize=(5,2))
# print(axs.flatten())


path = r"Analysis\data\mach_zehnder\rabi_pulse_data.csv"


def get_data(path):
    '''
    Args:
        path, string - the path of the data file to be loaded
    Returns:
        times, numpy array - array of times of data points
        ch1, numpy array - array of y values
    '''


    df = pd.read_csv(path)
    col1= df.iloc[19:, 0].values
    times = np.array(list(map(float, col1)))

    col2= df.iloc[19:, 1].values
    ch1 = np.array(list(map(float, col2)))

    return times, ch1


def get_range(arr1, arr2, ll, ul):
    '''
    Gets the x or y values in between 2 limits

    Args:
        arr1, array - array of values to search within
        arr2, array - array to get values of
        ll, float - lower limit of search
        ul, float - upper limit of search
    '''


    time_index = np.where((ll < arr1) & (arr1 < ul))
    ch_index = np.where((ll < arr1) & (arr1 < ul))

    time_data = arr1[time_index]
    ch_data = arr2[ch_index]
    return time_data, ch_data


data = get_range(*get_data(path), 0.0, 0.020)

# ax.plot(*get_data(path))


for count, ax in enumerate(axs.flatten()):
    #print(count, ax)
    if count >= 0:
        ax.plot(*get_range(*data, count/1000 - 0.0001, count/1000 +  0.0004 ))


fig.text(0.5, 0.03, 'Time (s)', ha='center')
fig.text(0.04, 0.5, 'Voltage (V)', va='center', rotation='vertical')


def get_line(x1, y1, x2, y2):
    '''
    calculates the equation of a line for finding the full width at half maximum
    for the raman pulses.

    Args: 
    x1, float - first x point
    y1, float - y value at x1
    x2, float - second x point
    y2, float - y value at x2
    '''


    points = [(x1,y1), (x2,y2)]
    x_coords, y_coords = zip(*points)
    x_coords = np.array(x_coords).flatten()
    # print( np.ones(len(x_coords)))
    A = np.vstack([x_coords, np.ones(len(x_coords))]).T
    m, c = np.linalg.lstsq(A, y_coords, rcond=None)[0]
    return m, c


def get_widths(data, height):
    '''
    gets the widths between pulses, or widths of pulses

    Args: 
        data, array - data for the pulses to be found in. 

    height, float - the height at which points should be looked for, for length
    of high pulses this should be approx 3.3V for low pulses this should be
    approx 0V
    '''


    widths = []

    for i, ax in enumerate(axs.flatten()):
        x_data, y_data = get_range(*data, i/1000 - 0.0001, i/1000 +  0.0004 )
 
        ll = height - 0.2
        ul = height + 0.2
        index = np.where((ll < y_data) & (y_data < ul))
        x_points = x_data[index]
        y_points = y_data[index]
        ax.plot(x_points, y_points, marker="o", mfc="red")
        # print(f"widths {x_points}")

        if len(x_points) == 1:
            index = index[0]
            print(index)
            # print(x_data)
            l_point_x = x_data[index - 1]
            l_point_y = y_data[index - 1]
            r_point_x = x_data[index + 1]
            r_point_y = y_data[index + 1]
            center_x = x_data[index]
            center_y = y_data[index]

            ax.plot(l_point_x, l_point_y, color="None", mfc = "purple", marker="o")
            ax.plot(r_point_x, r_point_y, color="None", mfc = "purple", marker="o")
            ax.plot(center_x, center_y, color="None", mfc = "purple", marker="o")


            l_m, l_c = get_line(l_point_x, l_point_y, center_x, center_y)
            r_m, r_c = get_line(r_point_x, r_point_y, center_x, center_y)
            
            half_y = center_y/2 

            l_x = (half_y - l_c) / l_m
            r_x = (half_y - r_c) / r_m


            width = r_x - l_x
            widths.append(width)
            ax.plot([l_x, r_x],[half_y, half_y], color="black", alpha = 0.5)

        if len(x_points) >= 2:
            # print("wide")
            index = index[0]
            left_index,right_index = index[0], index[-1]

            l_center_x, l_center_y = x_points[0], y_points[0]
            r_center_x, r_center_y = x_points[-1], y_points[-1]

            l_point_x, l_point_y = x_data[left_index - 1], y_data[left_index - 1]
            r_point_x, r_point_y = x_data[right_index + 1], y_data[right_index + 1]

            ax.plot(l_point_x, l_point_y, marker = "o", mfc = "pink", color="pink")
            ax.plot(r_point_x, r_point_y, marker = "o", mfc = "pink", color="hotpink")

            l_m, l_c = get_line(l_point_x, l_point_y, l_center_x, l_center_y)
            r_m, r_c = get_line(r_point_x, r_point_y, r_center_x, r_center_y)

            avg_y = np.mean(y_points)
            half_height = avg_y / 2

            l_x = (half_height - l_c) / l_m
            r_x = (half_height - r_c) / r_m

            width = r_x - l_x
            widths.append(width)

            ax.plot([l_x, r_x],[half_y, half_y], color="black", alpha = 0.5)
    widths=widths[1:]
    return widths

widths = get_widths(data, 3.3)
print(f"widths = {widths}")
x = range(1, len(widths) + 1)

ax1.errorbar(x, widths, yerr=4e-6, color="blue", ecolor="black", capsize = 2, label="actual")
ax1.plot([4,8,12,16],[4e-6,8e-6,12e-6,16e-6], marker = "o", color="none", mfc="green", mec="green")
ax1.grid()
ax1.set_xticks(x)
ax1.set_xlabel("Pulse number")
ax1.set_ylabel("Pulse Length ($\mu s$)")
expected_y = np.array(range(1,20))/1e+6
ax1.plot(x, expected_y, color="red", label="expected")

fig.tight_layout()

scale_y = 1e-6
ticks_y= ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y/scale_y))
ax1.yaxis.set_major_formatter(ticks_y)

y_ticks = []
for i in range(0, 25):
    if i%4 == 0:
        y_ticks.append(i)

y_tick_arr = np.array(y_ticks)/1e+6
ax1.set_yticks(y_tick_arr)

ax1.legend()

plt.show()