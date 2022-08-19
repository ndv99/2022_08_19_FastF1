import fastf1
import numpy as np
import pandas
from fastf1 import plotting as ff1_plotting
from itertools import groupby
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import colorbar
from matplotlib.collections import LineCollection
from matplotlib.ticker import MaxNLocator
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

fastf1.Cache.enable_cache("fastf1_cache")
ff1_plotting.setup_mpl()

def madness_in_germany():
    with suppress_stdout_stderr():
        session = fastf1.get_session(2019, "Germany", "R")
        session.load()
    
    drivers = pandas.unique(session.laps['Driver'])

    results = {}
    grid = {}

    for driver in drivers:
        results[driver] = session.get_driver(driver)['Position']
        grid[driver] = session.get_driver(driver)['GridPosition']

    driver_positions = {}

    for driver in grid:
        driver_positions[driver] = {
            "Name": session.get_driver(driver)['FullName'],
            "Positions": [grid[driver]],
            "Laps": [0]
            }
    

    lapsobj = session.laps.iterlaps()
    all_laps = []
    
    for lap in lapsobj:
        all_laps.append({"LapNumber": lap[1]['LapNumber'], "Time": lap[1]['Time'], "Driver": lap[1]['Driver']})
    
    def sortLapsByNumber(lap):
        return lap["LapNumber"]

    def sortLapsByTime(lap):
        return lap["Time"]
    
    all_laps.sort(key=sortLapsByNumber)

    for key, value in groupby(all_laps, sortLapsByNumber):
        # print(f"Lap {key}")
        value_as_list = list(value)
        value_as_list.sort(key=sortLapsByTime)
        for x in range(len(value_as_list)):
            v = value_as_list[x]
            driver_positions[v['Driver']]['Positions'].append(x+1)
            driver_positions[v['Driver']]['Laps'].append(v['LapNumber'])
    
    fig, ax = plt.subplots()

    colors_used = []
    
    for driver in driver_positions:
        color = session.get_driver(driver)['TeamColor']
        if color not in colors_used:
            colors_used.append(color)
            ax.plot(driver_positions[driver]['Laps'], driver_positions[driver]['Positions'], label=driver_positions[driver]['Name'], color=f"#{color}")
        else:
            ax.plot(driver_positions[driver]['Laps'], driver_positions[driver]['Positions'], label=driver_positions[driver]['Name'], color=f"#{color}", linestyle="dashed")

    
    ax.set_xlabel("Lap number")
    ax.set_ylabel("Position")
    
    ax.set_title("German Grand Prix 2019")
    ax.legend()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.yticks(np.arange(1, 21, 1.0))
    plt.gca().invert_yaxis()
    plt.show()

    print("")
    print("")
    print("")
    print("")
    print("\nDONE!!!!")


def fastest_ever_lap():
    with suppress_stdout_stderr():
        colormap = cm.plasma

        session = fastf1.get_session(2020, "Monza", "Q")
        session.load()

        # Get telemetry
        lap = session.laps.pick_driver("HAM").pick_fastest()
        x = lap.telemetry['X']              # values for x-axis
        y = lap.telemetry['Y']              # values for y-axis
        color = lap.telemetry['Speed']      # value to base color gradient on

        # Create line segments
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Create empty plot with title
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(f'Monza 2020 Qualifying - Lewis Hamilton - Speed', size=24, y=0.97)

        # Adjust margins and turn of axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')

        # Create background track line
        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

        # Set the values used for colormapping
        lc.set_array(color)

        # Merge all line segments together
        line = ax.add_collection(lc)

        # Create a color bar as a legend.
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = colors.Normalize(vmin=color.min(), vmax=color.max())
        legend = colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

        plt.show()
    print("")
    print("")
    print("")
    print("")
    print("\nDONE!!!!")

def max_vs_charles_imola_2022():

    with suppress_stdout_stderr():
        session = fastf1.get_session(2022, "Imola", "Q")
        session.load()

        # Get data for Leclerc
        lec_fastest = session.laps.pick_driver("LEC").pick_fastest()
        lec_car_data = lec_fastest.get_car_data()
        lec_time = lec_car_data['Time']
        lec_speed = lec_car_data['Speed']

        # Get data for Verstappen
        ver_fastest = session.laps.pick_driver("VER").pick_fastest()
        ver_car_data = ver_fastest.get_car_data()
        ver_time = ver_car_data['Time']
        ver_speed = ver_car_data['Speed']

    # Plotting

    fig, ax = plt.subplots()

    ax.plot(lec_time, lec_speed, label="Charles Leclerc", color="red")
    ax.plot(ver_time, ver_speed, label="Max Verstappen", color="blue")

    ax.set_xlabel('Time')
    ax.set_ylabel('Speed [Km/h]')

    ax.set_title("Leclerc vs Verstappen in Imola Q3 2022")
    ax.legend()
    plt.show()
    print("")
    print("")
    print("")
    print("")
    print("\nDONE!!!!")

def menu_loop():
    print("\nWelcome to Nick's hacked-together last-minute F1 data CLI!\n")
    exited = False
    while not exited:
        print("Please select an option:")
        print("1. Verstappen vs Leclerc in Imola Quali 3, 2022")
        print("2. The fastest ever F1 lap (Hamilton Monza Quali 3 2020)")
        print("3. Madness - 2019 German Grand Prix")
        print("0. Exit")
        userinput = input("> ")
        if userinput == "1":
            max_vs_charles_imola_2022()
        elif userinput == "2":
            fastest_ever_lap()
        elif userinput == "3":
            madness_in_germany()
        elif userinput == "0":
            exited = True
        else:
            print("You numpty. Select a valid option.\n")

if __name__ == "__main__":
    menu_loop()