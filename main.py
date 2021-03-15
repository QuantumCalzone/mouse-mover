import argparse
import caffeine
from datetime import datetime
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time

verbose = True
mouse = MouseController()
keyboard = KeyboardController()
execute_move_mouse = False
execute_press_shift_key = False
pixels_to_move = 1
move_mouse_every_seconds = 300
last_save_position = (0, 0)


def define_custom_seconds():
    if verbose:
        print(f"define_custom_seconds () | {get_now_timestamp()}")

    global move_mouse_every_seconds, pixels_to_move, execute_press_shift_key, execute_move_mouse

    parser = argparse.ArgumentParser(
        description="This program moves the mouse or press a key when it detects that you are away. "
                    "It won't do anything if you are using your computer. "
                    "Useful to trick your machine to think you are still working with it.")

    parser.add_argument("-s", "--seconds", type=int,
                        help="Define in seconds how long to wait after a user is considered idle. Default 300.")

    parser.add_argument("-p", "--pixels", type=int,
                        help="Set how many pixels the mouse should move. Default 1.")

    parser.add_argument("-m", "--mode",
                        help="Available options: keyboard, mouse, both; default is mouse. "
                             "This is the action that will be executed when the user is idle: "
                             "If keyboard is selected, the program will press the shift key. "
                             "If mouse is selected, the program will move the mouse. "
                             "If both is selected, the program will do both actions. ")

    args = parser.parse_args()
    mode = args.mode

    if args.seconds:
        move_mouse_every_seconds = int(args.seconds)

    if args.pixels:
        pixels_to_move = int(args.pixels)

    is_both_enabled = 'both' == mode
    is_keyboard_enabled = 'keyboard' == mode or is_both_enabled
    is_mouse_enabled = 'mouse' == mode or is_both_enabled or mode is None

    if is_keyboard_enabled:
        execute_press_shift_key = True

        if verbose:
            print(get_now_timestamp(), "Keyboard is enabled")

    if is_mouse_enabled:
        execute_move_mouse = True

        if verbose:
            print(get_now_timestamp(), "Mouse is enabled, moving", pixels_to_move, 'pixels')

    if verbose:
        print(get_now_timestamp(), 'Running every', str(move_mouse_every_seconds), 'seconds')


def move_mouse_when_unable_to_move(expected_mouse_position):
    if verbose:
        print(f"move_mouse_when_unable_to_move ( expected_mouse_position: {expected_mouse_position} ) | {get_now_timestamp()}")

    if expected_mouse_position != mouse.position:
        mouse.position = (0, 0)


def move_mouse():
    if verbose:
        print(f"move_mouse () | {get_now_timestamp()}")

    new_x = currentPosition[0] + pixels_to_move
    new_y = currentPosition[1] + pixels_to_move

    new_position = (new_x, new_y)
    mouse.position = new_position

    move_mouse_when_unable_to_move(new_position)

    current_position = mouse.position

    if verbose:
        print(get_now_timestamp(), 'Moved mouse to: ', current_position)

    return current_position


def press_shift_key():
    if verbose:
        print(f"press_shift_key () | {get_now_timestamp()}")

    keyboard.press(Key.shift)
    keyboard.release(Key.shift)


def get_now_timestamp():
    # if verbose:
    #     print("get_now_timestamp ()")

    now = datetime.now()
    return now.strftime("%H:%M:%S")


def execute_keep_awake_action():
    if verbose:
        print(f"execute_keep_awake_action () | {get_now_timestamp()}")

    if execute_move_mouse:
        move_mouse()

    if execute_press_shift_key:
        press_shift_key()


define_custom_seconds()

while True:
    currentPosition = mouse.position
    is_user_away = currentPosition == last_save_position

    if is_user_away:
        execute_keep_awake_action()
        currentPosition = mouse.position

    if verbose and not is_user_away:
        print(f"User activity detected | {get_now_timestamp()}")

    last_save_position = currentPosition

    time.sleep(move_mouse_every_seconds)
