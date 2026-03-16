


def print_mola_helper():
    """打印 MOLA HELPER CLI 启动横幅，含 ASCII 鱼和欢迎语。"""

    # ── ANSI 颜色 ──────────────────────────────────────
    BOLD   = "\033[1m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    GREY   = "\033[90m"
    GREEN  = "\033[92m"
    RESET  = "\033[0m"

    # ── 字母定义 (ANSI Shadow) ─────────────────────────
    letters = {
        'M': [
            "███╗   ███╗",
            "████╗ ████║",
            "██╔████╔██║",
            "██║╚██╔╝██║",
            "██║ ╚═╝ ██║",
            "╚═╝     ╚═╝",
        ],
        'O': [
            " ██████╗ ",
            "██╔═══██╗",
            "██║   ██║",
            "██║   ██║",
            "╚██████╔╝",
            " ╚═════╝ ",
        ],
        'L': [
            "██╗     ",
            "██║     ",
            "██║     ",
            "██║     ",
            "███████╗",
            "╚══════╝",
        ],
        'A': [
            " █████╗ ",
            "██╔══██╗",
            "███████║",
            "██╔══██║",
            "██║  ██║",
            "╚═╝  ╚═╝",
        ],
        'H': [
            "██╗  ██╗",
            "██║  ██║",
            "███████║",
            "██╔══██║",
            "██║  ██║",
            "╚═╝  ╚═╝",
        ],
        'E': [
            "███████╗",
            "██╔════╝",
            "█████╗  ",
            "██╔══╝  ",
            "███████╗",
            "╚══════╝",
        ],
        'P': [
            "██████╗ ",
            "██╔══██╗",
            "██████╔╝",
            "██╔═══╝ ",
            "██║     ",
            "╚═╝     ",
        ],
        'R': [
            "██████╗ ",
            "██╔══██╗",
            "██████╔╝",
            "██╔══██╗",
            "██║  ██║",
            "╚═╝  ╚═╝",
        ],
    }

    gap = "  "

    def build_word(word):
        return [gap.join(letters[ch][i] for ch in word) for i in range(6)]

    def pad_rows(rows):
        w = max(len(r) for r in rows)
        return [r.ljust(w) for r in rows], w

    # ── 构建文字行 ─────────────────────────────────────
    mola_rows, _= pad_rows(build_word("MOLA"))
    helper_rows, _ = pad_rows(build_word("HELPER"))

    # ── 鱼 ASCII Art (6 行，与字母等高) ────────────────
    fish_art = [
        "         ___            o  ",
        "   /\\  /  o  \\       o    ",
        "  <  >=|      >~~~       ",
        "  <  >=|      >~~~       ",
        "   \\/  \\____/            ",
        "     ~ . ~ . ~ . ~       ",
    ]
    fish_art, _ = pad_rows(fish_art)

    # ── 合并 MOLA + 鱼 (左右并排) ─────────────────────
    spacer = "        "
    combined = [mola_rows[i] + spacer + fish_art[i] for i in range(6)]

    # ── 欢迎语 ─────────────────────────────────────────
    welcome = [
        "><(((o>  Welcome to MOLA Helper v1.0!",
        "         Your intelligent assistant is ready.",
        "         Type '/help' to get started. Happy coding!",
    ]

    # ── 框架计算 ───────────────────────────────────────
    all_content = combined + helper_rows + welcome
    max_w = max(len(l) for l in all_content)
    pad = 4
    inner = max_w + 2 * pad

    border_t = "╔" + "═" * inner + "╗"
    border_b = "╚" + "═" * inner + "╝"
    empty    = "║" + " " * inner + "║"
    divider  = "║" + " " * pad + "─" * max_w + " " * pad + "║"

    # ── 带颜色的行格式化 ──────────────────────────────
    def row(text, color=WHITE):
        content = text.ljust(max_w)
        return f"{CYAN}║{RESET}" + " " * pad + f"{BOLD}{color}{content}{RESET}" + " " * pad + f"{CYAN}║{RESET}"

    def border(line):
        return f"{BOLD}{CYAN}{line}{RESET}"

    def empty_row():
        return f"{CYAN}║{RESET}" + " " * inner + f"{CYAN}║{RESET}"

    def divider_row():
        return f"{CYAN}║{RESET}" + " " * pad + f"{GREY}{'─' * max_w}{RESET}" + " " * pad + f"{CYAN}║{RESET}"

    # ── 输出 ───────────────────────────────────────────
    print()
    print(border(border_t))
    print(empty_row())

    for r in combined:
        print(row(r, BLUE))

    print(empty_row())

    for r in helper_rows:
        print(row(r, BLUE))

    print(empty_row())
    print(divider_row())
    print(empty_row())

    print(row(welcome[0], YELLOW))
    print(row(welcome[1], GREEN))
    print(row(welcome[2], GREEN))

    print(empty_row())
    print(border(border_b))
    print()
    



