import random
import time

def calculate_conflicts(board, N):
    count_diff = [0] * (2 * N - 1)  # Đếm row - col
    count_sum = [0] * (2 * N - 1)   # Đếm row + col
    total_conflicts = 0
    conflict_rows = set()

    for row in range(N):
        col = board[row]
        diff_index = row - col + N - 1
        sum_index = row + col
        count_diff[diff_index] += 1
        count_sum[sum_index] += 1

    for i, count in enumerate(count_diff):
        if count > 1:
            total_conflicts += count * (count - 1) // 2
            rows = [r for r in range(N) if r - board[r] + N - 1 == i]
            conflict_rows.update(rows)
    for i, count in enumerate(count_sum):
        if count > 1:
            total_conflicts += count * (count - 1) // 2
            rows = [r for r in range(N) if r + board[r] == i]
            conflict_rows.update(rows)

    return total_conflicts, count_diff, count_sum, conflict_rows

def get_delta_conflicts(row, c, c_prime, board, count_diff, count_sum, N):
    old_d = row - c + N - 1
    old_s = row + c
    new_d = row - c_prime + N - 1
    new_s = row + c_prime
    return count_diff[new_d] + count_sum[new_s] - count_diff[old_d] - count_sum[old_s] + 2

def update_counts(row, c_old, c_new, count_diff, count_sum, N):
    old_d = row - c_old + N - 1
    old_s = row + c_old
    new_d = row - c_new + N - 1
    new_s = row + c_new
    count_diff[old_d] -= 1
    count_sum[old_s] -= 1
    count_diff[new_d] += 1
    count_sum[new_s] += 1

def hill_climbing(N, max_time=19):
    best_board = list(range(N))
    random.shuffle(best_board)
    best_conflicts, count_diff, count_sum, conflict_rows = calculate_conflicts(best_board, N)
    start_time = time.time()

    # Chạy nhiều lần với random restart
    restart_count = 0
    while time.time() - start_time < max_time and best_conflicts > 0:
        board = best_board.copy()
        total_conflicts, count_diff, count_sum, conflict_rows = calculate_conflicts(board, N)
        restarts_remaining = 3 - restart_count

        while time.time() - start_time < max_time and total_conflicts > 0 and restarts_remaining > 0:
            improved = False
            # Ưu tiên các hàng có xung đột
            rows_to_try = list(conflict_rows) if conflict_rows else list(range(N))
            random.shuffle(rows_to_try)

            for row in rows_to_try[:100]:  # Giới hạn số hàng thử để tiết kiệm thời gian
                c = board[row]
                other_cols = list(range(N))
                other_cols.remove(c)
                random.shuffle(other_cols)

                for c_prime in other_cols[:200]:  # Tăng số cột thử lên 200
                    delta = get_delta_conflicts(row, c, c_prime, board, count_diff, count_sum, N)
                    if delta < 0:
                        r_prime = board.index(c_prime)
                        board[row], board[r_prime] = board[r_prime], board[row]
                        update_counts(row, c, c_prime, count_diff, count_sum, N)
                        update_counts(r_prime, c_prime, c, count_diff, count_sum, N)
                        total_conflicts += delta
                        improved = True
                        # Cập nhật conflict_rows
                        conflict_rows.discard(row)
                        conflict_rows.discard(r_prime)
                        new_conflicts, _, _, new_conflict_rows = calculate_conflicts(board, N)
                        conflict_rows.update(new_conflict_rows)
                        break
                if improved:
                    break

            if not improved:
                break

        # Cập nhật giải pháp tốt nhất
        if total_conflicts < best_conflicts:
            best_board = board.copy()
            best_conflicts = total_conflicts

        # Random restart nếu còn thời gian và chưa đạt 0 xung đột
        if best_conflicts > 0 and time.time() - start_time < max_time:
            board = list(range(N))
            random.shuffle(board)
            total_conflicts, count_diff, count_sum, conflict_rows = calculate_conflicts(board, N)
            restart_count += 1

    return best_board, best_conflicts

def print_solution(board, conflicts):
    print(f"Số xung đột: {conflicts}")
    if conflicts == 0:
        print("Đã tìm thấy giải pháp không xung đột!")
    else:
        print("Không tìm thấy giải pháp không xung đột, đây là cấu hình với số xung đột thấp nhất.")
    print("Cấu hình bàn cờ (hàng -> cột):")
    for row, col in enumerate(board):  # In
        print(f"{row}:{col}")

def main():
    N = 1000
    start_time = time.time()
    board, conflicts = hill_climbing(N)
    end_time = time.time()

    print_solution(board, conflicts)
    print(f"Thời gian chạy: {end_time - start_time:.2f} giây")

if __name__ == "__main__":
    main()