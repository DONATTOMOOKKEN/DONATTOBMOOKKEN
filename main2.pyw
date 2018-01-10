from Tkinter import*
import Tkinter as tk;
import easygui;
import easygui as eg;
import threading;
from PIL import Image
from PIL import ImageTk
import time;
import numpy as np
import pandas as pd;
from sklearn import svm
import optunity
import sklearn.svm;
from sklearn.feature_selection import SelectKBest;
from sklearn.feature_selection import chi2;
from sklearn.model_selection import GridSearchCV;
import shutil;
import string;
import time;
import tkFont
import sqlite3;
import os;
import getpass;
import tkMessageBox;


photoImg1, photoImg2,photoImg3,photoImg4, photoImg5 = (0, 0, 0, 0, 0);
path=None;
data=[];
num=[];
a=0;
flag=1;
save_flag=0;


root=Tk()
width=900;
height=600;
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.resizable(0,0);
root.title("AGRO CROP");



class Database(object):
        record=None;
        def __init__(self, rw, a):
                self.conn = sqlite3.connect('database1.db');
                self.db = self.conn.cursor();
                self.a=a;
                if(rw=="w"):
                        self.write();
                elif(rw=="r"):
                        self.read();
                elif(rw=="d"):
                        self.delete();

                self.conn.close();

        def delete(self):
                var=str(self.a[0])
                print var;
                
                self.db.execute('delete from data where name="' + var + '";');
                self.conn.commit();


        def write(self):
                print self.a[0];
                print self.a[0][1];
                print self.a;
                var="'"+str(self.a[0])+"',"+str(self.a[1])+","+str(self.a[2])+","+str(self.a[3])+",'"+str(self.a[4:])+"'";
                print var;
                self.db.execute('INSERT INTO data(name, c, gamma, score, list) values(' + var + ');');
                self.conn.commit();

        def read(self):
                print "READ-------", self.a;
                var = "select c, gamma, score, list from data where name='"+str(self.a[0]) +"';";
                print "VARIABLES====", var;
                self.db.execute(var);
                Database.record = self.db.fetchall();
                
                RegressionAnalysis.c=Database.record[0][0];
                RegressionAnalysis.gamma=Database.record[0][1];
                RegressionAnalysis.score=Database.record[0][2];
                record=Database.record[0][3];
                record=str(record);
                print record;
                record=string.split(record, ',');
                print record;
                record[0]=record[0][2:];
                no=len(record[len(record)-1]);
                record[len(record)-1]=record[len(record)-1][0:(no-2)]
                ProgressingWindow.records=[0]*len(record);

                
                for i in range(len(record)):
                        ProgressingWindow.records[i]=int(record[i]);
                
                #Database.record=Database.record[0];
                print "ProgressingWindow.records in database= :  ", ProgressingWindow.records;

class ParallelRunning(threading.Thread):
        completed=0;
        def __init__(self):
                threading.Thread.__init__(self, name="Thread-1");

        def run(self):
                global a, num, save_flag;
                global data;
                ob=RegressionAnalysis();

                print "Prallel Running Has Initialized:  \n";
                print ParallelRunning.completed;
                
                a=[];
                num=[];
                print "Value before num:  ", num,"\n";
                for i in range(len(data)):
                        num.append(int(data[i][1:]));
                num.sort();
                print "Value after num:  ", num, "\n";
                ProgressingWindow.records.sort();

                print num,"\n";
                print ProgressingWindow.records,"\n";

                for no in num:
                        a.append(RegressionAnalysis.INTERESTING_FEATURES[no]);

                print "value at a-8**********=", a;
                #ParallelRunning.completed=0;
                RegressionAnalysis.features_values = zip(*map(lambda f: RegressionAnalysis.df[f].values, a));
                RegressionAnalysis.features_values=np.array(RegressionAnalysis.features_values);
                RegressionAnalysis.target_value=np.array(RegressionAnalysis.target_value);
                print "prediction-shape:   features-:", RegressionAnalysis.features_values.shape;
                print "prediction-shape:   target-: ", RegressionAnalysis.target_value.shape;
                print "value of ProgressingWindow.records:  ", ProgressingWindow.records;
                print "type of ProgressingWindow.records:  ", type(ProgressingWindow.records);

                if ParallelRunning.completed==1 and num!=ProgressingWindow.records:
                        ParallelRunning.completed=0;
                
                if num!=ProgressingWindow.records:

                        save_flag=1;
                        print "value of num----------:", num;
                        

                        gamma_range=[1e-11,1e-12,1e-13,1e-14,1e-15,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1, 1e1, 1e2, 1e3, 1e4,1e5];
                        gamma_range=np.array(gamma_range);
                        C_range=[1e-1, 1e-2, 1e-3, 1e-4, 1, 10, 100, 1000, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9];
                        C_range=np.array(C_range);
                        #C_range = np.arange(1, 10000, 50); #2. ** np.array([-5,-3,-1, 1, 3, 5, 7, ])
                        #gamma_range = np.arange(1e-15, 1e5, 200); #2. ** np.array([ -7, -5, -3, -1, 1, 3, 5])
                        param_grid = {'gamma':gamma_range, 'C':C_range};


                        print "shapf=", RegressionAnalysis.features_values.shape;
                        print "shapt=", RegressionAnalysis.target_value.shape;
                
                        InputData.clf = GridSearchCV(svm.SVR(), param_grid=param_grid, n_jobs=4, cv=5)
                        #InputData.clf=svm.SVR( degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)
                
                        InputData.clf.fit(RegressionAnalysis.features_values, RegressionAnalysis.target_value)
                


                        print "___________>", InputData.clf.best_params_, "\n";
                        print "value of c: ,",InputData.clf.best_params_['C'], "\n";
                        print "Accuaray: ", InputData.clf.best_score_;
                        RegressionAnalysis.c=InputData.clf.best_params_['C'];
                        RegressionAnalysis.gamma=InputData.clf.best_params_['gamma']
                        RegressionAnalysis.score=InputData.clf.best_score_;
                
                        print InputData.clf;
                        #time.sleep(20);
                else:
                        save_flag=0;
                        print "Entered saved else";
                        InputData.clf=svm.SVR( degree=3, C=RegressionAnalysis.c, gamma=RegressionAnalysis.gamma, coef0=0.0, tol=0.001, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)
                        InputData.clf.fit(RegressionAnalysis.features_values, RegressionAnalysis.target_value);
                        time.sleep(20);
                        

                #print "InputData.clf in regression anlaysis out of else:  ", InputData.clf;
                print "completed--------------";
                ParallelRunning.completed=1;
                
                #self.can1.itemconfig(TEXT, text="COMPLETED   "+str(ParallelRunning.completed))
                print ParallelRunning.completed;

                

