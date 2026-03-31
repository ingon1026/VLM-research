# VLM-research

VLM 기초 학습 공간 — 튜토리얼 따라하기 및 개인 실습

<br>

## 현재 브랜치: `feature/metacity-vlm`

> **YOLO + VLM** 기반 도시 장면 관제 요약 시스템

YOLO26n으로 객체를 탐지하고, Qwen3-VL-4B가 관제 요약 JSON을 생성합니다.
Streamlit 대시보드에서 실시간 모니터링 시뮬레이션을 제공합니다.

```
이미지 → YOLO26n (객체 탐지) → Qwen3-VL-4B (관제 요약) → JSON + 대시보드
```

**[프로젝트 상세 보기 →](practice/metacity-vlm/)**

<br>

## 전체 브랜치 구조

| 브랜치 | 프로젝트 | 설명 |
|--------|----------|------|
| `main` | — | 레포 기본 설정 |
| `feature/imagesbase` | [research/imagesbase](https://github.com/ingon1026/VLM-research/tree/feature/imagesbase/research/imagesbase) | Qwen3-VL 이미지 VQA 실습 |
| **`feature/metacity-vlm`** | **[practice/metacity-vlm](practice/metacity-vlm/)** | **YOLO+VLM 도시 관제 요약 시스템** |
