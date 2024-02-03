import tkinter as tk
import random

class WelcomeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Wake Up")
        self.master.configure(bg='black')

        # Генерация слова "welcome" слева сверху
        self.word_label = tk.Label(self.master, text="", bg='black', fg='white', font=("Helvetica", 24))
        self.word_label.pack(anchor="nw", padx=30, pady=30)

        self.word = "welcome"
        self.current_text = ""
        self.index = 0
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        self.update_word_label()

        # Поля для ввода пароля
        self.password_label = tk.Label(self.master, text="Enter Password:", bg='black', fg='white', font=("Helvetica", 16))
        self.password_label.pack(anchor="center", pady=10)

        self.password_entry = tk.Entry(self.master, show="*", bg='black', fg='white', font=("Helvetica", 16))
        self.password_entry.pack(anchor="center")

        self.password_entry.focus_set()

        self.password_entry.bind("<Return>", self.check_password)  # Добавляем обработчик событий для нажатия Enter

    def update_word_label(self):
        if self.index < len(self.word):
            letter = self.word[self.index]
            for char in self.alphabet:
                self.current_text += char
                self.word_label.config(text=self.current_text)
                self.master.update()
                self.master.after(25)
                if char == letter:
                    self.index += 1
                    break
                self.current_text = self.current_text[:-1]
            self.master.after(100, self.update_word_label)

    def check_password(self, event=None):
        entered_password = self.password_entry.get()
        if entered_password == "322":
            self.password_label.pack_forget()
            self.password_entry.pack_forget()
            self.password_entry.unbind("<Return>")
            self.master.configure(bg='black')
            self.word_label.config(text="Main Menu")
            self.create_buttons()
            self.center_window()
        else:
            self.password_entry.delete(0, tk.END)  # Очистить поле ввода пароля
            self.password_label.config(text="Incorrect password", fg="red")

    def create_buttons(self):
        button_frame = tk.Frame(self.master, bg='black')
        button_frame.pack(anchor="center", pady=20)

        words = [
            "qewr", "eee", "wqe", "ewwq", "egr", "qq", "werg", "gwe", "sdaf", "zasxcv", 
            "dqwef", "rfsadf", "fr", "asdf", "1111", "sadf", "ft", "gg", "eh", "rq", 
            "fe", "sde", "fsa", "df", "sadfasdfsadf", "ww", "qewr", "eee", "wqe"
        ]

        random.shuffle(words)

        buttons = []

        for i, word in enumerate(words):
            button = tk.Button(button_frame, text=word, width=10, height=3, font=("Helvetica", 12), bg='black', fg='white')
            button.grid(row=i % 10, column=i // 10, padx=5, pady=5)
            buttons.append(button)

    def center_window(self):
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

def main():
    root = tk.Tk()
    app = WelcomeWindow(root)
    root.attributes("-fullscreen", True)
    root.mainloop()

if __name__ == "__main__":
    main()
