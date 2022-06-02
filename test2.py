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
data = pickle.loads(open('face_enc', "rb").read())


class Application:
    def __init__(self, output_path=os.path.abspath(os.curdir) + "/Images/"):
        self.vs = cv2.VideoCapture(0)
        self.output_path = output_path
        self.current_image = None

        self.root = tk.Tk()
        self.root.title("AuthId")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)

        self.panel = tk.Label(self.root)
        self.panel.pack(padx=10, pady=10)

        btn = tk.Button(self.root, text="Snapshot!", command=self.take_snapshot)
        btn.pack(fill="both", expand=True, padx=10, pady=10)
        self.video_loop()

    def video_loop(self):
        ok, frame = self.vs.read()
        if True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,
                                                 scaleFactor=1.1,
                                                 minNeighbors=5,
                                                 minSize=(60, 60),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)

            # convert the input frame from BGR to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # the facial embeddings for face in input
            encodings = face_recognition.face_encodings(rgb)
            names = []
            # loop over the facial embeddings incase
            # we have multiple embeddings for multiple fcaes
            for encoding in encodings:
                # Compare encodings with encodings in data["encodings"]
                # Matches contain array with boolean values and True for the embeddings it matches closely
                # and False for rest
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                # set name =inknown if no encoding matches
                name = "Unknown"
                # check to see if we have found a match
                if True in matches:
                    # Find positions at which we get True and store them
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        # Check the names at respective indexes we stored in matchedIdxs
                        name = data["names"][i]
                        # increase count for the name we got
                        counts[name] = counts.get(name, 0) + 1
                    # set name which has highest count
                    name = max(counts, key=counts.get)

                # update the list of names
                names.append(name)
                # loop over the recognized faces
                for ((x, y, w, h), name) in zip(faces, names):
                    # rescale the face coordinates
                    # draw the predicted face name on the image
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 255, 0), 2)

        if ok:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image.resize((400, 300)))  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.root.after(30, self.video_loop)

    def take_snapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.png".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.join(self.output_path, filename)
        self.current_image.save(p, "PNG")
        print("[INFO] saved {}".format(filename))

    def destructor(self):
        print("[INFO] closing...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()


print("[INFO] starting...")
pba = Application()
pba.root.mainloop()
