# utils/davis_utils.py

"""
🚂 Davis Equation 상수 정의 및 유틸 함수
기차 유형에 따라 상수 조정 가능
"""

def get_davis_constants(model: str = "default") -> tuple[float, float, float]:
    """
    기차 모델에 따른 Davis Equation 상수 반환

    Parameters:
        model (str): 기차 유형 (예: 'default', 'light', 'heavy')

    Returns:
        tuple: (A, B, C) 상수
    """
    if model == "light":
        return 2.0, 0.8, 0.02  # 가벼운 차량 (예: 승객용 경량차)
    elif model == "heavy":
        return 8.0, 1.5, 0.06  # 대형 화물열차
    else:  # default 중형
        return 5.0, 1.2, 0.05
