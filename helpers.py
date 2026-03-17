from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


DATA_PATH = Path(__file__).parent / "data" / "inventory.json"


def load_inventory() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def discount_percent(item: dict) -> int:
    return round(((item["new_price"] - item["return_price"]) / item["new_price"]) * 100)


def parse_budget(query: str) -> int | None:
    match = re.search(r"(?:under|below|max)\s*\$?(\d+)", query, re.IGNORECASE)
    return int(match.group(1)) if match else None


def cleaned_terms(query: str) -> list[str]:
    normalized = re.sub(r"(?:under|below|max)\s*\$?\d+", "", query.lower()).strip()
    return [term for term in normalized.split() if term]


def filter_inventory(
    inventory: Iterable[dict],
    query: str,
    category: str,
    condition: str,
    budget_choice: str,
) -> list[dict]:
    terms = cleaned_terms(query)
    query_budget = parse_budget(query)
    selected_budget = None if budget_choice == "Any budget" else int(budget_choice)
    active_budget = (
        min(query_budget, selected_budget)
        if query_budget is not None and selected_budget is not None
        else query_budget if query_budget is not None
        else selected_budget
    )

    matches = []
    for item in inventory:
        haystack = " ".join(
            [
                item["product"],
                item["brand"],
                item["category"],
                item["condition"],
                item["location"],
                *item["tags"],
            ]
        ).lower()

        matches_query = not terms or all(term in haystack for term in terms)
        matches_category = category == "All" or item["category"] == category
        matches_condition = condition == "All" or item["condition"] == condition
        matches_budget = active_budget is None or item["return_price"] <= active_budget

        if matches_query and matches_category and matches_condition and matches_budget:
            matches.append(item)

    return matches


def dashboard_stats(items: list[dict]) -> dict:
    if not items:
        return {"recovered_value": 0, "avg_discount": 0, "matched_items": 0}

    recovered_value = sum(item["return_price"] for item in items)
    avg_discount = round(sum(discount_percent(item) for item in items) / len(items))
    return {
        "recovered_value": recovered_value,
        "avg_discount": avg_discount,
        "matched_items": len(items),
    }


def suggestion_reason(item: dict, budget: int | None) -> str:
    if budget is not None and item["return_price"] <= budget:
        return f"Fits your budget and still lands a {discount_percent(item)}% markdown from retail."
    if item["fast_track"]:
        return "Fast-track routing makes this a strong choice if you want a quick, high-confidence deal."
    if item["condition"] == "Like New":
        return "Best fit if you want near-new quality while shopping the returns channel."
    return f"Balanced value with verified condition details and {discount_percent(item)}% off new."


def assistant_summary(query: str, items: list[dict]) -> str:
    if not items:
        return (
            f'No return deals match "{query or "your current filters"}" yet. '
            "Try widening the budget, choosing a broader category, or switching to Open Box."
        )

    best_discount = max(items, key=discount_percent)
    lowest_price = min(items, key=lambda item: item["return_price"])
    quick_ship = next((item for item in items if item["fast_track"]), None)

    base = (
        f'For "{query}" I found {len(items)} relevant return deals. '
        f'{best_discount["product"]} leads on value at {discount_percent(best_discount)}% off, '
        f'while {lowest_price["product"]} is the lowest upfront spend at '
        f'{format_currency(lowest_price["return_price"])}.'
    )
    if quick_ship:
        return base + f' Fastest route looks like {quick_ship["product"]}.'
    return base


def assistant_suggestions(items: list[dict], query: str, budget_choice: str) -> list[dict]:
    query_budget = parse_budget(query)
    selected_budget = None if budget_choice == "Any budget" else int(budget_choice)
    active_budget = (
        min(query_budget, selected_budget)
        if query_budget is not None and selected_budget is not None
        else query_budget if query_budget is not None
        else selected_budget
    )

    ranked = sorted(
        items,
        key=lambda item: discount_percent(item)
        + (5 if item["fast_track"] else 0)
        + (4 if item["condition"] == "Like New" else 0),
        reverse=True,
    )

    suggestions = []
    for item in ranked[:3]:
        suggestions.append(
            {
                **item,
                "discount": discount_percent(item),
                "reason": suggestion_reason(item, active_budget),
            }
        )
    return suggestions
