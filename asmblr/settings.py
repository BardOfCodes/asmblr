from typing import List, Tuple

class Settings:
    copy_mode: bool = True


def update_settings(copy_mode: bool = False):
    Settings.copy_mode = copy_mode
