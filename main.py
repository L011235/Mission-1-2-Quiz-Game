"""나만의 퀴즈 게임 - 단계별 완성 과정 [2/15] Quiz 클래스 · 기본 퀴즈 · 퀴즈 목록

이 파일은 main01.py → main15.py 로 이어지는 15단계 중 2번째 단계입니다.
단계마다 기능이 하나씩 늘어나며, main15.py 는 최종 완성본(main.py)과 같은 코드입니다.

[이번 단계에서 한 일]
  - Quiz 클래스: 문제/선택지 4개/정답 번호, 출력·정답 확인 메서드, 입력값 검사
  - 기본 퀴즈 7개(파이썬 & 개발 입문 주제)를 Quiz 객체로 작성

[눈여겨볼 개념]
  - 클래스, __init__, self, 속성(attribute), 메서드(method), list

[Git 커밋 메시지 예시]
  - Feat: Quiz 클래스 작성
  - Feat: 기본 퀴즈 데이터 추가

[진행 현황]
  ✅ 메뉴 기능 (4.2 / 4.3)
  ✅ Quiz 클래스 · 기본 퀴즈 (4.4 / 4.5)
  ⬜ 퀴즈 목록 (4.8)
  ⬜ 퀴즈 풀기 (4.6)
  ⬜ 점수 확인 (4.9)
  ⬜ 퀴즈 추가 (4.7)
  ⬜ QuizGame 클래스 (4.10)
  ⬜ state.json 저장/불러오기 (4.11)

실행 방법: python main02.py
참고: 아직 파일 저장이 없어서 프로그램을 끄면 퀴즈/점수가 사라집니다. (5단계에서 해결)
"""

import sys  # 파이썬 실행 환경 정보(표준 출력 등)를 다루는 모듈

TITLE = "나만의 퀴즈 게임"  # 메뉴 화면 맨 위에 보여 줄 제목 (문자열: str)
CHOICE_COUNT = 4  # 한 문제당 선택지 개수 (미션 조건: 4개가 기본) (정수: int)
WIDE_LINE = "=" * 40  # "=" 를 40번 반복한 문자열 (문자열 * 정수 = 반복)
THIN_LINE = "-" * 40  # 문제 사이를 나누는 얇은 구분선

MENU_PLAY = 1
MENU_ADD = 2
MENU_LIST = 3
MENU_SCORE = 4
MENU_EXIT = 5


class Quiz:
    """문제(question), 선택지(choices 4개), 정답 번호(answer 1~4)를 가진 퀴즈."""

    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제(question)는 비어 있지 않은 문자열이어야 합니다.")

        if not isinstance(choices, list) or len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지(choices)는 {CHOICE_COUNT}개의 목록이어야 합니다.")

        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValueError("선택지는 모두 비어 있지 않은 문자열이어야 합니다.")

        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답(answer)은 1~{CHOICE_COUNT} 사이의 정수여야 합니다.")

        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def correct_choice(self):
        """정답 선택지의 "내용"을 돌려준다."""
        return self.choices[self.answer - 1]


def create_default_quizzes():
    """기본 퀴즈 데이터를 만들어 돌려준다. 주제: '파이썬 & 개발 입문 기초'."""
    return [
        Quiz(
            "파이썬(Python)을 만든 사람은?",
            ["귀도 반 로섬", "리누스 토르발스", "비야네 스트롭스트룹", "제임스 고슬링"],
            1,
        ),
        Quiz(
            "파이썬에서 리스트(list)를 만들 때 사용하는 기호는?",
            ["()", "{}", "[]", "<>"],
            3,
        ),
        Quiz(
            "파이썬에서 7 // 2 의 결과는?",
            ["3.5", "4", "3", "2"],
            3,
        ),
        Quiz(
            "키(key)와 값(value)을 쌍으로 저장하는 자료형은?",
            ["list", "dict", "tuple", "set"],
            2,
        ),
        Quiz(
            "반복 횟수가 정해져 있지 않고, 조건이 참인 동안 계속 반복할 때 주로 쓰는 문은?",
            ["for", "if", "def", "while"],
            4,
        ),
        Quiz(
            "클래스로 객체를 만들 때 속성을 초기화하기 위해 자동으로 호출되는 메서드는?",
            ["__init__", "__start__", "__create__", "__main__"],
            1,
        ),
        Quiz(
            "Git에서 내 컴퓨터의 커밋을 GitHub 같은 원격 저장소로 올리는 명령어는?",
            ["git pull", "git clone", "git init", "git push"],
            4,
        ),
    ]


quizzes = create_default_quizzes()  # Quiz 객체들을 담은 리스트


def read_int(prompt, low, high):
    """low~high 사이의 정수를 입력받는다. 올바를 때까지 계속 다시 묻는다."""
    while True:
        raw = input(prompt).strip()

        if not raw:
            print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        try:
            value = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        if not low <= value <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        return value


def show_banner():
    """제목 배너(제목 + 위아래 구분선)를 출력한다."""
    print(WIDE_LINE)
    print(f" {TITLE}")
    print(WIDE_LINE)


def show_menu():
    """메뉴 화면을 출력한다."""
    print()
    show_banner()
    print(f"{MENU_PLAY}. 퀴즈 풀기")
    print(f"{MENU_ADD}. 퀴즈 추가")
    print(f"{MENU_LIST}. 퀴즈 목록")
    print(f"{MENU_SCORE}. 점수 확인")
    print(f"{MENU_EXIT}. 종료")
    print(WIDE_LINE)


def show_not_ready(feature_name):
    """아직 만들지 않은 기능을 골랐을 때 안내 메시지를 출력한다."""
    print(f"🚧 '{feature_name}' 기능은 아직 준비 중입니다. (다음 단계에서 만들어요)")


# ===========================================================================
# 기능 함수들
# ===========================================================================
def play_quiz():
    show_not_ready("퀴즈 풀기")


def show_score():
    show_not_ready("점수 확인")


def add_quiz():
    show_not_ready("퀴즈 추가")


def show_quiz_list():
    """퀴즈 목록 기능을 비구현(준비 중) 상태로 변경합니다."""
    show_not_ready("퀴즈 목록")


def main():
    """프로그램의 메인 흐름"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass

    show_banner()

    try:
        while True:
            show_menu()
            choice = read_int("선택: ", MENU_PLAY, MENU_EXIT)

            if choice == MENU_PLAY:
                play_quiz()
            elif choice == MENU_ADD:
                add_quiz()
            elif choice == MENU_LIST:
                show_quiz_list()
            elif choice == MENU_SCORE:
                show_score()
            elif choice == MENU_EXIT:
                print("프로그램을  종료합니다. 안녕히 가세요!")
                break

    except (KeyboardInterrupt, EOFError):
        print("\n\n입력이 중단되었습니다. 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()
