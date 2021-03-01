import time
import random
import cv2
import pandas as pd
import os
import numpy as np
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pyqrcode as qr
import png
import io
from tabulate import tabulate
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import re
from pandastable import Table, TableModel
import pyrebase


class SMART():
    def __init__(self,master):
        global value
        self.master=master
        firebaseConfig = {
            "apiKey": "AIzaSyA7lVv8P-dJveiVrro_4zJ6YiEDXnf1ID0",
            "authDomain": "fir-mart-152a3.firebaseapp.com",
            "databaseURL": "https://fir-mart-152a3-default-rtdb.firebaseio.com",
            "projectId": "fir-mart-152a3",
            "storageBucket": "fir-mart-152a3.appspot.com",
            "messagingSenderId": "935102395743",
            "appId": "1:935102395743:web:533aacdd7101f808a3f2ea",
            "measurementId": "G-ZPETCDBZCF"}
        firebase = pyrebase.initialize_app(firebaseConfig)
        self.customerID=''.join(random.choice('0123456789ABCDEF') for i in range(5))
        self.Storage = firebase.storage()
        self.name = 'techmart210@gmail.com'
        self.password = 'Password@1234'
        self.image = cv2.imread('3.jpg')
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        self.disp = ttk.Label(master, image=self.image)
        self.disp.pack()
        self.parentframe=Frame(master,relief=RAISED,height=350,width=300,bg='black')
        self.parentframe.place(relx=0.75,rely=0.50,anchor=CENTER)

        self.login=ttk.Label(self.parentframe,text='LOGIN',font=("times","27","bold","underline"),foreground='white',background='black')
        self.login.place(relx=0.5,rely=0.1,anchor=CENTER)
        global username
        global password
        global prod
        username = StringVar()
        password = StringVar()
        prod=StringVar()
        self.emaillabel = Label(self.parentframe, text='EMAIL ID:', font=("Times", "17", "bold"),foreground='white',background='black')
        self.emaillabel.place(relx=0.46, rely=0.30, anchor=CENTER)
        self.passwordLabel = Label(self.parentframe, text='PASSWORD:', font=("Times", "17", "bold"),foreground='white',background='black')
        self.passwordLabel.place(relx=0.5, rely=0.55, anchor=CENTER)

        self.email_idEntry = Entry(self.parentframe, textvariable=username)
        self.email_idEntry.place(relx=0.50, rely=0.40, anchor=CENTER)
        self.passwordEntry = Entry(self.parentframe, textvariable=password, show='*')
        self.passwordEntry.place(relx=0.5, rely=0.65, anchor=CENTER)

        self.submitButton = Button(self.parentframe, text='SUBMIT', command=self.loginform, font=("Times", "15", "bold"))
        self.submitButton.place(relx=0.50, rely=0.85, anchor=CENTER)
        self.img = cv2.imread('4.jpg')
        self.img = Image.fromarray(self.img)
        self.img = ImageTk.PhotoImage(self.img)
        self.disp1 = ttk.Label(master, image=self.img)

        self.nextBtn = Button(master, text="Next", command=lambda value=0: self.store(value), font=("Times", "15", "bold"))
        self.newFrame=ttk.Frame(master,height=500,width=300,relief='sunken')
        self.newFrame1=ttk.Frame(master,height=100,width=500,relief='raised')


        self.item_nope = Label(master, text="ITEM NOT ADDED", font=("Times", "15", "bold"))

        self.item =Label(master, text="ITEM ADDED", font=("Times", "15", "bold"))
        self.Show = Button(self.newFrame, text="SHOW CART", font=("Times", "15",),width=30)
        self.confirmBtn = Button(self.newFrame, text="PROCEED TO PAY", command=self.payment, font=("TIMES", "15"),width=30)
        self.backbutton = Button(self.newFrame, text="LOGOUT", command=master.destroy, font=("TIMES", "15"),width=38)
        self.add_itemButton = Button(self.newFrame, text='ADD ITEM',font=("times", "15"),width=30)
        self. exit_button = Button(self.newFrame, text="EXIT CART", command=self.exitingmart, font=("times", "15"),width=30)
        self.pro=Label(master,text="Sl.NO\tPRODUCT\tQUANTITY",font=("COURIER","18","bold","underline"))
        self.addM=Button(self.newFrame,text="ADD MANUALLY", command=self.manualadding, font=("TIMES", "15"),width=38)
        self.addtext=Entry(self.newFrame1, textvariable=prod)
        self.text=Label(self.newFrame1,text="TYPE THE SHELF CODE",font=("Times", "15","bold"))

        self.path = r'C:\Users\Siddarth\Desktop\projects\MART\customer_uploads'
        self.cam = cv2.VideoCapture(0)


    def password_check(self,password):
        while True:
            if (len(password) < 8):
                flag = False
                break
            elif not re.search("[a-z]", password):
                flag = False
                break
            elif not re.search("[A-Z]", password):
                flag = False
                break
            elif not re.search("[0-9]", password):
                flag = False
                break
            elif not re.search("[_@$]", password):
                flag = False
                break
            elif re.search("\s", password):
                flag = False
                break
            else:
                flag = True
                print("Valid Password")
                break

        if flag == False:
            print("Not a Valid Password")
        return flag





    def loginform(self):
        global email
        email = username.get()
        Password = username.get()
        print(email)

        # print(mail)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, email)):
            messagebox.showinfo(title='EMAIL VERIFICATION', message='WELCOME TO S-MART')
            self.disp.pack_forget()
            self.parentframe.place_forget()
            self.disp1.pack()
            self.newFrame.place(relx=0.18, rely=0.5, anchor=CENTER)
            self.nextBtn.place(relx=0.9, rely=0.9, anchor=CENTER)


        else:
            messagebox.showinfo(title='EMAIL VERIFICATION', message='INVALID PLEASE TRY AGAIN')

    def getimage(self):

        while True:
            _, img = self.cam.read()
            cv2.imshow("GETTING IMAGES", img)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('e'):
                cv2.imwrite('item.jpg', img)


                break

    def objectdetection(self):
        model = cv2.dnn.readNet('yolov3_testing_last.weights', 'yolov3_testing.cfg')
        classes = []
        with open('mart.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]
        self.getimage()

        while True:
            # _, img = cam.read()
            img = cv2.imread(os.path.join(self.path, "item.jpg"))

            img = cv2.resize(img, (800, 500))
            height, width, _ = img.shape
            ln = model.getLayerNames()
            ln = [ln[i[0] - 1] for i in model.getUnconnectedOutLayers()]

            # converting before feeding to yolo model
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)
            model.setInput(blob)
            # getting last layer output
            Layer_out = model.forward(ln)
            # prediction
            boxes = []
            confidences = []
            class_ids = []

            for output in Layer_out:
                for detection in output:
                    score = detection[5:]
                    class_id = np.argmax(score)
                    confidence = score[class_id]
                    if confidence > 0.8:
                        box = detection[0:4] * np.array([width, height, width, height])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)

            # method for bounding boxes
            # index method

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.7, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
            colors = np.random.uniform(0, 255, size=(len(boxes)))
            results = []
            # drawing
            if (len(indexes)) > 0:
                for i in indexes.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i], 2))
                    color = colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(img, label + "  " + confidence, (x, y - 5), font, 1, (0, 0, 0), 2)
                    results.append(label)
                # results.extend(results)
            # cv2.imshow("Object DETECTED", img)
            cv2.waitKey(10)
            count = 0
            q = []
            for i in range(len(results)):
                if results[i] in classes:
                    if results[i] == results[i - 1]:
                        count += 1
            q.append(count)
            # values = str(results)

            info = pd.DataFrame(list(zip(results, q)), columns=['PRODUCT', 'QUANTITY'])
            '''for i in range(len(results)):
                res = "{} item.csv".format(value)

                info.to_csv(res)

    '''

            return info, results,q

    global value

    def find_csv_filenames(self,path_to_dir=r"C:\Users\Siddarth\Desktop\projects\MART\customer_uploads", suffix=".csv"):
        filenames = os.listdir(path_to_dir)
        file = [filename for filename in filenames if filename.endswith(suffix)]
        if file != 'Mart List.csv':
            combined_csv = pd.concat([pd.read_csv(f) for f in file])
            combined_csv.drop('Unnamed: 0', axis=1, inplace=True)
            combined_csv.to_csv("product_info.csv", index=False)
        print("YOU WILL SOON GET YOUR BILL IN EMAIL")
        print("PLEASE WAIT AND CHECK OUT")

    def get_bill(self):

        df = pd.read_csv("product_info.csv")
        df1 = pd.read_csv(r"C:\Users\Siddarth\Desktop\projects\MART\customer_uploads\store\Mart List.csv")
        df3 = pd.merge(df, df1, how='inner')
        df3['NET AMOUNT'] = (df3.QUANTITY * df3.MRP)
        # print(tabulate(df, headers='keys', tablefmt='presto'))
        perproduct = list(df3['NET AMOUNT'])
        total = 0
        for ele in range(0, len(perproduct)):
            total = total + perproduct[ele]
        print(total)

        str_io = io.StringIO()
        df3.to_html(bold_rows=True, justify='center', border=5, buf=str_io, classes='table table-striped')
        html_str = str_io.getvalue()

        cart = Tk()
        cart.title("YOUR CART")

        cartdisplay = Frame(cart)
        cartdisplay.pack(fill='both', expand=True)
        pt = Table(cartdisplay, dataframe=df3)
        self.Show.configure(command=pt.show)
        self.Show.place(relx=0.3, rely=0.7,anchor=CENTER)

        return html_str, total



    def bill(self,html=None, amount=None, subject='YOUR BILL',
             from_mail='tech mart<techmart210@gmail.com>',
             to_email=None):
        # assert isinstance(to_email, list)
        # Html,Total=get_bill()
        image = """<img src = "https://i.postimg.cc/76tyD0hh/logo.jpg	" height = "50%" width = "100%" >"""
        res = f"""<!DOCTYPE html>
                <html>
                <head>

                <body>
                <center>
                {image}
                <h3>{html}</h3>
                <h3>Total={amount}</h3></center>
                <h4>PLEASE SEND YOUR FEEBACK THROUGH THIS LINK</h4>
                <a href="https://forms.gle/8xNyrRnA1ETwaEsU9">Visit S-MART agian!</a>
                </head>
                </body>
                </html>"""

        msg = MIMEMultipart('alternative')
        msg['From'] = from_mail
        msg['To'] = to_email
        msg['Subject'] = subject
        # html_part1=MIMEText(html,'html')
        # html_part=MIMEText(html,'html')
        # msg.attach(res)
        text_part = MIMEText(res, 'html')
        msg.attach(text_part)

        msg_str = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.name,self.password)
        server.sendmail(from_mail, to_email, msg_str)
        print("YOUR BILL HAS BEEN SENT TO YOUR MAIL!")
        server.quit()

    def exitingmart(self):
        self.add_itemButton.place_forget()
        self.exit_button.place_forget()

        self.cam.release()
        cv2.destroyAllWindows()
        self.find_csv_filenames()

        self.confirmBtn.place(relx=0.35, anchor=CENTER, rely=0.50)

        self.backbutton.place(relx=0.20, anchor=CENTER, rely=0.60)




    def payment(self):
        self.add_itemButton.place_forget()
        self.exit_button.place_forget()
        self.addM.place_forget()

        Html, Total = self.get_bill()
        QR = Toplevel(self.master)
        QR.title("PAYTM QR")
        QR.geometry('700x500')
        s = 'https://paytm.com/paytmwallet'
        url = qr.create(s)
        url.png('PAYTM.png', scale=10)
        im = cv2.imread('PAYTM.png')
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        code = Label(QR, image=im, width=500, height=500)
        code.place(relx=0.5, rely=0.5, anchor=CENTER)
        bye = Button(QR, text="SEND RECIPT", command=self.bill(Html, Total, to_email=email), font=("times", "15"))
        bye.place(relx=0.50, rely=0.94, anchor=CENTER)
        filename="product_info.csv"
        cloud_file_name="cart 1/{0}-product.csv".format(self.customerID)
        self.Storage.child(cloud_file_name).put(filename)

        print("csv removed")
        confirmLabel = Label(Mainwindow, text="PLEASE CONFIRM YOUR PAYEMENT", font=("Times", "16", "bold"))
        confirmLabel.place(relx=0.4, rely=0.7, anchor=CENTER)
        confirmBtn = Button(Mainwindow, text="CONFIRM", commmand=QR)
        confirmBtn.place(relx=0.6, rely=0., anchor=SE)

    value = 1

    def manualadding(self):

        cshelf = prod.get()
        q = "1"

        d = {"B901": 'cinthol',
             "39F0": 'dettol',
             "578D": 'pears',
             "B61E": 'oreo',
             "C653": 'bourbon',
             "1A9B": '5star',
             "3DBC": 'galaxy',
             "7BD8": 'kitkat',
             "8F97": 'lays',
             "95D2": 'banana'}
        if cshelf in d.keys():
            item = d[cshelf]
            print("PRODUCTED ADDED=", item)

            cart={"PRODUCT":item,"QUANTITY":q}
            df=pd.DataFrame([cart])
            print(df)
            df.to_csv("{}.csv".format(value))
            self.item.configure(text="{0}\t{1} \t   {2}".format(value, item, q))
            self.item.place(relx=0.6, rely=0.2, anchor=CENTER)


        else:
            messagebox.showinfo(title='Item', message='ITEM NOT ADDED')

    def store(self,value):
        self.nextBtn.place_forget()

        self.pro.place(relx=0.6,rely=0.1,anchor=CENTER)

        df, cart,quantity = self.objectdetection()


        if df.empty:
            self.newFrame1.place(relx=0.7,rely=0.65,anchor=CENTER)
            self.addtext.place(relx=0.5, rely=0.6, anchor=CENTER)
            self.text.place(relx=0.5, rely=0.35, anchor=CENTER)

            self.addM.place(relx=0.4,rely=0.45,anchor=CENTER)



           # self.item_nope.place(relx=0.6, rely=0.75, anchor=CENTER)


        else:
            #self.item_nope.place_forget()
            self.newFrame1.place_forget()
            self.addM.place_forget()
            self.item.configure(text="{0}\t{1} \t   {2}".format(value,cart[0],quantity[0]))
            self.item.place(relx=0.6, rely=0.2, anchor=CENTER)
            df.to_csv("{}.csv".format(value))


        print(value)


        self.add_itemButton.configure(command=lambda value=value+1: self.store(value),)
        self.add_itemButton.place(relx=0.4, rely=0.20, anchor=CENTER)
        global exit_button

        self.exit_button.place(relx=0.4, anchor=CENTER, rely=0.35)




def main():
    root=Tk()
    root.title("S-MART")
    root.geometry("800x500")


    obj=SMART(root)
    root.mainloop()

if __name__ == '__main__':main()
