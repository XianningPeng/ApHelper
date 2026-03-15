import json
from openai import OpenAI
from data import accuracyByUnitChart
from data import pieChart
import streamlit as st

client = OpenAI(
    api_key= st.secrets["deepseekAPI"],
    base_url="https://api.deepseek.com")


def classification (question):
    system_prompt = """

        There are 10 different units in this course and its corresponding exam, (which are 1.Limits and Continuity; 
        2. Differentiation: Definition and Basic Derivative Rules; 3. Differentiation: Composite, Implicit, and Inverse Functions; 
        4.Contextual Applications of Differentiation; 5.Applying Derivatives to Analyze Functions; 6.Integration and Accumulation of Change; 
        7.Differential Equations; 8.Applications of Integration; 9.Parametric Equations, Polar Coordinates, and Vector-Valued Functions; 
        10.Infinite Sequences and Series. 

        The user will provide an AP Calculus BC exam question. Your task is to determine which of the 10 official AP Calculus BC units the question belongs to.
        Respond with only one unit's number. Output the result in valid JSON format using the key "Unit"

        EXAMPLE INPUT: 
        Which of the following series is conditionally convergent?

        EXAMPLE JSON OUTPUT:
        {
          "Unit": "10"
        }

    """

    localQuestion = question

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": localQuestion}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    data = json.loads(response.choices[0].message.content)

    return data.get("Unit")





def analyze(userName):

    fileName = userName + ".json"


    system_prompt = f"""  
    
            There are 10 different units in this course and its corresponding exam, (which are 1.Limits and Continuity; 
            2. Differentiation: Definition and Basic Derivative Rules; 3. Differentiation: Composite, Implicit, and Inverse Functions; 
            4.Contextual Applications of Differentiation; 5.Applying Derivatives to Analyze Functions; 6.Integration and Accumulation of Change; 
            7.Differential Equations; 8.Applications of Integration; 9.Parametric Equations, Polar Coordinates, and Vector-Valued Functions; 
            10.Infinite Sequences and Series. 
            
            The user has finished a set of AP calculus bc exam. 
            His accuracy by unit is {accuracyByUnitChart(fileName)}. 
            You can also find how many questions he has finished with the units they belong to here: {pieChart(fileName)}
            
            according to there data, give the user an analysis and suggestion on future study.
    
    
    
    """

    localQuestion = "according to the user's data, give the user an analysis and suggestion on future study. start with no introduction."

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": localQuestion}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    return (response.choices[0].message.content)



