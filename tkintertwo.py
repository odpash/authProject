
from PIL import Image, ImageTk
from tkinter import Tk, BOTH, Frame
from tkinter.ttk import Frame, Label, Style, Button


class App(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in [InitUI, AddUI]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
        self.show_frame("InitUI")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class InitUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        super().__init__()
        self.controller = controller

        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#333")

        bard = Image.open("Images/2022-06-01_16-18-38.png").resize((400, 300))
        bardejov = ImageTk.PhotoImage(bard)
        imageStream = Label(self, image=bardejov)
        imageStream.image = bardejov
        imageStream.place(x=10, y=10)

        addToDb = Button(self, text="Добавить нового пользователя", command=lambda: controller.show_frame("AddUI"))
        addToDb.place(x=70, y=330)

        results = Label(self, text="Результаты")
        results.place(x=570, y=10)


class AddUI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        super().__init__()
        self.controller = controller
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#333")
        addToDb = Button(self, text="Вернуться назад", command=lambda: controller.show_frame("InitUI"))
        addToDb.place(x=70, y=330)


def main():
    root = Tk()
    root.resizable(False, False)
    root.geometry("800x375")
    app = App()
    root.mainloop()


if __name__ == '__main__':
    main()