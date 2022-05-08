# Learn Japanese program by dmyTRUEk

__version__ = "0.3.2"

from copy import deepcopy
from sys import exit as sys_exit

from colorama import Fore as fg
#from colorama import Back as bg
from colorama import Style

from extensions import unreachable, shuffled, avg, trim_by_first_line
from tests import Test, TestLength, TestType, generate_tests



class Constants:
    COMMAND_STOP: str = ";;"
    EXITING: str = "\nExiting..."



def colorize(s: str, /, *, fg=None, bg=None) -> str:
    is_fg: bool = fg is not None
    is_bg: bool = bg is not None
    return (
        (fg if is_fg else "") +
        (bg if is_bg else "") +
        s +
        (Style.RESET_ALL if (is_fg or is_bg) else "")
    )


def run_test(tests: list[Test], test_len: TestLength) -> tuple[list[bool], list[Test]]:
    statistics: list[bool] = []
    mistakes: list[Test] = []

    def ask_check_update(test: Test) -> bool:
        # this function will:
        # 1. ask question
        # 2. check answer
        # 3. update statistics
        print()
        print(test.message_to_fmt.format(test.question))

        user_answer = input("Answer: ")
        if user_answer == Constants.COMMAND_STOP: return True

        is_answered_correctly = test.chech_answer(user_answer)

        if is_answered_correctly:
            print(colorize("Correct.", fg=fg.GREEN))
        else:
            print(colorize(f"WRONG! Correct answer: {test.answer}", fg=fg.RED))
            mistaken_test = deepcopy(test)
            mistaken_test.user_answer = user_answer
            if mistaken_test not in mistakes:
                mistakes.append(mistaken_test)

        statistics.append(is_answered_correctly)
        # TODO?
        # return@ask_questions statistics
        return False

    try:
        match test_len:
            case TestLength.Endless:
                while True:
                    for test in shuffled(tests):
                        is_exited = ask_check_update(test)
                        if is_exited: return (statistics, mistakes)
            case TestLength.OnceEverySymbol:
                for test in shuffled(tests):
                    is_exited = ask_check_update(test)
                    if is_exited: return (statistics, mistakes)
            case TestLength.CertainAmount:
                assert(hasattr(test_len, "n"))
                tests_shuffle: list[Test] = []
                for _ in range(test_len.n):
                    if len(tests_shuffle) == 0:
                        tests_shuffle = shuffled(tests)
                    test = tests_shuffle.pop()
                    is_exited = ask_check_update(test)
                    if is_exited: return (statistics, mistakes)
            case _:
                unreachable()
    except KeyboardInterrupt:
        print(Constants.EXITING)
    return (statistics, mistakes)


def ask_test_type() -> TestType:
    print("Available test types:")
    for (i, test_type) in enumerate(TestType):
        print(f"{i+1}) {test_type.value}")
    try:
        chosen_option: int = int(input(f"Choose test type (1-{len(TestType)}): ")) - 1
    except KeyboardInterrupt:
        print(Constants.EXITING)
        sys_exit(0)
    test_type = TestType.get_by_index(chosen_option)
    return test_type


def ask_test_len() -> TestLength:
    print("Available test lenghts:")
    for (i, test_type) in enumerate(TestLength):
        print(f"{i+1}) {test_type.value}")
    try:
        chosen_option: int = int(input(f"Choose test lenght (1-{len(TestLength)}): ")) - 1
    except KeyboardInterrupt:
        print(Constants.EXITING)
        sys_exit(0)
    test_len = TestLength.get_by_index(chosen_option)
    if test_len == TestLength.CertainAmount:
        test_len.n = int(input("How many times? "))
    return test_len


def print_statistics(statistics: list[bool]):
    match avg(statistics):
        case float(fraction):
            percentage = 100.0 * fraction
            percentage_str = f"{percentage:.1f}%"
        case None:
            percentage_str = "--"
        case _:
            unreachable()
    print(f"Percentage of correct answers: {percentage_str}")


def print_mistakes(mistakes: list[Test]):
    print(f"Total mistakes: " + colorize(str(len(mistakes)), fg=fg.RED) + ". Your mistakes:")
    for (i, test) in enumerate(mistakes):
        assert(test.user_answer is not None)
        print(f"{i+1}. {test.message_to_fmt.format(test.question)}")
        print("   Correct answer: " + colorize(str(test.answer), fg=fg.GREEN))
        print("   Your    answer: " + colorize(test.user_answer, fg=fg.RED))


def main() -> None:
    print(trim_by_first_line(f"""
        Learn Japanese by dmyTRUEk, v{__version__}

        To exit input `{Constants.COMMAND_STOP}` or press Ctrl+C.
    """))
    print()

    test_type = ask_test_type()
    print()
    test_len = ask_test_len()

    tests = generate_tests(test_type)
    statistics, mistakes = run_test(tests, test_len)

    print()
    input("Press Enter to see results.")
    if mistakes:
        print()
        print_mistakes(mistakes)
    print()
    print_statistics(statistics)

    print()





if __name__ == "__main__":
    main()