class RegressionAnalysis(object):
        target, features, features_values, target_value, INTERESTING_FEATURES, df, c, gamma, score=(0,0,0,0,0,0, 0, 0, 0);
        def __init__(self):
                pass;
                #print RegressionAnalysis.target, RegressionAnalysis.features, RegressionAnalysis.features_values, RegressionAnalysis.target_value;
        def __str__(self):
                print "initialized";

        def featureset(self, file_path):
                
                self.file_path=file_path;
                RegressionAnalysis.df = pd.read_csv(self.file_path, header=0);
                RegressionAnalysis.INTERESTING_FEATURES = list(RegressionAnalysis.df);

                RegressionAnalysis.target=RegressionAnalysis.INTERESTING_FEATURES[0];    #col_0 target
                RegressionAnalysis.target_value = list(RegressionAnalysis.df[RegressionAnalysis.target].values);
                
                del(RegressionAnalysis.INTERESTING_FEATURES[0]);
                RegressionAnalysis.features = RegressionAnalysis.INTERESTING_FEATURES;
                
                RegressionAnalysis.features_values = zip(*map(lambda f: RegressionAnalysis.df[f].values, RegressionAnalysis.INTERESTING_FEATURES))
  
                return RegressionAnalysis.features_values, RegressionAnalysis.target_value, RegressionAnalysis.target, RegressionAnalysis.features;

        def prediction(self):
                RegressionAnalysis.features_values=np.array(RegressionAnalysis.features_values);
                RegressionAnalysis.target_value=np.array(RegressionAnalysis.target_value);


                return sklearn.feature_selection.mutual_info_regression(RegressionAnalysis.features_values, RegressionAnalysis.target_value, discrete_features='auto', n_neighbors=3, copy=True, random_state=None)

        def regression(self, pred, clf):
                #clf=svm.SVR(kernel='rbf', degree=3, gamma='auto', coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, cache_size=200, verbose=False, max_iter=-1)
                #clf.fit(RegressionAnalysis.features_values, RegressionAnalysis.target_value);
                pred = np.array(pred).reshape((1, -1))
                return clf.predict(pred);
        

#########################################  MAIN WINDOW  ############################################################
class Window(object):
        def __init__(self, title, size, previouswin, nextwin):
                global photoImg1, photoImg5, photoImg2;
                self.main=Frame(root, width=900*4, height=600);
                self.can1=Canvas(self.main,width=900, height=600, bg="white", highlightthickness=0, bd=0,relief='ridge');
        
                self.title=Canvas(self.can1, width=900, height=100, bg="black", highlightthickness=0, bd=0,relief='ridge');
                

                """img5 = Image.open("logo.gif")
                img5 = img5.resize((300,200), Image.ANTIALIAS)
                photoImg5 = ImageTk.PhotoImage(img5)
                image5 = self.title.create_image(100, 70, image=photoImg5)
                """



                self.mainlabel=Label(self.title, text="AGRO CROP", fg="#09E3E1", bg="black", font=('helvica', 18,tkFont.BOLD));
                self.mainlabel.place(x=220, y= 70);

                self.title.tag_bind("button_text", "<Enter>", lambda event: but2.mouse_in(event, self.title, '#1b3a6d', 'white'))
                self.title.tag_bind("button_text", "<Leave>", lambda event: but2.mouse_out(event, self.title, "white", '#1b3a6d'))
                self.title.place(x=0, y=0);
        

                self.can1.place(x=0, y=0);
                self.main.place(x=0, y=0);


                img5 = Image.open("back.gif")
                img5 = img5.resize((900,600), Image.ANTIALIAS)
                photoImg1 = ImageTk.PhotoImage(img5)
                image1 = self.can1.create_image(450+(900*0), 300, image=photoImg1)



                self.can1.create_text(50, 130, anchor=NW, text=title, justify=LEFT, font=('helvica', 19,tkFont.BOLD), tag="title_text", fill="#354d7c");


                sub_window=self.can1.create_rectangle(50, 180, 50+800, 180+size, fill="#1b3a6d", stipple="gray25", width=0 );


                self.mainbottomframe=Canvas(self.main, width=900, height=60, bg="black", highlightthickness=0, bd=0,relief='ridge');
        
                but3=MyButton("NEXT");
                but3.place(750, 10, 120, 40);
                self.button=but3.showdef(self.mainbottomframe, "nofill","Arial 12 normal", "#222323", "#222323");
        
                self.mainbottomframe.tag_bind("button_text", '<Button-1>', lambda event: ControlWindow(nextwin))
                self.mainbottomframe.place(x=0, y=540);


                self.mainbottomframe.bind("<Enter>", lambda event: but3.mouse_in(event, self.mainbottomframe, '#891111', '#891111'))
                self.mainbottomframe.bind("<Leave>", lambda event: but3.mouse_out(event, self.mainbottomframe, "#222323", "#222323"))

                back = MyButton("<");
                back.place(50, 30, 0, 0);
                back.create_circle(self.mainbottomframe, 20, "Arial 22 bold", "#222323", "no_fill", outline="#222323", fill="black", width=3)
                self.mainbottomframe.tag_bind("circle_button_text", "<Enter>", lambda event: back.circle_mouse_in(event, self.mainbottomframe, '#891111'))
                self.mainbottomframe.tag_bind("circle_button_text", "<Leave>", lambda event: back.circle_mouse_out(event, self.mainbottomframe, "#222323"))
                self.mainbottomframe.tag_bind("circle_button_text", '<Button-1>', lambda event: ControlWindow(previouswin))

        def __str__(self):
                return self.can1, self.mainbottomframe;

