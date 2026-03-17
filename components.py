from __future__ import annotations

from html import escape

import streamlit as st

from helpers import format_currency


CONDITION_COLORS = {
    "Like New": ("#dcfce7", "#166534"),
    "Open Box": ("#fef3c7", "#92400e"),
    "Damaged Packaging": ("#dbeafe", "#1d4ed8"),
    "Lightly Used": ("#e2e8f0", "#334155"),
}

CATEGORY_GRADIENTS = {
    "Electronics": "linear-gradient(135deg, #0284c7 0%, #06b6d4 50%, #2dd4bf 100%)",
    "Computers": "linear-gradient(135deg, #4338ca 0%, #2563eb 50%, #22d3ee 100%)",
    "Home": "linear-gradient(135deg, #ea580c 0%, #f59e0b 50%, #facc15 100%)",
    "Accessories": "linear-gradient(135deg, #db2777 0%, #f472b6 50%, #fb7185 100%)",
    "Wearables": "linear-gradient(135deg, #059669 0%, #14b8a6 50%, #22d3ee 100%)",
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top, rgba(125, 211, 252, 0.28), transparent 24%),
                radial-gradient(circle at right, rgba(165, 180, 252, 0.18), transparent 18%),
                linear-gradient(180deg, #f8fbff 0%, #eef6ff 52%, #f8fafc 100%);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3.5rem;
            max-width: 1260px;
        }
        .hero-card, .glass-card, .assistant-card, .product-card, .stat-card, .snapshot-card {
            border-radius: 30px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 28px 70px -46px rgba(15, 23, 42, 0.42);
            backdrop-filter: blur(12px);
        }
        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2.25rem;
            min-height: 320px;
            background:
                radial-gradient(circle at top right, rgba(255,255,255,0.55), transparent 26%),
                linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(240,249,255,0.96) 100%);
        }
        .hero-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(120deg, rgba(14,165,233,0.08), transparent 34%),
                linear-gradient(320deg, rgba(99,102,241,0.08), transparent 28%);
            pointer-events: none;
        }
        .eyebrow {
            position: relative;
            display: inline-block;
            padding: 0.5rem 0.9rem;
            border-radius: 999px;
            background: #e0f2fe;
            color: #0369a1;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.2em;
            text-transform: uppercase;
        }
        .hero-title {
            position: relative;
            font-size: 3.35rem;
            line-height: 0.98;
            font-weight: 900;
            color: #020617;
            margin: 1.15rem 0 0.9rem;
            max-width: 14ch;
        }
        .hero-copy {
            position: relative;
            color: #475569;
            font-size: 1.03rem;
            line-height: 1.82;
            max-width: 52rem;
        }
        .hero-chip-row {
            position: relative;
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1.2rem;
        }
        .hero-chip {
            border-radius: 999px;
            background: #f8fafc;
            border: 1px solid #dbeafe;
            color: #0f172a;
            padding: 0.48rem 0.85rem;
            font-size: 0.84rem;
            font-weight: 700;
        }
        .snapshot-card {
            overflow: hidden;
            padding: 1.6rem;
            min-height: 320px;
            color: white;
            background: linear-gradient(145deg, #0f172a 0%, #0f766e 54%, #22c55e 100%);
        }
        .snapshot-kicker {
            font-size: 0.75rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: rgba(255,255,255,0.72);
            font-weight: 800;
        }
        .snapshot-title {
            margin-top: 0.9rem;
            font-size: 2.2rem;
            font-weight: 900;
            line-height: 1.02;
        }
        .snapshot-copy {
            margin-top: 0.9rem;
            color: rgba(255,255,255,0.84);
            line-height: 1.75;
        }
        .snapshot-stat {
            margin-top: 1.2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255,255,255,0.16);
        }
        .snapshot-stat-label {
            color: rgba(255,255,255,0.68);
            font-size: 0.82rem;
        }
        .snapshot-stat-value {
            margin-top: 0.3rem;
            font-size: 1.65rem;
            font-weight: 800;
        }
        .glass-card {
            padding: 1.35rem;
        }
        .section-kicker {
            color: #64748b;
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            font-weight: 800;
        }
        .section-title {
            color: #020617;
            font-size: 1.45rem;
            font-weight: 900;
            margin-top: 0.35rem;
        }
        .section-copy {
            color: #475569;
            font-size: 0.96rem;
            line-height: 1.72;
            margin-top: 0.35rem;
        }
        .stat-card {
            padding: 1.2rem 1.25rem 1.3rem;
            min-height: 128px;
            position: relative;
            overflow: hidden;
        }
        .stat-card::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(90deg, #0ea5e9 0%, #22d3ee 50%, #2dd4bf 100%);
        }
        .stat-label {
            color: #64748b;
            font-size: 0.9rem;
        }
        .stat-value {
            margin-top: 0.5rem;
            color: #020617;
            font-size: 2rem;
            font-weight: 900;
        }
        .assistant-card {
            padding: 1.35rem;
            background:
                radial-gradient(circle at top right, rgba(224, 242, 254, 0.85), transparent 26%),
                rgba(255,255,255,0.95);
        }
        .assistant-heading {
            color: #020617;
            font-size: 1.3rem;
            font-weight: 900;
            margin-bottom: 0.35rem;
        }
        .assistant-copy {
            color: #475569;
            line-height: 1.72;
            font-size: 0.96rem;
        }
        .assistant-suggestion {
            margin-top: 0.95rem;
            padding: 1rem;
            border-radius: 22px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
        }
        .assistant-name {
            font-weight: 900;
            color: #020617;
        }
        .assistant-meta {
            color: #059669;
            font-size: 0.88rem;
            font-weight: 800;
            margin-top: 0.2rem;
        }
        .assistant-reason {
            margin-top: 0.45rem;
            color: #475569;
            font-size: 0.94rem;
            line-height: 1.6;
        }
        .product-card {
            overflow: hidden;
            margin-bottom: 1rem;
            transition: transform 180ms ease;
        }
        .product-card:hover {
            transform: translateY(-2px);
        }
        .product-hero {
            padding: 1.2rem 1.2rem 1.35rem;
            color: white;
            position: relative;
        }
        .product-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at top right, rgba(255,255,255,0.24), transparent 30%);
        }
        .product-body {
            padding: 1.2rem;
        }
        .category-pill, .track-pill, .condition-pill, .meta-pill, .tag-pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.34rem 0.8rem;
            font-size: 0.75rem;
            font-weight: 800;
        }
        .category-pill, .track-pill {
            position: relative;
            background: rgba(255,255,255,0.16);
            color: white;
            backdrop-filter: blur(6px);
        }
        .track-pill {
            margin-left: 0.45rem;
        }
        .product-brand {
            position: relative;
            margin-top: 1.25rem;
            opacity: 0.9;
            font-weight: 700;
        }
        .product-name {
            position: relative;
            font-size: 1.45rem;
            font-weight: 900;
            line-height: 1.1;
            margin-top: 0.3rem;
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
            font-weight: 900;
        }
        .new-price {
            color: #94a3b8;
            text-decoration: line-through;
            text-align: right;
        }
        .savings {
            color: #059669;
            font-weight: 800;
            margin-top: 0.3rem;
            text-align: right;
        }
        .note-box {
            margin-top: 1rem;
            border-radius: 20px;
            background: #f8fafc;
            padding: 1rem;
            color: #475569;
            line-height: 1.7;
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
            padding: 2.6rem 1.5rem;
            border: 1px dashed #cbd5e1;
            border-radius: 28px;
            background: white;
        }
        div[data-testid="stTextInputRootElement"] > div,
        div[data-testid="stSelectbox"] > div > div {
            border-radius: 18px !important;
        }
        div[data-baseweb="input"] {
            border: 1px solid #cbd5e1 !important;
            background: white !important;
            box-shadow: none !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 0 1px #0ea5e9 !important;
        }
        .stTextInput input, .stSelectbox input {
            font-size: 0.98rem !important;
        }
        .stButton > button {
            border-radius: 16px !important;
            border: 0 !important;
            background: linear-gradient(135deg, #0f172a 0%, #0369a1 100%) !important;
            color: white !important;
            font-weight: 800 !important;
            min-height: 3rem !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #082f49 0%, #0284c7 100%) !important;
            color: white !important;
        }
        @media (max-width: 900px) {
            .hero-title {
                font-size: 2.45rem;
            }
            .snapshot-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-card">
            <div class="eyebrow">Amazon-style returns marketplace MVP</div>
            <div class="hero-title">Recover more value from returns with guided deal discovery.</div>
            <div class="hero-copy">
                Browse inspected return inventory, surface the highest-value resale opportunities,
                and let a shopping assistant highlight the best matches by budget, condition, and category.
            </div>
            <div class="hero-chip-row">
                <span class="hero-chip">Search return deals</span>
                <span class="hero-chip">Explain item condition</span>
                <span class="hero-chip">Match by budget</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_snapshot_card(total_items: int, category_count: int) -> None:
    st.markdown(
        f"""
        <div class="snapshot-card">
            <div class="snapshot-kicker">Marketplace snapshot</div>
            <div class="snapshot-title">{total_items} active return SKUs</div>
            <div class="snapshot-copy">
                Inventory spans premium electronics, home upgrades, accessories, and wearables with condition notes
                ready for buyers.
            </div>
            <div class="snapshot-stat">
                <div class="snapshot-stat-label">Live categories</div>
                <div class="snapshot-stat-value">{category_count}</div>
            </div>
            <div class="snapshot-stat">
                <div class="snapshot-stat-label">Positioning</div>
                <div class="snapshot-stat-value">Value-first resale</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(kicker: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="section-kicker">{escape(kicker)}</div>
            <div class="section-title">{escape(title)}</div>
            <div class="section-copy">{escape(copy)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{escape(label)}</div>
            <div class="stat-value">{escape(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_assistant(summary: str, suggestions: list[dict]) -> None:
    html = [
        '<div class="assistant-card">',
        '<div class="section-kicker">Shopping assistant</div>',
        '<div class="assistant-heading">Deal guidance</div>',
        f'<div class="assistant-copy">{escape(summary)}</div>',
    ]

    for item in suggestions:
        html.append(
            f"""
            <div class="assistant-suggestion">
                <div class="assistant-name">{escape(item["product"])}</div>
                <div class="assistant-meta">{escape(format_currency(item["return_price"]))} | {item["discount"]}% off</div>
                <div class="assistant-reason">{escape(item["reason"])}</div>
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
    tags = "".join([f'<span class="tag-pill">{escape(tag)}</span>' for tag in item["tags"]])

    st.markdown(
        f"""
        <div class="product-card">
            <div class="product-hero" style="background: {gradient};">
                <span class="category-pill">{escape(item["category"])}</span>{fast_track}
                <div class="product-brand">{escape(item["brand"])}</div>
                <div class="product-name">{escape(item["product"])}</div>
            </div>
            <div class="product-body">
                <span class="condition-pill" style="background: {badge_bg}; color: {badge_fg};">
                    {escape(item["condition"])}
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
                <div class="note-box">{escape(item["note"])}</div>
                <div class="meta-row">
                    <span class="meta-pill">{escape(item["location"])}</span>
                    <span class="meta-pill">{item["inventory_count"]} inspected units</span>
                    <span class="meta-pill">Rating {item["rating"]}</span>
                </div>
                <div class="tag-row">{tags}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
