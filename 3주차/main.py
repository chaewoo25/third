import json
import math
import os
import time

EPSILON = 1e-6
DATA_FILE = "data.json"


def normalize_label(label):
    """라벨 정규화: cross, v, Cross -> 'Cross' / x, X -> 'X'"""
    if not isinstance(label, str):
        return str(label)
    clean_label = label.strip().lower()
    if clean_label in ["cross", "v"]:
        return "Cross"
    elif clean_label in ["x"]:
        return "X"
    return label.strip().capitalize()


def mac_operation(pattern, filter_matrix):
    """2차원 패턴과 필터 간의 MAC (Multiply-Accumulate) 연산 직접 구현"""
    rows = len(pattern)
    cols = len(pattern[0])
    score = 0.0
    op_count = rows * cols  # N x N 연산 횟수

    for i in range(rows):
        for j in range(cols):
            score += float(pattern[i][j]) * float(filter_matrix[i][j])

    return score, op_count


def evaluate_decision(score_a, score_b):
    """부동소수점 허용오차(EPSILON) 기반 동점 및 판정 로직"""
    diff = abs(score_a - score_b)
    if diff < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "Cross"
    else:
        return "X"


def input_3x3_matrix(matrix_name):
    """3x3 입력 예외 처리 및 수신 함수"""
    print(f"\n--- {matrix_name} (3줄 입력, 공백 구분) ---")
    matrix = []
    for i in range(3):
        while True:
            try:
                line = input(f"행 {i+1}: ").strip().split()
                if len(line) != 3:
                    print("❌ 오류: 각 줄에 정확히 3개의 숫자를 공백으로 구분하여 입력해주세요.")
                    continue
                row = [float(val) for val in line]
                matrix.append(row)
                break
            except ValueError:
                print("❌ 오류: 유효한 숫자를 입력해 주세요.")
    return matrix


def mode_1_user_input():
    """모드 1: 사용자 직접 입력 (3x3)"""
    print("\n==========================================")
    print("   [모드 1] 사용자 직접 입력 (3x3 MAC 연산)")
    print("==========================================")

    filter_a = input_3x3_matrix("필터 A (Cross)")
    filter_b = input_3x3_matrix("필터 B (X)")
    pattern = input_3x3_matrix("패턴 (3x3)")

    # MAC 연산 및 성능 측정 (10회 평균)
    start_time = time.perf_counter()
    for _ in range(10):
        score_a, _ = mac_operation(pattern, filter_a)
        score_b, _ = mac_operation(pattern, filter_b)
    end_time = time.perf_counter()

    avg_time_ms = ((end_time - start_time) / 10) * 1000
    decision = evaluate_decision(score_a, score_b)

    print("\n# [MAC 연산 결과]")
    print(f"  A 점수 (Cross) : {score_a:.10f}")
    print(f"  B 점수 (X)     : {score_b:.10f}")
    print(f"  평균 연산 시간 : {avg_time_ms:.4f} ms (10회 평균)")
    print(f"  최종 판정      : {decision}")
    if decision == "UNDECIDED":
        print(f"  (사유: |A - B| < {EPSILON} 이므로 동점 처리)")


def mode_2_json_analysis():
    """모드 2: data.json 데이터 분석 및 프로파일링"""
    print("\n==========================================")
    print("   [모드 2] data.json 패턴 분석 및 프로파일링")
    print("==========================================")

    if not os.path.exists(DATA_FILE):
        print(f"❌ 오류: '{DATA_FILE}' 파일을 찾을 수 없습니다.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON 로드 실패: {e}")
        return

    filters = data.get("filters", {})
    patterns = data.get("patterns", [])

    total_tests = 0
    pass_count = 0
    fail_count = 0
    fail_cases = []

    print("\n# [1] 패턴 분석 (라벨 정규화 및 테스트)")

    for item in patterns:
        case_id = item.get("id", "Unknown")
        size = item.get("size")
        pat_matrix = item.get("input")
        raw_expected = item.get("expected")

        expected = normalize_label(raw_expected)
        filter_key = f"size_{size}"

        if filter_key not in filters:
            fail_count += 1
            fail_cases.append(f"{case_id}: 필터 크기({filter_key}) 미존재")
            continue

        f_a = filters[filter_key].get("Cross")
        f_b = filters[filter_key].get("X")

        # 크기 검증
        if len(pat_matrix) != size or len(f_a) != size or len(f_b) != size:
            total_tests += 1
            fail_count += 1
            fail_cases.append(f"{case_id}: 패턴/필터 크기 불일치 (스체마 오류)")
            continue

        score_a, _ = mac_operation(pat_matrix, f_a)
        score_b, _ = mac_operation(pat_matrix, f_b)
        decision = evaluate_decision(score_a, score_b)

        total_tests += 1
        is_pass = (decision == expected)

        if is_pass:
            pass_count += 1
            status = "PASS"
        else:
            fail_count += 1
            status = "FAIL"
            fail_cases.append(
                f"- {case_id}: 판정({decision}) != expected({expected}) [동점 또는 오판]"
            )

        print(
            f"  -- {case_id} -- | Cross: {score_a:.4f} | X: {score_b:.4f} | 판정: {decision} | expected: {expected} | {status}"
        )

    # 크기별 성능 측정 (3x3, 5x5, 13x13, 25x25)
    print("\n# [2] 크기별 성능 분석 (평균 10회 연산)")
    print("------------------------------------------")
    print(" 크기      평균 시간(ms)     연산 횟수(N^2)")
    print("------------------------------------------")

    sizes = [3, 5, 13, 25]
    for s in sizes:
        dummy_pat = [[1.0] * s for _ in range(s)]
        dummy_flt = [[0.5] * s for _ in range(s)]

        start_t = time.perf_counter()
        for _ in range(10):
            _, op_cnt = mac_operation(dummy_pat, dummy_flt)
        end_t = time.perf_counter()

        avg_ms = ((end_t - start_t) / 10) * 1000
        print(f" {s:2d}x{s:<2d}      {avg_ms:8.4f} ms      {op_cnt:6d}")

    print("------------------------------------------")
    print("\n# [3] 결과 요약")
    print(f"  총 테스트 : {total_tests}개")
    print(f"  성공(PASS) : {pass_count}개")
    print(f"  실패(FAIL) : {fail_count}개")

    if fail_cases:
        print("\n  [실패 케이스 상세 목록]")
        for fc in fail_cases:
            print(f"   {fc}")


def main():
    while True:
        print("\n==========================================")
        print("  🤖 Mini NPU Simulator (패턴 매칭 & MAC)")
        print("==========================================")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석 및 프로파일링")
        print("3. 종료")

        choice = input("선택 (1~3): ").strip()
        if choice == "1":
            mode_1_user_input()
        elif choice == "2":
            mode_2_json_analysis()
        elif choice == "3":
            print("\n시뮬레이터를 종료합니다.")
            break
        else:
            print("❌ 올바른 번호를 선택해 주세요 (1~3).")


if __name__ == "__main__":
    main()