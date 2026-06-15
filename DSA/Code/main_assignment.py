"""
main_assignment.py — POLY-SHIP Logistics System
Menu console chính: chạy thử tất cả module thuật toán

Cấu trúc:
  1. Demo routing — shortest path giữa 2 kho       (Dijkstra)
  2. Demo MST — mạng kho tối thiểu                 (Kruskal + DSU)
  3. Demo hash table đơn hàng                      (HashTable tự cài)
  4. Demo hashing tổng hợp                         (group anagrams, consecutive, subarray sum)
  5. Demo rolling hash tìm pattern trong log        (Rabin-Karp)
  6. Demo DP cơ bản                                (Fibonacci, Climbing Stairs)
  7. Demo combo khuyến mãi                         (Knapsack 0/1 — 2D & 1D)
  8. Thoát
"""

import sys
import os

# ── Import các module cùng thư mục ──────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from routing import (
    demo_routing_shortest_path,
    demo_mst_network,
)
from hashing_tools import (
    demo_hash_table,
    demo_group_anagrams,
    demo_longest_consecutive,
    demo_subarray_sum,
    demo_rolling_hash,
)
from promo_optimizer import (
    demo_fibonacci,
    demo_climbing_stairs,
    demo_knapsack,
)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

SEPARATOR = "─" * 60

def pause():
    """Dừng lại chờ người dùng nhấn Enter."""
    input("\n  [Nhấn Enter để tiếp tục...]")


def clear():
    """Xóa màn hình (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """In banner tiêu đề hệ thống."""
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║          POLY-SHIP — LOGISTICS ALGORITHM LAB         ║")
    print("  ║   Thư viện giải thuật & Demo — Hệ thống hậu cần     ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()


def print_menu():
    """In menu lựa chọn."""
    print(SEPARATOR)
    print("  MENU CHÍNH")
    print(SEPARATOR)
    print()
    print("  ── PHẦN 1: ROUTING ─────────────────────────────────────")
    print("  [1]  Dijkstra   — Tìm tuyến giao hàng ngắn nhất")
    print("  [2]  Kruskal    — Thiết kế mạng kho tối thiểu (MST)")
    print()
    print("  ── PHẦN 2: HASHING ─────────────────────────────────────")
    print("  [3]  Hash Table — Quản lý & tra cứu đơn hàng O(1)")
    print("  [4]  Hashing    — Group anagrams, consecutive, subarray sum")
    print("  [5]  Rabin-Karp — Tìm pattern trong log giao hàng")
    print()
    print("  ── PHẦN 3: DYNAMIC PROGRAMMING ─────────────────────────")
    print("  [6]  DP cơ bản  — Fibonacci & Climbing Stairs")
    print("  [7]  Knapsack   — Combo khuyến mãi tối ưu (0/1 DP)")
    print()
    print("  ── TIỆN ÍCH ─────────────────────────────────────────────")
    print("  [a]  Chạy TẤT CẢ demo liên tiếp")
    print("  [8]  Thoát")
    print()
    print(SEPARATOR)


# ─────────────────────────────────────────────
# HANDLER CHO TỪNG MỤC
# ─────────────────────────────────────────────

def handle_1():
    print()
    print("  Thuật toán Dijkstra dùng min-heap (heapq).")
    print("  Đồ thị vô hướng có trọng số: dist[v] = min(dist[v], dist[u] + cost).")
    print("  Độ phức tạp: O((V + E) log V).")
    print()
    demo_routing_shortest_path()


def handle_2():
    print()
    print("  Kruskal: sắp xếp cạnh theo trọng số tăng dần,")
    print("  dùng DSU (Union-Find) để kiểm tra cycle.")
    print("  Độ phức tạp: O(E log E + E α(V)) ≈ O(E log E).")
    print()
    demo_mst_network()


def handle_3():
    print()
    print("  Bảng băm tự cài: separate chaining, load factor < 0.75,")
    print("  tự động resize. Tra cứu trung bình O(1).")
    print()
    demo_hash_table()


def handle_4():
    print()
    print("  Hashing ứng dụng:")
    print("  • Group anagrams: key = sorted(s) → O(n·k log k)")
    print("  • Longest consecutive: HashSet → O(n)")
    print("  • Subarray sum = k: prefix sum + hash map → O(n)")
    print()
    print("=" * 60)
    print("  DEMO 4 — HASHING TỔNG HỢP")
    print("=" * 60)
    print()
    demo_group_anagrams()
    print()
    demo_longest_consecutive()
    print()
    demo_subarray_sum()


def handle_5():
    print()
    print("  Rabin-Karp Rolling Hash: tính hash cửa sổ trượt.")
    print("  Trượt O(1) mỗi bước → tổng O(n + m) trung bình.")
    print("  Xác minh thực sự khi hash khớp để tránh collision.")
    print()
    print("=" * 60)
    print("  DEMO 5 — ROLLING HASH (RABIN-KARP)")
    print("  Tìm pattern trong log chuỗi giao hàng")
    print("=" * 60)
    print()
    demo_rolling_hash()


def handle_6():
    print()
    print("  Dynamic Programming nền tảng:")
    print("  • Memoization (top-down): đệ quy + cache kết quả cũ.")
    print("  • Tabulation (bottom-up): xây bảng từ base case lên.")
    print()
    demo_fibonacci()
    demo_climbing_stairs()


def handle_7():
    print()
    print("  Knapsack 0/1 — bài toán chọn combo tối ưu:")
    print("  • 2D: dp[i][w] = max value dùng i items, budget w.")
    print("  • 1D: tối ưu bộ nhớ, duyệt ngược để tránh dùng lại item.")
    print("  • Độ phức tạp: O(n × W) time, O(W) space (phiên bản 1D).")
    print()
    demo_knapsack()


def handle_all():
    """Chạy tuần tự tất cả demo."""
    for handler in [handle_1, handle_2, handle_3,
                    handle_4, handle_5, handle_6, handle_7]:
        handler()
        print()
        pause()
        print()


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────

MENU_MAP = {
    '1': handle_1,
    '2': handle_2,
    '3': handle_3,
    '4': handle_4,
    '5': handle_5,
    '6': handle_6,
    '7': handle_7,
    'a': handle_all,
    'A': handle_all,
}


def main():
    clear()
    print_banner()

    while True:
        print_menu()
        choice = input("  Chọn [1-8 / a]: ").strip()

        if choice in ('8', 'q', 'Q', 'exit'):
            print()
            print("  ★ Cảm ơn đã sử dụng POLY-SHIP Algorithm Lab!")
            print("     Thuật toán: Dijkstra | Kruskal/DSU | Hashing | DP Knapsack")
            print()
            break

        if choice in MENU_MAP:
            print()
            MENU_MAP[choice]()
            pause()
            clear()
            print_banner()
        else:
            print(f"\n  ✘ Lựa chọn '{choice}' không hợp lệ. Thử lại.\n")


if __name__ == "__main__":
    main()
