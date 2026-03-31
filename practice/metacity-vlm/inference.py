"""도시 장면 관제 요약 추론 파이프라인."""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import torch
from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

from config import MODEL_ID, GENERATION_CONFIG, OUTPUT_DIR
from prompts import SYSTEM_PROMPT, build_user_prompt


def load_model():
    """모델과 프로세서를 로드한다."""
    print(f"모델 로딩 중: {MODEL_ID}")

    model = Qwen3VLForConditionalGeneration.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    processor = AutoProcessor.from_pretrained(MODEL_ID)

    print("모델 로딩 완료")
    return model, processor


def run_inference(model, processor, image_path: str, detection_summary: str | None = None) -> str:
    """이미지 한 장에 대해 관제 요약을 생성한다.

    Args:
        detection_summary: YOLO 탐지 요약 텍스트. 있으면 프롬프트에 주입.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": build_user_prompt(detection_summary)},
            ],
        },
    ]

    # 입력 전처리
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    ).to(model.device)

    # 생성
    with torch.no_grad():
        output_ids = model.generate(**inputs, **GENERATION_CONFIG)

    # 입력 토큰 제거 후 디코딩
    generated_ids = output_ids[:, inputs.input_ids.shape[1]:]
    result = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return result


def save_result(image_path: str, result: str):
    """결과를 outputs/ 폴더에 JSON 파일로 저장한다."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stem = Path(image_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"{stem}_{timestamp}.json")

    # JSON 파싱 시도, 실패 시 raw 텍스트 저장
    try:
        parsed = json.loads(result)
        payload = {"image": image_path, "result": parsed}
    except json.JSONDecodeError:
        payload = {"image": image_path, "raw_output": result}

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"결과 저장: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="도시 장면 관제 요약")
    parser.add_argument("--image", required=True, help="분석할 이미지 경로")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"이미지를 찾을 수 없습니다: {args.image}")
        return

    model, processor = load_model()
    result = run_inference(model, processor, args.image)

    print("\n--- 관제 요약 ---")
    print(result)

    save_result(args.image, result)


if __name__ == "__main__":
    main()
