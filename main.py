
# Importing libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
DATA_PATH = "Training.csv"
data = pd.read_csv(DATA_PATH).dropna(axis = 1)
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])
X = data.iloc[:,:-1]
y = data.iloc[:, -1]
final_nb_model = GaussianNB()
final_nb_model.fit(X, y)
symptoms = X.columns.values
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.capitalize() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}
def predictDisease(symptoms):
    symptoms = symptoms.split(",")
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1
    print(data_dict)
    input_data = np.array(input_data).reshape(1, -1)
    prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    return prediction

print(symptoms)
# Testing the function
print(predictDisease("Itching,Skin Rash,Nodal Skin Eruptions"))
