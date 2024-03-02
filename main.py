#
#
# Author: Jay Patel
#
# The purpose of this program is to analyze CTA2 L data in Python
# where the data is stored in SQLite. This is a console-based Python
# program that inputs commands from the user and outputs data from 
# the CTA2 L daily ridership database.
#

import sqlite3
import matplotlib.pyplot as plt


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
  dbCursor = dbConn.cursor()

  print("General stats:")

  dbCursor.execute("Select count(*) From Stations;")
  row = dbCursor.fetchone()
  print("  # of stations:", f"{row[0]:,}")

  dbCursor.execute("select count(*) from Stops;")
  row = dbCursor.fetchone()
  print("  # of stops:", f"{row[0]:,}")
  
  dbCursor.execute("select count(*) from Ridership")
  row = dbCursor.fetchone()
  print("  # of ride entries:", f"{row[0]:,}")

  dbCursor.execute("select date(Ride_Date) from Ridership")
  row = dbCursor.fetchall()
  print("  date range:", row[0][0], "-", row[len(row)-1][0])

  dbCursor.execute("select sum(Num_Riders) from Ridership")
  row = dbCursor.fetchone()
  print("  Total ridership:", f"{row[0]:,}")
  total = row[0]
  
  dbCursor.execute("select sum(Num_Riders) from Ridership where Type_of_Day = 'W'")
  row = dbCursor.fetchone()
  percent = ( row[0] / total ) * 100
  print("  Weekday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")
  
  dbCursor.execute("select sum(Num_Riders) from Ridership where Type_of_Day = 'A'")
  row = dbCursor.fetchone()
  percent = ( row[0] / total ) * 100
  print("  Saturday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")
  
  dbCursor.execute("select sum(Num_Riders) from Ridership where Type_of_Day = 'U'")
  row = dbCursor.fetchone()
  percent = ( row[0] / total ) * 100
  print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({percent:.2f}%)")
  print()
  

##################################################################
#
# command_1
#
# Takes a partial station name from the user and retrieves the
# stations that are “like” the user’s input. Outputs station
# names in ascending order.
#
def command_1(dbConn):
  dbCursor = dbConn.cursor()

  partial_station_name = input("\nEnter partial station name (wildcards _ and %): ")

  sql = """select Station_ID, Station_Name from Stations where
           Station_Name like ? order by Station_Name asc;"""
  dbCursor.execute(sql, [partial_station_name])

  rows = dbCursor.fetchall()
  if len(rows) == 0:
    print("**No stations found...")
  else:
    for row in rows:
      print(row[0], ":", row[1])


##################################################################
#
# command_2
#
# Outputs the ridership at each station, in ascending order by
# station name. Along with each value, outputs the percentage
# this value represents across the total L ridership.
#
def command_2(dbConn):
  dbCursor = dbConn.cursor()

  print("** ridership all stations **")

  sql = """select Station_Name, sum(Num_Riders) from Ridership
           join Stations on Ridership.Station_ID = Stations.Station_ID
           group by Stations.Station_Name
           order by Stations.Station_Name asc;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  # variable to store total ridership which is then used to
  # calculate the percentages.
  total_Ridership = "select sum(Num_Riders) from Ridership;"
  dbCursor.execute(total_Ridership)
  total = dbCursor.fetchone()

  for row in rows:
    percentage = ( row[1] / total[0] ) * 100
    print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")


##################################################################
#
# command_3
#
# Outputs the top-10 busiest stations in terms of ridership,
# in descending order by ridership
#
def command_3(dbConn):
  dbCursor = dbConn.cursor()

  print("** top-10 stations **")

  sql = """select Station_Name, sum(Num_Riders) from Ridership 
           join Stations on Ridership.Station_ID = Stations.Station_ID
           group by Stations.Station_Name
           order by sum(Num_Riders) desc
           limit 10;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  # variable to store total ridership which is then used to
  # calculate the percentages.
  total_Ridership = "select sum(Num_Riders) from Ridership;"
  dbCursor.execute(total_Ridership)
  total = dbCursor.fetchone()

  for row in rows:
    percentage = ( row[1] / total[0] ) * 100
    print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")

