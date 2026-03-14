import pandas as pd

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
    df = pd.read_json(fileName)
    overallaccuracy = df["is_correct"].mean()
    return overallaccuracy

def accuracyByUnit (fileName):
    df = pd.read_json(fileName)
    accuracy = df.groupby("unit")["is_correct"].mean()
    return accuracy

def correctNumofQuestion (fileName):
    df = pd.read_json(fileName)
    correctNumber = df.groupby(["is_correct", "unit"])["unit"].count()
    return correctNumber

def totalNumOfQuestionsByUnit (fileName):
    df = pd.read_json(fileName)
    totalNumber = df.groupby("unit")["unit"].count()
    return totalNumber




# this function is being used to detect if there are some missing units
def is_missing (fileNmae):

    df = pd.read_json(fileNmae).groupby("unit")[["unit"]].count()   #df is a dataframe
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







# def accuracyByUnitChart (fileName):
#     accuracy = accuracyByUnit(fileName).to_list()
#
#     if len(accuracy) != 10:
#         missing = is_missing(fileName)
#         missing.sort()         # this line is removable
#
#         for unit in missing:
#             accuracy.insert(unit-1, 0)
#
#     data = {
#         'Unit': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#         'Accuracy': accuracy
#     }
#     df = pd.DataFrame(data)
#
#     plt.bar(df['Unit'], df['Accuracy'], color='skyblue')
#     plt.xlabel("Unit")
#     plt.ylabel("Accuracy")
#     plt.title("Accuracy by Unit")
#     plt.show()
#     return




# def pieChart (fileName):
#
#     Frequency = totalNumOfQuestionsByUnit(fileName).to_list()
#
#     if len(Frequency) != 10:
#         missing = is_missing(fileName)
#         missing.sort()  # this line is removable
#
#         for i in missing:
#             Frequency.insert(i-1, 0)
#
#     data = {
#         'Unit': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
#         'Frequency': Frequency
#     }
#     df = pd.DataFrame(data)
#
#     plt.pie(df['Frequency'], labels=df['Unit'], autopct='%1.0f%%')
#     plt.title("Number of Questions by Unit")
#     plt.show()
#     return


