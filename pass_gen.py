import tkinter as tk
from tkinter import ttk
import random
import string

# ----- Password Generator -----
def pass_gen(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=False):
    if length < 4:
        raise ValueError('Password length must be at least 4')

    char_sets = []
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_digits:
        char_sets.append(string.digits)
    if use_special:
        char_sets.append(string.punctuation)

    if not char_sets:
        raise ValueError('At least one character type must be selected')

    # Ensure at least one char from each selected set
    password_chars = [random.choice(char_set) for char_set in char_sets]

    # Fill the rest
    all_chars = ''.join(char_sets)
    password_chars += [random.choice(all_chars) for _ in range(length - len(password_chars))]

    random.shuffle(password_chars)
    return ''.join(password_chars)

# ----- Password Strength Checker -----
def get_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 12 and score == 4:
        return "Strong 💪"
    elif length >= 8 and score >= 3:
        return "Medium ⚠️"
    else:
        return "Weak 😬"

# ----- GUI -----
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x600")
root.config(bg="#120025")

# ----- Fonts -----
FONT_TITLE = ("Courier New", 22, "bold")
FONT_NORMAL = ("Courier New", 12)
FONT_BUTTON = ("Courier New", 12, "bold")

# ----- Style for Rounded Button -----
style = ttk.Style()
style.theme_use('default')
style.configure("Rounded.TButton",
                font=FONT_BUTTON,
                padding=14,
                relief="flat",
                foreground="#ffffff",
                background="#d4aaff",
                borderwidth=1,
                bordercolor="#d4aaff")
style.map("Rounded.TButton",
          background=[("active", "#c288ff")],
          foreground=[("active", "#ffffff")])

# ----- Title -----
title = tk.Label(root, text="🦋", font=("Arial", 64), bg="#120025", fg="#d84dff")
title.pack(pady=(20, 0))

strength_label = tk.Label(root, text="Password Strength", font=FONT_NORMAL, bg="#120025", fg="#ffffff")
strength_label.pack(pady=(10, 0))

# ----- Password Length Slider + Value -----
length_label_frame = tk.Frame(root, bg="#d4aaff")
length_label_frame.pack(pady=(20, 0))

tk.Label(length_label_frame, text="Password Length:", font=FONT_NORMAL, bg="#d4aaff", fg="#120025").pack(side="left")

length_var = tk.IntVar(value=12)
length_value_label = tk.Label(length_label_frame, text=f"{length_var.get()} characters",
                               font=FONT_NORMAL, bg="#d4aaff", fg="#120025")
length_value_label.pack(side="left", padx=(10, 0))

def update_length_label(event):
    length_value_label.config(text=f"{int(length_var.get())} characters")

length_slider = ttk.Scale(root, from_=4, to=32, variable=length_var, orient="horizontal", length=250)
length_slider.pack()
length_slider.bind("<Motion>", update_length_label)
length_slider.bind("<ButtonRelease-1>", update_length_label)

# ----- Checkboxes -----
options_frame = tk.Frame(root, bg="#120025")
options_frame.pack(pady=20)

use_upper = tk.BooleanVar(value=True)
use_lower = tk.BooleanVar(value=True)
use_digits = tk.BooleanVar(value=True)
use_special = tk.BooleanVar(value=False)

tk.Checkbutton(options_frame, text="Include Uppercase Letters", variable=use_upper,
               font=FONT_NORMAL, bg="#120025", fg="#d84dff", activebackground="#120025",
               selectcolor="#1c0030").pack(anchor="w")

tk.Checkbutton(options_frame, text="Include Lowercase Letters", variable=use_lower,
               font=FONT_NORMAL, bg="#120025", fg="#d84dff", activebackground="#120025",
               selectcolor="#1c0030").pack(anchor="w")

tk.Checkbutton(options_frame, text="Include Digits", variable=use_digits,
               font=FONT_NORMAL, bg="#120025", fg="#d84dff", activebackground="#120025",
               selectcolor="#1c0030").pack(anchor="w")

tk.Checkbutton(options_frame, text="Include Special Symbols", variable=use_special,
               font=FONT_NORMAL, bg="#120025", fg="#d84dff", activebackground="#120025",
               selectcolor="#1c0030").pack(anchor="w")

# ----- Generated Password Display -----
password_display = tk.Text(root, height=2, width=30, font=("Courier New", 14), bg="#1c0030", fg="#d84dff", bd=0)
password_display.pack(pady=20)

# ----- Generate Function -----
def generate_password():
    try:
        length = int(length_var.get())
        pwd = pass_gen(
            length=length,
            use_upper=use_upper.get(),
            use_lower=use_lower.get(),
            use_digits=use_digits.get(),
            use_special=use_special.get()
        )
        strength = get_strength(pwd)
        strength_label.config(text=f"Strength: {strength}")
        password_display.delete("1.0", tk.END)
        password_display.insert(tk.END, pwd)
    except ValueError as e:
        password_display.delete("1.0", tk.END)
        password_display.insert(tk.END, str(e))
        strength_label.config(text="Strength: ⚠️ Error")

# ----- Generate Button -----
gen_button = ttk.Button(root, text="Generate", command=generate_password, style="Rounded.TButton")
gen_button.pack(pady=10)

# ----- Run the app -----
root.mainloop()
