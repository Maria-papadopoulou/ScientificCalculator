import tkinter as tk
import customtkinter as ctk
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('320x460')  # Ορίζει τις διαστάσεις του παραθύρου
        self.root.title('Calculator')  # Ορίζει τον τίτλο του παραθύρου
        self.root.configure(bg='white')  # Ορίζει το φόντο ως λευκό
        self.root.bind('<Key>', self.key_input)  # Συνδέει την εισαγωγή πληκτρολογίου με handler
        self.scientific_mode = False  # Αρχική κατάσταση λειτουργίας: μη επιστημονική
        self.root.iconbitmap('calculator.ico') #εικονίδιο εφαρμογής
        self.root.resizable(False, False) 


        self.create_widgets()  # Δημιουργεί τα widgets

    def safe_eval(self, expression):
        """Ασφαλής αξιολόγηση της έκφρασης μόνο με τη βιβλιοθήκη math."""
        try:
            return eval(expression, {"math": math, "__builtins__": None})
        except Exception:
            return "Error"

    def display_input(self, _input):
        """Εισάγει το input στη θέση του δρομέα."""
        current_pos = self.input_box.index(tk.INSERT)
        self.input_box.insert(current_pos, _input)
        self.input_box.icursor(current_pos + len(_input))
        self.display_result()

    def display_result(self):
        """Αξιολογεί την έκφραση και εμφανίζει το αποτέλεσμα σε πραγματικό χρόνο."""
        try:
            # Μετατροπή συμβόλων σε Python-compatible σύνταξη
            calc = self.input_box.get().replace('×', '*').replace('÷', '/').replace('Mod', '%')
            calc = calc.replace('^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            calc = calc.replace('sin(', 'math.sin(math.radians(')
            calc = calc.replace('cos(', 'math.cos(math.radians(')
            calc = calc.replace('tan(', 'math.tan(math.radians(')
            calc = calc.replace('√(', 'math.sqrt(').replace('log(', 'math.log(')

            # Αντιμετώπιση ανοικτών/κλειστών παρενθέσεων
            open_p = calc.count('(')
            close_p = calc.count(')')
            if not calc.strip():
                self.result_label.config(text='')
                return
            if open_p > close_p:
                calc += ')' * (open_p - close_p)

            result = self.safe_eval(calc)

            # Στρογγυλοποίηση αποτελέσματος αν είναι float
            if isinstance(result, float):
                result = round(result, 4)
                result = int(result) if result.is_integer() else result

            self.result_label.config(text=f'={result}' if result != "Error" else "Error")
        except:
            self.result_label.config(text='Error')

    def delete_input(self):
        """Διαγράφει τον τελευταίο χαρακτήρα."""
        text = self.input_box.get()
        if text:
            self.input_box.delete(len(text) - 1, tk.END)
            self.display_result()

    def clear_input(self):
        """Καθαρίζει το input και το αποτέλεσμα."""
        self.input_box.delete(0, tk.END)
        self.result_label.config(text='')

    def highlight_result(self):
        """Υπολογίζει και εμφανίζει το αποτέλεσμα με έντονη μορφή."""
        self.display_result()
        self.input_box.config(font=('Bold', 15))
        self.result_label.config(font=('Bold', 30))

    def change_theme(self):
        """Αλλάζει μεταξύ light και dark theme."""
        current_bg = self.root.cget('bg')
        new_bg, new_fg = ('black', 'white') if current_bg == 'white' else ('white', 'black')
        self.root.config(bg=new_bg)
        self.input_box.config(bg=new_bg, fg=new_fg)
        self.result_label.config(bg=new_bg, fg='gray')
        self.theme_button.config(bg=new_bg, fg=new_fg)

    def change_scientific_mode(self):
        """Εναλλάσσει τη λειτουργία επιστημονικών κουμπιών."""
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.root.geometry('400x460')  # Αύξηση πλάτους για επιστημονική λειτουργία
            self.place_scientific_buttons()
        else:
            self.root.geometry('320x460')  # Επιστροφή στην αρχική διάσταση
            self.hide_scientific_buttons()

    def insert_function_template(self, fname):
        """Εισάγει συνάρτηση με παρενθέσεις και μετακινεί τον κέρσορα εντός."""
        pos = self.input_box.index(tk.INSERT)
        self.input_box.insert(pos, f"{fname}()")
        self.input_box.icursor(pos + len(fname) + 1)
        self.display_result()

    def create_widgets(self):
        """Δημιουργεί όλα τα γραφικά στοιχεία και κουμπιά."""
        self.input_box = tk.Entry(self.root, font=('Bold', 20), justify=tk.RIGHT, bd=0,
                                  bg='SystemButtonFace', highlightthickness=0)
        self.input_box.place(x=15, y=10, width=250, height=50)

        self.result_label = tk.Label(self.root, font=('Bold', 15), fg='gray', anchor=tk.E,
                                     bg='white', highlightthickness=0)
        self.result_label.place(x=15, y=75, width=250, height=50)

        self.theme_button = tk.Button(self.root, text='🌙', font=('Bold', 20), bd=0,
                                      command=self.change_theme)
        self.theme_button.place(x=30, y=400, width=40, height=40)

        # Κουμπιά λειτουργιών (Καθαρισμός, διαγραφή, Mod, διαίρεση)
        ctk.CTkButton(self.root, text='C', width=40, height=40, font=('Bold', 30),
                      fg_color='#FF7433', command=self.clear_input).place(x=30, y=135)
        ctk.CTkButton(self.root, text='←', width=40, height=40, font=('Bold', 25),
                      fg_color='#FF7433', command=self.delete_input).place(x=90, y=135)
        ctk.CTkButton(self.root, text='Mod', width=40, height=40, font=('Bold', 20),
                      fg_color='#FF7433', command=lambda: self.display_input('Mod')).place(x=150, y=135)
        ctk.CTkButton(self.root, text='÷', width=40, height=40, font=('Bold', 30),
                      fg_color='#FF7433', command=lambda: self.display_input('÷')).place(x=220, y=135)

        # Κύρια αριθμητικά και μαθηματικά κουμπιά
        buttons = [
            ('7', 30, 210), ('8', 90, 210), ('9', 150, 210), ('×', 220, 210),
            ('4', 30, 275), ('5', 90, 275), ('6', 150, 275), ('-', 220, 275),
            ('1', 30, 340), ('2', 90, 340), ('3', 150, 340), ('+', 220, 340),
            ('0', 90, 400), ('.', 150, 400)
        ]
        for text, x, y in buttons:
            ctk.CTkButton(self.root, text=text, width=40, height=40, font=('Bold', 20),
                          command=lambda t=text: self.display_input(t)).place(x=x, y=y)

        # Κουμπιά ίσον και επιστημονικής εναλλαγής
        ctk.CTkButton(self.root, text='=', width=40, height=40, font=('Bold', 30),
                      fg_color='#FF7433', command=self.highlight_result).place(x=220, y=400)
        ctk.CTkButton(self.root, text='Sci', width=40, height=40, font=('Bold', 20),
                      command=self.change_scientific_mode).place(x=270, y=400)

        # Επιστημονικά κουμπιά (αρχικά κρυμμένα)
        self.sin_button = ctk.CTkButton(self.root, text='sin', width=40, height=40, font=('Bold', 20),
                                        command=lambda: self.insert_function_template('sin'))
        self.cos_button = ctk.CTkButton(self.root, text='cos', width=40, height=40, font=('Bold', 20),
                                        command=lambda: self.insert_function_template('cos'))
        self.tan_button = ctk.CTkButton(self.root, text='tan', width=40, height=40, font=('Bold', 20),
                                        command=lambda: self.insert_function_template('tan'))
        self.sqrt_button = ctk.CTkButton(self.root, text='√', width=40, height=40, font=('Bold', 20),
                                         command=lambda: self.insert_function_template('√'))
        self.log_button = ctk.CTkButton(self.root, text='log', width=40, height=40, font=('Bold', 20),
                                        command=lambda: self.insert_function_template('log'))
        self.pi_button = ctk.CTkButton(self.root, text='π', width=40, height=40, font=('Bold', 20),
                                       command=lambda: self.display_input('π'))
        self.e_button = ctk.CTkButton(self.root, text='e', width=40, height=40, font=('Bold', 20),
                                      command=lambda: self.display_input('e'))
        self.power_button = ctk.CTkButton(self.root, text='^', width=40, height=40, font=('Bold', 20),
                                          command=lambda: self.display_input('^'))
        self.open_parens = ctk.CTkButton(self.root, text='(', width=40, height=40, font=('Bold', 20),
                                         command=lambda: self.display_input('('))
        self.close_parens = ctk.CTkButton(self.root, text=')', width=40, height=40, font=('Bold', 20),
                                          command=lambda: self.display_input(')'))

    def key_input(self, event):
        """Αντιμετωπίζει την εισαγωγή από το πληκτρολόγιο."""
        key = event.keysym
        char = event.char

        # Διαχείριση ειδικών πλήκτρων
        if key in ('Return', 'KP_Enter'):
            self.highlight_result()
            return "break"
        elif key == 'BackSpace':
            self.delete_input()
            return "break"
        elif key == 'Escape':
            self.clear_input()
            return "break"

        # Συντομεύσεις για επιστημονικές συναρτήσεις
        if char.lower() == 's':
            self.insert_function_template('sin')
            return "break"
        elif char.lower() == 'c':
            self.insert_function_template('cos')
            return "break"
        elif char.lower() == 't':
            self.insert_function_template('tan')
            return "break"
        elif char.lower() == 'l':
            self.insert_function_template('log')
            return "break"
        elif char.lower() == 'r':
            self.insert_function_template('√')
            return "break"
        elif char.lower() == 'p':
            self.display_input('π')
            return "break"
        elif char.lower() == 'e':
            self.display_input('e')
            return "break"

        # Εισαγωγή αριθμών και βασικών συμβόλων
        if char in '0123456789.+-*/%^()':
            display_char = char
            #return "break"
            if char == '*':
                display_char = '×'
            elif char == '/':
                display_char = '÷'
            self.display_input(display_char)
            return "break"

        return "break"

    def place_scientific_buttons(self):
        """Εμφανίζει τα επιστημονικά κουμπιά."""
        self.sin_button.place(x=270, y=135)
        self.cos_button.place(x=330, y=135)
        self.tan_button.place(x=270, y=190)
        self.sqrt_button.place(x=330, y=190)
        self.log_button.place(x=270, y=245)
        self.pi_button.place(x=330, y=245)
        self.power_button.place(x=270, y=300)
        self.e_button.place(x=330, y=300)
        self.open_parens.place(x=270, y=350)
        self.close_parens.place(x=330, y=350)

    def hide_scientific_buttons(self):
        """Κρύβει τα επιστημονικά κουμπιά."""
        for btn in [self.sin_button, self.cos_button, self.tan_button, self.sqrt_button,
                    self.log_button, self.pi_button, self.e_button,
                    self.power_button, self.open_parens, self.close_parens]:
            btn.place_forget()

if __name__ == "__main__":
    root = tk.Tk()  # Δημιουργεί το κύριο παράθυρο
    app = CalculatorApp(root) # Δημιουργεί την εφαρμογή υπολογιστή
    root.mainloop() # Εκκινεί το loop του παραθύρου