class MyUtils():
	def showRoundRect(self, can, x, y, width, height, rad, color, flag):
                if flag=="fill":
                        st=tk.PIESLICE;
                else:
                        st=tk.ARC;
		can.create_arc(x, y+rad*2, x+rad*2,y, start=90, extent=90,  style=st, fill=color,outline=color, width=3, tag="button");
		can.create_line(x+rad, y, x+width-rad,y, fill=color, width=3, tag="buttonl");
		can.create_arc(x+width-rad*2, y+rad*2, x+width, y, start=0, extent=90, style=st, fill=color,outline=color, width=3, tag="button");
		can.create_line(x+width, y+rad, x+width, y+height-rad, fill=color, width=3, tag="buttonl");
		can.create_arc(x+width-rad*2, y+height, x+width, y+height-rad*2, start=270, extent=90, style=st, fill=color,outline=color, width=3, tag="button");
		can.create_line(x+width-rad, y+height, x+rad, y+height, fill=color, width=3, tag="buttonl");
		can.create_arc(x, y+height, x+rad*2, y+height-rad*2, start=180, extent=90, style=st, fill=color,outline=color, width=3, tag="button");
		can.create_line(x, y+height-rad, x, y+rad, fill=color, width=3, tag="buttonl");


                
	def clearRect(self, can, x1, y1, x2, y2, r, color):

		can.create_rectangle(x1, y1+(r), x2,y2-r, fill = color, tag="button_body")
                can.create_rectangle(x1+r, y1, x2-r, y2, fill=color, width=0, tag="button_body")		



class MyButton():
	def __init__(self, caption):
		self.x=0;	
		self.y=0;
		self.width=100;
		self.height=50;
		self.caption=caption;
		self.flag=None;
	
	def place(self, x, y, w, h):
		self.x = x;
		self.y = y;
		self.width=w;
		self.height=h;

	def showdef(self, can, flag, ft, ftcolor, linecolor):
                self.flag=flag;
                if(flag=="fill"):
                        MyUtils().clearRect(can, self.x, self.y, self.x+self.width, self.y+self.height, 10, linecolor);
                MyUtils().showRoundRect(can, self.x, self.y, self.width, self.height, 10, linecolor, flag);
    		can.create_text(self.x+self.width/2, self.y+self.height/2, fill=ftcolor, font=ft, text = self.caption, tag="button_text");
        def mouse_in(self, event, can, color, bdcolor):
            #but1.showdef(self.mainbottomframe, "nofill","Arial 12 normal", "white", "white");
            can.itemconfig("buttonl", fill=bdcolor)
            can.itemconfig("button", outline=bdcolor)
            can.itemconfig("button_text", fill=color)
            if self.flag=="fill":
                can.itemconfig("button", outline=bdcolor)
                can.itemconfig("button", fill=bdcolor)
                can.itemconfig("button_body", fill=bdcolor)
                
        
        def mouse_out(self, event, can, color, bdcolor):
            #but1.showdef(self.mainbottomframe, "nofill","Arial 12 normal", "#222323", "#222323");
                    
            can.itemconfig("buttonl", fill=bdcolor)
            can.itemconfig("button", outline=bdcolor)
            can.itemconfig("button_text", fill=color)
            if self.flag=="fill":
                can.itemconfig("button", outline=bdcolor)
                can.itemconfig("button", fill=bdcolor)
                can.itemconfig("button_body", fill=bdcolor)

        def circle_mouse_in(self, event, can, color):
                can.itemconfig("circle_button", outline=color)
                can.itemconfig("circle_button_text", fill=color)
                if self.flag=="fill":
                        can.itemconfig("circle_button", fill=color)
                
        def circle_mouse_out(self, event, can, color):
                can.itemconfig("circle_button", outline=color)
                can.itemconfig("circle_button_text", fill=color)
                if self.flag=="fill":
                        can.itemconfig("circle_button", fill=color)

        def create_circle(self, can, r, ft, ftcolor, flag, **kwargs):
            self.flag=flag;
            can.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, tag="circle_button", **kwargs)
            if self.caption != "":
                    can.create_text(self.x, self.y, fill=ftcolor, font=ft, text = self.caption, tag="circle_button_text");


