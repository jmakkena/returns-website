from __future__ import annotations

import streamlit as st

from helpers import format_currency


CONDITION_COLORS = {
    "Like New": ("#dcfce7", "#166534"),
    "Open Box": ("#fef3c7", "#92400e"),
    "Damaged Packaging": ("#dbeafe", "#1d4ed8"),
    "Lightly Used": ("#e2e8f0", "#334155"),
}

CATEGORY_GRADIENTS = {
    "Electronics": "linear-gradient(135deg, #0ea5e9 0%, #22d3ee 50%, #2dd4bf 100%)",
    "Computers": "linear-gradient(135deg, #4f46e5 0%, #3b82f6 50%, #22d3ee 100%)",
    "Home": "linear-gradient(135deg, #fb923c 0%, #f59e0b 50%, #facc15 100%)",
    "Accessories": "linear-gradient(135deg, #ec4899 0%, #f472b6 50%, #fb7185 100%)",
    "Wearables": "linear-gradient(135deg, #10b981 0%, #14b8a6 50%, #22d3ee 100%)",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top, rgba(125, 211, 252, 0.35), transparent 28%),
                linear-gradient(180deg, #f8fbff 0%, #eff6ff 48%, #f8fafc 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1240px;
        }
        .hero-card, .panel-card, .assistant-card, .product-card, .stat-card {
            border-radius: 28px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 22px 60px -42px rgba(15, 23, 42, 0.38);
        }
        .hero-card {
            padding: 2rem;
        }
        .eyebrow {
            display: inline-block;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            background: #e0f2fe;
            color: #0369a1;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }
        .hero-title {
            font-size: 3rem;
            line-height: 1.05;
            font-weight: 800;
            color: #020617;
            margin: 1rem 0 0.75rem;
        }
        .hero-copy {
            color: #475569;
            font-size: 1rem;
            line-height: 1.75;
            max-width: 52rem;
        }
        .query-hint {
            margin-top: 0.8rem;
            color: #64748b;
            font-size: 0.92rem;
        }
        .stat-card {
            padding: 1.25rem;
            min-height: 132px;
        }
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
        }
        .stat-value {
            margin-top: 0.45rem;
            color: #020617;
            font-size: 2rem;
            font-weight: 800;
        }
        .assistant-card, .panel-card {
            padding: 1.4rem;
        }
        .assistant-heading, .panel-heading {
            color: #020617;
            font-size: 1.3rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .assistant-copy {
            color: #475569;
            line-height: 1.7;
            font-size: 0.96rem;
        }
        .assistant-suggestion {
            margin-top: 0.9rem;
            padding: 1rem;
            border-radius: 20px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }
        .assistant-name {
            font-weight: 800;
            color: #020617;
        }
        .assistant-meta {
            color: #059669;
            font-size: 0.88rem;
            font-weight: 700;
        }
        .assistant-reason {
            margin-top: 0.4rem;
            color: #475569;
            font-size: 0.94rem;
            line-height: 1.6;
        }
        .product-card {
            overflow: hidden;
            margin-bottom: 1rem;
        }
        .product-hero {
            padding: 1.15rem 1.2rem;
            color: white;
        }
        .product-body {
            padding: 1.2rem;
        }
        .category-pill, .track-pill, .condition-pill, .meta-pill, .tag-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.32rem 0.78rem;
            font-size: 0.76rem;
            font-weight: 700;
        }
        .category-pill, .track-pill {
            background: rgba(255,255,255,0.16);
            color: white;
            backdrop-filter: blur(6px);
        }
        .track-pill {
            margin-left: 0.45rem;
        }
        .product-brand {
            margin-top: 1.2rem;
            opacity: 0.88;
            font-weight: 600;
        }
        .product-name {
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.15;
            margin-top: 0.25rem;
        }
        .price-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: flex-end;
            margin-top: 1rem;
        }
        .return-price {
            color: #020617;
            font-size: 2rem;
            font-weight: 800;
        }
        .new-price {
            color: #94a3b8;
            text-decoration: line-through;
            text-align: right;
        }
        .savings {
            color: #059669;
            font-weight: 700;
            margin-top: 0.3rem;
            text-align: right;
        }
        .note-box {
            margin-top: 1rem;
            border-radius: 18px;
            background: #f8fafc;
            padding: 0.95rem;
            color: #475569;
            line-height: 1.65;
            font-size: 0.94rem;
        }
        .meta-row, .tag-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        .meta-pill, .tag-pill {
            background: #e2e8f0;
            color: #334155;
        }
        .empty-card {
            text-align: center;
            padding: 2.5rem 1.5rem;
            border: 1px dashed #cbd5e1;
            border-radius: 28px;
            background: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_assistant(summary: str, suggestions: list[dict]) -> None:
    html = [
        '<div class="assistant-card">',
        '<div class="assistant-heading">Shopping assistant</div>',
        f'<div class="assistant-copy">{summary}</div>',
    ]

    for item in suggestions:
        html.append(
            f"""
            <div class="assistant-suggestion">
                <div class="assistant-name">{item["product"]}</div>
                <div class="assistant-meta">{format_currency(item["return_price"])} • {item["discount"]}% off</div>
                <div class="assistant-reason">{item["reason"]}</div>
            </div>
            """
        )

    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def render_product_card(item: dict, discount: int, savings: str) -> None:
    badge_bg, badge_fg = CONDITION_COLORS.get(item["condition"], ("#e2e8f0", "#334155"))
    gradient = CATEGORY_GRADIENTS.get(
        item["category"],
        "linear-gradient(135deg, #475569 0%, #64748b 50%, #94a3b8 100%)",
    )

    fast_track = '<span class="track-pill">Fast-track return</span>' if item["fast_track"] else ""
    tags = "".join([f'<span class="tag-pill">{tag}</span>' for tag in item["tags"]])

    st.markdown(
        f"""
        <div class="product-card">
            <div class="product-hero" style="background: {gradient};">
                <span class="category-pill">{item["category"]}</span>{fast_track}
                <div class="product-brand">{item["brand"]}</div>
                <div class="product-name">{item["product"]}</div>
            </div>
            <div class="product-body">
                <span class="condition-pill" style="background: {badge_bg}; color: {badge_fg};">
                    {item["condition"]}
                </span>
                <div class="price-row">
                    <div>
                        <div style="color:#64748b; font-size:0.82rem; text-transform:uppercase; letter-spacing:0.12em;">
                            Return price
                        </div>
                        <div class="return-price">{format_currency(item["return_price"])}</div>
                    </div>
                    <div>
                        <div class="new-price">{format_currency(item["new_price"])}</div>
                        <div class="savings">Save {savings} ({discount}%)</div>
                    </div>
                </div>
                <div class="note-box">{item["note"]}</div>
                <div class="meta-row">
                    <span class="meta-pill">{item["location"]}</span>
                    <span class="meta-pill">{item["inventory_count"]} inspected units</span>
                    <span class="meta-pill">Rating {item["rating"]}</span>
                </div>
                <div class="tag-row">{tags}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
