# MLB Data Explorer
Formerly the MLB History Explorer/Baseball Historical Dashboard, this application is a portfolio project built using [Plotly's Dash](https://plotly.com/dash/)
, faculty.ai's [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/), Pandas, and SKLearn. 
Using historical MLB (Major League Baseball) data, this application provides visualizations for team and player statistics dating from 1903 to 2020. 
This application also provides player projections and uses a Linear Regression to evaluate player performance.

## The Analysis
For historical analysis, this application breaks down each baseball teams win/loss performance within a range determined my MLB era (epoch). 
Additionally, this application will break down the batting performance with the team's batting average, BABIP, strikeout rate. The application also 
brakes down the pitching performance using the teams Earned Run Average, strikeout to walk ratio, and outing distribution. Finally the fielding 
performance of each team is illustrated with total errors and double plays. The application will similarly breakdown each teams players statistics within 
the given era. Finally, this application provides player projections that are displayed in a data-table along side career statistics while a regression 
analysis of the players career and recent seasons are displayed in an oscillating bar chart. Team rosters used are based on the 2020 season.

## Dependencies
- Python 3.8.5+
- Dash 1.19
- Dash Bootstrap Components 0.11.1
- Pandas 1.1
- Sklearn 0.24.2

## The Data
The data used in this application was retrieved from [Sean Lahman's Baseball Database](http://www.seanlahman.com/baseball-archive/statistics/).
Provided by [Chadwick Baseball Bureau's GitHub](https://github.com/chadwickbureau/baseballdatabank/). 
This database is copyright 1996-2021 by Sean Lahman. This data is licensed under a Creative Commons Attribution-ShareAlike 
3.0 Unported License. For details see: [CreativeCommons](http://creativecommons.org/licenses/by-sa/3.0/)

### Application deployed on [Heroku](https://historicalbaseball.herokuapp.com/).
