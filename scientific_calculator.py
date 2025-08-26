"""
Scientific Calculator with Tkinter (GUI)
----------------------------------------

Author: Aayush Suthar
GitHub: https://github.com/Aayushsuthar

Description:
------------
A scientific calculator built using Python's Tkinter library with:
- Round buttons for UI
- Support for trigonometric, logarithmic, exponential functions
- DEG/RAD angle modes
- Memory (stub for future use)
- Previous answer recall (Ans)
- Error handling

Usage:
------
Run the script:
    python scientific_calculator.py
"""

import tkinter as tk
from tkinter import messagebox
import math
import random


class RoundButton(tk.Canvas):
    """
    Custom round button widget for Tkinter.
    """
    def __init__(self, parent, text, command=None,
                 bg="#444", fg="white", font=("Arial", 16, "bold"), diameter=70):
        super().__init__(parent, width=diameter, height=diameter,
                         bg=parent["bg"], highlightthickness=0)

        self.command = command
        self.diameter = diameter
        self.bg = bg
        self.fg = fg
        self.font = font

        # Draw button shape
        self.circle = self.create_oval(2, 2, diameter - 2, diameter - 2,
                                       fill=bg, outline=bg)
        # Add text
        self.text = self.create_text(diameter // 2, diameter // 2,
                                     text=text, fill=fg, font=font)

        # Bind events
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_click(self, event):
        """Trigger button command on click."""
        if self.command:
            self.command()

    def on_hover(self, event):
        """Change color when hovered."""
        self.itemconfig(self.circle, fill="#666")

    def on_leave(self, event):
        """Restore color when mouse leaves."""
        self.itemconfig(self.circle, fill=self.bg)


