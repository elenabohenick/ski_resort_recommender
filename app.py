import flask
from flask import request
import pickle
import numpy as np
import pandas as pd

with open("data/resort_topics_for_recommender.pkl","rb") as f:
    ski_rec = pickle.load(f)

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/", methods=['GET','POST'])

def render():
    return flask.render_template('user_form.html')


@app.route("/results", methods=['POST'])
def recommend():

    print(request.form)

    filters = ['beginner','powder','family','for_kids', 'scenic_views', 'food', 'crowds']

    current_filter = []

    # geo
    geo = str(request.form['geography'])
    geo = geo.strip().replace("-","").strip()

    if geo in ski_rec['state_region'].unique():
        temp = ski_rec[ski_rec['state_region']==geo]
    elif geo in ski_rec['country'].unique():
        temp = ski_rec[ski_rec['country']==geo]
    else:
        temp = ski_rec[ski_rec['region']==geo]

    # Beginner
    if int(request.form['ability_level'])==0:
        current_filter = ['beginner']
    else:
        pass

    # Snow_conditions
    if int(request.form['snow_conditions'])==1:
        current_filter.append('powder')
    else:
        pass


    # Family-friendly
    if str(request.form['family_friendly'])=="Yes":
        current_filter.append('family')
    else:
        pass


    # Kdis-lesssons
    if str(request.form['kids'])=="Yes":
        current_filter.append('for_kids')
    else:
        pass

    # Scenic views    # Kdis-lesssons
    if "feat_1" in request.form:
        current_filter.append('scenic_views')
    else:
        pass


    # food
    if "feat_2" in request.form:
        current_filter.append('food')
    else:
        pass

    # crowds
    if "feat_3" in request.form:
        current_filter.append('crowds')
    else:
        pass


    columns = ['resort_name','country','resort_website']+current_filter

    temp = temp[columns]
    temp['total_score'] = temp.sum(axis=1)

    resorts_out = []
    countries_out = []
    sites_out = []

    for res_i in np.argsort(temp.loc[:,'total_score'])[-3:]:
        resorts_out.append(temp.iloc[res_i,0])
        countries_out.append(temp.iloc[res_i,1])
        sites_out.append(temp.iloc[res_i,2])

    resort_names = []

    for i in range(3):
        rec = str(resorts_out[i]) + " (" + str(countries_out[i]) + ")"
        resort_names.append(rec)

    recs = list(zip(resort_names, sites_out))



    return flask.render_template('ski_recs.html',
    recommendation=recs,
    resort_sites = sites_out)


# Run the app
app.run(debug=True)
