# Historical Baseball Statistics Dashboard
This application is built using Plotly Dash. The applicaiton takes historical MLB (Major League Baseball) data and displays team statistics dating from 1903 to 2015. Selecting from a dropdown menu, an era is choosen, updating the list of available teams and the range set on the slider. The slider allows the user to adjust the range of years with wich the data shows.

## The Analysis
The applicaiton breaks down each baseballs teams win/loss performance within a range of the teams history. Additionally, the app will break down the batting performance with the team batting average, BABIP, and strikeout rate. I also broke down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding performance of each team is illustrated with total errors and double plays. \*The applicaiton will also breakdown each of teams players statistics within the given era. The graphs are designed with a single CSV file queried with Pandas.

## Dependencies
- Python 3.8+
- Dash 1.14
- Dash Bootstrap Components 0.11.1
- Pandas 1.1
- Numpy 1.19.1

## The Data
The data was retrieved from Kaggel and was created by code at https://github.com/benhamner/baseball. It is a processed version of the 2015 data at www.seanlahman.com/baseball-archive/statistics/. The original database was copyright 1996-2015 by Sean Lahman and licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. For details see: http://creativecommons.org/licenses/by-sa/3.0/

* *Applicaiton feature is recently added and still under construction*
