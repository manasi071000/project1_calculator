import tkinter as tk
from tkinter import messagebox
import math

# Main window
root = tk.Tk()
root.title("Calculator")
root.geometry("420x720")  # Adjusted window height to avoid extra space at the bottom
root.resizable(True, True)

expression = ""

# Theme setup
current_theme = "light"
themes = {
    "light": {
        "bg": "#ffffff",
        "fg": "#000000",
        "btn_bg": "lightgray",
        "hover_bg": "#d0d0d0",
        "entry_bg": "#ffffff"
    },
    "dark": {
        "bg": "#2e2e2e",
        "fg": "#ffffff",
        "btn_bg": "#4d4d4d",
        "hover_bg": "#606060",
        "entry_bg": "#3c3c3c"
    }
}

# Button reference for hover tracking
all_buttons = []

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()

def apply_theme():
    theme = themes[current_theme]
    root.configure(bg=theme["bg"])
    display.configure(bg=theme["entry_bg"], fg=theme["fg"])
    theme_button.configure(bg="gray", fg="white")
    for btn in all_buttons:
        color = btn.default_color
        if color not in ("lightgreen", "salmon", "lightblue"):
            color = theme["btn_bg"]
        btn.configure(bg=color, fg=theme["fg"])
        btn.default_color = color

def button_click(symbol):
    global expression
    expression += str(symbol)
    display_var.set(expression)

def clear_display():
    global expression
    expression = ""
    display_var.set("")

def calculate_result():
    global expression
    try:
        expr = expression.replace('^', '**')
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('log2', 'math.log2')
        expr = expr.replace('exp', 'math.exp')
        expr = expr.replace('abs', 'math.fabs')
        expr = expr.replace('pi', str(math.pi))
        expr = expr.replace('e', str(math.e))
        result = str(eval(expr))
        display_var.set(result)
        expression = result
    except Exception:
        messagebox.showerror("Error", "Invalid Input")
        expression = ""
        display_var.set("")

def handle_function(func_name):
    global expression
    expression += func_name + "("
    display_var.set(expression)

# Hover events
def on_enter(e):
    btn = e.widget
    if btn.default_color not in ("lightgreen", "salmon", "lightblue"):
        btn.configure(bg=themes[current_theme]["hover_bg"])

def on_leave(e):
    btn = e.widget
    btn.configure(bg=btn.default_color)

# Display setup
display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=("Arial", 24), bd=10,
                   width=22, borderwidth=5, relief="ridge", justify="right")
display.grid(row=0, column=0, columnspan=5, pady=20, ipady=15, padx=10)

# Buttons layout
buttons = [
    ['7', '8', '9', '/', '('],
    ['4', '5', '6', '*', ')'],
    ['1', '2', '3', '-', '^'],
    ['0', '.', '=', '+', 'C'],
    ['sin', 'cos', 'tan', 'e', 'sqrt'],
    ['abs', 'pi', 'log', 'log2', 'exp']
]

# Ensure columns expand evenly
for i in range(5):
    root.grid_columnconfigure(i, weight=1)

# Create and place buttons
for r, row in enumerate(buttons, start=1):
    for c, btn_text in enumerate(row):
        if btn_text == '':
            continue
        if btn_text == '=':
            cmd = calculate_result
            color = "lightgreen"
        elif btn_text == 'C':
            cmd = clear_display
            color = "salmon"
        elif btn_text in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'log2', 'abs', 'pi', 'e']:
            cmd = lambda t=btn_text: handle_function(t)
            color = "lightblue"
        else:
            cmd = lambda t=btn_text: button_click(t)
            color = themes[current_theme]["btn_bg"]

        btn = tk.Button(root, text=btn_text, font=("Arial", 14), bg=color,
                        height=2, width=6, command=cmd)
        btn.grid(row=r, column=c, padx=5, pady=5, sticky='nsew')
        btn.default_color = color
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        all_buttons.append(btn)

# Theme toggle button at bottom right
theme_button = tk.Button(root, text="🌗 Theme", font=("Arial", 12),
                         command=toggle_theme, bg="gray", fg="white", relief="raised")
theme_button.grid(row=7, column=4, padx=5, pady=5, sticky='e')  # Reduced padding

# Apply the theme initially
apply_theme()

# Configure the last row to expand and fill the remaining space to avoid bottom gap
root.grid_rowconfigure(7, weight=0)

# Run the app
root.mainloop()
