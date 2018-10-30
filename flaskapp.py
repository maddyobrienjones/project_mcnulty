import flask
from xgboost import XGBClassifier
import pickle
import numpy as np
import pandas as pd

data = pd.read_csv("pluto.csv")
data.set_index(['Address'], inplace=True)
features = data[['311','hmc_v','hmc_c', 'dev','dc','dv','AssessTot','UnitsRes','LotArea']]
features.columns = ['311 Complaints','HMC Violations','HMC Complaints', 'DOB ECB Violations','DOB Complaints','DOB Violations','AssessTot','UnitsRes','LotArea']
target = data['has_lit']

with open('xgb.pkl','rb') as f:
    model = pickle.load(f)

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    with open("page.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    address = flask.request.get_data()
    address = address.decode('utf-8')
    address = address.split('=')[1].replace('+',' ').upper()
    risk = model.predict_proba(pd.DataFrame(features.loc[address][['311 Complaints', 'HMC Violations', 'HMC Complaints', 'DOB ECB Violations', 'DOB Complaints', 'DOB Violations', 'AssessTot', 'UnitsRes', 'LotArea']]).T)[0][1]    # Put the result in a nice dict so we can send it as json
    risk = round(risk,3)
    results = dict()
    results['Zip Code'] = str(int(data.loc[address]['ZipCode']))
    results['Property Value'] = '$' + str(data.loc[address]['AssessTot'])
    results['Year Built'] = str(int(data.loc[address]['YearBuilt']))
    if data.loc[address]['YearAlter2'] != 0:
        results['Last Renovated'] = str(data.loc[address]['YearAlter2'])
    else:
        if data.loc[address]['YearAlter1'] != 0:
            results['Last Renovated'] = str(data.loc[address]['YearAlter1'])
        else:
            results['Last Renovated'] = 'N/A'
    results['Risk of Litigation'] = str(risk)
    results['Previous Litigations'] = str(data.loc[address]['lits'])
    results['311 Complaints'] = str(data.loc[address]['311'])
    results['Housing Maintenance Code Complaints'] = str(data.loc[address]['hmc_c'])
    results['Housing Maintenance Code Violations'] = str(data.loc[address]['hmc_v'])
    results['Department of Buildings Complaints'] = str(data.loc[address]['dc'])
    results['Department of Buildings Violations'] = str(data.loc[address]['dv'])
    results['Environmental Control Board Violations'] = str(data.loc[address]['dev'])
    return flask.render_template('template2.html',address=address,results=results.items())

app.run(host='0.0.0.0')
app.run(debug=True)
