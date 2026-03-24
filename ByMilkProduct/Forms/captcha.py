import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
import random
import os

class captcha(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.correct = [
            [1, 2],
            [3, 4],
        ]
        self.current = []
        self.labels = []
        self.selected = None

        self.mix()
        self.draw()

    def mix(self):
        flat =  [1, 2, 3, 4]
        random.shuffle(flat)
        self.current = [
            [flat[0], flat[1]],
            [flat[2], flat[3]]
        ]

    def draw(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.labels = []
        for row in range(2):
            row_labels = []
            for column in range(2):
                num = self.current[row][column]
                path =os.path.join("Img", f"{num}.png")
                img = Image.open(path)
                img  = img.resize((70,70))
                tk_img = ImageTk.PhotoImage(img)
                lbl = tkinter.Label(self, image = tk_img)
                lbl.image = tk_img

                lbl.bind("<Button-1>", lambda e, r=row, c=column: self.click(r, c))
                lbl.grid(row=row, column=column)
                row_labels.append(lbl)
            self.labels.append(row_labels)

    def click(self, row, column):
        if self.selected ==None:
            self.selected = (row,column)
        else:
            r1, c1 = self.selected
            r2, c2 = row, column

            self.current[r1][c1], self.current[r2][c2] = self.current[r2][c2], self.current[r1][c1]
            self.selected = None
            self.draw()