class MainWindow():
    def __init__(self):
        self.MAIN_WINDOW();
    
    def printdata(self, event):
        self.mainbottomframe.delete("all");
        self.can1.delete("all");
        self.frm1.delete("all");
        self.can1.after_cancel(self.iteration)
        self.main.place_forget();
        ControlWindow(2)
    
    def next_image(self, flag, pix, add, silence, count):

        if flag==1:
            flag=0;
            self.can1.move(self.can1_win, 0, 0)
            self.can1.update()
        if(pix%900==0 and add==-30)or (pix==900*4 and add==100):
            silence=1;
            count= count + 1;
            if count==100:
                silence=0;
                count=0;
            else:
                pass;
        else:
            pass;
    
        if silence==0:
            if((pix == 900 or add==100) and pix != (900*4)):
                self.can1.move(self.can1_win, 100, 0)
                self.can1.update()
                add=100;

            else:
                self.can1.move(self.can1_win, -30, 0)
                self.can1.update()
                add=-30

            pix=pix + add;
        
        self.can1.after(5);
        
        self.iteration = self.can1.after_idle(self.next_image, flag, pix, add, silence, count)

   
    def MAIN_WINDOW(self):
        global photoImg1, photoImg2,photoImg3,photoImg4, photoImg5;
        self.main=Frame(root, width=900*4, height=600);
        self.can1=Canvas(self.main,width=900, height=600, bg="blue");
        self.frm1=Canvas(self.can1, width=900*4, height=600,  bg="red");

        img = Image.open("one.jpg")
        img = img.resize((900,600), Image.ANTIALIAS)
        photoImg1 = ImageTk.PhotoImage(img)
        image1 = self.frm1.create_image(450+(900*0), 300, image=photoImg1)

        img = Image.open("two.jpg")
        img = img.resize((900,600), Image.ANTIALIAS)
        photoImg2 = ImageTk.PhotoImage(img)
        image2 = self.frm1.create_image(450+(900*1), 300, image=photoImg2)

        img = Image.open("three.jpg")
        img = img.resize((900,600), Image.ANTIALIAS)
        photoImg3 = ImageTk.PhotoImage(img)
        image3 = self.frm1.create_image(450+(900*2), 300, image=photoImg3)

        img = Image.open("four.jpg")
        img = img.resize((900,600), Image.ANTIALIAS)
        photoImg4 = ImageTk.PhotoImage(img)
        image4 = self.frm1.create_image(450+(900*3), 300, image=photoImg4)


        self.can1_win=self.can1.create_window(900*2,300,window=self.frm1, tag="one");
        self.can1.place(x=0, y=0);

        self.next_image(1,900*4, -30, 0, 0);

        self.mainbottomframe=Canvas(self.main, width=900, height=60, bg="black", highlightthickness=0, bd=0,relief='ridge');

        """img5 = Image.open("logo.gif")
        img5 = img5.resize((200,130), Image.ANTIALIAS)
        photoImg5 = ImageTk.PhotoImage(img5)
        image5 = self.mainbottomframe.create_image(80, 40, image=photoImg5)
        """

        self.mainlabel=Label(self.mainbottomframe, text="AGRO CROP", fg="#09E3E1", bg="black", font=('helvica', 18,tkFont.BOLD));
        self.mainlabel.place(x=160, y= 25);
        but1=MyButton("CONTINUE");
        but1.place(750, 10, 120, 40);
        self.button=but1.showdef(self.mainbottomframe, "nofill","Arial 12 normal", "#222323", "#222323");

        self.mainbottomframe.tag_bind("button_text", '<Button-1>', self.printdata)
        self.mainbottomframe.place(x=0, y=540);


        self.mainbottomframe.bind("<Enter>", lambda event: but1.mouse_in(event, self.mainbottomframe, '#891111', '#891111'))
        self.mainbottomframe.bind("<Leave>", lambda event: but1.mouse_out(event, self.mainbottomframe, "#222323", "#222323"))
        self.main.place(x=0, y=0);


############################################  ABOUT  ######################################################
class AboutWindow(Window):
    def __init__(self):
        super(AboutWindow, self).__init__("ABOUT", 300, 2, 3)
        self.can1, self.mainbottomframe=super(AboutWindow, self).__str__()
        self.ABOUT_WINDOW()
        #Window.__init__(self, "ABOUT", 300, 2, 3);

    def ABOUT_WINDOW(self):
        self.mainbottomframe.delete("circle_button");
        self.mainbottomframe.delete("circle_button_text");
        text="""
Agro crop  will  help  you  to  predict  the  yield  of your  culitvaion. It  is a perfect
data-scientist. We can help all in your path. Only need to do is enter the data. Make
your agriculture as a business.

HOW TO USE & ABOUT

   Upload the training data. Analyze the data. Enter the values for having prediction.
This is application is build in Python. Using machine-learning we are predicting with
a 100% accuracy. This is compeletly a free software."""
        self.can1.create_text(60, 200, anchor=NW, fill="#354d7c", font=('Arial',15,tkFont.BOLD), text = text);
        
        
