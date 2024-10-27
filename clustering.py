from sklearn.cluster import DBSCAN
import pandas as pd
from calibration_repository import get_calibration_parameter
from calibration import calibration_attempt
from clustering_result_repository import save_clustering_result


def clusterize(people):
    df = pd.DataFrame(people, columns=["ID", "Genero", "Faixa_etaria", "Hobbies", "Personalidade"])

    for column in df.columns:
        if column != "ID":
            if df.loc[0, column] == "Sem preferencia":
                df = df.drop(columns=[column])

    no_preference = check_no_preference(df)
    if no_preference:
        return convert_to_list_of_objects(people)

    df_encoded = df.drop(columns=["ID"])

    for column in df_encoded.columns:
        if df_encoded.loc[0, column] != "Sem preferencia":
            df_encoded = pd.get_dummies(df_encoded, columns=[column])

    calibration = get_calibration_parameter()
    eps_value = calibration['eps']
    min_samples_value = calibration['min_samples']

    calibration_attempt(calibration, eps_value)

    model = DBSCAN(eps=eps_value, min_samples=min_samples_value, metric='euclidean')
    clusters = model.fit_predict(df_encoded)

    df["Cluster"] = clusters

    result = convert_dataframe_to_list_of_objects(df)
    result_id = save_clustering_result(result)
    return {"id": result_id, "doctors": result}


def check_no_preference(df):
    all_without_preference = []
    for column in df.columns:
        if column != "ID":
            if df.loc[0, column] == "Sem preferencia":
                df = df.drop(columns=[column])
                all_without_preference.append(True)
            else:
                all_without_preference.append(False)

    return not False in all_without_preference


def convert_to_list_of_objects(matrix):
    matrix_as_list = [
        {"id": emp[0], "gender": emp[1], "age": emp[2], "hobbies": emp[3]}
        for emp in matrix
    ]
    matrix_as_list.pop(0)
    return matrix_as_list


def convert_dataframe_to_list_of_objects(df):
    result = df.to_dict(orient='records')
    converted_result = []
    for emp in result:
        emp_dict = {}

        if "ID" in emp and emp["ID"] is not None:
            emp_dict["id"] = emp["ID"]
        if "Genero" in emp and emp["Genero"] is not None:
            emp_dict["gender"] = emp["Genero"]
        if "Faixa_etaria" in emp and emp["Faixa_etaria"] is not None:
            emp_dict["age"] = emp["Faixa_etaria"]
        if "Hobbies" in emp and emp["Hobbies"] is not None:
            emp_dict["hobbies"] = emp["Hobbies"]

        if emp_dict and df.iloc[0]["Cluster"] == emp["Cluster"]:
            converted_result.append(emp_dict)

    if converted_result:
        converted_result.pop(0)

    return converted_result