class ScientificCalculator:
    """
    Scientific Calculator with Tkinter GUI.
    Supports trigonometry, logarithms, power, factorial,
    reciprocal, and more.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("750x900")
        self.root.config(bg="#23272e")

        self.expression = ""   # Current input expression
        self.ans = ""          # Previous result
        self.angle_mode = "DEG"  # Default angle mode
        self.memory = 0        # Memory storage

        self.create_widgets()

    def create_widgets(self):
        """Setup calculator display and buttons."""
        # Variables
        self.input_text = tk.StringVar()
        self.expr_text = tk.StringVar()
        self.mode_text = tk.StringVar(value=self.angle_mode)

        # Title label
        math_label = tk.Label(self.root, text=" Mathematics is a language ",
                              font=('Courier', 30, 'bold'),
                              bg="#23272e", fg="#ffffff", anchor='center')
        math_label.pack(fill="x", padx=10, pady=(10, 0))

        # Expression display
        expr_label = tk.Label(self.root, textvariable=self.expr_text,
                              font=('Arial', 16), bg="#23272e",
                              fg="#a0a0a0", anchor='e')
        expr_label.pack(fill="x", padx=10, pady=(10, 0))

        # Input field
        input_field = tk.Entry(self.root, font=('Arial', 28, 'bold'),
                               textvariable=self.input_text,
                               bg="#ffffff", fg="#000000",
                               bd=0, justify='right',
                               insertbackground="#5d585a")
        input_field.pack(fill="x", padx=10, pady=(0, 10), ipady=15)

        # Angle mode display
        mode_label = tk.Label(self.root, textvariable=self.mode_text,
                              font=('Arial', 14),
                              bg="#23272e", fg="#ffffff", anchor='w')
        mode_label.pack(fill="x", padx=10, pady=(0, 5))

        # Button grid frame
        btns_frame = tk.Frame(self.root, bg="#1a2029")
        btns_frame.pack(expand=True, fill="both")

        # Buttons layout
        buttons = [
            ["MC", "MR", "MS", "M+", "M-", "←", "CE", "C"],
            ["7", "8", "9", "/", "%", "x^2", "x^3", "x^y"],
            ["4", "5", "6", "*", "n!", "(", ")", "1/x"],
            ["1", "2", "3", "-", "sin", "cos", "tan", "ln"],
            ["0", ".", "π", "+", "Ans", "DEG", "RAD", "="]
        ]

        # Colors for buttons
        btn_colors = {
            "num": {"bg": "#D8D8DA", "fg": "#23272e"},
            "op": {"bg": "#D8D8DA", "fg": "#23272e"},
            "func": {"bg": "#D8D8DA", "fg": "#23272e"},
            "mem": {"bg": "#D8D8DA", "fg": "#23272e"},
            "ctrl": {"bg": "#D8D8DA", "fg": "#23272e"},
            "mode": {"bg": "#D8D8DA", "fg": "#23272e"},
            "eq": {"bg": "#D8D8DA", "fg": "#23272e"},
        }

        # Helper to classify button type
        def btn_type(btn):
            if btn in "0123456789.":
                return "num"
            if btn in ["+", "-", "*", "/", "%", "(", ")", "^", "x^y"]:
                return "op"
            if btn in ["sin", "cos", "tan", "ln", "log", "√",
                       "x^2", "x^3", "exp", "n!", "1/x", "|x|",
                       "Rand", "mod", "EE", "π"]:
                return "func"
            if btn in ["MC", "MR", "MS", "M+", "M-"]:
                return "mem"
            if btn in ["C", "CE", "←", "±"]:
                return "ctrl"
            if btn in ["DEG", "RAD", "GRAD", "Ans"]:
                return "mode"
            if btn == "=":
                return "eq"
            return "num"

        # Place buttons
        for i, row in enumerate(buttons):
            for j, btn in enumerate(row):
                t = btn_type(btn)
                color = btn_colors[t]

                rbtn = RoundButton(btns_frame, text=btn,
                                   bg=color["bg"], fg=color["fg"],
                                   command=lambda x=btn: self.on_click(x),
                                   diameter=80)
                rbtn.grid(row=i, column=j, padx=10, pady=10)

    def on_click(self, btn):
        """Handle button press actions."""
        try:
            if btn in ["DEG", "RAD", "GRAD"]:
                self.angle_mode = btn
                self.mode_text.set(self.angle_mode)
            elif btn == "C":
                self.expression = ""
                self.input_text.set("")
                self.expr_text.set("")
            elif btn == "CE":
                self.input_text.set("")
            elif btn == "←":
                self.expression = self.expression[:-1]
                self.input_text.set(self.expression)
            elif btn == "=":
                result = str(self.evaluate_expression(self.expression))
                self.ans = result
                self.input_text.set(result)
                self.expr_text.set(self.expression)
                self.expression = result
            elif btn == "Ans":
                self.expression += self.ans
                self.input_text.set(self.expression)
            elif btn == "π":
                self.expression += str(math.pi)
                self.input_text.set(self.expression)
            elif btn == "Rand":
                rnd_val = str(random.random())
                self.expression += rnd_val
                self.input_text.set(self.expression)
            elif btn in ["MS", "MR", "MC", "M+", "M-"]:
                pass  # Memory functionality placeholder
            elif btn in ["sin", "cos", "tan", "ln", "log", "√",
                         "x^2", "x^3", "x^y", "exp", "n!",
                         "1/x", "|x|"]:
                self.expression += btn + "("
                self.input_text.set(self.expression)
            else:
                self.expression += btn
                self.input_text.set(self.expression)
        except Exception:
            messagebox.showerror("Error", "Invalid Input")
            self.expression = ""
            self.input_text.set("")

    def evaluate_expression(self, expr):
        """Convert math expressions into Python's eval-compatible form."""
        expr = expr.replace("^", "**").replace("π", str(math.pi))
        expr = expr.replace("√(", "math.sqrt(").replace("x^2(", "pow(").replace("x^3(", "pow(")
        expr = expr.replace("ln(", "math.log(").replace("log(", "math.log10(")
        expr = expr.replace("exp(", "math.exp(").replace("n!(", "math.factorial(")
        expr = expr.replace("1/x(", "1/(").replace("|x|(", "abs(").replace("mod", "%")
        expr = expr.replace("x^y", "**").replace("EE", "e")

        # Handle angle modes
        if self.angle_mode == "DEG":
            expr = expr.replace("sin(", "math.sin(math.radians(")
            expr = expr.replace("cos(", "math.cos(math.radians(")
            expr = expr.replace("tan(", "math.tan(math.radians(")
        elif self.angle_mode == "RAD":
            expr = expr.replace("sin(", "math.sin(").replace("cos(", "math.cos(").replace("tan(", "math.tan(")

        expr = expr.replace("pow(", "math.pow(")

        try:
            return eval(expr, {"math": math, "abs": abs, "e": math.e, "pow": pow})
        except Exception:
            return "Error"


if __name__ == "__main__":
    root = tk.Tk()
    calc = ScientificCalculator(root)
    root.mainloop()