class UploadWindow(Window):
    def __init__(self):
        super(UploadWindow, self).__init__("UPLOAD", 300, 2, 3)
        self.can1, self.mainbottomframe=super(UploadWindow, self).__str__()
        file_path=None;
        self.state="r1";

        self.path=None;
        self.username = getpass.getuser()
        self.UPLOAD_WINDOW()
        
    def rotate_load(self, can, start, extent, count, time):
            self.count=count;
            self.time=time;
            if start>=361:
                    start=0;
            start = start + 5;
            can.itemconfig(self.load, start=++start, extent=extent);
            can.after(5);
            
            self.count=self.count+1;
            if(self.time==2 and self.count==(self.time*1000)/5):
                can.after_cancel(self.iteration)
                can.delete(self.load);
            
            else:
                    self.iteration=can.after_idle(self.rotate_load, can, start, extent, self.count, self.time)

    def radio_button_hover(self, event, tag, tag1):
        if tag!=self.state:
                color="#2958a3";
                self.can1.itemconfig(tag, fill=color);
                self.can1.itemconfig(tag1, fill=color);

    def radio_button_out(self, event, tag, tag1):
            if tag!=self.state:
                    self.can1.itemconfig(tag, fill="#1b3a6d");
                    self.can1.itemconfig(tag1, fill="#1b3a6d");
                    

    def radio_button_click(self, event, tag, tag1):
            self.can1.itemconfig("r1i", fill="#1b3a6d");
            self.can1.itemconfig("r2i", fill="#1b3a6d");
            self.can1.itemconfig("r1", fill="#1b3a6d");
            self.can1.itemconfig("r2", fill="#1b3a6d");
            self.state=tag;
            self.can1.itemconfig(tag1, fill="white");

            print tag;

            if tag=="r2":
                    print "Entered r2";


                        
                    self.path="C:\Users\\" + self.username + "\AppData\Roaming\predizon\dataset\\";
                    print self.path;

            else:
                    self.path=None;
                    print self.path;
            
            
    def radio_button(self, x, y, text, tag):
            width=15;
            tag1=tag+"i";
            self.can1.create_rectangle(x, y, x+width, y+width, fill="#1b3a6d", outline="#1b3a6d", tag=tag);
            self.can1.create_text(x+20+20, y+10, anchor=W, text=text, fill="#1b3a6d");
            x=x+2;
            y=y+2;
            width=11;
            self.can1.create_rectangle(x, y, x+width, y+width, fill="#1b3a6d", outline="#1b3a6d", tag=tag1);

            self.can1.tag_bind(tag, "<Enter>", lambda event: self.radio_button_hover(event, tag, tag1));
            self.can1.tag_bind(tag, "<Leave>", lambda event: self.radio_button_out(event, tag, tag1));
            self.can1.tag_bind(tag, "<Button-1>", lambda event: self.radio_button_click(event, tag, tag1));
            
            print tag;
            self.can1.tag_bind(tag1, "<Enter>", lambda event: self.radio_button_hover(event, tag, tag1));
            self.can1.tag_bind(tag1, "<Leave>", lambda event: self.radio_button_out(event, tag, tag1));
            self.can1.tag_bind(tag1, "<Button-1>", lambda event: self.radio_button_click(event, tag, tag1));

    def varify(self):
            

        msg = "Are you sure to delete the file " + str(self.delete_path[self.delete_length-1])+ " ?"
        title = "Please Confirm"
        print "*******************************varify**********************************"
        print "self.text, str(self.delete_path[self.delete_length-1])= ", self.text, "***", str(self.delete_path[self.delete_length-1]);
                
        
        if tkMessageBox.askyesno(title, msg):      
                            try:
                                    os.remove(str(self.delete_file_path));
                                    print "remove\n";
                                    self.delete_length=len(self.delete_path);
                                    print "length\n"
                                    Database("d", [str(self.delete_path[self.delete_length-1])]);
                                    print "database\n";


                                    tkMessageBox.showinfo("Deleted", "Successfully deleted " + str(self.delete_path[self.delete_length-1]) + " file...")
                    
                            except OSError:
                                    tkMessageBox.showinfo("Error", "Error has occured")
                    
                                    print "cannot delte the file";

        else:  # user chose Cancel
                        print "ccbox passed clicked cancel button\n";


    def delete(self, event):
            self.delete_path="C:\Users\\" + self.username + "\AppData\Roaming\predizon\dataset\\";
            self.delete_file_path=easygui.fileopenbox(default=self.delete_path, title="Delete File", filetypes=['*.csv']);
            print "delete path:  ", self.delete_file_path;
            if self.delete_file_path!= None:
                    self.delete_path=str(self.delete_file_path);
                    self.delete_path=string.split(self.delete_file_path, "\\");
                    self.delete_length=len(self.delete_path);
                    if self.text==str(self.delete_path[self.delete_length-1]) and self.file_path!= None:
                            print "Entered to equal\n";
                            tkMessageBox.showinfo("Warning!", self.text + " already in use. Cannot delete file.");
                    elif self.delete_file_path!= None:
                            print "Entered not None";
                            self.varify();
                            print "return to main\n";
      
    def Browse(self, event, can, x, y, r, color):
            global path;
            print "before fileopenbox:  ", self.path, "\n";
            self.file_path=easygui.fileopenbox(default=self.path, title="Open File", filetypes=['*.csv']);
            print "Browse path", self.file_path, "\n";
            path=self.file_path;
            files=os.listdir("C:\\Users\\" + self.username + "\\AppData\\Roaming\\predizon\\dataset");
 
            UploadWindow.file_path=str(path);
            print "path:  ", type(UploadWindow.file_path);


            if self.file_path!=None:
                    
                    UploadWindow.file_path=string.split(UploadWindow.file_path, "\\");
                    no=len(UploadWindow.file_path);
                    if self.state=="r2":
                        ParallelRunning.completed=1;
                        print "upload True\n";
                        self.text=str(UploadWindow.file_path[no-1]);
                        print "self.text=  ", self.text;
                    else:
                        ParallelRunning.completed=0;
                        print "Upload False\n";
                        self.text=str(path);
                    print "upload1 ",UploadWindow.file_path[:no-1];
                    print "upload2 ", string.split("C:\\Users\\" + self.username + "\\AppData\\Roaming\\predizon\\dataset", "\\");
                    root.title(self.text);
                    no=len(UploadWindow.file_path);
                    print "Browse window self.file_path", UploadWindow.file_path[:no-1];


                    can.itemconfig("button_text", text=self.text);
                    self.load=can.create_arc(x, y+20, x+r, y+r+20, start=0, extent=310,  style=tk.ARC, outline=color, width=2);
                    self.rotate_load(can, 0, 290, 0, 2);
            if self.file_path==None:
                    can.itemconfig("button_text", text="No file is selected...");
		
            
    def NEXT_WINDOW(self, event):
            global flag;
            flag=1;
            if self.state=="r2":
                 Database("r",[self.text]);
                 
            if self.file_path!= None and self.count==(self.time*1000)/5:
                    ControlWindow(4)


    def UPLOAD_WINDOW(self):
        self.text="";
        text_box=MyButton("Enter a file...");
        text_box.place(50+20, 180+70, 650, 40);
        self.button=text_box.showdef(self.can1, "fill","Arial 12 normal", "#1b3a6d", "white");
        browse_button=self.can1.create_rectangle(50+20+650+10, 180+50+20, 840, 180+50+40+20, fill="#2d8730",  width=0 );
        browse_text=self.can1.create_text(50+20+650+10+110/2, 20+180+50+40/2, fill="white", font=('Arial',12,tkFont.BOLD), text = "Browse");
        self.can1.tag_bind(browse_text, '<Enter>', lambda event: self.can1.itemconfig(browse_button, fill="#3CA340"));
        self.can1.tag_bind(browse_text, '<Leave>', lambda event: self.can1.itemconfig(browse_button, fill="#2d8730"));
        self.can1.tag_bind(browse_text, '<Button-1>', lambda event: self.Browse(event, self.can1, 50+20+650+10+8, 180+50+15, 10, "white"));

        delete_button=self.can1.create_rectangle(50+20+650+10, 180+50+20+110, 840, 180+50+40+20+110, fill="#2d8730",  width=0 );
        delete_text=self.can1.create_text(50+20+650+10+110/2, 110+20+180+50+40/2, fill="white", font=('Arial',12,tkFont.BOLD), text = "Delete");
        self.can1.tag_bind(delete_text, '<Enter>', lambda event: self.can1.itemconfig(delete_button, fill="#3CA340"));
        self.can1.tag_bind(delete_text, '<Leave>', lambda event: self.can1.itemconfig(delete_button, fill="#2d8730"));
        self.can1.tag_bind(delete_text, '<Button-1>', lambda event: self.delete(event));

        self.radio_button(100, 200, "Attach New File", "r1");
        self.radio_button(300, 200, "Attach Saved File", "r2");
        self.can1.itemconfig("r1i", fill="white");
        
        self.mainbottomframe.tag_unbind("button_text", '<Button-1>')
        self.mainbottomframe.tag_bind("button_text", '<Button-1>', lambda event: self.NEXT_WINDOW(event))

