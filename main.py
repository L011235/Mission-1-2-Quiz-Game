"""나만의 퀴즈 게임 - 단계별 완성 과정 p
[이번 단계에서 한 일]
  - '복사 → 섞기 → 자르기' 세 줄을 random.sample(목록, 개수) 한 줄로 정리
  - 퀴즈가 1개뿐이면 문제 수를 묻지 않음


[눈여겨볼 개념]
  - random.sample 은 원본을 바꾸지 않고 중복 없이 뽑아 새 리스트를 돌려줌

[Git 커밋 메시지 예시]
  - Refactor: 랜덤 출제와 문제 수 선택을 random.sample 로 정리

[진행 현황]
  ✅ 메뉴 기능 (4.2 / 4.3)
  ✅ Quiz 클래스 · 기본 퀴즈 (4.4 / 4.5)
  ✅ 퀴즈 목록 (4.8)
  ✅ 퀴즈 풀기 (4.6)
  ✅ 점수 확인 (4.9)
  ✅ 퀴즈 추가 (4.7)
  ✅ QuizGame 클래스 (4.10)
  ✅ state.json 저장/불러오기 (4.11)
  ✅ [보너스] 5.1 랜덤 출제
  ✅ [보너스] 5.2 문제 수 선택
 
"""

# ---------------------------------------------------------------------------
# import: 다른 사람이 만들어 둔 도구(모듈)를 가져와서 쓰는 문장이다.
# 아래는 모두 파이썬에 기본으로 들어 있는 "표준 라이브러리"이다.
# (따로 설치할 필요가 없다 -> 미션의 "외부 라이브러리 금지" 조건을 지킨다.)
# ---------------------------------------------------------------------------
import json  # 파이썬 데이터(딕셔너리/리스트)와 JSON 문자열을 서로 변환해 주는 모듈
import os  # 운영체제 기능(파일 이름 바꾸기/교체 등)을 쓰기 위한 모듈
import random  # [보너스 5.1/5.2] 무작위로 뽑거나 섞을 때 쓰는 모듈
import sys  # 파이썬 실행 환경 정보(표준 출력 등)를 다루는 모듈
from pathlib import Path  # 파일/폴더 경로를 "객체"로 편하게 다루게 해 주는 클래스

# ---------------------------------------------------------------------------
# 상수(constant): 프로그램 곳곳에서 쓰는, 바뀌지 않는 값들.
# 파이썬에는 "진짜 상수" 문법이 없어서, 관례적으로 대문자 + 밑줄로 이름을 짓는다.
# 숫자나 문자열을 코드 여기저기에 직접 쓰는 대신(= 매직 넘버) 이름을 붙여 두면
#   1) 코드를 읽기 쉽고  2) 나중에 바꿀 때 한 곳만 고치면 된다.
# ---------------------------------------------------------------------------

# 데이터 파일 경로: 프로젝트 루트(= 이 main.py 가 들어 있는 폴더)의 state.json
#   __file__            : 지금 실행 중인 이 파이썬 파일(main.py)의 경로
#   Path(...).resolve() : 상대경로를 절대경로로 바꿔 준다.
#   .parent             : 그 파일이 들어 있는 "폴더"를 뜻한다.
#   / "state.json"      : Path 객체에서는 / 연산자로 경로를 이어 붙일 수 있다.
# 이렇게 하면 터미널을 어느 폴더에서 열어 실행해도 항상 main.py 옆에 저장된다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"

TITLE = "나만의 퀴즈 게임"  # 메뉴 화면 맨 위에 보여 줄 제목
CHOICE_COUNT = 4  # 한 문제당 선택지 개수 (미션 조건: 4개가 기본)
WIDE_LINE = "=" * 40  # "=" 를 40번 반복한 문자열 (문자열 * 정수 = 반복)
THIN_LINE = "-" * 40  # 문제 사이를 나누는 얇은 구분선

# 메뉴 번호에 이름을 붙여 둔다. 코드에 1, 2, 3 이 그냥 나오는 것보다
# MENU_PLAY 라고 쓰면 "퀴즈 풀기 메뉴구나" 하고 바로 이해할 수 있다.
MENU_PLAY = 1
MENU_ADD = 2
MENU_LIST = 3
MENU_SCORE = 4
MENU_EXIT = 5


