"""
routing.py — POLY-SHIP Logistics System
Phần 1: Thuật toán định tuyến giữa các kho
  - Dijkstra: tìm đường ngắn nhất (Shortest Path)
  - Kruskal + DSU: cây khung nhỏ nhất (MST)
"""

import heapq


# ─────────────────────────────────────────────
# 1.1  DIJKSTRA — SHORTEST PATH
# ─────────────────────────────────────────────

def build_graph(edges):
    """
    Xây dựng đồ thị dạng adjacency list (vô hướng).
    Input : list of (u, v, cost)
    Output: dict { u: [(v, cost), ...], ... }
    """
    graph = {}
    for u, v, cost in edges:
        graph.setdefault(u, []).append((v, cost))
        graph.setdefault(v, []).append((u, cost))
    return graph


def dijkstra(graph, source):
    """
    Dijkstra dùng heapq (min-heap).
    Trả về:
      dist   — dict { node: chi_phí_ngắn_nhất }
      parent — dict { node: node_trước_đó }  (để truy vết route)
    """
    dist   = {node: float('inf') for node in graph}
    parent = {node: None         for node in graph}
    dist[source] = 0

    # heap item: (chi_phí_tích_lũy, node)
    heap = [(0, source)]

    visited = set()

    while heap:
        d, u = heapq.heappop(heap)

        if u in visited:
            continue
        visited.add(u)

        for v, cost in graph.get(u, []):
            new_dist = d + cost
            if new_dist < dist[v]:
                dist[v]   = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, parent


def shortest_route(graph, source, target):
    """
    Gọi Dijkstra rồi truy vết đường đi từ source → target.
    Trả về: (total_cost, route_list)
      route_list = [source, ..., target]  hoặc [] nếu không tồn tại
    """
    dist, parent = dijkstra(graph, source)

    if dist[target] == float('inf'):
        return float('inf'), []

    # Truy vết ngược từ target
    route = []
    cur = target
    while cur is not None:
        route.append(cur)
        cur = parent[cur]
    route.reverse()

    return dist[target], route


def demo_routing_shortest_path():
    """
    Demo: mạng kho POLY-SHIP (7 đỉnh).
    In đường ngắn nhất giữa một số cặp kho tiêu biểu.
    """
    print("=" * 60)
    print("  DEMO 1 — SHORTEST PATH (DIJKSTRA)")
    print("  Hệ thống: tìm tuyến giao hàng ngắn nhất giữa các kho")
    print("=" * 60)

    # Dữ liệu đồ thị — (u, v, cost)  [cost = đơn vị thời gian/tiền]
    edges = [
        ("WH1", "HCM",  5),
        ("WH1", "BD",   8),
        ("WH1", "LA",  15),
        ("WH2", "HP",   4),
        ("WH2", "LA",  20),
        ("WH2", "DN",  14),
        ("DN",  "HP",   6),
        ("DN",  "BD",  10),
        ("DN",  "HCM", 12),
        ("HCM", "BD",   3),
        ("HCM", "LA",   7),
        ("BD",  "LA",   9),
        ("HP",  "WH2",  4),
    ]

    graph = build_graph(edges)

    print("\n  Danh sách kho / điểm giao:")
    for node in sorted(graph):
        neighbors = ", ".join(f"{v}({c})" for v, c in graph[node])
        print(f"    {node:6s} → {neighbors}")

    # Các ca test
    test_cases = [
        ("WH1", "WH2"),
        ("WH1", "HP"),
        ("LA",  "DN"),
        ("BD",  "WH2"),
    ]

    print()
    for src, tgt in test_cases:
        cost, route = shortest_route(graph, src, tgt)
        arrow = " → ".join(route)
        print(f"  [{src} → {tgt}]")
        print(f"    Tuyến  : {arrow}")
        print(f"    Chi phí: {cost}")
        print()

    # Cho phép nhập tay
    print("  Nhập tay (Enter để bỏ qua):")
    src_in = input("    Nguồn: ").strip().upper() or "WH1"
    tgt_in = input("    Đích  : ").strip().upper() or "WH2"

    if src_in in graph and tgt_in in graph:
        cost, route = shortest_route(graph, src_in, tgt_in)
        if route:
            print(f"\n    Tuyến  : {' → '.join(route)}")
            print(f"    Chi phí: {cost}")
        else:
            print("    Không tìm thấy đường đi!")
    else:
        print("    Node không tồn tại trong mạng.")


