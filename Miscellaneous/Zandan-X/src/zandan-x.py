import re
import traceback
from types import CodeType

# Only characters allowed:
# - Lowercase alphabet
# - Carriage return and line feed
# - Space
# - .
# - :
# - Parenthesis
# - Plus
ALLOWED_REGEX = r"[a-z0-9\r\n \.:\(\)\+]*"

BANNED_NAMES = {
    "mro",
    "fromhex"
}

BUILTINS = {
    "exc": BaseException,
}

def is_forbidden(string):
    return None is re.fullmatch(ALLOWED_REGEX, string)

def check_code_str(code_str):
    if is_forbidden(code_str):
        raise Exception(f"Your code doesn't fully match the regex '{ALLOWED_REGEX}'")

def check_code(code):
    if not isinstance(code, CodeType):
        return

    for x in code.co_consts + code.co_names:
        if type(x) is str and (is_forbidden(x) or x in BANNED_NAMES):
            raise Exception(f"Bad const or name: {x!r}")

    for const in code.co_consts:
        check_code(const)

def sandbox_run(code_str):
    try:
        check_code_str(code_str)
        code = compile(code_str, "", "exec")
        check_code(code)
        eval(code, {"__builtins__": BUILTINS}, {})
    except:
        traceback.print_exc()

# Everything below should not be of concern to you,
#   it shouldn't help you escape the sandbox.

if "__main__" == __name__:
    while True:
        while not (line := input(">>> ")): pass
        lines = [line]
        while True:
            try:
                line = input()
            except EOFError:
                break

            lines += [line]
            if not any(lines[-2:]):
                break

        sandbox_run('\n'.join(lines))
