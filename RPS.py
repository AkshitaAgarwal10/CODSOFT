import tkinter as tk
from tkinter import messagebox, simpledialog, font
import random

class RPSGame:
    def __init__(self, master):
        self.master = master
        self.master.title("✨ Rock Paper Scissors ✨")
        self.master.geometry("400x500")
        self.master.configure(bg='#faf3f0')
        self.scores = {"You": 0, "Computer": 0}
        self.round = 0
        self.player_name = self.get_player_name()
        
        self.colors = {
            "background": "#faf3f0",
            "primary": "#d4e2d4",
            "secondary": "#ffcacc", 
            "accent": "#ef7c8e",   
            "text": "#5c5c5c",     
            "highlight": "#a2d2ff" 
        }

        self.options = [
            {"name": "Rock", "emoji": "🪨", "color": "#d4b483"}, 
            {"name": "Paper", "emoji": "📜", "color": "#f0e6dd"}, 
            {"name": "Scissors", "emoji": "✂️", "color": "#b8b8d1"}
        ]

        title_font = font.Font(family='Helvetica', size=20, weight='bold')
        button_font = font.Font(family='Segoe UI', size=12)
        
        tk.Label(master, text=f"RPS · {self.player_name} vs Computer", 
                font=title_font, bg=self.colors["background"],
                fg=self.colors["text"]).pack(pady=(25,15))
        
        self.score_label = tk.Label(master, text="You: 0  |  Computer: 0", 
                                  font=('Helvetica', 14), 
                                  bg=self.colors["background"],
                                  fg=self.colors["text"])
        self.score_label.pack()
        
        self.round_label = tk.Label(master, text="Round: 0", 
                                  font=('Helvetica', 12), 
                                  bg=self.colors["background"],
                                  fg=self.colors["text"])
        self.round_label.pack(pady=(0,25))
        btn_frame = tk.Frame(master, bg=self.colors["background"])
        btn_frame.pack(pady=15)
        
        self.buttons = []
        for option in self.options:
            btn = tk.Button(btn_frame, text=f"{option['emoji']} {option['name']}",
                          font=button_font, 
                          bg=option["color"],
                          fg=self.colors["text"],
                          activebackground=self.colors["highlight"],
                          borderwidth=2, relief="ridge",
                          width=10,
                          padx=5, pady=5,  
                          command=lambda c=option['name']: self.play_round(c))
            btn.pack(side=tk.LEFT, padx=6, pady=5)
            self.buttons.append(btn)
        
        self.result_text = tk.StringVar()
        self.result_label = tk.Label(master, textvariable=self.result_text,
                                   font=('Helvetica', 14, 'bold'), 
                                   bg=self.colors["background"])
        self.result_label.pack(pady=20)
        
        self.choice_text = tk.StringVar()
        tk.Label(master, textvariable=self.choice_text,
               font=('Helvetica', 12), 
               bg=self.colors["background"],
               fg=self.colors["text"]).pack()
    
    def get_player_name(self):
        """Get player name with aesthetic dialog"""
        self.master.withdraw() 
        name = simpledialog.askstring("Welcome!", "Enter your name:",
                                    parent=self.master)
        self.master.deiconify() 
        return name if name else "Player"
    
    def animate_button(self, button):
        """Subtle animation for clicked button"""
        original_bg = button['bg']
        for i, color in [(1, self.colors["highlight"]), 
                        (2, original_bg)]:
            button.config(bg=color)
            self.master.update()
            self.master.after(150)
    
    def play_round(self, player_choice):
        for btn in self.buttons:
            if player_choice.lower() in btn['text'].lower():
                self.animate_button(btn)
                break
        
        self.round += 1
        computer_choice = random.choice(self.options)['name']
        
        player_emoji = next(o['emoji'] for o in self.options if o['name'] == player_choice)
        comp_emoji = next(o['emoji'] for o in self.options if o['name'] == computer_choice)
        self.choice_text.set(f" You: {player_emoji}  vs  Computer: {comp_emoji} ")
        self.round_label.config(text=f"Round: {self.round}")
        
        result_colors = {
            "win": ("#4CAF50", "#e8f5e9"),  
            "lose": ("#EF5350", "#ffebee"), 
            "tie": ("#5C6BC0", "#e3f2fd")    
        }
        
        if player_choice == computer_choice:
            result = ("It's a tie! ✨", *result_colors["tie"])
        elif (player_choice == "Rock" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Rock") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            self.scores["You"] += 1
            result = ("You win! 🌟", *result_colors["win"])
        else:
            self.scores["Computer"] += 1
            result = ("Computer wins! 🤖", *result_colors["lose"])
        
        self.result_text.set(result[0])
        self.result_label.config(fg=result[1])
        self.score_label.config(text=f"You: {self.scores['You']}  |  Computer: {self.scores['Computer']}")
        self.master.config(bg=result[2])
        
        self.master.after(800, lambda: self.master.config(bg=self.colors["background"]))
        
        if not messagebox.askyesno("Continue?", "Play another round?",
                                 parent=self.master):
            self.show_final_results()
            self.reset_game()
    
    def show_final_results(self):
        win_percent = (self.scores["You"] / self.round) * 100 if self.round > 0 else 0
        performance = (
            "🏆 Champion!" if win_percent >= 75 else
            "✨ Great job!" if win_percent >= 50 else
            "🌱 Keep going!"
        )
        
        message = (
            f"🌿 Final Results 🌿\n\n"
            f"Player: {self.player_name}\n"
            f"Rounds: {self.round}\n"
            f"Wins: {self.scores['You']} ({win_percent:.1f}%)\n\n"
            f"{performance}"
        )
        messagebox.showinfo("Game Over", message)
    
    def reset_game(self):
        self.scores = {"You": 0, "Computer": 0}
        self.round = 0
        self.score_label.config(text="You: 0  |  Computer: 0")
        self.round_label.config(text="Round: 0")
        self.result_text.set("")
        self.choice_text.set("")

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()
