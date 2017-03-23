"""
Use the power_data.csv file AND the zipcode database
to answer the questions below.  Make sure all answers
are printed in a readable format. (i.e. "The city with the highest electricity cost in Illinois is XXXXX."

The power_data dataset, compiled by NREL using data from ABB,
the Velocity Suite and the U.S. Energy Information
Administration dataset 861, provides

average residential,
average commercial,
average industrial

electricity rates by zip code for
both investor owned utilities (IOU) and non-investor owned
utilities. Note: the file includes average rates for each
utility, but not the detailed rate structure data found in the
OpenEI U.S. Utility Rate Database.

This is a big dataset.
Below are some questions that you likely would not be able
to answer without some help from a programming language.
It's good geeky fun.  Enjoy.

FOR ALL THE RATES, ONLY USE THE BUNDLED VALUES (NOT DELIVERY).
This rate includes transmission fees and grid fees that are part of the true rate.
"""
import csv, sys
from operator import itemgetter

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D as Patch

with open("power_data.csv") as tsv:
    data = list(csv.reader(tsv))
with open("free-zipcode-database-Primary.csv") as tsv:
    zip_data = list(csv.reader(tsv))

labels = data[0]
zip_labels = zip_data[0]
data = data[1:]
zip_data = zip_data[1:]
print(labels)
print(zip_labels)
print()

# 1  What is the average residential rate for YOUR zipcode?
# You will need to read the power_data into your program to answer this.  (7pts)
my_zipcode = 60614
for dat in data:
    if int(dat[labels.index('zip')]) == my_zipcode:
        my_rate = dat[labels.index('res_rate')]
print("What is the average residential rate for YOUR zipcode?\nMy zipcode is", my_zipcode, "and my rate is", my_rate,
      "\n")

# 2 What is the MEDIAN rate for all BUNDLED RESIDENTIAL rates in Illinois?
# Use the data you extracted to check all "IL" zipcodes to answer this. (10pts)

my_state = "IL"
my_service = "Bundled"
my_rate = []
for dat in data:
    if dat[labels.index('state')] == my_state and dat[labels.index('service_type')] == my_service:
        my_rate.append(float(dat[labels.index('res_rate')]))
my_rate.sort()
my_median = my_rate[len(my_rate) // 2]
print("What is the MEDIAN rate for all BUNDLED RESIDENTIAL rates in Illinois?\nMy state is", my_state,
      "and my service is", my_service, "and my median is", my_median, "\n")

# 3 What city in Illinois has the lowest residential rate?  Which has the highest?
# You will need to go through the database and compare each value for this one.
# Then you will need to reference the zipcode dataset to get the city.  (15pts)
message = [80, 76, 69, 65, 83, 69, 32, 87, 65, 73, 84, 58, 32, 82, 85, 78, 78, 73, 78, 71, 32, 84, 72, 73, 83, 32, 84,
           65, 75, 69, 83, 32, 65, 32, 82, 69, 65, 76, 76, 89, 32, 82, 69, 65, 76, 76, 89, 32, 82, 69, 65, 76, 76, 89,
           32, 82, 69, 65, 76, 76, 89, 32, 86, 69, 82, 89, 32, 76, 79, 78, 71, 32, 84, 73, 77, 69, 46, 46, 46, 32, 46,
           46, 46, 32, 46, 46, 46]

bar_value = 1190 // (len(message) - 2)

i = 0
my_state = "IL"
my_rate = []
for n in range(len(data)):
    dat = data[n]
    if dat[labels.index('state')] == my_state:
        if not n % bar_value:
            sys.stdout.write(chr(message[i]))
            i += 1
            sys.stdout.flush()
        for zdat in zip_data:
            if dat[labels.index('zip')] == zdat[zip_labels.index("Zipcode")]:
                my_rate.append(
                    [float(dat[labels.index('res_rate')]), dat[labels.index('zip')], zdat[zip_labels.index("City")],
                     zdat])
                break
my_rate = sorted(my_rate, key=itemgetter(0))
my_lowest = my_rate[0][2]
my_highest = my_rate[len(my_rate) - 1][2]
print("\n\nWhat city in Illinois has the lowest residential rate?  Which has the highest?\nThe lowest is", my_lowest,
      "and the highest is", my_highest, "\n")

# FOR #4  CHOOSE ONE OF THE FOLLOWING TWO PROBLEMS. The first one is easier than the second.
# 4  (Easier) USING ONLY THE ZIP CODE DATA...
# Make a scatterplot of all the zip codes in Illinois according to their Lat/Long.
# Make the marker size vary depending on the population contained in that zip code.
# Add an alpha value to the marker so that you can see overlapping markers.

# 4 (Harder) USING BOTH THE ZIP CODE DATA AND THE POWER DATA...
# Make a scatterplot of all zip codes in Illinois according to their Lat/Long.
# Make the marker red for the top 25% in residential power rate.
# Make the marker yellow for the middle 25 to 50 percentile.
# Make the marker green if customers pay a rate in the bottom 50% of residential power cost.
# This one is very challenging.  You are using data from two different datasets and merging them into one.
# There are many ways to solve. (20pts)

plt.figure(figsize=[7, 10], tight_layout=True)

x, y, size, color_list = list(), list(), list(), list()

maximum = my_rate[len(my_rate) - 1][0]
minimum = my_rate[0][0]

difference = maximum - minimum

colors = ['green', 'yellow', 'red']

for rate in my_rate:
    if rate[0] < maximum - difference * .50:
        color_list.append(colors[0])
    elif rate[0] < maximum - difference * .25:
        color_list.append(colors[1])
    else:
        color_list.append(colors[2])
    dat = rate[3]
    if dat[zip_labels.index('State')] == 'IL':
        y.append(float(dat[zip_labels.index('Lat')]))
    if dat[zip_labels.index('State')] == 'IL':
        x.append(float(dat[zip_labels.index('Long')]))
    if dat[zip_labels.index('EstimatedPopulation')] and dat[zip_labels.index('State')] == 'IL':
        size.append(float(dat[zip_labels.index('EstimatedPopulation')]) / 100)

plt.scatter(x, y, size, color=color_list, alpha=0.5)

plt.show()
