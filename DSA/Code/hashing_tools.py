"""
hashing_tools.py — POLY-SHIP Logistics System
Phần 2: Quản lý đơn hàng & tìm kiếm pattern bằng Hashing
  - HashTable: demo cấu trúc bảng băm tự cài (separate chaining)
  - group_anagrams: nhóm đơn hàng có mã SKU hoán vị nhau
  - longest_consecutive: tìm chuỗi ngày liên tiếp dài nhất
  - subarray_sum_k: đếm dải đơn hàng có tổng giá trị = k
  - rolling_hash_search: tìm pattern trong chuỗi log giao hàng (Rabin-Karp)
"""


# ─────────────────────────────────────────────
# 2.0  HASH TABLE — CÀI ĐẶT THỦ CÔNG
# ─────────────────────────────────────────────

class HashTable:
    """
    Bảng băm tự cài — Separate Chaining (dùng list tại mỗi bucket).
    Hỗ trợ: set, get, delete, __len__, display.
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size     = 0
        self.buckets  = [[] for _ in range(capacity)]   # list of (key, value)

    def _hash(self, key):
        """Hash function: dùng Python hash + modulo."""
        return hash(key) % self.capacity

    def set(self, key, value):
        idx    = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)   # cập nhật
                return
        bucket.append((key, value))        # thêm mới
        self.size += 1

        # Resize nếu load factor > 0.75
        if self.size / self.capacity > 0.75:
            self._resize()

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None   # không tìm thấy

    def delete(self, key):
        idx    = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self):
        old_buckets   = self.buckets
        self.capacity *= 2
        self.buckets   = [[] for _ in range(self.capacity)]
        self.size      = 0
        for bucket in old_buckets:
            for k, v in bucket:
                self.set(k, v)

    def __len__(self):
        return self.size

    def display(self, max_buckets=8):
        """In trạng thái bảng băm (tối đa max_buckets bucket có dữ liệu)."""
        shown = 0
        for i, bucket in enumerate(self.buckets):
            if bucket:
                print(f"    bucket[{i:2d}] → {bucket}")
                shown += 1
                if shown >= max_buckets:
                    break
        remaining = sum(1 for b in self.buckets if b) - shown
        if remaining:
            print(f"    ... và {remaining} bucket khác có dữ liệu")


def demo_hash_table():
    """Demo HashTable: quản lý đơn hàng theo mã tracking."""
    print("=" * 60)
    print("  DEMO 3 — HASH TABLE ĐƠN HÀNG")
    print("  Lưu trữ & tra cứu đơn hàng bằng mã tracking")
    print("=" * 60)

    ht = HashTable(capacity=8)

    orders = [
        ("PS-001", {"customer": "Nguyen Van A", "value": 350_000, "status": "delivered"}),
        ("PS-002", {"customer": "Tran Thi B",   "value": 120_000, "status": "shipping"}),
        ("PS-003", {"customer": "Le Van C",      "value": 890_000, "status": "pending"}),
        ("PS-004", {"customer": "Pham Thi D",    "value": 450_000, "status": "delivered"}),
        ("PS-005", {"customer": "Hoang Van E",   "value": 200_000, "status": "cancelled"}),
        ("PS-006", {"customer": "Vu Thi F",      "value": 670_000, "status": "shipping"}),
        ("PS-007", {"customer": "Dang Van G",    "value": 310_000, "status": "delivered"}),
    ]

    print(f"\n  Nạp {len(orders)} đơn hàng vào bảng băm...")
    for code, data in orders:
        ht.set(code, data)

    print(f"  Capacity: {ht.capacity}  |  Load factor: {len(ht)/ht.capacity:.2f}")
    print("\n  Cấu trúc bucket:")
    ht.display()

    print("\n  Tra cứu nhanh O(1):")
    for code in ["PS-003", "PS-007", "PS-999"]:
        result = ht.get(code)
        if result:
            print(f"    {code} → {result['customer']}, {result['value']:,}đ, [{result['status']}]")
        else:
            print(f"    {code} → KHÔNG TÌM THẤY")

    print("\n  Xoá đơn PS-005 (cancelled)...")
    ht.delete("PS-005")
    print(f"  Tổng đơn còn lại: {len(ht)}")


# ─────────────────────────────────────────────
# 2.1  GROUP ANAGRAMS
# ─────────────────────────────────────────────

def group_anagrams(strings):
    """
    Nhóm các chuỗi là hoán vị (anagram) của nhau.
    Kỹ thuật: key = tuple(sorted(s)) → O(n · k log k)
    Ứng dụng: nhóm mã SKU / barcode tương tự.
    """
    table = {}
    for s in strings:
        key = tuple(sorted(s))
        table.setdefault(key, []).append(s)
    return list(table.values())


def demo_group_anagrams():
    """Demo nhóm SKU / mã đơn hàng hoán vị."""
    print("  Nhóm SKU hoán vị (group anagrams):")
    skus = ["ABCD", "DCBA", "BCDA", "EFGH", "HGFE", "IJKL", "ABDC", "FGEH", "XYZ"]
    groups = group_anagrams(skus)
    for i, g in enumerate(groups, 1):
        print(f"    Nhóm {i}: {g}")


# ─────────────────────────────────────────────
# 2.2  LONGEST CONSECUTIVE SEQUENCE
# ─────────────────────────────────────────────

def longest_consecutive(nums):
    """
    Tìm chuỗi số nguyên liên tiếp dài nhất trong mảng.
    Dùng HashSet → O(n).
    Ứng dụng: tìm chuỗi ngày có đơn hàng liên tục (phát hiện surge).
    """
    num_set = set(nums)
    best    = 0

    for n in num_set:
        if (n - 1) not in num_set:     # n là điểm bắt đầu chuỗi
            cur = n
            length = 1
            while (cur + 1) in num_set:
                cur    += 1
                length += 1
            best = max(best, length)

    return best


def demo_longest_consecutive():
    """Demo tìm chuỗi ngày liên tiếp dài nhất có đơn hàng."""
    print("  Chuỗi ngày liên tiếp dài nhất (longest consecutive):")
    # Ngày trong tháng có đơn hàng (mã hóa bằng số)
    order_days = [15, 3, 1, 7, 2, 14, 16, 4, 17, 13, 18, 5]
    result = longest_consecutive(order_days)
    sorted_days = sorted(order_days)
    print(f"    Ngày có đơn: {sorted_days}")
    print(f"    Chuỗi dài nhất: {result} ngày liên tiếp")


# ─────────────────────────────────────────────
# 2.3  SUBARRAY SUM = K
# ─────────────────────────────────────────────

def subarray_sum_k(nums, k):
    """
    Đếm số dải con (subarray) có tổng = k.
    Kỹ thuật: prefix sum + hash map → O(n).
    Ứng dụng: tìm khoảng thời gian có tổng doanh thu = target.
    """
    prefix_count = {0: 1}   # prefix_sum → số lần xuất hiện
    prefix_sum   = 0
    count        = 0

    for val in nums:
        prefix_sum += val
        need        = prefix_sum - k
        count      += prefix_count.get(need, 0)
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1

    return count


def demo_subarray_sum():
    """Demo đếm dải đơn hàng có tổng giá trị = target."""
    print("  Đếm dải đơn hàng có tổng = target (subarray sum = k):")
    # Giá trị đơn hàng theo giờ (đơn vị: 100k đồng)
    hourly_values = [3, 1, 2, 4, 2, 3, 1, 2, 1, 4]
    target = 6
    result = subarray_sum_k(hourly_values, target)
    print(f"    Doanh thu theo giờ: {hourly_values}")
    print(f"    Số dải có tổng = {target}: {result} dải")

    # Thêm vài ví dụ
    for t in [3, 4, 7]:
        r = subarray_sum_k(hourly_values, t)
        print(f"    Số dải có tổng = {t}: {r} dải")


# ─────────────────────────────────────────────
# 2.4  ROLLING HASH — RABIN-KARP
# ─────────────────────────────────────────────

BASE = 31
MOD  = 10**9 + 7


def rolling_hash_search(text, pattern):
    """
    Tìm tất cả vị trí xuất hiện của pattern trong text.
    Thuật toán Rabin-Karp với rolling hash → O(n + m) trung bình.
    Ứng dụng: tìm pattern lỗi / mã đơn hàng trong log giao hàng.

    Trả về: list vị trí bắt đầu (0-indexed).
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []

    # Tính hash của pattern và cửa sổ đầu tiên
    def char_val(c):
        return ord(c) - ord('a') + 1 if c.islower() else ord(c) - ord('A') + 27

    pat_hash = 0
    win_hash = 0
    power    = 1   # BASE^(m-1) % MOD

    for i in range(m):
        pat_hash = (pat_hash * BASE + char_val(pattern[i])) % MOD
        win_hash = (win_hash * BASE + char_val(text[i]))    % MOD
        if i < m - 1:
            power = (power * BASE) % MOD

    results = []
    for i in range(n - m + 1):
        if win_hash == pat_hash:
            # Xác minh thực sự (tránh hash collision)
            if text[i:i + m] == pattern:
                results.append(i)

        if i < n - m:
            # Trượt cửa sổ: xóa ký tự cũ, thêm ký tự mới
            win_hash = (win_hash - char_val(text[i]) * power) % MOD
            win_hash = (win_hash * BASE + char_val(text[i + m])) % MOD
            win_hash = (win_hash + MOD) % MOD   # đảm bảo không âm

    return results


