""" simple curses print function """
import curses


def stdscr_get():
    """get curses window"""
    # BEGIN ncurses startup/initialization...
    # Initialize the curses object.
    stdscr = curses.initscr()

    # Do not echo keys back to the client.
    curses.noecho()

    # Non-blocking or cbreak mode... do not wait for Enter key to be pressed.
    curses.cbreak()

    # Turn off blinking cursor
    curses.curs_set(False)

    # Enable color if we can...
    if curses.has_colors():
        curses.start_color()

    # Optional - Enable the keypad. This also decodes multi-byte key sequences
    # stdscr.keypad(True)
    return stdscr


def stdscr_print(stdscr: curses, pos_x: int, pos_y: int, text: str) -> None:
    """print text to curses window"""
    # Print text to the screen.
    stdscr.addstr(pos_x, pos_y, text)
    # Actually draws the text above to the positions specified.
    stdscr.refresh()


def stdscr_end(stdscr, line: int) -> None:
    """end curses window"""

    stdscr.addstr(
        line,
        curses.COLS - len("Press a key to quit."),
        "Press a key to quit.",
    )

    # Actually draws the text above to the positions specified.
    stdscr.refresh()

    # Grabs a value from the keyboard without Enter having to be pressed (see cbreak above)
    stdscr.getch()
    # BEGIN ncurses shutdown/deinitialization...
    # Turn off cbreak mode...
    curses.nocbreak()

    # Turn echo back on.
    curses.echo()

    # Restore cursor blinking.
    curses.curs_set(True)

    # Turn off the keypad...
    # stdscr.keypad(False)

    # Restore Terminal to original state.
    curses.endwin()

    # END ncurses shutdown/deinitialization...