# ===========================================================================
# Quiz 클래스: 퀴즈 "한 문제"를 표현한다.
#
# [클래스(class)란?]
#   관련 있는 데이터(속성)와 기능(메서드)을 하나로 묶은 "설계도"이다.
#   예) 붕어빵 틀(클래스) 하나로 붕어빵(객체)을 여러 개 찍어 낼 수 있다.
#   여기서는 Quiz 라는 틀로 "문제 1", "문제 2" ... 같은 퀴즈 객체를 여러 개 만든다.
#
# [왜 클래스를 쓸까?]
#   퀴즈 하나는 문제/선택지/정답 이라는 3가지 정보가 항상 함께 다닌다.
#   변수 3개를 따로 들고 다니는 대신 하나의 객체로 묶으면 관리가 쉽다.
# ===========================================================================
class Quiz:
    """문제(question), 선택지(choices 4개), 정답 번호(answer 1~4)를 가진 퀴즈."""

    # -----------------------------------------------------------------------
    # __init__ : "생성자". Quiz(...) 로 객체를 만드는 순간 자동으로 호출된다.
    #
    # [self란?]
    #   "지금 만들어지고 있는(또는 지금 사용 중인) 바로 그 객체 자신"을 가리킨다.
    #   self.question = ... 은 "이 객체의 question 속성에 값을 저장한다"는 뜻이다.
    #   메서드의 첫 번째 매개변수는 항상 self 로 쓰는 것이 규칙이다.
    #   (호출할 때는 self 를 직접 쓰지 않는다. 파이썬이 알아서 넣어 준다.)
    #
    # [속성(attribute)이란?]
    #   객체가 가지고 있는 변수. self.이름 형태로 만든다.
    # -----------------------------------------------------------------------
    def __init__(self, question, choices, answer):
        # --- 입력값 검사(validation) -------------------------------------
        # 잘못된 값으로는 객체 자체를 만들 수 없게 막는다.
        # 이렇게 해 두면 손상된 state.json 을 읽다가 이상한 퀴즈가 섞여 들어와도
        # 여기서 바로 걸러진다. (raise ValueError = "값이 이상해요!" 하고 오류를 일으킴)

        # isinstance(값, 타입): 값이 그 타입인지 True/False 로 알려 준다.
        # question.strip(): 앞뒤 공백을 제거한다. 공백만 있으면 빈 문자열("")이 되고,
        # 빈 문자열은 조건문에서 False 로 취급된다. -> "not" 이 붙어 있으니 True 가 되어 오류.
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제(question)는 비어 있지 않은 문자열이어야 합니다.")

        # choices 는 list(목록)여야 하고, 길이(len)가 정확히 4개여야 한다.
        if not isinstance(choices, list) or len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지(choices)는 {CHOICE_COUNT}개의 목록이어야 합니다.")

        # all(...): 안의 조건이 "전부" True 일 때만 True.
        # "for c in choices" 로 선택지를 하나씩 꺼내 검사한다. (제너레이터 표현식)
        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValueError("선택지는 모두 비어 있지 않은 문자열이어야 합니다.")

        # 정답 번호 검사.
        #  - 파이썬에서 bool(True/False)은 int 의 일종이라 True == 1 이다.
        #    그래서 isinstance(True, int) 가 True 가 되어 버리므로, bool 은 따로 걸러낸다.
        #  - 1 <= answer <= 4 처럼 부등호를 연달아 써서 "범위 안인지" 한 번에 검사할 수 있다.
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답(answer)은 1~{CHOICE_COUNT} 사이의 정수여야 합니다.")

        # --- 검사를 모두 통과하면 속성으로 저장한다 -------------------------
        self.question = question.strip()  # 문제 문장 (앞뒤 공백 제거)
        # 리스트 컴프리헨션: choices 의 각 요소에서 공백을 제거한 새 리스트를 만든다.
        self.choices = [c.strip() for c in choices]
        self.answer = answer  # 정답은 1~4 "번호"로 관리한다. (0부터 시작하는 인덱스가 아님에 주의!)

    # -----------------------------------------------------------------------
    # 메서드(method): 클래스 안에 정의된 함수. 객체가 할 수 있는 "행동"이다.
    # -----------------------------------------------------------------------
    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다.

        number 에 번호를 주면 "[문제 1]" 같은 머리글을 함께 출력한다.
        number=None 은 "기본값" 이다. 값을 안 넘기면 None(= 값 없음)이 들어온다.
        """
        if number is not None:  # None 비교는 == 대신 is / is not 을 쓰는 것이 관례
            print(f"[문제 {number}]")  # f-string: 문자열 안의 {} 자리에 변수 값을 넣어 준다.
        print(self.question)
        # enumerate(목록, start=1): (번호, 요소) 쌍을 돌려 준다. start=1 이면 번호가 1부터 시작.
        # 사람에게 보여 줄 번호는 1부터가 자연스럽기 때문이다.
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답인지 확인한다. (맞으면 True, 틀리면 False)"""
        # == 는 비교 연산자이고, 결과는 True/False 이다. 그 결과를 그대로 반환(return)한다.
        return user_answer == self.answer

    def correct_choice(self):
        """정답 선택지의 "내용"을 돌려준다. (오답일 때 정답을 알려 주기 위해 사용)"""
        # 리스트의 위치(인덱스)는 0부터 시작하지만 정답 번호는 1부터이므로 1을 빼 준다.
        # 예) 정답이 3번 -> self.choices[2]
        return self.choices[self.answer - 1]

    def to_dict(self):
        """이 퀴즈를 JSON 으로 저장할 수 있는 딕셔너리로 바꾼다.

        JSON 은 "객체(Quiz)" 자체는 저장하지 못하고, 숫자/문자열/리스트/딕셔너리 같은
        기본 자료형만 저장할 수 있다. 그래서 저장하기 전에 변환 과정이 필요하다.
        """
        return {
            "question": self.question,
            "choices": list(self.choices),  # list() 로 복사본을 만들어 원본이 바뀌지 않게 한다.
            "answer": self.answer,
        }

    # @classmethod: "객체"가 아니라 "클래스 자체"에서 호출하는 메서드.
    # Quiz.from_dict(...) 처럼 쓴다. 첫 매개변수는 self 대신 cls(= Quiz 클래스)를 받는다.
    # 여기서는 "딕셔너리 -> Quiz 객체" 로 되돌리는 "또 다른 생성 방법"으로 쓰인다.
    @classmethod
    def from_dict(cls, data):
        """딕셔너리(JSON 에서 읽은 데이터)로부터 Quiz 객체를 만든다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 딕셔너리 형태여야 합니다.")
        # data["question"] 처럼 대괄호로 꺼낼 때 키가 없으면 KeyError 가 난다.
        # 이 오류는 파일을 불러오는 쪽(load_state)의 try/except 에서 잡아 처리한다.
        # cls(...) 는 Quiz(...) 와 같다. -> __init__ 의 입력값 검사도 함께 실행된다.
        return cls(data["question"], data["choices"], data["answer"])


def create_default_quizzes():
    """기본 퀴즈 데이터를 만들어 돌려준다. 주제: '파이썬 & 개발 입문 기초'.

    state.json 이 없을 때(첫 실행) 또는 손상됐을 때 이 퀴즈들로 시작한다.
    함수가 Quiz "객체"들의 리스트를 반환한다.
    (미션 조건: 퀴즈 5개 이상, 각 퀴즈는 문제 + 선택지 4개 + 정답 번호)
    """
    return [
        # Quiz(문제, [선택지 4개], 정답번호) 형태로 Quiz 클래스의 "인스턴스"를 만든다.
        # 정답 번호가 한 곳에 몰리지 않도록 1~4번에 골고루 배치했다.
        Quiz(
            "파이썬(Python)을 만든 사람은?",
            ["귀도 반 로섬", "리누스 토르발스", "비야네 스트롭스트룹", "제임스 고슬링"],
            1,  # 정답: 1번
        ),
        Quiz(
            "파이썬에서 리스트(list)를 만들 때 사용하는 기호는?",
            ["()", "{}", "[]", "<>"],
            3,  # 정답: 3번 []
        ),
        Quiz(
            "파이썬에서 7 // 2 의 결과는?",  # // 는 나눗셈의 "몫"만 구하는 연산자
            ["3.5", "4", "3", "2"],
            3,  # 정답: 3번 (7 ÷ 2 = 3 ... 1)
        ),
        Quiz(
            "키(key)와 값(value)을 쌍으로 저장하는 자료형은?",
            ["list", "dict", "tuple", "set"],
            2,  # 정답: 2번 dict
        ),
        Quiz(
            "반복 횟수가 정해져 있지 않고, 조건이 참인 동안 계속 반복할 때 주로 쓰는 문은?",
            ["for", "if", "def", "while"],
            4,  # 정답: 4번 while
        ),
        Quiz(
            "클래스로 객체를 만들 때 속성을 초기화하기 위해 자동으로 호출되는 메서드는?",
            ["__init__", "__start__", "__create__", "__main__"],
            1,  # 정답: 1번 __init__
        ),
        Quiz(
            "Git에서 내 컴퓨터의 커밋을 GitHub 같은 원격 저장소로 올리는 명령어는?",
            ["git pull", "git clone", "git init", "git push"],
            4,  # 정답: 4번 git push
        ),
    ]


# ===========================================================================
# QuizGame 클래스: 게임 "전체"를 관리한다.
#
# 역할 분담:
#   Quiz      -> 퀴즈 "한 문제"의 데이터와 동작
#   QuizGame  -> 퀴즈 "여러 개"를 모아서 메뉴/출제/저장 등 프로그램 흐름을 책임짐
# 이렇게 역할을 나누면 코드가 길어져도 "어디를 고치면 되는지" 찾기 쉽다.
# ===========================================================================
class QuizGame:
    """퀴즈 목록, 최고 점수, 메뉴 흐름, 파일 저장/불러오기를 담당한다."""

    def __init__(self, state_path=STATE_FILE):
        # state_path 의 기본값은 위에서 만든 STATE_FILE 이다.
        # (테스트할 때는 다른 경로를 넘겨서 진짜 데이터 파일을 건드리지 않을 수도 있다.)
        # Path(...) 로 감싸면 문자열이 들어와도 Path 객체로 통일할 수 있다.
        self.state_path = Path(state_path)

        # ----- 게임이 기억해야 하는 데이터(속성) -----
        self.quizzes = []  # Quiz 객체들을 담는 리스트 (처음엔 비어 있음)
        self.best_score = None  # 최고 점수(100점 만점). 아직 안 풀었다면 None(= 값 없음)
        self.best_correct = None  # 최고 점수를 냈을 때 맞힌 문제 수
        self.best_total = None  # 최고 점수를 냈을 때 전체 문제 수

    # =======================================================================
    # 1. 입력 처리
    # 사용자가 무엇을 입력할지는 알 수 없다. (abc, 빈 칸, 9999 ...)
    # 그래서 "올바른 값이 들어올 때까지 다시 묻는" 함수를 따로 만들어 두고
    # 프로그램 어디서든 가져다 쓴다. -> 코드 중복을 막고, 검사 규칙을 한 곳에 모은다.
    # =======================================================================

    # @staticmethod: self(객체)가 필요 없는 메서드를 클래스 안에 넣을 때 붙인다.
    # 이 메서드는 self.quizzes 같은 객체 데이터를 전혀 쓰지 않기 때문이다.
    @staticmethod
    def read_int(prompt, low, high):
        """low~high 사이의 정수를 입력받는다. 올바를 때까지 계속 다시 묻는다.

        매개변수:
            prompt : 입력을 받을 때 보여 줄 안내 문구 (예: "선택: ")
            low    : 허용하는 최솟값
            high   : 허용하는 최댓값
        반환값:
            사용자가 입력한 올바른 정수
        """
        # while True: "조건이 항상 참" -> 무한 반복. return 을 만나야 빠져나온다.
        # [for 와 while 의 차이]
        #   for   : 반복 횟수가 "정해져 있을 때" (예: 퀴즈 7개를 하나씩)
        #   while : 언제 끝날지 "모를 때"      (예: 올바른 입력이 들어올 때까지)
        while True:
            # input(): 사용자가 키보드로 입력한 내용을 "문자열"로 돌려준다. (Enter 를 누르면 종료)
            # .strip(): 앞뒤 공백 제거 -> " 1 " 같은 입력도 "1" 로 처리된다.
            raw = input(prompt).strip()

            # (1) 빈 입력(그냥 Enter): 빈 문자열은 False 취급이므로 "not raw" 가 True 가 된다.
            if not raw:
                print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue  # continue: 이번 반복의 나머지를 건너뛰고 while 맨 위로 돌아가 다시 묻는다.

            # (2) 숫자 변환 실패: "abc" 같은 문자열은 int() 가 ValueError 를 일으킨다.
            # [try / except 란?]
            #   try 블록 안에서 오류가 나면, 프로그램이 죽는 대신 except 블록이 실행된다.
            #   "오류가 날 수도 있는 코드"를 안전하게 감싸는 문법이다.
            try:
                value = int(raw)  # 문자열 -> 정수 변환
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue

            # (3) 허용 범위 밖의 숫자 (예: 메뉴 9번, 정답 0번)
            if not low <= value <= high:
                print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
                continue

            # 세 가지 검사를 모두 통과했으면 값을 돌려주고 함수를 끝낸다.
            return value

    @staticmethod
    def read_text(prompt):
        """비어 있지 않은 문자열을 입력받는다. (문제/선택지 입력용)"""
        while True:
            text = input(prompt).strip()
            if text:  # 내용이 있으면(= 빈 문자열이 아니면) 돌려준다.
                return text
            print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")

    # =======================================================================
    # 2. 화면 출력
    # =======================================================================
    def show_banner(self):
        """제목 배너(제목 + 위아래 구분선)를 출력한다."""
        print(WIDE_LINE)
        print(f" {TITLE}")
        print(WIDE_LINE)

    def show_menu(self):
        """메뉴 화면을 출력한다."""
        print()  # 아무것도 안 쓰고 print() 하면 빈 줄이 한 줄 출력된다. (화면 가독성용)
        self.show_banner()  # 같은 클래스의 다른 메서드는 self.메서드() 로 호출한다.
        print(f"{MENU_PLAY}. 퀴즈 풀기")
        print(f"{MENU_ADD}. 퀴즈 추가")
        print(f"{MENU_LIST}. 퀴즈 목록")
        print(f"{MENU_SCORE}. 점수 확인")
        print(f"{MENU_EXIT}. 종료")
        print(WIDE_LINE)

    # =======================================================================
    # 3. 기능: 퀴즈 풀기  [보너스 5.1 랜덤 출제 / 5.2 문제 수 선택]
    # =======================================================================
    def play_quiz(self):
        """퀴즈를 랜덤 순서로 출제하고, 정답 여부와 최종 결과를 보여 준다."""

        # 퀴즈가 하나도 없는 경우: 빈 리스트는 False 취급이므로 "not self.quizzes" 가 True.
        # 안내 메시지를 출력하고 return 으로 이 함수를 바로 끝낸다. (조기 반환)
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 '퀴즈 추가'로 퀴즈를 등록해 주세요.")
            return

        # --- [보너스 5.2] 풀 문제 수 선택 ---------------------------------
        available = len(self.quizzes)  # 지금 등록되어 있는 퀴즈 수
        if available == 1:
            count = 1  # 퀴즈가 1개뿐이면 고를 필요가 없으니 묻지 않는다.
        else:
            count = self.read_int(f"풀 문제 수를 선택하세요 (1-{available}): ", 1, available)

        # --- [보너스 5.1] 랜덤 출제 ---------------------------------------
        # random.sample(목록, k): 목록에서 중복 없이 k개를 "무작위 순서"로 뽑아 새 리스트로 준다.
        #   -> 문제 순서가 섞이고(5.1), 동시에 count 개만 뽑힌다(5.2). 한 번에 두 가지가 해결된다.
        # 원본 self.quizzes 는 바뀌지 않는다. (그래서 파일에 저장되는 순서와 목록 번호는 그대로다.)
        # 참고: random.shuffle(목록) 은 "원본 자체"를 섞어 버리므로 여기서는 쓰지 않았다.
        selected = random.sample(self.quizzes, count)

        correct = 0  # 맞힌 문제 수를 세는 변수 (처음엔 0)

        print(f"퀴즈를 시작합니다! (총 {count}문제)")

        # for 문: 뽑힌 퀴즈를 하나씩 꺼내 "끝까지" 반복한다. (횟수가 정해져 있으므로 for)
        for number, quiz in enumerate(selected, start=1):
            print(THIN_LINE)
            quiz.display(number)  # Quiz 객체의 display 메서드로 문제를 출력

            # 선택지는 4개이므로 1~4 사이의 번호만 받는다.
            user_answer = self.read_int("정답 입력: ", 1, CHOICE_COUNT)

            # if / else 로 정답 여부에 따라 다른 동작을 한다.
            if quiz.is_correct(user_answer):
                correct += 1  # correct = correct + 1 과 같다. (맞힌 개수 1 증가)
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번 ({quiz.correct_choice()}) 입니다.")

        # --- 결과 계산 ---
        score = round(correct * 100 / count)  # 100점 만점 (round: 반올림)

        print(WIDE_LINE)
        print(f"결과: {count}문제 중 {correct}문제 정답! ({score}점)")

        # 최고 점수와 비교해서 갱신한다. 갱신했다면 True 가 돌아온다.
        if self.update_best_score(score, correct, count):
            print("🎉 새로운 최고 점수입니다!")
        print(WIDE_LINE)

        # 최고 점수가 바뀌었을 수 있으므로 파일에 저장해 둔다.
        self.save_state()

    def update_best_score(self, score, correct, total):
        """이번 점수를 최고 점수와 비교해 더 높으면 갱신한다. 갱신했으면 True 를 돌려준다."""
        # best_score 가 None 이면 "아직 한 번도 안 푼 상태"이므로 이번 점수가 곧 최고 점수.
        # (None 과 > 비교를 하면 오류가 나므로, None 검사를 반드시 먼저 한다.
        #  or 는 앞 조건이 True 면 뒤 조건을 검사하지 않는다. -> 단락 평가)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            return True
        # 같거나 낮은 점수는 "새로운 최고 점수"가 아니므로 기록을 바꾸지 않는다.
        return False

    # =======================================================================
    # 4. 기능: 퀴즈 추가
    # =======================================================================
    def add_quiz(self):
        """사용자에게 문제/선택지 4개/정답 번호를 입력받아 새 퀴즈를 등록한다."""
        print("새로운 퀴즈를 추가합니다.")

        question = self.read_text("문제를 입력하세요: ")

        # 리스트 컴프리헨션으로 선택지 4개를 입력받는다.
        # range(1, 5) 는 1, 2, 3, 4 를 만든다. (끝 숫자 5는 포함되지 않는다.)
        # 아래 한 줄은 "for 문으로 4번 입력받아 리스트에 하나씩 append" 하는 것과 같다.
        choices = [
            self.read_text(f"선택지 {index}: ") for index in range(1, CHOICE_COUNT + 1)
        ]

        answer = self.read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)

        # Quiz 객체를 만들어 퀴즈 목록(리스트)에 추가한다. (append = 맨 뒤에 붙이기)
        self.quizzes.append(Quiz(question, choices, answer))

        # 저장에 성공(True)했는지에 따라 다른 메시지를 보여 준다.
        if self.save_state():
            print("✅ 퀴즈가 추가되었습니다!")
        else:
            print("⚠️ 퀴즈는 추가되었지만 파일 저장에 실패했습니다. (프로그램을 끄면 사라질 수 있어요)")

    # =======================================================================
    # 5. 기능: 퀴즈 목록
    # =======================================================================
    def show_quiz_list(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:  # 퀴즈가 없는 경우 처리
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    # =======================================================================
    # 6. 기능: 점수 확인
    # =======================================================================
    def show_score(self):
        """저장된 최고 점수를 출력한다."""
        if self.best_score is None:
            # 아직 퀴즈를 한 번도 풀지 않은 경우
            print("아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요!")
        elif self.best_correct is not None and self.best_total is not None:
            # 점수와 함께 "몇 문제 중 몇 문제"까지 알고 있는 경우 (정상적인 경우)
            print(f"최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct}문제 정답)")
        else:
            # 점수만 있는 경우 (예: 직접 만든 state.json 에 best_score 만 적혀 있을 때)
            print(f"최고 점수: {self.best_score}점")

    # =======================================================================
    # 7. 파일 저장 / 불러오기 (state.json)
    #
    # [JSON 이란?]
    #   JavaScript Object Notation 의 약자. 데이터를 "텍스트"로 표현하는 형식이다.
    #   파이썬의 딕셔너리/리스트와 모양이 거의 같고, 사람이 읽기 쉬우며,
    #   거의 모든 프로그래밍 언어가 읽고 쓸 수 있어서 데이터 저장/교환에 널리 쓰인다.
    #
    # [왜 파일에 저장할까?]
    #   변수에 들어 있는 데이터는 프로그램이 꺼지면 사라진다. (메모리에만 있기 때문)
    #   파일(디스크)에 써 두면 껐다 켜도 데이터가 남아 있다. = 데이터 영속성(persistence)
    # =======================================================================
    def to_state(self):
        """현재 게임 상태를 state.json 에 저장할 딕셔너리로 만든다."""
        return {
            # 리스트 컴프리헨션: Quiz 객체 하나하나를 to_dict() 로 변환한 리스트
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,  # None 은 JSON 에서 null 로 저장된다.
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }

    @staticmethod
    def _optional_count(value, name):
        """None 이거나 0 이상의 정수여야 하는 값을 검사한다.

        이름 앞의 밑줄(_)은 "클래스 안에서만 쓰려는 내부용 메서드"라는 관례적 표시이다.
        """
        if value is None:
            return None
        # bool 제외, 정수가 아니거나, 음수이면 올바르지 않은 값이다.
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} 값이 올바르지 않습니다.")
        return value

    def apply_state(self, data):
        """파일에서 읽어 온 데이터를 검사한 뒤, 문제가 없을 때만 한꺼번에 반영한다.

        [왜 "검사 먼저, 반영은 나중에" 일까?]
        검사 도중에 오류가 나면, 이미 일부만 반영된 어정쩡한 상태가 되어 버린다.
        지역 변수(quizzes 등)에 먼저 만들어 보고, 전부 성공했을 때만 self 에 넣으면
        실패했을 때 기존 데이터가 그대로 남는다.
        """
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터는 딕셔너리여야 합니다.")

        # data["quizzes"]: 키가 없으면 KeyError 가 발생한다. (load_state 에서 처리)
        raw_quizzes = data["quizzes"]
        if not isinstance(raw_quizzes, list):
            raise ValueError("quizzes 는 목록이어야 합니다.")

        # 딕셔너리 -> Quiz 객체로 변환. 잘못된 퀴즈가 하나라도 있으면 ValueError 가 발생한다.
        quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

        # data.get(키): 키가 없어도 오류 대신 None 을 돌려준다. (선택 항목에 적합)
        best_score = self._optional_count(data.get("best_score"), "best_score")
        best_correct = self._optional_count(data.get("best_correct"), "best_correct")
        best_total = self._optional_count(data.get("best_total"), "best_total")

        # 여기까지 오류 없이 왔다면 데이터가 안전하므로 진짜 속성에 반영한다.
        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total

    def reset_to_default(self):
        """퀴즈를 기본 퀴즈로, 점수를 '기록 없음'으로 초기화한다."""
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = None
        self.best_total = None

    def save_state(self):
        """현재 상태를 state.json 에 저장한다. 성공하면 True, 실패하면 False 를 돌려준다.

        [안전하게 저장하는 방법]
        state.json 에 바로 쓰다가 도중에 문제가 생기면 파일이 반쯤 쓰인 채로 망가질 수 있다.
        그래서 (1) 임시 파일(.tmp)에 먼저 완전히 쓰고, (2) 성공하면 진짜 파일과 교체한다.
        교체(os.replace)는 한 번에 일어나므로 "반쯤 쓰인 파일"이 남지 않는다.
        """
        # with_name(): 같은 폴더에 이름만 바꾼 경로를 만든다. -> state.json.tmp
        temp_path = self.state_path.with_name(self.state_path.name + ".tmp")
        try:
            # [파일 열기/쓰기/닫기의 기본 과정]
            #   open(경로, 모드, encoding) 으로 파일을 열고 -> 쓰고 -> 닫는다.
            #   모드 "w": 쓰기(write), 기존 내용은 지우고 새로 씀. (읽기는 "r")
            #   encoding="utf-8": 한글이 깨지지 않도록 문자 인코딩을 지정한다.
            # with 문: 블록이 끝나면(오류가 나더라도) 파일을 "자동으로 닫아" 준다.
            with open(temp_path, "w", encoding="utf-8") as file:
                # json.dump(데이터, 파일): 파이썬 데이터를 JSON 텍스트로 파일에 쓴다.
                #   ensure_ascii=False : 한글을 \uXXXX 같은 코드로 바꾸지 않고 그대로 저장
                #   indent=2           : 들여쓰기 2칸으로 보기 좋게 정리
                json.dump(self.to_state(), file, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.state_path)  # 임시 파일을 진짜 파일로 교체
            return True
        except (OSError, TypeError, ValueError) as error:
            # OSError: 디스크 가득 참, 권한 없음 등 파일 관련 오류
            # TypeError/ValueError: JSON 으로 변환할 수 없는 값이 있는 경우
            # "as error": 발생한 오류 객체를 error 라는 이름으로 받아 메시지를 출력할 수 있다.
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {error}")
            return False

    def load_state(self):
        """state.json 을 불러온다. 파일이 없거나 손상돼도 프로그램은 계속 실행된다.

        세 가지 상황을 모두 처리한다.
          (1) 파일이 없음(첫 실행)   -> 기본 퀴즈로 시작
          (2) 파일이 손상됨          -> 안내 후 기본 퀴즈로 복구
          (3) 파일을 읽을 수 없음    -> 안내 후 기본 퀴즈로 시작
        """
        # (1) 파일이 존재하지 않는 경우: 기본 퀴즈를 사용하고, 바로 파일을 만들어 둔다.
        if not self.state_path.exists():
            self.reset_to_default()
            print("저장된 데이터가 없어 기본 퀴즈로 시작합니다. (첫 실행)")
            self.save_state()
            return  # 더 할 일이 없으므로 함수 종료

        try:
            # 모드 "r": 읽기(read). 저장할 때와 똑같이 utf-8 로 읽어야 한글이 안 깨진다.
            with open(self.state_path, "r", encoding="utf-8") as file:
                data = json.load(file)  # JSON 텍스트 -> 파이썬 딕셔너리/리스트
            self.apply_state(data)  # 내용 검사 후 반영 (여기서도 오류가 날 수 있다)

        # (2) 파일 내용이 손상된 경우
        #   ValueError : JSON 문법 오류(JSONDecodeError), 글자 깨짐(UnicodeDecodeError),
        #                퀴즈 값이 이상함 등. (JSONDecodeError/UnicodeDecodeError 는 ValueError 의 자식)
        #   KeyError   : "quizzes" 같은 꼭 필요한 키가 없음
        #   TypeError  : 예상과 다른 자료형이 들어 있음
        # 괄호로 묶어서 여러 종류의 오류를 한 번에 잡을 수 있다.
        except (ValueError, KeyError, TypeError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self.backup_corrupted_file()  # 원본은 지우지 않고 따로 보관
            self.reset_to_default()
            self.save_state()  # 새(기본) 데이터로 깨끗한 state.json 을 다시 만든다.

        # (3) 파일을 읽는 것 자체가 안 되는 경우 (권한 문제 등)
        except OSError as error:
            print(f"⚠️ 데이터 파일을 읽을 수 없어 기본 퀴즈로 시작합니다: {error}")
            self.reset_to_default()

        # try 의 else: try 블록이 "오류 없이" 끝났을 때만 실행된다. (정상 불러오기 성공)
        else:
            score_text = "기록 없음" if self.best_score is None else f"{self.best_score}점"
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

    def backup_corrupted_file(self):
        """손상된 파일은 지우지 않고 .corrupt 로 이름을 바꿔 남겨 둔다. (복구 시도에 쓸 수 있도록)"""
        backup_path = self.state_path.with_name(self.state_path.name + ".corrupt")
        try:
            os.replace(self.state_path, backup_path)  # 파일 이름 바꾸기(이동)
            print(f"   (손상된 파일은 '{backup_path.name}' 로 보관했습니다.)")
        except OSError:
            # 백업에 실패해도 게임 진행에는 지장이 없으므로 조용히 넘어간다.
            # pass: "아무것도 하지 않음" 을 뜻하는 문장
            pass

    # =======================================================================
    # 8. 프로그램 전체 흐름
    # =======================================================================
    def run(self):
        """프로그램의 메인 흐름: 불러오기 -> 메뉴 반복 -> 종료 시 저장."""

        # 딕셔너리로 "메뉴 번호 -> 실행할 메서드" 를 연결해 둔다.
        # 주의: self.play_quiz 처럼 괄호 () 를 붙이지 않았다!
        #       괄호를 붙이면 "지금 실행"이고, 붙이지 않으면 "함수 자체를 값으로 저장"한다.
        # 이렇게 하면 if/elif 를 길게 늘어놓지 않고 actions[choice]() 로 바로 실행할 수 있다.
        # (종료 메뉴는 반복문을 빠져나와야 하므로 여기에 넣지 않고 따로 처리한다.)
        actions = {
            MENU_PLAY: self.play_quiz,
            MENU_ADD: self.add_quiz,
            MENU_LIST: self.show_quiz_list,
            MENU_SCORE: self.show_score,
        }

        self.show_banner()
        self.load_state()  # 시작할 때 저장된 데이터를 불러온다.

        # [Ctrl+C / 입력 종료 처리]
        #   KeyboardInterrupt : 사용자가 Ctrl+C 를 눌렀을 때 발생
        #   EOFError          : 입력 스트림이 끝났을 때 발생 (예: Ctrl+D / Ctrl+Z, 입력 파일이 끝남)
        # 이 오류들을 잡지 않으면 빨간 오류 메시지와 함께 "비정상 종료" 가 된다.
        # try 로 감싸 두면 안내 메시지를 보여 주고 깔끔하게 끝낼 수 있다.
        try:
            while True:  # 사용자가 "종료"를 고를 때까지 메뉴를 계속 반복
                self.show_menu()
                choice = self.read_int("선택: ", MENU_PLAY, MENU_EXIT)

                if choice == MENU_EXIT:
                    print("프로그램을 종료합니다. 안녕히 가세요!")
                    break  # break: 반복문을 완전히 빠져나간다.

                # 딕셔너리에서 choice 에 해당하는 메서드를 꺼내(actions[choice]) 바로 호출(())한다.
                actions[choice]()

        except (KeyboardInterrupt, EOFError):
            # 줄바꿈 \n 을 앞에 붙인 이유: Ctrl+C 를 누르면 입력 줄이 어중간하게 끊겨 있어서
            # 새 줄에서 메시지가 시작되도록 하기 위함이다.
            print("\n\n입력이 중단되었습니다. 데이터를 저장하고 안전하게 종료합니다.")

        # finally: 오류가 나든 안 나든, break 로 나가든 "항상" 마지막에 실행된다.
        # 어떤 방식으로 종료되더라도 데이터를 한 번 더 저장해 두기 위해 사용한다.
        finally:
            self.save_state()


def main():
    """프로그램의 시작점. 환경을 준비하고 게임을 실행한다."""

    # 터미널(특히 일부 윈도우 콘솔)이 한글/이모지를 표현하지 못하면 print 가
    # UnicodeEncodeError 로 프로그램을 죽일 수 있다.
    # errors="replace" 로 바꿔 두면, 표현할 수 없는 글자를 ? 로 대체하고 계속 실행한다.
    for stream in (sys.stdout, sys.stderr):  # 일반 출력과 오류 출력 둘 다 설정
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            # 출력 장치에 reconfigure 기능이 없으면 그냥 넘어간다.
            pass

    # QuizGame() : 클래스로 객체(인스턴스)를 만든다. -> __init__ 이 자동 실행된다.
    # .run()     : 만들어진 객체의 run 메서드를 실행해 게임을 시작한다.
    QuizGame().run()


# [if __name__ == "__main__": 의 의미]
#   이 파일을 "직접 실행"하면(python main.py) __name__ 이 "__main__" 이 되어 main() 이 실행된다.
#   반대로 다른 파일에서 "import main" 으로 가져다 쓰기만 할 때는 실행되지 않는다.
#   (그래서 Quiz 클래스만 따로 가져다 테스트하는 것도 가능하다.)
if __name__ == "__main__":
    main()