def demo_rolling_hash():
    """Demo tìm pattern lỗi trong chuỗi log giao hàng."""
    print("  Rolling Hash — tìm pattern trong log (Rabin-Karp):")

    # Mô phỏng chuỗi mã trạng thái đơn hàng trong log
    log = "DELOKDELSHIPDELOKFAILDELOKSHIPDELSHIPDEL"
    patterns = ["DEL", "FAIL", "SHIP", "XYZ"]

    print(f"    Log chuỗi : {log}")
    for pat in patterns:
        positions = rolling_hash_search(log, pat)
        if positions:
            print(f"    Pattern '{pat}': tìm thấy tại vị trí {positions} ({len(positions)} lần)")
        else:
            print(f"    Pattern '{pat}': KHÔNG TÌM THẤY")


# ─────────────────────────────────────────────
# ENTRY POINT — chạy tất cả demo hashing
# ─────────────────────────────────────────────

def demo_all_hashing():
    """Chạy toàn bộ demo hashing liên quan đến đơn hàng."""
    demo_hash_table()
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
    print()
    print("=" * 60)
    print("  DEMO 5 — ROLLING HASH (RABIN-KARP)")
    print("  Tìm pattern trong log chuỗi giao hàng")
    print("=" * 60)
    print()
    demo_rolling_hash()
