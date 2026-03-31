"""Metacity VLM — 도시 관제 모니터링 대시보드."""

import json
import os
import tempfile
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd

from inference import load_model, run_inference, save_result
from detector import detect
from config import IMAGE_DIR

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Metacity VLM",
    page_icon="🏙️",
    layout="wide",
)

# --- 위험도 색상 매핑 ---
RISK_COLORS = {
    "low": "#22c55e",
    "moderate": "#f59e0b",
    "high": "#ef4444",
    "critical": "#dc2626",
}


# --- 모델 캐싱 (앱 전체에서 1회만 로드) ---
@st.cache_resource
def get_model():
    return load_model()


def get_image_files():
    """images/samples/ 폴더에서 이미지 파일 목록을 가져온다."""
    patterns = ["*.jpg", "*.jpeg", "*.png"]
    files = []
    samples_dir = Path(IMAGE_DIR) / "samples"
    for p in patterns:
        files.extend(samples_dir.glob(p))
    return sorted(files)


def parse_result(raw: str) -> dict | None:
    """VLM 출력을 JSON으로 파싱한다."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def render_result_card(result: dict):
    """분석 결과를 카드 형태로 표시한다."""
    risk = result.get("risk_level", "low")
    color = RISK_COLORS.get(risk, "#6b7280")

    st.markdown(f"""
    <div style="
        background: #1e1e2e;
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 12px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <span style="color: #94a3b8; font-size: 14px;">Scene Type</span>
            <span style="color: white; font-size: 18px; font-weight: bold;">
                {result.get('scene_type', '-').upper()}
            </span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8;">Risk Level</span>
            <span style="color: {color}; font-weight: bold;">{risk.upper()}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8;">Time of Day</span>
            <span style="color: white;">{result.get('time_of_day', '-')}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8;">Weather</span>
            <span style="color: white;">{result.get('weather', '-')}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8;">Traffic Density</span>
            <span style="color: white;">{result.get('traffic_density', '-')}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94a3b8;">Pedestrian Density</span>
            <span style="color: white;">{result.get('pedestrian_density', '-')}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
            <span style="color: #94a3b8;">Anomalies</span>
            <span style="color: {'#ef4444' if result.get('anomalies') else '#22c55e'};">
                {', '.join(result.get('anomalies', [])) or 'None'}
            </span>
        </div>
        <div style="
            background: #2a2a3e;
            border-radius: 6px;
            padding: 12px;
            color: #e2e8f0;
            font-size: 14px;
        ">
            {result.get('summary', '-')}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_log_row(entry: dict):
    """관제 로그 한 줄을 반환한다."""
    risk = entry.get("risk_level", "low")
    color = RISK_COLORS.get(risk, "#6b7280")
    return (
        f"| {entry['timestamp']} "
        f"| {entry.get('image', '-')[:25]} "
        f"| **{entry.get('scene_type', '-')}** "
        f"| :{color}[**{risk.upper()}**] "
        f"| {entry.get('summary', '-')[:40]} |"
    )


