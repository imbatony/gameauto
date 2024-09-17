import pyautogui as pyautogui

class BaseOctCommand:
    def __init__(self, name, description, help):
        self.name = name
        self.description = description
        self.help = help

    def execute(self, args):
        raise NotImplementedError

    def __str__(self):
        return f"{self.name}: {self.description}"
    


