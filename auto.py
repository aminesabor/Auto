import time
import threading
import json
from tkinter import Button as TkButton, Text, Label, Scrollbar, Tk, WORD, RIGHT, Y, END
from pynput.mouse import Button as MouseButton, Controller

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x400")
        self.root.resizable(0, 0)

        self.mouse_controller = Controller()
        self.clicking = False
        self.logs = []

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        self.start_stop_button = TkButton(self.root, text="Start", command=self.toggle_clicking)
        self.start_stop_button.pack(pady=10)

        self.reset_button = TkButton(self.root, text="Reset", command=self.reset_logs)
        self.reset_button.pack(pady=5)

        self.logs_label = Label(self.root, text="Logs:")
        self.logs_label.pack(pady=5)

        self.logs_text = Text(self.root, wrap=WORD, height=15, width=35)
        self.logs_text.pack(padx=5)

        self.scrollbar = Scrollbar(self.root, command=self.logs_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.logs_text.config(yscrollcommand=self.scrollbar.set)

    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.start_stop_button.config(text="Stop")
            self.start_clicking()
        else:
            self.start_stop_button.config(text="Start")

    def start_clicking(self):
        if self.clicking:
            self.mouse_controller.click(MouseButton.left, 1)
            log_entry = "Clicked at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            self.logs.append(log_entry)
            self.logs_text.insert(END, log_entry + "\n")
            self.logs_text.see(END)
            threading.Timer(1, self.start_clicking).start()

    def reset_logs(self):
        self.logs = []
        self.logs_text.delete(1.0, END)

    def on_close(self):
        self.save_logs()
        self.root.destroy()

    def save_logs(self):
        with open("click_logs.json", "w") as file:
            json.dump(self.logs, file, indent=4)

if __name__ == "__main__":
    root = Tk()
    gui = AutoClickerGUI(root)
    root.mainloop()
