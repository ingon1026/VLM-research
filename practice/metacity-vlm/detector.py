"""YOLO26n 기반 객체 탐지 모듈."""

from collections import Counter

import numpy as np
from PIL import Image
from ultralytics import YOLO

# 관제 관련 클래스만 필터링 (COCO 클래스 기준)
MONITOR_CLASSES = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
    9: "traffic light",
    11: "stop sign",
    15: "cat",
    16: "dog",
}

# 모델 싱글턴
_model = None


def get_yolo_model() -> YOLO:
    """YOLO26n 모델을 로드한다 (최초 1회)."""
    global _model
    if _model is None:
        print("YOLO26n 모델 로딩 중...")
        _model = YOLO("yolo26n.pt")
        print("YOLO26n 모델 로딩 완료")
    return _model


def detect(image_path: str, conf: float = 0.3) -> dict:
    """이미지에서 객체를 탐지한다.

    Returns:
        {
            "detections": [{"class": "car", "conf": 0.85, "bbox": [x1,y1,x2,y2]}, ...],
            "counts": {"car": 5, "person": 3, ...},
            "summary": "car 5, person 3, truck 1",
            "annotated_image": PIL.Image,
        }
    """
    model = get_yolo_model()
    results = model(image_path, conf=conf, verbose=False)[0]

    detections = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id not in MONITOR_CLASSES:
            continue
        detections.append({
            "class": MONITOR_CLASSES[cls_id],
            "conf": float(box.conf[0]),
            "bbox": box.xyxy[0].tolist(),
        })

    # 클래스별 카운트
    counts = Counter(d["class"] for d in detections)

    # 요약 텍스트 (VLM 프롬프트 주입용)
    if counts:
        summary_parts = [f"{cls} {cnt}" for cls, cnt in counts.most_common()]
        summary = ", ".join(summary_parts)
    else:
        summary = "no notable objects detected"

    # 바운딩 박스가 그려진 이미지
    annotated = Image.fromarray(results.plot()[:, :, ::-1])  # BGR → RGB

    return {
        "detections": detections,
        "counts": dict(counts),
        "summary": summary,
        "annotated_image": annotated,
    }
