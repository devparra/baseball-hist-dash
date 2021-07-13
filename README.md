# Historical Baseball Statistics Dashboard
This application is a portfolio project built using Plotly's Dash, faculty.ai's Dash Bootstrap Components, and Pandas.
Using historical MLB (Major League Baseball) data, this application provides visualizations for team and player
statistics dating from 1903 to 2020. This application also provides player projections and uses a Linear Regression to
evaluate player performance.

## The Analysis
The applicaiton breaks down each baseball teams win/loss performance within a range of the teams history.
Additionally, the application will break down the batting performance with the team batting average, BABIP, and strikeout
rate. The application also brakes down the piching perfomance using the teams ERA and strikeout to walk ratio. Finally the feilding
performance of each team is illustrated with total errors and double plays. The applicaiton will similarly breakdown
each teams players statistics within the given era. The projections are displayed in a datatable while the regression analysis
of the players career and recent seasons are displayed in an oscillating bar chart.

## Dependencies
- Python 3.8.5+
- Dash 1.19
- Dash Bootstrap Components 0.11.1
- Sklearn 0.24.1
- Pandas 1.1

## The Data
The data used in this application was retrieved from [Seanlahman.com](http://www.seanlahman.com/baseball-archive/statistics/).
Provided by [Chadwick Baseball Bureau's GitHub](https://github.com/chadwickbureau/baseballdatabank/). 
This database is copyright 1996-2021 by Sean Lahman. This data is licensed under a Creative Commons Attribution-ShareAlike 
3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)

### Application deployed on Heroku [here](https://historicalbaseball.herokuapp.com/).
