import threading
import tkinter as tk
import time
import random

class Leaderboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Leaderbaord Speed typing")
        self.root.geometry("900x600")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.results_label = tk.Label(self.frame, text=self.get_top_results(), font=("Helvetica", 10))
        self.results_label.grid(row=1, column=1)
        self.root.mainloop()

    def sort_results_by_time(self):
        with open("wyniki.txt", "r") as file:
            lines = file.readlines()

        def sort_key(line):
            return float(line.split("\t")[0])

        lines.sort(key=sort_key, reverse=True)

        with open("wyniki.txt", "w") as file1:
            file1.writelines(lines)

    def get_top_results(self):
        self.sort_results_by_time()
        with open("wyniki.txt", "r") as file:
            lines = file.readlines()
        top_five_lines = lines[:5]
        return '\n'.join(top_five_lines)

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speed typing")
        self.root.geometry("900x600")
        self.frame = tk.Frame(self.root)

        # dane użytkownika
        self.username_label = tk.Label(self.frame, text="Nazwa gracza: ", font=("Helvetica", 14))
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame, width=10, font=("Helvetica", 14))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        # tworzenie zdania do przepisania
        self.sample_label = tk.Label(self.frame, text=self.generate_sentence(), font=("Helvetica", 14))
        self.sample_label.grid(row=1, column=1, columnspan=3, padx=5, pady=10)

        # główne wejście wylosowanego tekstu
        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.input_entry.bind("<KeyRelease>", self.start)

        #label od prędkości
        self.speed_label = tk.Label(self.frame,
                                    text="Speed: 0.00 CPS - znaków na sekunde \n 0.00 CPM - znaków na minutę "
                                         "\n słów na sekundę: 0.00 słów na minutrę: 0.00", font=("Helvetica", 18))
        self.speed_label.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 18))
        self.reset_button.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
        # TODO wyniki
        self.leaderboard = tk.Button(self.frame, text="Ranking wyników", command=Leaderboard, font=("Helvetica", 18))
        self.leaderboard.grid(row=4, column=1, columnspan=3, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.started = False
        self.running = False
        self.end_result = 0

        self.root.mainloop()

    def start(self, event):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.time_thread)
            t.start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.sample_label.cget('text') == self.input_entry.get():
            self.running = False
            self.input_entry.config(fg="green")
            self.safe_results()

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            cps = len(self.input_entry.get()) / self.counter
            cpm = cps * 60
            wps = len(self.input_entry.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.config(
                text=f"Speed: {cps: .2f} CPS - znaków na sekunde \n {cpm:.2f} CPM - znaków na minutę \n"
                     f" słów na sekundę: {wps: .2f} słów na minutrę: {wpm: .2f}")
            self.end_result = wpm

    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: 0.00 CPS - znaków na sekunde \n 0.00 CPM - znaków na minutę\n"
                                     " słów na sekundę: 0.00 słów na minutrę: 0.00")
        self.sample_label.config(text=self.generate_sentence())
        self.input_entry.delete(0, tk.END)

    def generate_sentence(self):
        words = open("venv/words.txt", "r").read().split("\n")
        chosen_words = random.sample(words, 2)
        return chosen_words

    def safe_results(self):
        osoba = self.username_entry.get()
        wynik = self.speed_label.cget('text').replace("\n", "\t")
        czas = self.end_result
        with open("wyniki.txt", 'a') as save:
            save.write(f"{czas:.2f} \t WPM \t Gracza: {osoba} \t Pełne dane: {wynik} \n")


Game()
# https://www.mit.edu/~ecprice/wordlist.10000