class ProgressingWindow(Window):
    records=[];
    def __init__(self):
        global data;
        del data[:]
        super(ProgressingWindow, self).__init__("FILTER DATA", 300, 3, 5)
        self.can1, self.mainbottomframe=super(ProgressingWindow, self).__str__()
        
        self.PROGRESSING_WINDOW()
        #Window.__init__(self, "ABOUT", 300, 2, 3);

    def checkbox_hover(self, event, tag):
            #print "trigered in"
            self.can1.itemconfig(tag, fill="white");
    def checkbox_out(self, event, tag):

            self.can1.itemconfig(tag, fill="#354d7c");

    def click(self, event, tag_check, tag, data):
            if tag not in data:
                    self.can1.itemconfig(tag_check, fill="#354d7c");
                    self.can1.itemconfig(tag_check, outline="#354d7c");
                    data.append(tag);
            else:
                    index=data.index(tag);
                    del data[index];
                    self.can1.itemconfig(tag_check, fill="#E8E8E8");
                    self.can1.itemconfig(tag_check, outline="#E8E8E8");

    def bind_checkbox(self, y, color, outline, tag,  tag_check, perc, text, data):
                r=6;
                x=75;
                self.can1.create_oval(x-r, y-r, x+r, y+r, fill=color, width=2, outline=outline, tag=tag_check)
                self.can1.create_text(x+r+15, y, anchor=W, font=('helvica', 15,tkFont.BOLD), fill="#354d7c", text=text, tag=tag);
                self.can1.create_text(50+400+30, y, anchor=W, font=('helvica', 15,tkFont.BOLD), fill="#354d7c", text=perc, tag=tag)
                self.can1.tag_bind(tag, "<Enter>", lambda event: self.checkbox_hover(event, tag));
                self.can1.tag_bind(tag, "<Leave>", lambda event: self.checkbox_out(event, tag));
                self.can1.tag_bind(tag, "<Button-1>", lambda event: self.click(event, tag_check, tag, data));

    def checkbox(self, no, data): #x, y, r, color, outline, tag, text, perc):
        record=[];
        print "Value of ParallelRunnining in checkbox:  ", ParallelRunning.completed, "\n";
                
        for i in range(0, len(self.prediction_array)):
                y=250+(i*33);
                tag_check="check" + str(i);
                tag="o"+str(i);


                        
                percentange=self.prediction_array[i]*100;

                print "True or False:  ", (ParallelRunning.completed==1) and (i in ProgressingWindow.records);


                if (ParallelRunning.completed==0 and percentange>=65.0) or ((ParallelRunning.completed==1) and (i in ProgressingWindow.records)):
                                print "Entered\n";
                                color="#354d7c";
                                outline="#354d7c";
                                data.append(tag);
                        
                else:
                                color="#E8E8E8";
                                outline="#E8E8E8";
                perc=str(percentange)+" %"
                text=str(self.features_title[i])
                        
                        
                        
                print "value of data:  ", data;
                self.bind_checkbox(y, color, outline, tag, tag_check, perc, text, data);


    def BackgroundRunning(self, event):
                print "Donatto B Mookken\n";
                print "BackgroudnRunning Initialized\n";
                background=ParallelRunning();
                background.start();
                ControlWindow(5);
           
            
    def PROGRESSING_WINDOW(self):
            global path, data;
            r=6;
            sub_window=self.can1.create_rectangle(50, 180, 50+800, 180+40, fill="#1b3a6d", width=0 );
            self.can1.create_text(80+20, 180+20, anchor=W, font=('helvica', 15,tkFont.BOLD), fill="white", text="Features")
            self.can1.create_text(50+400+50, 180+20, anchor=W, font=('helvica', 15,tkFont.BOLD), fill="white", text="Dependencies")

            obj=RegressionAnalysis()
            self.features, self.target, self.target_title, self.features_title = obj.featureset(path)

            self.prediction_array=obj.prediction();

            self.checkbox(1, data);

            self.mainbottomframe.tag_unbind("button_text", '<Button-1>')
            self.mainbottomframe.tag_bind("button_text", '<Button-1>', lambda event: self.BackgroundRunning(event))


