import tkinter as tk


class ScalesBar(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scaleR = tk.Scale(self)
        self.scaleG = tk.Scale(self)
        self.scaleB = tk.Scale(self)

        self.extra_init()

    def extra_init(self):
        padx = 65

        label_to_scaleR = tk.Label(self)
        self.set_label_to_scale(label_to_scaleR, 'Кол-во красных бит')
        label_to_scaleR.grid(row=0, column=0, padx=padx)
        self.set_scale(self.scaleR)
        self.scaleR.grid(row=1, column=0)

        label_to_scaleG = tk.Label(self)
        self.set_label_to_scale(label_to_scaleG, 'Кол-во зеленых бит')
        label_to_scaleG.grid(row=0, column=1, padx=padx)
        self.set_scale(self.scaleG)
        self.scaleG.grid(row=1, column=1)

        label_to_scaleB = tk.Label(self)
        self.set_label_to_scale(label_to_scaleB, 'Кол-во синих бит')
        label_to_scaleB.grid(row=0, column=2, padx=padx)
        self.set_scale(self.scaleB)
        self.scaleB.grid(row=1, column=2)

    @staticmethod
    def set_scale(scale):
        scale['orient'] = tk.HORIZONTAL
        scale['length'] = 150
        scale['from_'] = 0
        scale['to'] = 8
        scale['tickinterval'] = 1
        scale['resolution'] = 1

    @staticmethod
    def set_label_to_scale(label, text):
        label['font'] = "Arial 10"
        label['text'] = text

    @property
    def get_coding_options(self):
        r_count = self.scaleR.get()
        g_count = self.scaleG.get()
        b_count = self.scaleB.get()
        return r_count, g_count, b_count
