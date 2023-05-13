from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests


# Create your views here.
def news(request):
    url = "https://newsapi.org/v2/top-headlines"
    querystring = {"country": "in", "category": "health", "apiKey": "97f83e569bf74eaf814abc8993751dfb"}
    res = requests.request("GET", url, params=querystring).json()
    result = {"status": 1, "res": res["articles"][5:8]}
    return result


def index(request):
    res = news(request)
    return render(request, "index.html", res)


def diagnose(request):
    res = ['None', 'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
           'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting',
           'burning_micturition', 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets',
           'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level',
           'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration',
           'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
           'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
           'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
           'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
           'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
           'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
           'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain'
                                                                            'weakness_in_limbs', 'fast_heart_rate',
           'pain_during_bowel_movements',
           'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
           'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
           'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid',
           'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
           'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech',
           'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
           'swelling_joints', 'movement_stiffness', 'spinning_movements',
           'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
           'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
           'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
           'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
           'altered_sensorium', 'red_spots_over_body', 'belly_pain',
           'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes',
           'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
           'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
           'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
           'stomach_bleeding', 'distention_of_abdomen',
           'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum',
           'prominent_veins_on_calf', 'palpitations', 'painful_walking',
           'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
           'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
           'blister' 'red_sore_around_nose', 'yellow_crust_ooze']

    return render(request, 'appointment.html', {"res": res})


def googles(dis):
    from googlesearch import search
    import wikipedia
    result = wikipedia.search(dis)
    page = wikipedia.page(result[0])
    summary = page.summary
    content=page.content
    query = dis
    l = []
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        l.append(j)
    return {"resg": l, "resw": summary, "resc":content}


def predictDisease(symptomss):
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import LabelEncoder
    from sklearn.naive_bayes import GaussianNB
    DATA_PATH = "C:\\Users\\nihar\\PycharmProjects\\pythonProject1\\Training.csv"
    data = pd.read_csv(DATA_PATH).dropna(axis=1)
    encoder = LabelEncoder()
    data["prognosis"] = encoder.fit_transform(data["prognosis"])
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    final_nb_model = GaussianNB()
    final_nb_model.fit(X, y)
    symptoms = X.columns.values
    symptom_index = {}
    c=0
    for value in symptoms:
        symptom_index[value] = c
        c+=1
    data_dict = {
        "symptom_index": symptom_index,
        "predictions_classes": encoder.classes_
    }
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptomss:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
    input_data = np.array(input_data).reshape(1, -1)
    prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    return prediction


def diagnoser(request):
    print(request.POST)
    l = []
    l.append(request.POST["select1"])
    l.append(request.POST["select2"])
    l.append(request.POST["select3"])
    l.append(request.POST["select4"])
    l = list(set(l))
    if 'None' in l:
        l.remove('None')
    if 'spotting_urination' in l:
        l.remove('spotting_urination')
        l.append('spotting_ urination')
    dis = ''
    if len(l) == 0:
        return render(request, 'diagnose.html')
    dis = predictDisease(l)
    res = googles(dis)
    return render(request, 'diagnose.html', {"res": res, "disease": dis})