class InputData(Window):
        no=0;
        clf=0;
        def __init__(self):
            #Window.__init__(self, "ABOUT", 300, 2, 3);

            Window.__init__(self, "INPUT DATA", 335, 4, 6)
            print "Input data Intiallised.\n";
            self.can1, self.mainbottomframe=Window.__str__(self)
            global a;

            self.INPUT_DATA();

        
        def create_text(self, i, display):
                self.y=160+(i*44);

                self.y= self.y+40;
                text_box=MyButton("");
                text_box.place(370, self.y-5, 450, 35);
                self.button=text_box.showdef(self.can1, "fill","Arial 12 normal", "white", "white");

                self.can1.create_text(70, self.y+10, font = ('times', 16, 'bold'), anchor=W, text=display[6:])

                string="self.e"+str(i);
                text=string+"=Entry(self.can1, width=32, bd=0,fg = '#bec0c4', font = ('times', 18, 'bold'), bg = None)";

                exec(text);
                
                exec(string+".insert(0, '" + str(display) +"')");

                exec(string+".place(x=400, y=" + str(self.y) + ")");

        def NOTIFICATION(self):
                self.can1.itemconfig(TEXT, text="COMPLETED   "+str(ParallelRunning.completed));

        def NEXT_WINDOW(self, event, a):
                global flag;
                InputData.no=[];
                for i in range(len(a)):
                        exec("InputData.no.append(float(self.e"+str(i)+".get()));");


                if flag==1:
                    n=6;
                else:
                    n=7;

                ControlWindow(n)

        def INPUT_DATA(self):
                
                print "Value's in a:  ", a, "\n";
                for i in range(len(a)):
                        display="Enter " + str(a[i]);
                        display=display.title();
                        self.create_text(i, display);

                self.mainbottomframe.tag_unbind("button_text", '<Button-1>')
                self.mainbottomframe.tag_bind("button_text", '<Button-1>', lambda event: self.NEXT_WINDOW(event, a))


