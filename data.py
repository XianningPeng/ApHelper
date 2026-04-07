import pandas as pd
import streamlit as st
from supabase import create_client, Client
from datetime import datetime


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

    #initialization
    if "df" not in st.session_state:
        userName = st.session_state.userName
        fileName = userName + ".json"
        response = supabase.storage.from_("usersdata").download(fileName).decode('utf-8')
        st.session_state.df = pd.read_json(response)

    df = st.session_state.df
    overallaccuracy = df["is_correct"].mean()
    return overallaccuracy

def accuracyByUnit (fileName):
    df = st.session_state.df
    accuracy = df.groupby("unit")["is_correct"].mean()
    return accuracy

def correctNumofQuestion (fileName):
    df = st.session_state.df
    correctNumber = df.groupby(["is_correct", "unit"])["unit"].count()
    return correctNumber

def totalNumOfQuestionsByUnit (fileName):
    df = st.session_state.df
    totalNumber = df.groupby("unit")["unit"].count()
    return totalNumber




# handle missing data
def is_missing (fileNmae):

    response = supabase.storage.from_("usersdata").download(fileNmae).decode('utf-8')
    df = st.session_state.df.groupby("unit")[["unit"]].count()

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



# number of questions by week
def count(fileName):

    df = st.session_state.df



    col1, col2 = st.columns(2)

    with col1:
        option_Year = st.selectbox(
            "pick a year",
            ("2026", "2025"),
            placeholder="pick a year",
        )

    with col2:
        option_Unit = st.selectbox(
            "pick a unit",
            ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
            index=None,
            placeholder="pick a unit",
        )

    filtered_df = df[df["year"] == int(option_Year)]

    if option_Unit is not None:
        filtered_df = filtered_df[filtered_df["unit"] == int(option_Unit)]

    filtered_df = filtered_df.groupby(["week"])["week"].count()
    dictNum = filtered_df.to_dict()

    try:
        start = next(iter(dictNum))
        if option_Year == "2026":
            end = datetime.now().isocalendar().week
        else:
            end = 52

        week = []
        count = []
        for i in range(start, end + 1):
            week.append(i)
            try:
                count.append(dictNum[i])
            except:
                count.append(0)

        data = {
            "week": week,
            "count": count
        }

        st.line_chart(data, x="week", y="count")
    except:
        st.write("No Data")

def accuracyByTime():
    df = st.session_state.df

    col1, col2 = st.columns(2)

    with col1:
        option_Year = st.selectbox(
            " ",
            ("2026", "2025"),
            placeholder="pick a year",
        )

    with col2:
        option_Unit = st.selectbox(
            "choose a unit",
            ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
            index=None,
            placeholder="pick a unit",
        )

    filtered_df = df[df["year"] == int(option_Year)]

    if option_Unit is not None:
        filtered_df = filtered_df[filtered_df["unit"] == int(option_Unit)]

    filtered_df = filtered_df.groupby(["week"])["is_correct"].mean()
    dictNum = filtered_df.to_dict()

    try:
        start = next(iter(dictNum))
        if int(option_Year) == datetime.now().isocalendar().year:
            end = datetime.now().isocalendar().week
        else:
            end = 52

        week = []
        accuracy = []
        for i in range(start, end + 1):
            week.append(i)
            try:
                accuracy.append(dictNum[i])
            except:
                accuracy.append(0)

        data = {
            "week": week,
            "accuracy": accuracy
        }

        st.line_chart(data, x="week", y="accuracy")
    except:
        st.write("No Data")
