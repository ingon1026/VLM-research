# Image VQA with Qwen3-VL

Qwen3-VL 모델을 활용한 이미지 질의응답(VQA) 실습 프로젝트입니다.

## 모델
- [Qwen3-VL-2B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct)

## 환경 설정
```bash
conda env create -f environment.yml
conda activate vlm-research
```

## 사용 방법

### 단일 이미지
```bash
python vqa.py --image test1.png --question "이 이미지에 뭐가 있어?"
```

### 여러 이미지 한번에
```bash
python vqa.py --image test1.png test2.png --question "이 이미지에 뭐가 있어?"
```

## 출력 예시
```
이미지: test1.png
질문: 이 이미지에 뭐가 있어?
답변: 아이들이 공원에서 놀고 있습니다.
----------------------------------------
```

## 구현 내용
- Qwen3-VL 모델 로드 및 추론
- argparse를 활용한 CLI 인터페이스
- 여러 이미지 배치 처리

- <img width="1103" height="389" alt="image" src="https://github.com/user-attachments/assets/96a5af70-eab4-4610-b2e5-a7f495f9b69e" />
