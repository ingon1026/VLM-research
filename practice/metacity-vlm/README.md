# Metacity VLM

> **YOLO + VLM** 기반 도시 장면 관제 요약 시스템

<br>

## Overview

도시 장면 이미지를 입력받아 **YOLO26n으로 객체를 탐지**하고, 탐지 결과를 근거로 **Qwen3-VL-4B가 관제 요약 JSON**을 생성합니다.

Streamlit 대시보드에서 실시간 모니터링 시뮬레이션을 제공합니다.

```
이미지 → YOLO26n (객체 탐지) → Qwen3-VL-4B (관제 요약) → JSON + 대시보드
```

<br>

## Key Features

| 기능 | 설명 |
|------|------|
| YOLO → VLM 파이프라인 | YOLO 탐지 결과를 VLM 프롬프트에 주입, hallucination 감소 |
| 관제 대시보드 | Streamlit 기반, 이미지 업로드 즉시 분석 |
| 바운딩 박스 시각화 | YOLO 탐지 결과를 이미지 위에 오버레이 |
| 데모 모니터링 | 샘플 이미지 순차 투입 시뮬레이션 |
| 위험도 필터링 | 로그에서 위험도별 필터 |
| 위험도 통계 | 위험도별 색상 바 + 요약 |
| 이상 알림 | HIGH/CRITICAL 감지 시 경고 배너 |

<br>

## Demo

### 대시보드 화면

- 메인: 이미지 업로드 → YOLO 탐지 → VLM 분석 결과 카드
- 사이드바: 데모 모니터링, 위험도 필터, 통계
- 하단: 관제 로그 테이블 (시간순 누적)

### 출력 예시

```json
{
  "scene_type": "highway",
  "time_of_day": "daytime",
  "weather": "rain",
  "traffic_density": "medium",
  "pedestrian_density": "none",
  "anomalies": [],
  "risk_level": "moderate",
  "summary": "비가 내리는 도로에서 차량들이 주행하고 있으며, 운전자는 비를 피하기 위해 주의해야 합니다."
}
```

<br>

## Tech Stack

| 구분 | 내용 | 링크 |
|------|------|------|
| Object Detection | YOLO26n | [Ultralytics Docs](https://docs.ultralytics.com/models/yolo26/) |
| Vision-Language Model | Qwen3-VL-4B-Instruct | [HuggingFace](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) |
| Dashboard | Streamlit | [streamlit.io](https://streamlit.io/) |
| GPU | NVIDIA RTX 4070 Ti (12GB) | |
| Dataset | BDD100K (샘플) | [bdd-data.berkeley.edu](https://bdd-data.berkeley.edu/) |

<br>

## Quick Start

```bash
# 1. conda 환경 생성 및 활성화
conda env create -f environment.yml
conda activate metacity

# 2. 대시보드 실행
streamlit run app.py

# 3. 브라우저에서 http://localhost:8501 접속
```

### CLI로 단건 분석

```bash
python inference.py --image images/samples/sample.jpg
```

<br>

## How to Use

### 대시보드 (Streamlit)

[Streamlit](https://streamlit.io/)은 Python 스크립트를 웹 대시보드로 변환하는 프레임워크입니다.
별도의 프론트엔드 코드 없이 `app.py` 하나로 대시보드가 실행됩니다.

```bash
streamlit run app.py
# → 브라우저에서 http://localhost:8501 자동 오픈
```

#### 이미지 업로드 분석 (메인 기능)

1. 메인 화면의 업로드 영역에 도시 장면 이미지를 드래그앤드롭
2. YOLO26n이 객체를 탐지 → 바운딩 박스가 그려진 이미지 표시
3. Qwen3-VL-4B가 탐지 결과를 근거로 관제 요약 JSON 생성
4. 결과 카드 + 관제 로그에 자동 추가

#### 데모 모니터링

1. 사이드바에서 이미지 간격(초) 설정
2. **데모 시작** 버튼 클릭
3. `images/samples/` 이미지가 순차적으로 분석됨
4. 관제 로그가 실시간으로 누적

#### 위험도 필터 / 통계

- 사이드바 **로그 필터**: low / moderate / high / critical 체크박스로 로그 필터링
- 사이드바 **위험도 통계**: 위험도별 색상 바 + 요약 수치
- HIGH/CRITICAL 감지 시 결과 카드 위에 **경고 배너** 자동 표시

<br>

## Project Structure

```
metacity-vlm/
├── environment.yml    # conda 환경 설정
├── app.py             # Streamlit 관제 대시보드
├── detector.py        # YOLO26n 객체 탐지
├── inference.py       # VLM 추론 파이프라인
├── prompts.py         # 관제 관점 프롬프트 (YOLO 결과 주입)
├── config.py          # 모델·파라미터·스키마 설정
├── images/            # 입력 이미지
│   └── samples/       # BDD100K 샘플
└── outputs/           # 추론 결과 JSON (gitignore)
```

<br>

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  이미지 입력  │────▶│  YOLO26n 탐지     │────▶│  Qwen3-VL-4B 분석  │
└─────────────┘     │  car 7, person 2  │     │  + 탐지 결과 주입   │
                    │  + 바운딩 박스     │     │  → 관제 요약 JSON   │
                    └──────────────────┘     └───────────────────┘
                            │                         │
                    ┌───────▼─────────────────────────▼──────┐
                    │         Streamlit 대시보드              │
                    │  이미지(bbox) │ 결과 카드 │ 관제 로그    │
                    └────────────────────────────────────────┘
```

<br>

## TODO

- [ ] 다중 카메라 시뮬레이션 — 카메라 여러 대가 동시에 들어오는 관제 뷰
- [ ] 동영상 입력 — 영상 프레임 추출 → 실시간 분석
- [ ] 이상 알림 히스토리 — HIGH/CRITICAL 이벤트 별도 타임라인
- [ ] 대시보드 스크린샷 — README Demo 섹션에 실제 화면 첨부

<br>

## License

This project is for educational and research purposes.
