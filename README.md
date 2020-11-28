# sqlalchemy-challenge: Climate Research #

## Objectives ##

### Precipitation Analysis ###

1. Design a query to retrieve the last 12 months of precipitation data.
2. Select only the date and prcp values.
3. Load the query results into a Pandas DataFrame and set the index to the date column.
4. Sort the DataFrame values by date.
5. Plot the results using the DataFrame plot method.
6. Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis ###

1. Design a query to calculate the total number of stations.
2. Design a query to find the most active stations.
3. List the stations and observation counts in descending order.
4. Find the most active station.
5. Design a query to retrieve the last 12 months of temperature observation data (TOBS).
6. Filter by the station with the highest number of observations.
7. Plot the results as a histogram with bins=12.

All objectives executed in climate.ipynb notebook

### Flask API ###

Created a flask API with the following routes:
/api/v1.0/precipitation
- returns dictionary of precipitation values for each date in the dataset and plot for the last year of data
/api/v1.0/stations
- returns name and identifier for the stations from which measurements were taken
/api/v1.0/tobs
- returns list and plot of temperature observations over the past year for the most active station
/api/v1.0/{start} & /api/v1.0/{start}/{end}
- format: /api/v1.0/2016-08-22 or /api/v1.0/2016-08-22/2016-09-28
- returns min, max, and average temperature observations between the specified dates for the most active station
if no end date is given, the end date will be the last date in the dataset

API can be accessed by cloning the repository, navigating to the root, and running `python app.py` or `flask run` 

