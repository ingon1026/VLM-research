# 👋 VLM-research

안녕하세요! **Vision AI R&D 엔지니어**입니다.

이 레포는 **GitHub 사용법을 익히면서** 동시에 **VLM(Vision-Language Model) 사이드 프로젝트**를 하나씩 구현해 올리는 공간입니다.

학습과 실습을 병행하다 보니 퀄리티가 부족할 수 있지만, 하나씩 개선해 나가고 있습니다. 🙏

<br>

## 🗂️ 사이드 프로젝트

각 프로젝트는 **브랜치별로 분리**되어 있습니다. 아래 링크를 클릭하면 바로 확인할 수 있습니다!

| # | 프로젝트 | 설명 | 기술 스택 | 바로가기 |
|---|----------|------|-----------|----------|
| 1 | 🏙️ **Metacity VLM** | YOLO+VLM 도시 관제 요약 시스템 | Qwen3-VL-4B, YOLO26n, Streamlit | [📂 보러가기](https://github.com/ingon1026/VLM-research/tree/feature/metacity-vlm/practice/metacity-vlm) |
| 2 | 🖼️ **Image VQA** | 이미지 질의응답 실습 | Qwen3-VL-2B | [📂 보러가기](https://github.com/ingon1026/VLM-research/tree/feature/imagesbase/research/imagesbase) |

> 💡 **브랜치 전환 방법**: 위 GitHub 페이지 좌측 상단의 브랜치 드롭다운에서 `feature/metacity-vlm` 또는 `feature/imagesbase`를 선택하세요.

<br>

## 🛠️ 개발 환경

| 구분 | 내용 |
|------|------|
| 🖥️ GPU | NVIDIA RTX 4070 Ti (12GB) |
| 🐍 Python | 3.11 (Anaconda) |
| 🤗 Framework | HuggingFace Transformers, Ultralytics |

<br>

## 📌 레포 구조

```
VLM-research/
├── practice/          # 🔨 구현, 프로토타입
│   └── metacity-vlm/  # → feature/metacity-vlm
└── research/          # 📝 연구, 비교, 노트
    └── imagesbase/    # → feature/imagesbase
```

<br>

---

🚀 새로운 프로젝트가 추가될 때마다 업데이트됩니다. 감사합니다!
