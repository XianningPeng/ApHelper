import streamlit as st
from supabase import create_client, Client
import base64
from qwen import ocr
from main import main


url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)




def getQuestion(uploadedFile):

    encodedImage = base64.b64encode(uploadedFile.read()).decode("utf-8")
    extractedDict = ocr(encodedImage)
    questionInfo["text"] = extractedDict.get("question")
    questionInfo["choiceA"] = extractedDict.get("choiceA")
    questionInfo["choiceB"] = extractedDict.get("choiceB")
    questionInfo["choiceC"] = extractedDict.get("choiceC")
    questionInfo["choiceD"] = extractedDict.get("choiceD")
    questionInfo["choiceE"] = extractedDict.get("choiceE")
    return


def getChoice():

    correct_input = st.radio("What is the correct answer of this question?",
                             ["A", "B", "C", "D", "E"], index=None, key=f"correctAns_{i}")
    ans_input = st.radio("What is the your answer of this question?",
                         ["A", "B", "C", "D", "E"], index=None, key=f"ans_{i}")
    questionInfo["correct_input"] = correct_input
    questionInfo["ans_input"] = ans_input
    return








st.write(st.session_state.userName)
st.divider()

userName = st.session_state.userName

# the number of questions the user want to input
numberInput = st.number_input(
    "How many questions do you want to input?",
    min_value = 1,
    max_value = 45,
    value=1,
    placeholder="Type a number..."
)

for i in range(numberInput):
    st.divider()



    inputOptions = st.radio(
        "pick a way to upload question",
        ["take a picture", "upload a picture", "input manually"],
        index=None,
        key=f"option{i}"
    )

    questionInfo ={}

        # text": "",
        #     "choiceA": "",
        #     "choiceB": "",
        #     "choiceC": "",
        #     "choiceD": "",
        #     "choiceE": "",
        #     "correct_input": "",
        #     "ans_input": "



    if inputOptions == "take a picture":
        uploadedFile = st.camera_input("Take a picture", disabled=False, key=f"camera{i}")
        try:
            getQuestion(uploadedFile)
            getChoice()
        except:
            st.write("")

    elif inputOptions == "upload a picture":

        try:
            getChoice()
            uploadedFile = st.file_uploader("upload image of the question", type=["jpg", "jpeg", "png"],
                                            key=f"upload{i}")
            getQuestion(uploadedFile)

        except:
            st.write("")

    elif inputOptions is not None:
        question_input = st.text_area("please put your question here:", key = f"question_{i}")            # "key" is necessary here.
        choice_a = st.text_input("Choice A", key=f"choice_a_{i}")
        choice_b = st.text_input("Choice B", key=f"choice_b_{i}")
        choice_c = st.text_input("Choice C", key=f"choice_c_{i}")
        choice_d = st.text_input("Choice D", key=f"choice_d_{i}")
        choice_e = st.text_input("Choice E", key=f"choice_e_{i}")

        # store into dict
        questionInfo["text"] = question_input
        questionInfo["choiceA"] = choice_a
        questionInfo["choiceB"] = choice_b
        questionInfo["choiceC"] = choice_c
        questionInfo["choiceD"] = choice_d
        questionInfo["choiceE"] = choice_e

        getChoice()




    if (len(questionInfo) == 8) and st.button("Submit", key = f"{i}button"): # have to add this "submit" button, otherwise the app would automatically save questions when you click something
        with st.spinner("This might take a while", show_time=True):
            overallAccuracy = main(userName,
                                   questionInfo["text"],
                                   questionInfo["choiceA"],
                                   questionInfo["choiceB"],
                                   questionInfo["choiceC"],
                                   questionInfo["choiceD"],
                                   questionInfo["choiceE"],
                                   questionInfo["correct_input"],
                                   questionInfo["ans_input"])
        st.write("Question classified and logged successfully.")