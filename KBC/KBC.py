import tkinter as tk
from tkinter import messagebox

# Define questions and levels
questions = [
    ["Q1.Besides Sachin Tendulkar, who is the only other Indian cricketer to have scored over 13,000 runs in test cricket?", "Virat Kohli", "Sunil Gavaskar", "VVS laxman", "Rahul Dravid", 4],
    ["Q2.Ranthambore, Sariska and Keoladeo Ghana are all names of what?", "National Parks", "Goosebumps", "Mountains", "Rivers", 1],
    ["Q3.India official entry to Oscars 2021, \u201d Jallikattu\u201d is, a film in which language?", "Hindi", "Punjabi", "Kannada", "Malayalam", 4],
    ["Q4.In terms of production, which of these is the largest train coach manufacturing unit in the world?", "Integral Coach Factory, Bangalore", "Integral Coach Factory, Mumbai", "Integral Coach Factory, Chennai", "Integral Coach Factory, Kolkata", 3],
    ["Q5.In 2020, Louise Gluck won the Nobel Prize in which category?", "Music", "Sports", "Literature", "Dance", 3],
    ["Q6.Which of the following companies was originally started as a loom manufacturing unit in 1909?", "Suzuki", "CEAT", "Honda", "Mercedes", 1],
    ["Q7.In 1994, who became the winner of the first-ever Filmfare R D Burman Award for New Music Talent?", "Udit Narayan", "A. R. Rahman", "Lata Mangeshkar", "Raj Burman", 2],
    ["Q8.What colour did Lord Shiva's throat turn into when he drank the deadly poison during Samudra Manthan?", "Red", "Yellow", "Blue", "Black", 3],
    ["Q9.What is the profession of Kabir in the film Kabir Singh?", "Engineer", "Cricketer", "Athlete", "Doctor", 4],
    ["Q10.Which of these national parks is named after the river that flows through the park?", "Pench", "Tadoba", "Vrindavan", "Wildera", 1],
    ["Q11.Which state is the largest producer of sugarcane in India?", "Maharashtra", "Karnataka", "Madhya Pradesh", "Uttar Pradesh", 4],
    ["Q12.Which of these colors when mixed with red will produce the color orange?", "Violet", "Green", "Orange", "Yellow", 4],
    ["Q13.Which of these is an ashram set up by Gandhiji set up near Wardha in Maharashtra?", "Sri Aurobindo Ashram", "Parmarth Niketan Ashram", "Sevagram", "Sivananda Ashram", 3],
    ["Q14.Who of the following personalities is not married to a sports person?", "Anushka Sharma", "Sakshi Singh Rawat", "Mahesh Bhupathi", "Sharmila Tagore", 3],
    ["Q15.Which part of the plant absorbs water and nutrients from the soil?", "Stem", "Buds", "Leafs", "Root", 4],
    ["Q16.Which process enables earthen pots (matkas) to keep water cool?", "Absorption", "Suction", "Evaporation", "Adiabatic Process", 3],
]
levels = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 1200000, 320000, 640000, 1250000, 2500000, 5000000, 10000000, 70000000]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.question_index = 0
        self.money = 0
        self.initialize_ui()

    def initialize_ui(self):
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")

        self.title_label = tk.Label(
            self.root, text="Quiz Game", font=("Helvetica", 24, "bold"), bg="#1a1a1a", fg="white"
        )
        self.title_label.pack(pady=20)

        self.question_label = tk.Label(
            self.root, text="", wraplength=700, font=("Helvetica", 16), bg="#1a1a1a", fg="white"
        )
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.options_frame.pack()

        self.option_buttons = []
        for i in range(4):
            option_button = tk.Button(
                self.options_frame,
                text="",
                font=("Helvetica", 14),
                bg="#333333",
                fg="white",
                activebackground="#444444",
                activeforeground="white",
                command=lambda i=i: self.check_answer(i + 1),
                width=30,
                pady=10,
            )
            option_button.grid(row=i, column=0, pady=10)
            self.option_buttons.append(option_button)

        self.quit_button = tk.Button(
            self.root,
            text="Quit",
            font=("Helvetica", 14),
            bg="#ff4d4d",
            fg="white",
            activebackground="#ff6666",
            activeforeground="white",
            command=self.quit_game,
        )
        self.quit_button.pack(pady=20)

        self.update_question()

    def update_question(self):
        question = questions[self.question_index]
        self.question_label.config(text=f"Question for Rs. {levels[self.question_index]}:\n{question[0]}")
        for i in range(4):
            self.option_buttons[i].config(text=f"{chr(65 + i)}. {question[i + 1]}")

    def check_answer(self, selected_option):
        if selected_option == questions[self.question_index][5]:
            self.money = levels[self.question_index]
            self.question_index += 1
            if self.question_index < len(questions):
                self.update_question()
            else:
                self.show_result()
        else:
            self.show_result()

    def quit_game(self):
        messagebox.showinfo("Quit", f"You quit the game. Money you will be taking home is Rs. {self.money}")
        self.root.destroy()

    def show_result(self):
        messagebox.showinfo("Game Over", f"Money you will be taking home is Rs. {self.money}")
        self.root.destroy()

# Initialize the tkinter app
root = tk.Tk()
root.title("Quiz Game")
app = QuizApp(root)
root.mainloop()