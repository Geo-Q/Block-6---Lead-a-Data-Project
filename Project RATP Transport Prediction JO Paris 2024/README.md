# RATP Transport Prediction during JO Paris 2024


  - link of the dashboard : https://parisjo24-streamlit-gqforjedha-e3ca8d1fcf8e.herokuapp.com/


## Company's Description

The RATP is a public company managing the rail and road public transport networks in Paris and its suburbs : metro, RER, bus, etc. The RATP fulfills its public transport mission within the framework of multi-year operating contracts signed with Île-de-France Mobilités, the transport organizing authority in the Île-de-France region.


## Project

Paris will host the next Olympic Games in the summer of 2024. This international event is expected to attract many tourists from around the world who will attend the sporting competitions. This additional flow of people could greatly disrupt the smooth functioning of public transport in Paris.

In order to optimize the management of its public transport networks, predict the demand for public transport during the PARIS 2024 Olympic Games could allow the RATP to better organize human flows during this period.


## Goals

Predict the demand for public transport during the PARIS 2024 Olympic Games, at least for stations attached to central Paris sites.


## Data

<a href="https://data.iledefrance-mobilites.fr/explore/dataset/histo-validations-reseau-ferre/table/" target="_blank">Data from iledefrance-mobilites</a>


## Deliverable

To complete this project, you will need to produce a slide deck explaining the steps and conclusions of your project, specically insist on:

* The problem you are trying to solve
* What type of data are you working with
* What solution(s) did you implement
* A demo of your final product
* Some perspective on the actual impact your solution may have in the real world
* Some improvement, and next step ideas to push your project further


## Warning !!!

The "data_concatenaited.csv" file which should be in each "99-Data_Clean" folder was not pushed to github because of its too large size (over 850 MB). 
To obtain this file, simply run the notebook "Data_collection_&_transformation.ipynb" in the folder "01 - Data Collection & Transformation", which will create this csv file "data_concatenaited.csv" in the subfolder "99-Data_Clean ". 
Then copy this "data_concatenaited.csv" file obtained into each of the "99-Data_Clean" subfolders within the "02 - Time Series ML" and "03 - Dashboard" folders.
All notebook and python files will then be able to work normally.