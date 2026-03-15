import os
from LLM import classification
from datetime import datetime
import json
from data import overallAccuracy


def main(userName, question, correctAns, answer):

    is_correct = False
    if correctAns == answer:
        is_correct = True


    question1 = {
        "text": question,
        "unit": classification(question),
        "correct answer": correctAns.upper(),
        "user's answer": answer.upper(),
        "is_correct": is_correct,
        "time": datetime.now().isoformat()
    }
    file_name = userName + ".json"


    if os.path.isfile(file_name):

        # deserialization
        # change it to a list or dictionary
        # append
        # serialization

        with open(file_name, "r") as f:
            data = json.load(f)
        data.append(question1)

        json_str2 = json.dumps(data, indent=len(data))
        with open(file_name, "w") as f:
            f.write(json_str2)

    else:
        theList = [question1]
        json_str = json.dumps(theList, indent=1)
        with open(file_name, "w") as f:
            f.write(json_str)

    # store data to json file ends here



    # print("Your overall accuracy is: " + str(overallAccuracy(file_name)))
    # #print(accuracyByUnit(file_name))
    # #print(correctNumofQuestion(file_name))
    # #print(totalNumOfQuestionsByUnit(file_name))
    #
    # accuracyByUnitChart(file_name)
    # pieChart(file_name)


    return overallAccuracy(file_name)