class ProgressingRegression(Window):

        def __init__(self):
                Window.__init__(self, "ANALYZING DATA...", 300, 5, 7)
                self.can1, self.mainbottomframe=Window.__str__(self)
                self.username = getpass.getuser()
                self.destinaion="C:\\Users\\" + self.username + "\\AppData\\Roaming\\predizon\\temp";
                self.destinaion2="C:\\Users\\" + self.username + "\\AppData\\Roaming\\predizon\\dataset";
                self.PROGRESSING_REGRESSION();


        def save_data(self, event):
                global num, path;
                print "saving...\n";
                name=UploadWindow.file_path[self.no-1];
                self.save_name=self.save_entry.get();
                files=os.listdir(self.destinaion2);
                print "self.save_name:  ", self.save_name;
                print "files:  ", files;
                print "name:   ", name;
                if self.save_name!="Enter file name..." and self.save_name!="":
                        self.save_name=self.save_name+".csv";
                        if self.save_name not in files:
                                cwd=os.getcwd();
                                print "value of current working directory :  ", cwd;
                                os.chdir(self.destinaion);
                                print "path, self.destination:  ", path, "--", self.destinaion;
                                shutil.copy2(path, self.destinaion);
                                new_path="C:\\Users\\" + self.username + "\\AppData\\Roaming\\predizon\\temp\\" + self.save_name;
                                os.rename(name, self.save_name);
                                shutil.copy2(new_path, self.destinaion2);
                                os.remove(new_path);
                                os.chdir(cwd);

                                new_name=self.save_name;
                                c=InputData.clf.best_params_['C']
                                gamma=InputData.clf.best_params_['gamma']
                                score=RegressionAnalysis.score;

                                
                                Database("w", [new_name,c,gamma, score, num]);
                                print "Data saved...\n";
                                tkMessageBox.showinfo("Saved", new_name + " saved succesfully...");
                                self.save_entry.delete(0, "end");
                                self.save_entry.insert(0, "Enter file name...");
                        else:
                                tkMessageBox.showinfo("Warning", self.save_name + " already exist. Not saved.");

                else:
                        print "Data cannot be saved....\n";
                        tkMessageBox.showinfo("Error!", "Check your entry");

        def on_entry_click(self,event):
               if self.save_entry.get() == "Enter file name...":
                        self.save_entry.delete(0, "end") 
                        self.save_entry.insert(0, '') 
                        self.save_entry.config(fg = '#354d7c')

        def on_focusout(self,event):	
                if self.save_entry.get() == '':
                        self.save_entry.config(fg = '#59828F', show = "");
                        self.save_entry.insert(0, "Enter file name...");      

        def analyzing_complete(self):
            global path, save_flag;
            print "Entered analyzing_complete\n";
            self.no=len(UploadWindow.file_path)
            
            self.can1.after_cancel(self.iteration)
            self.can1.delete(self.load);
            self.can1.itemconfig("title_text", text="COMPLETED");
            self.mainbottomframe.itemconfig("buttonl", fill="#222323")
            self.mainbottomframe.itemconfig("button", outline="#222323")
            self.mainbottomframe.itemconfig("button_text", fill="#222323")
            ob=MyButton("");
            self.mainbottomframe.bind("<Enter>", lambda event: ob.mouse_in(event, self.mainbottomframe, '#891111', '#891111'))
            self.mainbottomframe.bind("<Leave>", lambda event: ob.mouse_out(event, self.mainbottomframe, "#222323", "#222323"))
            self.mainbottomframe.tag_bind("button_text", '<Button-1>', lambda event: ControlWindow(7))

            self.can1.create_text(260, 330, anchor=W, text="ACCURACY OF THE GIVEN MODEL ", font=('times', 18, 'bold'), fill="white")
            self.can1.create_text(455  , 370, anchor=CENTER, text=str(RegressionAnalysis.score), font=('times', 18, 'bold'), fill="red")
            files=os.listdir(self.destinaion);
            print "files in ANALYSING COMPLETED:  ", files, "\n";
            print files, "\n";
            print UploadWindow.file_path[self.no-2], "\n";
            print UploadWindow.file_path[self.no-1], "\n";
            print UploadWindow.file_path[self.no-2]!="dataset"
            print UploadWindow.file_path[self.no-1] not in files;

            print UploadWindow.file_path[self.no-2]!="dataset" and (UploadWindow.file_path[self.no-1] not in files)

            no=len(UploadWindow.file_path);
            print "True of flase:  ", UploadWindow.file_path[:no-1]!=string.split(self.destinaion) ;
            print UploadWindow.file_path[:no-1];
            print string.split(self.destinaion, "\\");
            y=200;
            save_button=self.can1.create_rectangle(20+20+650+10, y, 840-20, y+35, fill="#2d8730",  width=0 );
            save_text=self.can1.create_text(-25+50+20+650+10+110/2, (y)+int(35/2), fill="white", font=('Arial',12,tkFont.BOLD), text = "Save");

           
            text_box=MyButton("");
            text_box.place(90, y, 600, 35);
            self.button=text_box.showdef(self.can1, "fill","Arial 12 normal", "white", "white");

                
            self.save_entry=Entry(self.can1, width=45, bd=0,fg = '#bec0c4', font = ('times', 18, 'bold'), bg = "white");
            self.save_entry.bind('<FocusIn>', self.on_entry_click)
            self.save_entry.bind('<FocusOut>', self.on_focusout)
            self.save_entry.insert(0, "Enter file name...");

            self.save_entry.place(x=100, y=y+5);


            if save_flag==0:
                    self.can1.itemconfig(save_button, fill="gray");
                    self.can1.itemconfig(save_text, fill="white");
            elif save_flag==1:
                    self.can1.itemconfig(save_button, fill="#3CA340");
                    self.can1.itemconfig(save_text, fill="white");
                    self.can1.tag_bind(save_text, '<Enter>', lambda event: self.can1.itemconfig(save_button, fill="#3CA340"));
                    self.can1.tag_bind(save_text, '<Leave>', lambda event: self.can1.itemconfig(save_button, fill="#2d8730"));
                    self.can1.tag_bind(save_text, "<Button-1>", lambda event: self.save_data(event))
                    #self.can1.bind("<Return>", lambda event: self.save_data(event));


        def rotate_load(self, start, extend, j, i):
                
            state = ParallelRunning.completed;
            #print "Entered rotate_load\n";
            #print "value of ParallelRunning.completed:  ", ParallelRunning.completed;
            if start>=361:
                    start=0;
            if extend>=361:
                    #extend=0;
                    i=-1;
            elif extend<5:
                    i=1;

            #j=j+(i*1);
            start = start + 6;
            extend=extend+(i*3);
            self.can1.itemconfig(self.load, start=start, extent=extend);

            self.can1.after(10);
            self.iteration=self.can1.after_idle(self.rotate_load, start, extend, j, i)

            
            if state==1:
                self.analyzing_complete();
                

        def PROGRESSING_REGRESSION(self):
                #self.mainbottomframe.delete("circle_button");
                #elf.mainbottomframe.delete("circle_button_text");
                self.mainbottomframe.itemconfig("buttonl", fill="black")
                self.mainbottomframe.itemconfig("button", outline="black")
                self.mainbottomframe.itemconfig("button_text", fill="black")
         

                
                self.mainbottomframe.unbind('<Enter>');
                self.mainbottomframe.unbind('<Leave>');
                self.mainbottomframe.tag_unbind("button_text", '<Button-1>');
                
                x=450;
                y=320;
                self.load=self.can1.create_arc(x-20, y-20, x+20, y+20, start=0, extent=200,  style=tk.ARC, outline="#354d7c", width=4);
                self.rotate_load(0, 0, 0, 1);
                
class ResultWindow(Window):            
        def __init__(self):
                
                Window.__init__(self, "RESULT", 300, 5, 3)
                self.can1, self.mainbottomframe=Window.__str__(self)
                self.clf=InputData.clf;
                self.RESULT_DATA();

        def RESULT_DATA(self):
                global flag;
                flag=0;
                self.mainbottomframe.tag_unbind("circle_button_text", '<Button-1>');
                self.mainbottomframe.tag_bind("circle_button_text", '<Button-1>', lambda event: ControlWindow(5))


                self.mainbottomframe.itemconfig("button_text", text="Attach File")
                
                no=InputData.no;
                ob=RegressionAnalysis();
                pred=ob.regression(no, self.clf);
                self.can1.create_text(260, 280, anchor=W, text="PREDIZON PREDICTED VALUES IS", font=('times', 18, 'bold'), fill="white")
                self.can1.create_text(455  , 320, anchor=CENTER, text=str(pred[0]), font=('times', 18, 'bold'), fill="red");
                
class ControlWindow():
    def __init__(self, win):
        if(win==1):
            ob1=MainWindow();
        if(win==2):
            ob2=AboutWindow();
        if(win==3):
            ob3=UploadWindow();
        if(win==4):
            ob4=ProgressingWindow();
        if(win==5):
                ob5=InputData();
        if(win==6):
                ob6=ProgressingRegression();
        if(win==7):
                ob7=ResultWindow();

conn2 = sqlite3.connect('database1.db');
cursor2 = conn2.execute("UPDATE settings SET var=1 WHERE id=1;");
conn2.commit();

contwin=ControlWindow(1)
root.mainloop();
