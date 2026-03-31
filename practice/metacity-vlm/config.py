"""모델 설정 및 출력 스키마 정의."""

# --- 모델 ---
MODEL_ID = "Qwen/Qwen3-VL-4B-Instruct"

# --- 생성 파라미터 ---
GENERATION_CONFIG = {
    "max_new_tokens": 1024,
    "temperature": 0.3,       # 낮게: 일관된 구조화 출력
    "top_p": 0.9,
    "do_sample": True,
}

# --- 출력 JSON 스키마 (프롬프트 참조용) ---
OUTPUT_SCHEMA = {
    "scene_type": "장면 유형 (intersection, highway, residential, commercial, park)",
    "time_of_day": "시간대 (daytime, nighttime, dawn, dusk)",
    "weather": "날씨 (clear, rain, fog, snow, overcast)",
    "traffic_density": "교통 밀도 (low, medium, high, congested)",
    "pedestrian_density": "보행자 밀도 (none, low, medium, high)",
    "anomalies": "이상 징후 리스트 (빈 리스트 가능)",
    "risk_level": "위험 수준 (low, moderate, high, critical)",
    "summary": "운영자를 위한 1-2문장 한국어 요약",
}

# --- 이미지 설정 ---
IMAGE_DIR = "images"
OUTPUT_DIR = "outputs"
