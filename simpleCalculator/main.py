import tkinter as tk
from simpleCalculator import SimpleCalculator



if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCalculator(root)
    root.mainloop()