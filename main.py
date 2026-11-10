import sys

# 상수 설정
TITLE = "나만의 퀴즈 게임 (메뉴 테스트)"
WIDE_LINE = "=" * 40

# 메뉴 번호 상수 정의
MENU_PLAY = 1
MENU_ADD = 2
MENU_LIST = 3
MENU_SCORE = 4
MENU_DELETE = 5
MENU_HISTORY = 6
MENU_EXIT = 7


class QuizGame:
    """메뉴 흐름과 입력 검증만 테스트하기 위한 클래스."""

    def __init__(self):
        pass

    @staticmethod
    def parse_int(raw, low, high):
        """입력받은 문자열을 검증하여 정수로 변환합니다."""
        raw = raw.strip()

        if not raw:
            print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            return None

        try:
            value = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            return None

        if not low <= value <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            return None

        return value

    @staticmethod
    def read_int(prompt, low, high):
        """올바른 메뉴 숫자가 들어올 때까지 무한 반복하여 입력받습니다."""
        while True:
            value = QuizGame.parse_int(input(prompt), low, high)
            if value is not None:
                return value

    def show_banner(self):
        """상단 타이틀 배너 출력"""
        print(WIDE_LINE)
        print(f" {TITLE}")
        print(WIDE_LINE)

    def show_menu(self):
        """메뉴 구성 출력"""
        print()
        self.show_banner()
        print(f"{MENU_PLAY}. 퀴즈 풀기")
        print(f"{MENU_ADD}. 퀴즈 추가")
        print(f"{MENU_LIST}. 퀴즈 목록")
        print(f"{MENU_SCORE}. 점수 확인")
        print(f"{MENU_DELETE}. 퀴즈 삭제")
        print(f"{MENU_HISTORY}. 점수 기록")
        print(f"{MENU_EXIT}. 종료")
        print(WIDE_LINE)

    def run(self):
        """메뉴 입력 무한 루프 테스트"""
        try:
            while True:
                self.show_menu()
                choice = self.read_int("선택: ", MENU_PLAY, MENU_EXIT)

                if choice == MENU_EXIT:
                    print("프로그램을 종료합니다  안녕히 가세요!")
                    break

                # 아직 기능이 없으므로 입력받은 번호만 출력 확인
                print(f"\n📢 [테스트] {choice}번 메뉴가 정상적으로 선택되었습니다.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n입력이 중단되었습니다. 안전하게 종료합니다.")


def main():
    # 윈도우 인코딩 예외 방지 설정
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass

    # 게임 실행
    QuizGame().run()


if __name__ == "__main__":
    main()
