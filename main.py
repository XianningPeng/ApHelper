import os
from LLM import classification
from datetime import datetime
import json
from data import overallAccuracy
from supabase import create_client, Client
import streamlit as st


url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)



def main(userName, question, choiceA, choiceB, choiceC, choiceD, choiceE, correctAns, answer):

    is_correct = False
    if correctAns == answer:
        is_correct = True


    question1 = {
        "text": question,
        "choiceA": choiceA,
        "choiceB": choiceB,
        "choiceC": choiceC,
        "choiceD": choiceD,
        "choiceE": choiceE,
        "unit": classification(question),
        "correct answer": correctAns.upper(),
        "user's answer": answer.upper(),
        "is_correct": is_correct,
        "week": datetime.now().isocalender().week,
        "year": datetime.now().isocalendar().year,
        "time": datetime.now().isoformat()
    }
    file_name = userName + ".json"


    try:
        responseLocal = supabase.storage.from_("usersdata").download(file_name)  # get the file
        data = json.loads(responseLocal)
        data.append(question1)

        json_str2 = json.dumps(data, indent=len(data)).encode('utf-8')
        response = (
            supabase.storage.from_("usersdata")
            .upload(
                file=json_str2,
                path=file_name,
                file_options={"cache-control": "3600", "upsert": "true"}
            )
        )

    except:  # new user

        theList = [question1]
        json_str = json.dumps(theList, indent=1).encode('utf-8')
        response = (
            supabase.storage.from_("usersdata")
            .upload(
                file=json_str,
                path=file_name,
                file_options={"cache-control": "3600", "upsert": "false"}
            )
        )


    return overallAccuracy(file_name)


