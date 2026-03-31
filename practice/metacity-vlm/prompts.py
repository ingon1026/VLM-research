"""관제 관점 프롬프트 템플릿."""

import json
from config import OUTPUT_SCHEMA

SYSTEM_PROMPT = """You are an urban monitoring analyst for a digital twin city system.
Your role is to analyze city scene images from an operator's perspective and provide structured surveillance summaries.

Rules:
- Focus on operationally relevant information (traffic, pedestrians, anomalies, risks)
- Be objective and concise
- Always respond in the exact JSON format specified
- Write the "summary" field in Korean
- Do not hallucinate objects that are not clearly visible"""

USER_PROMPT_TEMPLATE = """Analyze this city scene image from a monitoring operator's perspective.

Return your analysis as a JSON object with exactly these fields:

{schema}

Respond ONLY with the JSON object. No explanation, no markdown."""

USER_PROMPT_WITH_DETECTION_TEMPLATE = """Analyze this city scene image from a monitoring operator's perspective.

An object detector has identified the following objects in this image:
{detection_summary}

Use this detection data as quantitative evidence for your analysis.
The object counts should directly inform your density assessments (traffic_density, pedestrian_density).

Return your analysis as a JSON object with exactly these fields:

{schema}

Respond ONLY with the JSON object. No explanation, no markdown."""


def build_user_prompt(detection_summary: str | None = None) -> str:
    """스키마를 포함한 유저 프롬프트 생성.

    Args:
        detection_summary: YOLO 탐지 요약 텍스트. None이면 탐지 없이 동작.
    """
    schema_str = json.dumps(OUTPUT_SCHEMA, indent=2, ensure_ascii=False)

    if detection_summary:
        return USER_PROMPT_WITH_DETECTION_TEMPLATE.format(
            detection_summary=detection_summary,
            schema=schema_str,
        )
    return USER_PROMPT_TEMPLATE.format(schema=schema_str)
