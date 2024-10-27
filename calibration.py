from clustering_result_repository import get_all_clustering_result_feedback
from calibration_repository import save_calibration_parameter


def calibration_attempt(calibration, eps_value):
    feedbacks = get_all_clustering_result_feedback()
    feedback_list = list(feedbacks)
    if len(feedback_list) > 100:
        calibrate(calibration, eps_value, feedback_list)


def calibrate(calibration, eps_value, feedback_list):
    true_percentage = get_porcentage_true(feedback_list)
    if true_percentage < 50:
        eps_value = eps_value + 0.01
    elif true_percentage < 70 and eps_value > 0:
        eps_value = eps_value - 0.01
    calibration['eps'] = eps_value
    save_calibration_parameter(calibration)


def get_porcentage_true(lista):
    total_true = lista.count(True)
    total = len(lista)
    return (total_true / total) * 100 if total > 0 else 0
