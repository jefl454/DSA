"""
promo_optimizer.py — POLY-SHIP Logistics System
Phần 3: Tối ưu hóa khuyến mãi bằng Dynamic Programming
  - fibonacci_dp     : Fibonacci có memoization / tabulation
  - climbing_stairs  : số cách leo n bậc (1 hoặc 2 bước mỗi lần)
  - knapsack_2d      : knapsack 0/1 bảng 2 chiều (trực quan)
  - knapsack_1d      : knapsack 0/1 bảng 1 chiều (tối ưu bộ nhớ)
"""


# ─────────────────────────────────────────────
# 3.0  FIBONACCI — DP CƠ BẢN
# ─────────────────────────────────────────────

def fibonacci_memo(n, memo=None):
    """
    Fibonacci với Memoization (top-down DP).
    Tránh tính lại sub-problem → O(n) time, O(n) space.
    """
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]


def fibonacci_tab(n):
    """
    Fibonacci với Tabulation (bottom-up DP).
    Xây bảng từ nhỏ lên → O(n) time, O(1) space.
    """
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        curr  = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1


def demo_fibonacci():
    """Demo so sánh Fibonacci đệ quy ngây thơ vs DP."""
    print("=" * 60)
    print("  DEMO 6a — FIBONACCI (DYNAMIC PROGRAMMING)")
    print("  Ví dụ nền tảng: tránh tính lại bài toán con")
    print("=" * 60)

    print("\n  Bảng Fibonacci (n = 0 → 15):")
    print("    n  : " + "  ".join(f"{i:3d}" for i in range(16)))
    print("    F(n): " + "  ".join(f"{fibonacci_tab(i):3d}" for i in range(16)))

    print("\n  So sánh Memo vs Tabulation:")
    for n in [10, 20, 35, 50]:
        fm = fibonacci_memo(n)
        ft = fibonacci_tab(n)
        print(f"    F({n:2d}) = {fm:12,}   (memo) | {ft:12,}   (tab)")

    print("\n  ★ Bài học: DP lưu kết quả trung gian, tránh exponential recursion.")


# ─────────────────────────────────────────────
# 3.1  CLIMBING STAIRS
# ─────────────────────────────────────────────

def climbing_stairs(n):
    """
    Số cách leo n bậc thang, mỗi lần 1 hoặc 2 bậc.
    DP: f(n) = f(n-1) + f(n-2) — giống Fibonacci.
    Ứng dụng: số tổ hợp giao hàng theo lô.
    """
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        curr  = prev1 + prev2
        prev2 = prev1
        prev1 = curr
    return prev1


def demo_climbing_stairs():
    """Demo climbing stairs — số cách giao theo lô."""
    print("\n  DEMO 6b — CLIMBING STAIRS")
    print("  Số cách chia lô giao hàng (1 hoặc 2 đơn/lượt):")
    print()
    for n in range(1, 11):
        ways = climbing_stairs(n)
        bar  = "█" * min(ways, 40)
        print(f"    {n:2d} đơn hàng → {ways:4d} cách  {bar}")
    print()
    print("  ★ Nhận xét: f(n) = f(n-1) + f(n-2) → cùng cấu trúc Fibonacci.")


# ─────────────────────────────────────────────
# 3.2  KNAPSACK 0/1 — BẢNG 2 CHIỀU
# ─────────────────────────────────────────────

def knapsack_2d(weights, values, capacity):
    """
    Knapsack 0/1 — bảng DP 2 chiều.
    dp[i][w] = giá trị lớn nhất dùng i sản phẩm đầu, ngân sách w.

    Trả về: (max_value, dp_table, selected_items)
    """
    n  = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(capacity + 1):
            # Không chọn item i
            dp[i][w] = dp[i - 1][w]
            # Chọn item i (nếu đủ ngân sách)
            if w >= w_i:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - w_i] + v_i)

    # Truy vết: tìm các item được chọn
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)      # 0-indexed
            w -= weights[i - 1]
    selected.reverse()

    return dp[n][capacity], dp, selected


# ─────────────────────────────────────────────
# 3.3  KNAPSACK 0/1 — BẢNG 1 CHIỀU (tối ưu)
# ─────────────────────────────────────────────

