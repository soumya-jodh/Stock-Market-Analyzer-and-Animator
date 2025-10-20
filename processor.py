# backend/processor.py
from typing import List, Dict

def find_best_trade(series: List[Dict]) -> Dict:
    """
    Uses Kadane’s Algorithm (Maximum Sum Subarray) to find
    the best single buy-sell days for maximum profit.

    series: list of {"date": str, "price": float}
    Returns JSON-friendly dict with:
      - best_buy
      - best_sell
      - profit
    """
    if not series or len(series) < 2:
        raise ValueError("Need at least 2 price points")

    # Step 1: Extract price list
    prices = [p['price'] for p in series]

    # Step 2: Compute daily price differences
    diffs = [prices[i + 1] - prices[i] for i in range(len(prices) - 1)]

    # Step 3: Apply Kadane’s Algorithm
    max_sum = 0
    curr_sum = 0
    start = 0
    best_start = 0
    best_end = 0

    for i, change in enumerate(diffs):
        curr_sum += change
        if curr_sum > max_sum:
            max_sum = curr_sum
            best_start = start
            best_end = i
        if curr_sum < 0:
            curr_sum = 0
            start = i + 1

    # Step 4: Derive buy/sell indices
    buy_index = best_start
    sell_index = best_end + 1  # +1 because diffs are 1 element shorter

    # Step 5: Build output
    result = {
        "series": series,
        "best_buy": {
            "index": buy_index,
            "date": series[buy_index]['date'],
            "price": series[buy_index]['price']
        },
        "best_sell": {
            "index": sell_index,
            "date": series[sell_index]['date'],
            "price": series[sell_index]['price']
        },
        "profit": round(max_sum, 6),
        "note": "Algorithm: Kadane’s Algorithm (Maximum Sum Subarray)"
    }
    return result
