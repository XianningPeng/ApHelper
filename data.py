import pandas as pd
import streamlit as st
from supabase import create_client, Client

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

units = [
    "1. Limits and Continuity",
    "2. Differentiation: Definition and Basic Derivative Rules",
    "3. Differentiation: Composite, Implicit, and Inverse Functions",
    "4. Contextual Applications of Differentiation",
    "5. Applying Derivatives to Analyze Functions",
    "6. Integration and Accumulation of Change",
    "7. Differential Equations",
    "8. Applications of Integration",
    "9. Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
    "10. Infinite Sequences and Series"
]

def overallAccuracy (fileName):
    response = supabase.storage.from_("usersdata").download(fileName).decode('utf-8')
    df = pd.read_json(response)
    overallaccuracy = df["is_correct"].mean()
    return overallaccuracy

def accuracyByUnit (fileName):
    response = supabase.storage.from_("usersdata").download(fileName).decode('utf-8')
    df = pd.read_json(response)
    accuracy = df.groupby("unit")["is_correct"].mean()
    return accuracy

def correctNumofQuestion (fileName):
    response = supabase.storage.from_("usersdata").download(fileName).decode('utf-8')
    df = pd.read_json(response)
    correctNumber = df.groupby(["is_correct", "unit"])["unit"].count()
    return correctNumber

def totalNumOfQuestionsByUnit (fileName):
    response = supabase.storage.from_("usersdata").download(fileName).decode('utf-8')
    df = pd.read_json(response)
    totalNumber = df.groupby("unit")["unit"].count()
    return totalNumber




# this function is being used to detect if there are some missing units
def is_missing (fileNmae):

    response = supabase.storage.from_("usersdata").download(fileNmae).decode('utf-8')
    df = pd.read_json(response).groupby("unit")[["unit"]].count()

    dict = df.to_dict()

    missing = []

    for i in range(1, 11):
        if dict.get("unit").get(i) is None:
            missing.append(i)

    return missing



#graph
def accuracyByUnitChart (fileName):
    accuracy = accuracyByUnit(fileName).to_list()

    if len(accuracy) != 10:
        missing = is_missing(fileName)
        missing.sort()         # this line is removable

        for unit in missing:
            accuracy.insert(unit-1, 0)

    data = {
        'Unit': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Accuracy': accuracy
    }
    return data



def pieChart (fileName):

    Frequency = totalNumOfQuestionsByUnit(fileName).to_list()

    if len(Frequency) != 10:
        missing = is_missing(fileName)
        missing.sort()  # this line is removable

        for i in missing:
            Frequency.insert(i-1, 0)

    data = {
        'Unit': units,
        'Frequency': Frequency
    }
    df = pd.DataFrame(data)

    return df


