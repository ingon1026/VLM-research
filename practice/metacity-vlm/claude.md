# metacity-vlm

## Purpose
YOLO + VLM 기반 도시 장면 관제 요약 시스템. Streamlit 대시보드 제공.

## Stack
- Object Detection: YOLO26n (Ultralytics)
- VLM: Qwen3-VL-4B-Instruct (HuggingFace transformers)
- Dashboard: Streamlit
- GPU: RTX 4070 Ti 12GB

## Structure
- `app.py`: Streamlit 관제 대시보드 (메인 진입점)
- `detector.py`: YOLO26n 객체 탐지 + 바운딩 박스 시각화
- `inference.py`: VLM 추론 파이프라인 (YOLO 결과 주입 지원)
- `prompts.py`: 시스템/유저 프롬프트 템플릿 (탐지 결과 포함 버전)
- `config.py`: 모델 ID, 생성 파라미터, 출력 스키마
- `images/samples/`: BDD100K 샘플 이미지
- `outputs/`: 결과 저장 (gitignore 대상)

## Pipeline
이미지 → YOLO26n (객체 탐지) → 탐지 요약을 VLM 프롬프트에 주입 → Qwen3-VL-4B (관제 요약 JSON)

## Rules
- outputs/ 폴더는 커밋하지 않는다
- 이미지는 소량 샘플만 포함한다
- 모델 가중치(*.pt)는 커밋하지 않는다
- zip 파일은 커밋하지 않는다
