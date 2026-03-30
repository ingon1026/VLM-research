import argparse
import torch
from PIL import Image
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration


def load_model(model_name: str):
    print(f"[모델 로딩] {model_name} ...")
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    processor = AutoProcessor.from_pretrained(model_name)
    print("[모델 로딩 완료]\n")
    return model, processor


def run_vqa(model, processor, image_path: str, question: str) -> str:
    image = Image.open(image_path).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": question},
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    generated_ids = model.generate(**inputs, max_new_tokens=256)
    generated_ids_trimmed = [
        out_ids[len(in_ids):]
        for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True
    )
    return output[0]


def parse_args():
    parser = argparse.ArgumentParser(description="Qwen3-VL 기반 이미지 VQA")
    parser.add_argument("--image", type=str, nargs="+", required=True, help="이미지 파일 경로 (여러 개 가능)")
    parser.add_argument("--question", type=str, required=True, help="이미지에 대한 질문")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-VL-2B-Instruct", help="모델 이름")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    model, processor = load_model(args.model)

    for image_path in args.image:
        print(f"이미지: {image_path}")
        print(f"질문: {args.question}")
        answer = run_vqa(model, processor, image_path, args.question)
        print(f"답변: {answer}")
        print("-" * 40)