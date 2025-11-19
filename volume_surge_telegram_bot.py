import random
import sys

def generate_quizzes():
    """
    퀴즈에 사용할 숫자와 정답을 생성합니다.
    """
    # 1. 1~20까지의 제곱수 (Number: Square) - 정수형 문자열로 저장
    squares = {
        i: str(i**2)  # <-- **수정됨: 정수 문자열로 저장**
        for i in range(1, 21)
    }

    # 2. 1~20까지의 역수 (Number: Reciprocal rounded to 3 decimal places)
    reciprocals_1_20 = {
        i: f"{1/i:.3f}"
        for i in range(1, 21)
    }

    # 3. 30부터 100까지 5단위 증가 숫자의 역수 (Number: Reciprocal)
    reciprocals_30_100_by_5 = {
        i: f"{1/i:.3f}"
        for i in range(30, 101, 5)
    }

    return squares, reciprocals_1_20, reciprocals_30_100_by_5

def run_quiz(title, quiz_data, question_format, answer_format_func):
    """
    주어진 퀴즈 데이터를 사용하여 퀴즈를 실행합니다.
    """
    print(f"\n{'='*40}")
    print(f"**{title} 퀴즈 시작!** (언제든지 '종료'를 입력하면 끝납니다.)")
    print(f"{'='*40}")

    items = list(quiz_data.items())
    random.shuffle(items)
    total_questions = len(items)
    correct_count = 0

    for num, correct_answer in items:
        while True:
            # 질문 출력
            user_input = input(question_format.format(num=num)).strip()
            
            # 1. '종료' 명령어 처리
            if user_input.lower() == '종료':
                print("\n👋 프로그램을 종료합니다.")
                sys.exit()

            # 사용자 입력과 정답 비교
            try:
                if '역수' in title:
                    # 역수 퀴즈의 경우: 입력값을 float으로 변환 후, 소수점 셋째 자리 반올림 포맷으로 변환하여 비교
                    user_answer = f"{float(user_input):.3f}"
                else:
                    # 제곱수 퀴즈의 경우: 입력된 정수를 문자열로 변환하여 비교 (정답은 이미 '196' 형태의 문자열임)
                    user_answer = str(int(user_input))

            except ValueError:
                print("🚨 오류: 입력 형식이 올바르지 않거나 숫자 입력이 필요합니다. 다시 시도해 주세요.")
                continue

            if user_answer == correct_answer:
                correct_count += 1
                print(f"✅ 정답입니다! (현재 점수: {correct_count}/{total_questions})")
                break
            else:
                print(f"❌ 틀렸습니다. 다시 시도해 보세요.")
                print(f"💡 힌트: {answer_format_func(correct_answer)}")

    print(f"\n🎉 **{title} 퀴즈 종료!** 최종 점수: {correct_count}/{total_questions}")
    return correct_count == total_questions


def start_all_quizzes():
    """
    모든 퀴즈를 순서대로 시작합니다.
    """
    squares, reciprocals_1_20, reciprocals_30_100_by_5 = generate_quizzes()

    # 1. 제곱수 퀴즈
    run_quiz(
        title="1~20까지의 제곱수",
        quiz_data=squares,
        question_format="👉 {num}의 제곱수는 무엇인가요? (정수 입력): ",
        answer_format_func=lambda ans: f"정답은 {ans}입니다."
    )

    # 2. 1~20까지의 역수 퀴즈
    run_quiz(
        title="1~20까지의 역수 (소수점 셋째 자리까지)",
        quiz_data=reciprocals_1_20,
        question_format="👉 {num}의 역수를 소수점 셋째 자리까지 구하시오 (예: 0.125): ",
        answer_format_func=lambda ans: f"정답은 {ans}입니다."
    )

    # 3. 30부터 100까지 5단위 증가 숫자의 역수 퀴즈
    run_quiz(
        title="30~100 (5단위) 역수 (소수점 셋째 자리까지)",
        quiz_data=reciprocals_30_100_by_5,
        question_format="👉 {num}의 역수를 소수점 셋째 자리까지 구하시오 (예: 0.033): ",
        answer_format_func=lambda ans: f"정답은 {ans}입니다."
    )

if __name__ == "__main__":
    start_all_quizzes()