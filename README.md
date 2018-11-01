# Welcome to my 'Project McNulty' repo!   

For this project at Metis, I used supervised learning (classification), Amazon Web Services, PostgreSQL, Flask, and D3 to create a web app that consolidates data on housing throughout the city. Users can find information on complaints about the building and area, crime rates, as well as the 'Sketchy Landlord' index, created by a classification model trained on data where tenants ended up suing their landlords.

In this repo, I've uploaded my code, the data I used, and the presentation I gave at Metis on this project.  
  
Blog post is currently a work in progress.
  
## Repo Contents:   

### Data
* All data is available on [NYC Open Data]. The datasets used in this project are up-to-date as of October 17th, 2018.

### Data Cleaning
* [data_cleaning.py](data_cleaning.py) - cleaning of NYC open data and PLUTO data
* all performed on AWS
  
### Modeling
* [mvp_maddy_obrien_jones.ipynb](mvp_maddy_obrien_jones.ipynb) - minimum viable product
* [baseline.ipynb](baseline.ipynb) - baseline model built on DOB complaints only
* [model_testing.ipynb](model_testing.ipynb) - feature engineering and model testing
* [final_modeling.ipynb](final_modeling.ipynb) - building XGBoost model and scoring on data

### Web App Building
* [flaskapp.py](flaskapp.py) - Flask app to look up building information
* [page.html](page.html) - first page of Flask app (search bar)
* [template2.html](template2.html) - second page of Flask app (building information)
* [xgb.pkl](xgb.pkl) - pickled model to predict risk of litigation

### Presentation
* [Predicting Housing Litigation.pdf](Predicting Housing Litigation.pdf) - powerpoint
* [screen_recording.mov](screen_recording.mov) - demonstration of Flask app

*work in progress

[NYC Open Data]: https://opendata.cityofnewyork.us/
