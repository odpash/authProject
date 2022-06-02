import json

from imutils import paths

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2
from tkinter.ttk import Frame, Label, Style, Button
from PIL import Image, ImageTk
from tkinter import Tk, BOTH, Frame, Entry
import pickle

import face_recognition
from PIL import Image, ImageTk
import tkinter as tk
import datetime
import cv2
import os

cascPathface = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_image = None
        self.counts = {}
        self.vs = cv2.VideoCapture(0)
        self.output_path = os.path.abspath(os.curdir) + "/Images/"
        self.geometry('800x375')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container
        self.video_loop()
        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def video_loop(self):
        ok, frame = self.vs.read()
        if True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,
                                                 scaleFactor=1.1,
                                                 minNeighbors=5,
                                                 minSize=(60, 60),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            names = []
            if len(encodings) == 0:
                self.counts = {}
            data = pickle.loads(open('face_enc', "rb").read())
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Unknown"
                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    self.counts = {}
                    for i in matchedIdxs:
                        name = data["names"][i]
                        self.counts[name] = self.counts.get(name, 0) + 1
                    name = max(self.counts, key=self.counts.get)
                else:
                    self.counts = {}
                names.append(name)
                for ((x, y, w, h), name) in zip(faces, names):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                                0.75, (0, 255, 0), 2)

            print(self.counts)
        if ok:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image).resize((400, 300))  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            imageStream = Label(self, image=imgtk)
            imageStream.image = imgtk
            imageStream.place(x=10, y=10)
        self.container.after(1, self.video_loop)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.labels = []
        addToDb = Button(self, text="Добавить нового пользователя", command=lambda: controller.show_frame("PageOne"))
        addToDb.place(x=70, y=330)
        self.generate_stats()

    def generate_stats(self):
        results = Label(self, text="Результаты:", font=self.controller.title_font)
        results.place(x=550, y=10)

        z = 40
        f = json.loads(open('db.json', 'r', encoding='UTF-8').read())

        for i in self.labels:
            i.destroy()

        for i in self.controller.counts.keys():
            for j in f:
                if j['fio'] == i:
                    l = Label(self,
                              text=f"id: {j['id']}\nФио: {j['fio']}\nТелефон: {j['phone']}\nНаправление: {j['napr']}\nГруппа: {j['group']}")
                    l.place(x=550, y=z)
                    self.labels.append(l)
            z += 90
        self.controller.after(1, self.generate_stats)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_image = controller.current_image
        self.fio = tk.StringVar()
        self.group = tk.StringVar()
        self.napravlenie = tk.StringVar()
        self.phone = tk.StringVar()
        self.photoName = ""

        addToDb = Button(self, text="Вернуться в меню", command=lambda: controller.show_frame("StartPage"))
        addToDb.place(x=125, y=330)

        results = Label(self, text="Добавить нового пользователя", font=controller.title_font)
        results.place(x=465, y=10)

        fioL = Label(self, text="ФИО")
        fioE = Entry(self, bd=5, textvariable=self.fio)
        fioL.place(x=475, y=100)
        fioE.place(x=550, y=92)

        groupL = Label(self, text="Группа")
        groupE = Entry(self, bd=5, textvariable=self.group)
        groupL.place(x=470, y=150)
        groupE.place(x=550, y=142)

        naprL = Label(self, text="Направление")
        naprE = Entry(self, bd=5, textvariable=self.napravlenie)
        naprL.place(x=450, y=200)
        naprE.place(x=550, y=192)

        phoneL = Label(self, text="Моб. телефон")
        phoneE = Entry(self, bd=5, textvariable=self.phone)
        phoneL.place(x=450, y=250)
        phoneE.place(x=550, y=242)

        addToDb = Button(self, text="Добавить", command=lambda: self.add(controller))
        addToDb.place(x=550, y=300)

    def add(self, controller):
        o = json.loads(open('db.json', 'r', encoding='UTF-8').read())
        o.append({'id': len(o) + 1, 'fio': self.fio.get(), 'phone': self.phone.get(), 'group': self.group.get(),
                  'napr': self.napravlenie.get()})
        with open('db.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(o))
        f.close()
        self.fio.set("")
        self.phone.set("")
        self.group.set("")
        self.napravlenie.set("")
        self.make_screen(o[-1]['id'])
        self.update_info()
        controller.show_frame("StartPage")

    def make_screen(self, filename):
        p = os.path.join(os.path.abspath(os.curdir) + "/Images/", str(filename) + '.png')
        self.controller.current_image.save(p, "PNG")

    def update_info(self):
        info = json.loads(open('db.json', 'r', encoding='UTF-8').read())
        knownNames = []
        for i in info:
            knownNames.append(i['fio'])
        imagePaths = list(paths.list_images('Images'))
        knownEncodings = []
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
