# Historical Baseball Statistics Dashboard
This application is built using Plotly Dash. The app takes historical MLB (Major League Baseball) data and displays team statistics dating from 1903 to 2015. Selecting from a dropdown menu, an era is selected updating the list of available teams and the range set on the years slider. The slider is on a range, allowing the user to adjust the range of years with wich the data shows. This application was intended for me to practice the use of the Python language, basic data analysis, and basic data visualization using Dash.

## The Analysis
The applicaiton breaks down each baseballs teams win/loss performance over the teams history. Additionally, I break down the batting performance with the team batting average, BABIP, and strikeout rate. I also broke down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding performance of each team is illustrated with total errors and double plays. The graphs are designed with a single CSV file queried with Pandas.

## Dependencies
- Dash 1.14
- Pandas 1.1
- Numpy 1.19.1

## The Data
The data was retrieved from Kaggel and was created by code at https://github.com/benhamner/baseball. It is a processed version of the 2015 data at www.seanlahman.com/baseball-archive/statistics/. The original database was copyright 1996-2015 by Sean Lahman and licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License. For details see: http://creativecommons.org/licenses/by-sa/3.0/
