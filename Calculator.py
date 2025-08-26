import tkinter as tk

class RoundButton(tk.Canvas):
    def __init__(self, parent, text, bg, fg, command=None, diameter=80):
        super().__init__(parent, width=diameter, height=diameter, highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.diameter = diameter
        self.bg_color = bg
        self.fg_color = fg

        # Draw circle
        self.circle = self.create_oval(2, 2, diameter - 2, diameter - 2, fill=bg, outline=bg)

        # Centered text
        self.text = self.create_text(
            diameter // 2,
            diameter // 2,
            text=text,
            fill=fg,
            font=("Helvetica", 14, "bold")
        )

        # Bind click events
        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if self.command:
            self.command()

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mathematics is a Language 🧮")
        self.configure(bg="#1e1e2e")

        # Display
        self.display = tk.Entry(self, font=("Helvetica", 24), bd=0, relief="flat", bg="#313244", fg="white", justify="right")
        self.display.pack(fill="both", padx=20, pady=20, ipady=10)

        # Buttons layout
        buttons = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C"]
        ]

        # Button colors
        self.btn_colors = {
            "num": {"bg": "#89b4fa", "fg": "black"},
            "op": {"bg": "#f38ba8", "fg": "white"},
            "eq": {"bg": "#a6e3a1", "fg": "black"},
            "cl": {"bg": "#f9e2af", "fg": "black"}
        }

        # Buttons frame
        btns_frame = tk.Frame(self, bg="#1e1e2e")
        btns_frame.pack(expand=True)

        for i, row in enumerate(buttons):
            for j, btn in enumerate(row):
                t = self.btn_type(btn)
                color = self.btn_colors[t]

                rbtn = RoundButton(
                    btns_frame,
                    text=btn,
                    bg=color["bg"],
                    fg=color["fg"],
                    command=lambda x=btn: self.on_click(x),
                    diameter=80
                )
                rbtn.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                rbtn.config(width=80, height=80)  # lock canvas size

        # Lock grid sizes
        for i in range(len(buttons)):
            btns_frame.grid_rowconfigure(i, weight=1, minsize=100)
        for j in range(len(max(buttons, key=len))):
            btns_frame.grid_columnconfigure(j, weight=1, minsize=100)

    def btn_type(self, btn):
        if btn.isdigit() or btn == ".":
            return "num"
        elif btn in ["+", "-", "×", "÷"]:
            return "op"
        elif btn == "=":
            return "eq"
        else:
            return "cl"

    def on_click(self, char):
        if char == "C":
            self.display.delete(0, tk.END)
        elif char == "=":
            try:
                expr = self.display.get().replace("×", "*").replace("÷", "/")
                result = eval(expr)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, char)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