##################################################################
#
# command_4
#
# Outputs the top-10 least busiest stations in terms of ridership,
# in ascending order by ridership
#
def command_4(dbConn):
  dbCursor = dbConn.cursor()

  print("** least-10 stations **")

  sql = """select Station_Name, sum(Num_Riders) from Ridership 
           join Stations on Ridership.Station_ID = Stations.Station_ID
           group by Stations.Station_Name
           order by sum(Num_Riders) asc
           limit 10;"""
  dbCursor.execute(sql)
  rows = dbCursor.fetchall()

  # variable to store total ridership which is then used to
  # calculate the percentages.
  total_Ridership = "select sum(Num_Riders) from Ridership;"
  dbCursor.execute(total_Ridership)
  total = dbCursor.fetchone()

  for row in rows:
    percentage = ( row[1] / total[0] ) * 100
    print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")


##################################################################
#
# command_5
#
# Inputs a line color from the user and outputs all stop names
# that are part of that line, in ascending order.
#
def command_5(dbConn):
  dbCursor = dbConn.cursor()

  line_color = input("\nEnter a line color (e.g. Red or Yellow): ")

  sql = """select Stop_Name, Direction, ADA from Stops 
           join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           join Lines on StopDetails.Line_ID = Lines.Line_ID
           where Color like ?
           order by Stop_Name asc;"""

  dbCursor.execute(sql, [line_color])

  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No such line...")
    return

  # if ADA value is 1 then 'yes' statement is printed else 'no' is printed
  for row in rows:
    if row[2] == 1:
      print(row[0], ": direction = ", row[1], "(accessible? yes)")
    else:
      print(row[0], ": direction = ", row[1], "(accessible? no)")
  

