from __future__ import annotations

import streamlit as st

from components import inject_styles, render_assistant, render_product_card, render_stat_card
from helpers import (
    assistant_summary,
    assistant_suggestions,
    dashboard_stats,
    discount_percent,
    filter_inventory,
    format_currency,
    load_inventory,
)


st.set_page_config(
    page_title="Returns Marketplace MVP",
    page_icon="📦",
    layout="wide",
)

inject_styles()
inventory = load_inventory()

categories = ["All", *sorted({item["category"] for item in inventory})]
conditions = ["All", *sorted({item["condition"] for item in inventory})]
budget_options = ["Any budget", "100", "200", "350", "500", "1000"]

if "query" not in st.session_state:
    st.session_state.query = "headphones under $200"


st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">Amazon-style returns marketplace MVP</div>
        <div class="hero-title">Recover more value from returns with guided deal discovery.</div>
        <div class="hero-copy">
            Browse inspected return inventory, surface the highest-value resale opportunities,
            and let a shopping assistant highlight the best matches by budget, condition, and category.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.6, 1.0], gap="large")

with left:
    query = st.text_input(
        "Search return deals",
        value=st.session_state.query,
        placeholder="Try: headphones under $200",
        label_visibility="collapsed",
    )
    st.session_state.query = query
    st.caption("Popular searches: headphones under $200, travel tech, home office, kitchen, apple")

with right:
    if st.button("Reset filters", use_container_width=True):
        st.session_state.query = ""
        st.rerun()


filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    selected_category = st.selectbox("Category", categories)
with filter_col2:
    selected_condition = st.selectbox("Condition", conditions)
with filter_col3:
    selected_budget = st.selectbox(
        "Budget",
        budget_options,
        format_func=lambda value: "Any budget" if value == "Any budget" else f"Under ${value}",
    )

filtered_items = filter_inventory(
    inventory=inventory,
    query=st.session_state.query,
    category=selected_category,
    condition=selected_condition,
    budget_choice=selected_budget,
)

stats = dashboard_stats(filtered_items)
suggestions = assistant_suggestions(filtered_items, st.session_state.query, selected_budget)

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    render_stat_card("Recovered value", format_currency(stats["recovered_value"]))
with stat_col2:
    render_stat_card("Average discount", f'{stats["avg_discount"]}%')
with stat_col3:
    render_stat_card("Matched items", str(stats["matched_items"]))

content_col, assistant_col = st.columns([1.7, 0.9], gap="large")

with assistant_col:
    render_assistant(assistant_summary(st.session_state.query, filtered_items), suggestions)

with content_col:
    st.markdown(
        """
        <div class="panel-card">
            <div class="panel-heading">Filtered inventory</div>
            <div class="assistant-copy">
                Use the search bar, category, condition, and budget filters to surface the best return deals.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    if not filtered_items:
        st.markdown(
            """
            <div class="empty-card">
                <h3 style="margin-bottom: 0.35rem; color:#020617;">No deals match the current filters</h3>
                <p style="color:#64748b; margin:0;">Try widening the budget or switching to a broader category.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        product_columns = st.columns(2, gap="large")
        for index, item in enumerate(filtered_items):
            with product_columns[index % 2]:
                render_product_card(
                    item=item,
                    discount=discount_percent(item),
                    savings=format_currency(item["new_price"] - item["return_price"]),
                )