def knapsack_1d(weights, values, capacity):
    """
    Knapsack 0/1 — bảng DP 1 chiều (space-optimized).
    dp[w] = giá trị lớn nhất với ngân sách w.
    Duyệt w từ lớn → nhỏ để đảm bảo mỗi item chọn tối đa 1 lần.

    Trả về: max_value
    """
    dp = [0] * (capacity + 1)

    for i in range(len(weights)):
        w_i = weights[i]
        v_i = values[i]
        for w in range(capacity, w_i - 1, -1):   # duyệt ngược
            dp[w] = max(dp[w], dp[w - w_i] + v_i)

    return dp[capacity]


def demo_knapsack():
    """
    Demo knapsack 0/1: chọn combo sản phẩm khuyến mãi
    trong giới hạn ngân sách nhưng đạt giá trị cao nhất.
    """
    print("=" * 60)
    print("  DEMO 7 — COMBO KHUYẾN MÃI (KNAPSACK 0/1)")
    print("  Chọn gói sản phẩm tối ưu trong giới hạn ngân sách")
    print("=" * 60)

    # Danh sách sản phẩm POLY-SHOP
    products = [
        {"name": "Áo thun",       "weight": 2, "value": 30},
        {"name": "Quần jean",     "weight": 4, "value": 70},
        {"name": "Giày thể thao", "weight": 5, "value": 90},
        {"name": "Túi xách",      "weight": 3, "value": 50},
        {"name": "Mũ lưỡi trai", "weight": 1, "value": 20},
        {"name": "Dép sandal",    "weight": 2, "value": 35},
        {"name": "Balo laptop",   "weight": 6, "value": 110},
    ]

    weights  = [p["weight"] for p in products]
    values   = [p["value"]  for p in products]
    capacity = 10   # ngân sách (đơn vị điểm / trọng số)

    print(f"\n  Ngân sách khuyến mãi: {capacity} điểm")
    print(f"  {'#':3s} {'Sản phẩm':20s} {'Trọng số':10s} {'Giá trị':10s}")
    print(f"  {'-'*45}")
    for i, p in enumerate(products):
        print(f"  {i+1:3d} {p['name']:20s} {p['weight']:10d} {p['value']:10d}")

    # ── Knapsack 2D
    max_val_2d, dp, selected = knapsack_2d(weights, values, capacity)

    print(f"\n  ── Kết quả Knapsack 2D ──")
    print(f"  Giá trị tối đa: {max_val_2d}")
    print(f"  Sản phẩm được chọn:")
    total_w = 0
    for idx in selected:
        p = products[idx]
        total_w += p["weight"]
        print(f"    ✔ {p['name']:20s}  w={p['weight']}  v={p['value']}")
    print(f"  Tổng trọng số dùng: {total_w}/{capacity}")

    # ── In bảng DP (rút gọn)
    print(f"\n  Bảng DP 2D (dp[item][budget]) — rút gọn:")
    header = "        " + "".join(f"{w:4d}" for w in range(capacity + 1))
    print(f"  {header}")
    for i in range(len(products) + 1):
        label = f"  item{i:2d} " if i > 0 else "  base   "
        row   = "".join(f"{dp[i][w]:4d}" for w in range(capacity + 1))
        print(f"  {label}{row}")

    # ── Knapsack 1D
    max_val_1d = knapsack_1d(weights, values, capacity)
    print(f"\n  ── Kết quả Knapsack 1D (space-optimized) ──")
    print(f"  Giá trị tối đa: {max_val_1d}  (khớp với 2D: {'✔' if max_val_1d == max_val_2d else '✘'})")
    print(f"  Bộ nhớ: O(W) = {capacity + 1} ô thay vì O(n·W) = {(len(products)+1)*(capacity+1)} ô")

    # ── Thêm case: nhiều ngân sách khác nhau
    print(f"\n  Bảng tối ưu theo ngân sách:")
    print(f"  {'Ngân sách':12s} {'Max Value 1D':15s}")
    print(f"  {'-'*28}")
    for cap in range(0, capacity + 1):
        mv = knapsack_1d(weights, values, cap)
        bar = "▪" * (mv // 5)
        print(f"  {cap:12d} {mv:15d}  {bar}")

    print()
    print("  ★ Kết luận: Knapsack 0/1 DP cho phép POLY-SHIP đề xuất")
    print("    combo sản phẩm có giá trị cao nhất trong giới hạn ngân")
    print("    sách khuyến mãi — bài toán NP-hard giải được bằng DP")
    print("    trong O(n × W) thời gian.")