# --- 헤더 ---
st.markdown("""
<h1 style="text-align: center; color: #e2e8f0; margin-bottom: 0;">
    Metacity VLM
</h1>
<p style="text-align: center; color: #94a3b8; margin-top: 4px; margin-bottom: 32px;">
    Digital Twin City Monitoring System
</p>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if "log" not in st.session_state:
    st.session_state.log = []
if "running" not in st.session_state:
    st.session_state.running = False

# --- 사이드바 ---
with st.sidebar:
    st.header("데모 모니터링")
    image_files = get_image_files()
    st.markdown(f"샘플 이미지: **{len(image_files)}장**")
    interval = st.slider("이미지 간격 (초)", min_value=1, max_value=30, value=3)
    demo_col1, demo_col2 = st.columns(2)
    with demo_col1:
        demo_start = st.button("데모 시작", use_container_width=True)
    with demo_col2:
        demo_stop = st.button("중지", use_container_width=True)

    st.markdown("---")

    st.header("로그 필터")
    risk_filter = st.multiselect(
        "위험도 선택",
        options=["low", "moderate", "high", "critical"],
        default=["low", "moderate", "high", "critical"],
    )

    st.markdown("---")

    if st.button("로그 초기화", use_container_width=True):
        st.session_state.log = []
        st.rerun()

    st.markdown("---")

    # 위험도 통계
    st.header("위험도 통계")
    if st.session_state.log:
        total = len(st.session_state.log)
        counts = Counter(e.get("risk_level", "low") for e in st.session_state.log)
        risk_order = ["low", "moderate", "high", "critical"]
        risk_labels = {"low": "LOW", "moderate": "MOD", "high": "HIGH", "critical": "CRIT"}

        # 위험도별 색상 바 (HTML)
        for r in risk_order:
            cnt = counts.get(r, 0)
            if cnt == 0:
                continue
            color = RISK_COLORS[r]
            pct = int(cnt / total * 100)
            st.markdown(f"""
            <div style="display:flex; align-items:center; margin-bottom:6px;">
                <span style="color:{color}; font-weight:bold; width:42px; font-size:13px;">{risk_labels[r]}</span>
                <div style="flex:1; background:#2a2a3e; border-radius:4px; height:20px; margin:0 8px;">
                    <div style="background:{color}; width:{pct}%; height:100%; border-radius:4px;"></div>
                </div>
                <span style="color:#e2e8f0; font-size:13px; width:30px; text-align:right;">{cnt}</span>
            </div>
            """, unsafe_allow_html=True)

        # 요약
        alert_count = counts.get("high", 0) + counts.get("critical", 0)
        if alert_count > 0:
            st.error(f"주의: **{alert_count}/{total}건**")
        else:
            st.success(f"**{total}건** 정상")
    else:
        st.caption("분석 데이터가 없습니다.")

# --- 메인: 이미지 업로드 ---
uploaded = st.file_uploader(
    "분석할 도시 장면 이미지를 업로드하세요",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=False,
)

# 고정 레이아웃
scene_area = st.empty()
log_area = st.empty()
status_area = st.empty()

if demo_stop:
    st.session_state.running = False


def render_log_table():
    """관제 로그 테이블을 렌더링한다 (위험도 필터 적용)."""
    if not st.session_state.log:
        return
    filtered = [e for e in st.session_state.log if e.get("risk_level", "low") in risk_filter]
    with log_area.container():
        st.markdown("---")
        st.markdown(f"### 관제 로그 ({len(filtered)}/{len(st.session_state.log)}건)")
        if filtered:
            log_header = "| 시간 | 소스 | 장면 | 위험도 | 요약 |\n|------|------|------|--------|------|\n"
            log_rows = "\n".join(render_log_row(e) for e in filtered[:20])
            st.markdown(log_header + log_rows, unsafe_allow_html=True)
        else:
            st.info("선택한 위험도에 해당하는 로그가 없습니다.")


def analyze_and_display(image_path: str, caption: str, source_name: str):
    """YOLO 탐지 → VLM 분석 파이프라인을 실행하고 화면에 표시한다."""
    model, processor = get_model()

    with scene_area.container():
        col_image, col_result = st.columns([1.2, 1])

        with col_image:
            # Step 1: YOLO 탐지
            with st.spinner("YOLO 객체 탐지 중..."):
                det = detect(image_path)

            # 바운딩 박스 이미지 표시
            st.image(det["annotated_image"], caption=caption, use_container_width=True)

            # 탐지 요약 표시
            if det["counts"]:
                counts_text = " | ".join(f"**{cls}** {cnt}" for cls, cnt in det["counts"].items())
                st.markdown(f"탐지 결과: {counts_text}")
            else:
                st.markdown("탐지 결과: 관제 대상 객체 없음")

        with col_result:
            # Step 2: VLM 분석 (YOLO 탐지 결과를 프롬프트에 주입)
            with st.spinner("VLM 분석 중..."):
                raw = run_inference(model, processor, image_path, detection_summary=det["summary"])
                result = parse_result(raw)

            if result:
                # 이상 알림: high/critical이면 경고 배너
                risk = result.get("risk_level", "low")
                if risk == "critical":
                    st.markdown("""
                    <div style="background: #dc2626; color: white; padding: 12px 16px;
                         border-radius: 8px; margin-bottom: 12px; font-weight: bold;
                         text-align: center; font-size: 16px;">
                        ⚠ CRITICAL — 즉시 확인 필요
                    </div>
                    """, unsafe_allow_html=True)
                elif risk == "high":
                    st.markdown("""
                    <div style="background: #ef4444; color: white; padding: 12px 16px;
                         border-radius: 8px; margin-bottom: 12px; font-weight: bold;
                         text-align: center; font-size: 16px;">
                        ⚠ HIGH RISK — 주의 필요
                    </div>
                    """, unsafe_allow_html=True)

                render_result_card(result)
                save_result(image_path, raw)

                st.session_state.log.insert(0, {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "image": source_name,
                    **result,
                })
            else:
                st.error(f"JSON 파싱 실패: {raw[:200]}")

    render_log_table()
    return result


# --- 업로드 이미지 분석 (메인 기능) ---
if uploaded:
    tmp_path = os.path.join(tempfile.gettempdir(), uploaded.name)
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())

    analyze_and_display(tmp_path, f"업로드: {uploaded.name}", f"[upload] {uploaded.name}")

# --- 데모 모니터링 (사이드바에서 시작) ---
elif demo_start and image_files:
    st.session_state.running = True

    for i, img_path in enumerate(image_files):
        if not st.session_state.running:
            break

        analyze_and_display(
            str(img_path),
            f"[{i+1}/{len(image_files)}] {img_path.name}",
            img_path.name,
        )

        if i < len(image_files) - 1:
            time.sleep(interval)

    st.session_state.running = False
    status_area.success("데모 모니터링 완료")

# --- 대기 상태 ---
else:
    render_log_table()