##################################################################
#
# command_6
#
# Outputs total ridership by month, in ascending order by month.
# After the output, the user is given the option to plot the data.
# 
def command_6(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by month **")

  sql = """select strftime('%m', Ride_Date), sum(Num_Riders) 
           from Ridership group by strftime('%m', Ride_Date) 
           order by strftime('%m', Ride_Date) asc;"""
  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  for row in rows:
    print(row[0], " : ", f"{row[1]:,}")

  plot = input("Plot? (y/n) ")

  if plot != "y":
    return

  # variables to store months in x and number of riders in y.
  x = []
  y = []

  for row in rows:
    x.append(row[0])
    y.append(row[1])

  plt.xlabel("month")
  plt.ylabel("number of riders (x*10^8)")
  plt.title("monthly ridership")

  plt.plot(x, y)
  plt.show()


##################################################################
#
# command_7
#
# Outputs total ridership by year, in ascending order by year.
# After the output, the user is given the option to plot the data.
# 
def command_7(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by year **")

  sql = """select strftime('%Y', Ride_Date), sum(Num_Riders) 
           from Ridership group by strftime('%Y', Ride_Date) 
           order by strftime('%Y', Ride_Date) asc;"""
  dbCursor.execute(sql)

  rows = dbCursor.fetchall()

  for row in rows:
    print(row[0], " : ", f"{row[1]:,}")

  plot = input("Plot? (y/n) ")

  if plot != "y":
    return

  # variables to store years in x and number of riders in y.
  x = []
  y = []

  for row in rows:
    x.append(row[0][2:4])
    y.append(row[1])

  plt.xlabel("year")
  plt.ylabel("number of riders (x*10^8)")
  plt.title("yearly ridership")

  plt.plot(x, y)
  plt.show()


##################################################################
#
# command_8
#
# Takes a year and the names of two stations(full or partial names),
# and then outputs the daily ridership at each station for that year.
#
def command_8(dbConn):
  dbCursor = dbConn.cursor()

  year = input("\nYear to compare against? ")

  # station 1 is taken as input and then it is checked if 
  # there is no station or multiple stations, in which case
  # the function returns.
  station_1 = input("\nEnter station 1 (wildcards _ and %): ")
  sql = """select Station_ID, Station_Name from Stations where 
           Station_Name like ? order by Station_Name asc;"""

  dbCursor.execute(sql, [station_1])
  rows_1 = dbCursor.fetchall()
  if len(rows_1) == 0:
    print("**No station found...")
    return
  elif len(rows_1) > 1:
    print("**Multiple stations found...")
    return

  # station 2 is taken as input and then it is checked if 
  # there is no station or multiple stations, in which case
  # the function returns.
  station_2 = input("\nEnter station 2 (wildcards _ and %): ")
  sql = """select Station_ID, Station_Name from Stations where 
           Station_Name like ? order by Station_Name asc;"""

  dbCursor.execute(sql, [station_2])
  rows_2 = dbCursor.fetchall()
  if len(rows_2) == 0:
    print("**No station found...")
    return
  elif len(rows_2) > 1:
    print("**Multiple stations found...")
    return

  x = [] # stores the days of the year
  y1 = [] # stores number of riders for station 1
  y2 = [] # stores number of riders for station 2
  day = 1 # used for append the x values of plot
  
  for row in rows_1:
    print("Station 1:", row[0], row[1])

  sql = """select date(Ride_Date), Num_Riders from Ridership 
           join Stations on Stations.Station_ID = Ridership.Station_ID
           where Ridership.Station_ID = (select Station_ID from Stations 
           where Station_Name like ?) and strftime('%Y', Ride_Date) = ?;"""
  dbCursor.execute(sql, [station_1, year])
  station_1 = rows_1[0][1]
  
  rows = dbCursor.fetchall()

  for row in rows: # Station 1
    if day < 6 or day > len(rows) - 5: # condition to print first 5 and last 5 values
      print(row[0], row[1])

    x.append(day)
    y1.append(row[1])
    day += 1;

  for row in rows_2:
    print("Station 2:", row[0], row[1])

  sql = """select date(Ride_Date), Num_Riders from Ridership 
           join Stations on Stations.Station_ID = Ridership.Station_ID
           where Ridership.Station_ID = (select Station_ID from Stations 
           where Station_Name like ?) and strftime('%Y', Ride_Date) = ?;"""
  dbCursor.execute(sql, [station_2, year])
  station_2 = rows_2[0][1]
  
  rows = dbCursor.fetchall()

  day = 1 # variable used again but only for the if/else condition.
  for row in rows: # Station 2
    if day < 6 or day > len(rows) - 5: # condition to print first 5 and last 5 values
      print(row[0], row[1])

    y2.append(row[1])
    day += 1;

  plot = input("Plot? (y/n) ")
  if plot != "y":
    return

  plt.xlabel("day")
  plt.ylabel("number of riders")
  plt.title("riders each day of %s" %year)
  plt.ioff()
  plt.plot(x, y1)
  plt.plot(x, y2)
  plt.legend([station_1, station_2])
  plt.show()
  

##################################################################
#
# command_9
#
# Inputs a line color from the user and outputs all station names
# that are part of that line, in ascending order.
#
def command_9(dbConn):
  dbCursor = dbConn.cursor()

  color = input("\nEnter a line color (e.g. Red or Yellow): ")

  sql = """select distinct Station_Name, Latitude, Longitude from Stations
           join Stops on Stations.Station_ID = Stops.Station_ID
           join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
           join Lines on StopDetails.Line_ID = Lines.Line_ID
           where Color like ? order by Station_Name"""
  dbCursor.execute(sql, [color])

  rows = dbCursor.fetchall()

  x = [] # stores the longitude of stations
  y = [] # stores the latitude of stations

  if len(rows) == 0:
    print("**No such line...")
    return
  
  for row in rows:
    print(row[0], f": ({row[1]},", f"{row[2]})")
    x.append(row[2])
    y.append(row[1])

  plot = input("Plot? (y/n) ")
  if plot != "y":
    return

  image = plt.imread("chicago.png")
  xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the map:
  plt.imshow(image, extent=xydims)

  plt.title(color.lower() + " line")
  #
  # color is the value input by user, we can use that to plot the # 
  # figure *except* we need to map Purple-Express to Purple:
  #
  if (color.lower() == "purple-express"):
    color="Purple"  # color="#800080"
  
  plt.plot(x, y, "o", c=color)

  for row in rows:
    plt.annotate(row[0], (row[2], row[1])) 

  plt.xlim([-87.9277, -87.5569])  
  plt.ylim([41.7012, 42.0868])
  plt.show()


##################################################################
#
# user_input
#
# Takes command from the user and calls various functions
# based on the user input.
#
def user_input(dbConn):

  command = input("Please enter a command (1-9, x to exit): ")

  while command != "x":
  
    if command == "1":
      command_1(dbConn)
    elif command == "2":
      command_2(dbConn)
    elif command == "3":
      command_3(dbConn)
    elif command == "4":
      command_4(dbConn)
    elif command == "5":
      command_5(dbConn)
    elif command == "6":
      command_6(dbConn)
    elif command == "7":
      command_7(dbConn)
    elif command == "8":
      command_8(dbConn)
    elif command == "9":
      command_9(dbConn)
    else:
      print("**Error, unknown command, try again...")

    print()
    command = input("Please enter a command (1-9, x to exit): ")


##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn) # function to print general stats

user_input(dbConn) # function that takes user commands

#
# done
#