# ─────────────────────────────────────────────
# 1.2  DSU (Union-Find) + KRUSKAL MST
# ─────────────────────────────────────────────

class DSU:
    """
    Disjoint Set Union (Union-Find)
    - Path compression (find)
    - Union by size
    """

    def __init__(self, vertices):
        self.parent = {}
        self.size   = {}
        for v in vertices:
            self.make_set(v)

    def make_set(self, v):
        self.parent[v] = v
        self.size[v]   = 1

    def find(self, v):
        """Tìm đại diện (root) của tập chứa v — có path compression."""
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])   # path compression
        return self.parent[v]

    def union(self, u, v):
        """
        Gộp 2 tập chứa u và v.
        Trả về True nếu gộp thành công, False nếu cùng tập (sẽ tạo cycle).
        """
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return False  # cùng tập → bỏ qua (tránh cycle)

        # Union by size: tập nhỏ treo vào tập lớn
        if self.size[root_u] < self.size[root_v]:
            root_u, root_v = root_v, root_u

        self.parent[root_v] = root_u
        self.size[root_u]  += self.size[root_v]
        return True


def kruskal_mst(vertices, edges):
    """
    Kruskal's Algorithm — Minimum Spanning Tree.
    Input : vertices (list), edges (list of (u, v, cost))
    Output: (mst_edges, total_cost)
      mst_edges = list of (u, v, cost) được chọn vào MST
    """
    # Bước 1: sắp xếp cạnh theo chi phí tăng dần
    sorted_edges = sorted(edges, key=lambda e: e[2])

    dsu        = DSU(vertices)
    mst_edges  = []
    total_cost = 0

    # Bước 2: duyệt từng cạnh
    for u, v, cost in sorted_edges:
        if dsu.union(u, v):          # không tạo cycle → đưa vào MST
            mst_edges.append((u, v, cost))
            total_cost += cost
            if len(mst_edges) == len(vertices) - 1:
                break                # đủ n-1 cạnh → xong

    return mst_edges, total_cost


def demo_mst_network():
    """
    Demo: thiết kế mạng kho tối thiểu (MST) — Kruskal + DSU.
    """
    print("=" * 60)
    print("  DEMO 2 — MST NETWORK (KRUSKAL + DSU)")
    print("  Hệ thống: lắp đặt đường truyền nội bộ chi phí thấp nhất")
    print("=" * 60)

    vertices = ["WH1", "WH2", "HCM", "DN", "HP", "BD", "LA"]

    edges = [
        ("WH1", "HCM",  5),
        ("WH1", "BD",   8),
        ("WH1", "LA",  15),
        ("WH2", "HP",   4),
        ("WH2", "LA",  20),
        ("WH2", "DN",  14),
        ("DN",  "HP",   6),
        ("DN",  "BD",  10),
        ("DN",  "HCM", 12),
        ("HCM", "BD",   3),
        ("HCM", "LA",   7),
        ("BD",  "LA",   9),
    ]

    print(f"\n  Tổng số kho : {len(vertices)}")
    print(f"  Tổng số cạnh: {len(edges)}")
    print(f"  Cạnh sắp xếp theo chi phí:")
    for u, v, c in sorted(edges, key=lambda e: e[2]):
        print(f"    ({u} ↔ {v}) = {c}")

    mst_edges, total_cost = kruskal_mst(vertices, edges)

    print(f"\n  ✔ Kết quả MST ({len(mst_edges)} tuyến chọn):")
    print(f"  {'Tuyến':20s}  Chi phí")
    print(f"  {'-'*30}")
    for u, v, c in mst_edges:
        print(f"  {u} ↔ {v}{'':15s}  {c}")
    print(f"  {'-'*30}")
    print(f"  Tổng chi phí lắp đặt: {total_cost}")

    print()
    print("  ★ Nhận xét: Đây là bộ khung tối thiểu (MST).")
    print("    Tất cả kho đã được kết nối với chi phí cáp/đường truyền")
    print("    thấp nhất có thể. Các tuyến giao hàng chi tiết (có thể")
    print("    đi qua nhiều nút trung gian) sử dụng Dijkstra trên mạng")
    print("    đầy đủ — không bị giới hạn bởi các cạnh MST.")
