from ttkthemes import ThemedStyle
import tkinter as tk
from tkinter import Scrollbar, Text, filedialog, messagebox, ttk
import cv2
import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageTk
# from sklearn.cluster import KMeans
import sqlite3

# Model used is yolov5 object detection pre-trained model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s',pretrained=True,)  # load yolo model. Store it in variable called model

# this code gets the dominant colours to perform cluster algorithm 
def visualise_Dominant_colors(cluster, C_centroids):
    C_labels = np.arange(0, len(np.unique(cluster.labels_)) + 1) # create an np array from zero to number of clusters labels+1
    (C_hist, _) = np.histogram(cluster.labels_, bins = C_labels) #compute histogram of number of labels to get dominant, bins is number of width of combined values, take the range of clabels
    C_hist = C_hist.astype("float") # convert return value to become float
    C_hist /= C_hist.sum() # normalise the values to be in same range
    img_colors = sorted([(percent, color) for (percent, color) in zip(C_hist, C_centroids)]) # sort colours in image from higher percentage colour in img
    return list(img_colors[0][1]) # take higher percentage colour in image and cast to list then return it

def resize_image(img,scale_percent):
    width = int(img.shape[1] * scale_percent / 100)  # take percentage of image width based on scale percent passed to the function
    height = int(img.shape[0] * scale_percent / 100)  # take percentage of image height based on scale percent passed to the function
    dim = (width, height) # new dimension is saved in new dim
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA) # image is now resized to new dimension and returned

# apply detection algorithm
# detect people in image using yolo algorithm
# take all people in image and apply kmeans machine learning algorithm to cluster image into two clusters
# assign every person to cluster
def apply(path):
    im2 = cv2.imread(path) # read image from passed path
    if im2.shape[0]>400 or im2.shape[1]>800: # check if image size > 400 width or 800 height
        im2 = cv2.resize(im2, (800, 400)) # if bigger, resize image to become 800*400
    else:
        im2 = cv2.resize(im2, (im2.shape[1], im2.shape[0])) # if not bigger resize image to it's size
    frame=cv2.cvtColor(im2, cv2.COLOR_RGB2BGR) # convert image from rgb colours to bgr colours
    mainShape=frame.shape # save image shape to global variable mainShape
    results = model(frame) # predict result of yolo model for given image
    df=results.pandas().xyxy[0]  # convert result to pandas dataframe
    df=df[(df["confidence"]>0.5)] # only take images with confidence > 50% to be sure it's people
    team1=[]  # team1 list to save results
    team2=[]  # team2 list to save results
    for i in range(df.shape[0]): ## iterate on selected part of data frame
        if df.name[i]=="person": # check if selected row now contains a person
            xmin=int(df["xmin"].loc[i]) # takes the xmin position in main image and cast it to integer to process it.
            ymin=int(df["ymin"].loc[i]) # takes the ymin position in main image and cast it to integer to process it.
            xmax=int(df["xmax"].loc[i]) # takes the xmax position in main image and cast it to integer to process it.
            ymax=int(df["ymax"].loc[i]) # takes the ymax position in main image and cast it to integer to process it.
            cropimage=frame[ymin:ymax,xmin:xmax] # crop image of selected player from main image
            cropimage=resize_image(cropimage,400) # resize image to be bigger than its range to process it
            gray = cv2.cvtColor(cropimage,cv2.COLOR_BGR2GRAY) # convert cropped image to gray scale to detect the player body
            edges = cv2.Canny(gray,50,150,apertureSize = 3) # apply the canny edge detection to detect player body in cropped image
            rect=cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) # kernel to apply dilation and erosion both for encancment the player cropped image after apply canny edge detection
            dilation = cv2.dilate(edges,rect,iterations = 5) # applying the dilation for 5 iterations
            erosion = cv2.erode(dilation, rect, iterations=4) # applying the erosion for 4 iterations
            maskReversed=cv2.bitwise_and(cropimage,cropimage, mask=erosion) # perform the result of both on cropped images using bitwise operations
            cropimage2 = cropimage.reshape((maskReversed.shape[0] * maskReversed.shape[1], 3)) # convert all player body images to become array of values to apply kmeans algorithm to cluster colours in image
            clt = KMeans(n_clusters = 2) # init kmeans cluster algorithm from sklearn library
            clt.fit(cropimage2) # fit the model on cropped image array
            try:
                visualise_color = visualise_Dominant_colors(clt, clt.cluster_centers_) # call dominant colour function to get dominant colour of player body and save it to visualise_colour
                # compare the values and differentiate the players based on ranges of colours
				# if player body colour is in range of players in team1 list then this player is team 1
                # if player body colour is in range of players in team2 list then this player is team 2
                if (len(team1)<=0): 
                    team1.append(visualise_color)
                    team=1
                elif (len(team2)<=0):
                    team2.append(visualise_color)
                    team=2
                else:
                    if team1[0][0]-visualise_color[0]<=20 and team1[0][1]-visualise_color[1]<=20 and team1[0][2]-visualise_color[2]<=20:
                        team1.append(visualise_color)
                        team=1
                    elif team1[0][0]-visualise_color[0]>50 and team1[0][1]-visualise_color[1]>50 and team1[0][2]-visualise_color[2]>50:
                        team2.append(visualise_color)
                        team=2
                    else:
                        team2.append(visualise_color)
                        team=2
                if team==1: # check if player is in team1 or team2
                    # put text on main image behind player for correct team, colour is(255,255,255) white
                    cv2.putText(frame,"Team="+str(team),(xmin+3,ymin+32),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                elif team==2:
                    # put text on main image behind player for correct team, colour is(0,0,255) blue
                    cv2.putText(frame,"Team="+str(team),(xmin+3,ymin+32),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
                
            except:
                pass
            # draw rectangle on players we detected using (255,0,0) red
            cv2.rectangle(frame, (xmin,ymin),(xmax,ymax), (255,0,0), 2)
    im2=None
    return frame  # return image after the process




# These are updated forms

class ImageApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		
		# Apply a modern theme using ttkthemes
		style = ThemedStyle(self)
		style.set_theme("arc")


		
		# create a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initialise frames to an empty array
		self.frames = {}
		# iterate through a tuple consisting of the different page layouts
		for F in (LoginPage, ImagePage, SignupPage):

			frame = F(container, self)

			# initialise frame of that object from startpage, page1, page2 respectively with for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(LoginPage)

	# to display current frame passed as parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		
		if(cont == LoginPage or cont == SignupPage):
			self.geometry("400x280")
			self.title("Log In")
			if(cont == SignupPage):
				self.geometry("400x400")
				self.title("Sign Up")
		else:
			self.geometry('+{}+{}'.format(0, 0))
			self.geometry('1920x1080')
			self.title("Image Viewer")

		frame.configure(background='#fff8eb')
		frame.tkraise()


# first window frame
class LoginPage(tk.Frame):

	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		self.controller = controller

		# Create the heading label
		heading_label = ttk.Label(self, text="Welcome Back", font=('Arial', 16, 'bold'), background="#fff8eb", foreground="#000")
		heading_label.place(relx=0.5, rely=0.1, anchor='center')

		# Create the username label
		username_label = ttk.Label(self, text="Username:", width=36)
		username_label.place(relx=0.5, rely=2.5, anchor='center', in_=heading_label)
		username_label.config(foreground="black", background="#fff8eb")

		# Create the username entry widget and add styling options
		username_entry = ttk.Entry(self, width=30, font=('Arial', 10))
		username_entry.place(relx=0.5, rely=2.1, anchor='center', in_=username_label)
		username_style = ttk.Style()
		username_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		username_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		username_entry.config(style='TEntry')

		# Create the password label
		password_label = ttk.Label(self, text="Password:", width=36)
		password_label.place(relx=0.5, rely=1.5, anchor='center', in_=username_entry)
		password_label.config(foreground="black", background="#fff8eb")

		# Create the password entry widget and add styling options
		password_entry = ttk.Entry(self, width=30, font=('Arial', 10))
		password_entry.place(relx=0.5, rely=2.5, anchor='center', in_=username_entry)
		password_style = ttk.Style()
		password_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		password_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		password_entry.config(style='TEntry', show='*')
		
		# Create the Warning label
		lblWarning = ttk.Label(self, text ="", background="#fff8eb")
		lblWarning.place(relx=0, rely=1.25, in_=password_entry)
		lblWarning.config(foreground="red")

		# Create the login button and add styling options
		submit_style = ttk.Style()
		submit_style.configure('TButton', foreground='#000', background='#fff8eb', font=('Arial', 8), padding=2)
		submitbtn = ttk.Button(self, text='Login', command=lambda: self.checkLogin(username_entry.get(), password_entry.get(), lblWarning))
		submitbtn.place(relx=0.22, rely=2.5, anchor='center', width=100 , in_=password_entry)
		submitbtn.config(style='TButton')

		# Create the signup button and add styling options
		signup_style = ttk.Style()
		signup_style.configure('TButton', foreground='#000', background='#fff8eb', font=('Arial', 8), padding=2, bordercolor='#333')
		signUpbtn = ttk.Button(self, text='SignUp', command=lambda: controller.show_frame(SignupPage))
		signUpbtn.place(relx=1.75, rely=0.5, anchor='center', width=100, in_=submitbtn)
		signUpbtn.config(style='TButton')
		
	def clear_placeholder(self, event):
		if self.password_entry.get() == 'Enter password':
			self.password_entry.delete(0, tk.END)

	def set_placeholder(self, event):
		if not self.password_entry.get():
			self.password_entry.insert(0, 'Enter password')

	def checkLogin(self,username, password, lblWarning):
		if(username == ""):
			lblWarning.config(text="Username field must not be empty.")
			return
		if(password == ""):			
			lblWarning.config(text="Password field must not be empty.")
			return

		con = sqlite3.connect("users.db")
		cursor = con.cursor()

		listOfTables = cursor.execute("SELECT * FROM sqlite_master;").fetchall()

		if listOfTables == []:
			cursor.execute("CREATE TABLE USERS(USERNAME VARCHAR(50),EMAIL VARCHAR(50), PASSWORD VARCHAR(50));")
			lblWarning.config(text="You are not registered. Please sign up with new details.")
			con.commit()
			con.close()
			return

		# Table in the database
		savequery = "select * from USERS WHERE USERNAME='" + username + "' AND PASSWORD = '"+ password + "';"
		try:
			cursor.execute(savequery)
			myresult = cursor.fetchall()
			
			if(len(myresult) > 0):
				lblWarning.config(text="Successfully Logged in!")
				self.controller.show_frame(ImagePage)
			else:
				lblWarning.config(text="You are not registered. Please sign up with new details.")			
		except:
			con.rollback()
			lblWarning.config(text="MySQL Connection Error occurred!")
		con.commit()
		con.close()

class SignupPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		
		# Create the heading label
		heading_label = ttk.Label(self, text="Welcome", font=('Arial', 16, 'bold'), background="#fff8eb", foreground="#000")
		heading_label.place(relx=0.5, rely=0.1, anchor='center')

		# Create the username label
		username_label = ttk.Label(self, text="Username:", width=36)
		username_label.place(relx=0.5, rely=2.5, anchor='center', in_=heading_label)
		username_label.config(foreground="black", background="#fff8eb")
		# Create the username entry widget and add styling options
		username = ttk.Entry(self, width=30, font=('Arial', 10))
		username.place(relx=0.5, rely=2.1, anchor='center', in_=username_label)
		username_style = ttk.Style()
		username_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		username_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		username.config(style='TEntry')
		
		# Create the Email label
		Email_label = ttk.Label(self, text="Email:", width=36)
		Email_label.place(relx=0.5, rely=1.5, anchor='center', in_=username)
		Email_label.config(foreground="black", background="#fff8eb")
		# Create the Email entry widget and add styling options
		email = ttk.Entry(self, width=30, font=('Arial', 10))
		email.place(relx=0.5, rely=2.5, anchor='center', in_=username)
		email_style = ttk.Style()
		email_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		email_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		email.config(style='TEntry')

		# Create the new password label
		lblNewPwd = ttk.Label(self, text="Password:", width=36)
		lblNewPwd.place(relx=0.5, rely=1.5, anchor='center', in_=email)
		lblNewPwd.config(foreground="black", background="#fff8eb")
		# Create the new password entry widget and add styling options
		pwdNew = ttk.Entry(self, width=30, font=('Arial', 10))
		pwdNew.place(relx=0.5, rely=2.5, anchor='center', in_=email)
		pwdNew_style = ttk.Style()
		pwdNew_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		pwdNew_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		pwdNew.config(style='TEntry', show='*')

		# Create the Confirm Password label
		lblCrmPwd = ttk.Label(self, text="Confirm Password:", width=36)
		lblCrmPwd.place(relx=0.5, rely=1.5, anchor='center', in_=pwdNew)
		lblCrmPwd.config(foreground="black", background="#fff8eb")
		# Create the Confirm Password entry widget and add styling options
		pwdCrm = ttk.Entry(self, width=30, font=('Arial', 10))
		pwdCrm.place(relx=0.5, rely=2.5, anchor='center', in_=pwdNew)
		pwdCrm_style = ttk.Style()
		pwdCrm_style.configure('TEntry', foreground='#333', background='#fff', padding=2)
		pwdCrm_style.map('TEntry', fieldbackground=[('disabled', '#eee')])  # Disable background color on inactive widget
		pwdCrm.config(style='TEntry', show='*')
		
		lblWarning = ttk.Label(self, text ="", background="#fff8eb")
		lblWarning.place(relx=0, rely=1.25, in_=pwdCrm)
		lblWarning.config(foreground="red")

		# Create the submit button and add styling options
		submit_style = ttk.Style()
		submit_style.configure('TButton', foreground='#000', background='#fff8eb', font=('Arial', 8), padding=2)
		submitbtn = ttk.Button(self, text ="Register",
		command = lambda : self.signup(username.get(), email.get(), pwdNew.get(), pwdCrm.get(), lblWarning))
		submitbtn.place(relx=0.22, rely=2.5, anchor='center', width=100 , in_=pwdCrm)
		
		# Create the login button and add styling options
		login_style = ttk.Style()
		login_style.configure('TButton', foreground='#000', background='#fff8eb', font=('Arial', 8), padding=2, bordercolor='#333')
		loginBtn = ttk.Button(self, text ="Back to Login",
		command = lambda : controller.show_frame(LoginPage))
		loginBtn.place(relx=1.75, rely=0.5, anchor='center', width=100, in_=submitbtn)
		
	def signup(self,username, email, pwd1, pwd2, lblWarning):
		if(username == ""):
			lblWarning.config(text="Username field must not be empty.")
			return
		if(email == ""):
			lblWarning.config(text="Email field must not be empty.")
			return
		if(pwd1 == ""):
			lblWarning.config(text="Password field must not be empty.")
			return
		if(pwd2 == ""):
			lblWarning.config(text="Password Confirmation field must not be empty.")
			return
		if(pwd1 != pwd2):
			lblWarning.config(text="Passwords do not match. Enter matching passwords.")
			return
		
		# DB Operation for Sqlite file "users.db"
		con = sqlite3.connect("users.db")
		cursor = con.cursor()

		listOfTables = cursor.execute("SELECT * FROM sqlite_master;").fetchall()

		if listOfTables == []:
			cursor.execute("CREATE TABLE USERS(USERNAME VARCHAR(50),EMAIL VARCHAR(50), PASSWORD VARCHAR(50));")

		# Table in the database
		query = "INSERT INTO USERS (USERNAME, EMAIL, PASSWORD) VALUES ('{}', '{}', '{}')".format(username, email, pwd1)
		try:
			cursor.execute(query)
			lblWarning.config(foreground='black')
			lblWarning.config(text="Successfully Registered.")
		except:
			con.rollback()
			lblWarning.config(text="MySQL Connection Error occurred!")
		con.commit()
		con.close()

		
# second window frame
class ImagePage(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		# Create buttons with modern styling

		img = tk.PhotoImage(file=r".\assets\icons8-football-64.png")
		label2 = tk.Label(self,image=img , background="#fff8eb")
		label2.img = img
		# label2.pack()
		label2.place(relx=0.15, rely=0.1, anchor='center') 
		# Label for title
		label3 = ttk.Label(self,text="Team Members Detection App", foreground="#000" , font=("Helvetica",45,"bold"), background="#fff8eb")
		label3.place(relx=8.15, rely=0.5, anchor='center', in_=label2) 
		# Label for LoadPath
		label55 = ttk.Label(self,text="Load Path",font=("Helvetica",12,"bold"),background="#fff8eb", foreground="#000")
		label55.place(relx=0, rely=2, anchor='center',in_=label3) 
		# Label for SavePath
		label556 = ttk.Label(self,text="Save Path",font=("Helvetica",12,"bold"),background="#fff8eb", foreground="#000")
		label556.place(relx=0.55, rely=2, anchor='center',in_=label3) 
		# Label for SavePath
		img2 = tk.PhotoImage(file=r".\assets\icons8-football-64(1).png")
		label222 = ttk.Label(self, image=img2, background="#fff8eb")
		label222.img = img2

		label222.place(relx=0, rely=4, anchor='center', in_=label3) 

		# Text for loading path
		T = Text(self, height = 1, width = 50)
		T.place(relx=2.5, rely=1.5, anchor='center', in_=label55)
		# Text for loading path
		T1 = Text(self, height = 1, width = 50)
		T1.place(relx=2.5, rely=1.5, anchor='center', in_=label556)
		# Image view Label
		label = ttk.Label(self)
		label.place(x=10, y=370) 
		# Separator
		separator = ttk.Separator(self, orient='horizontal', takefocus= 0)
		separator.place(x=0,y=129,relwidth=1)
		# Separator
		separator2 = ttk.Separator(self, orient='horizontal')
		separator2.place(x=0,y=250,relwidth=1)

		
		# Load Button
		open_button = ttk.Button(self, text="Load", command = lambda : self.open_image(label, T), style="TButton")
		open_button.place(relx=4.61, rely=0.27, anchor='center', in_=label55) 

		# Load Button
		open_button2 = ttk.Button(self, text="Load", command=lambda :self.open_image1(T1), style="TButton")
		open_button2.place(relx=4.61, rely=0.27, anchor='center', in_=label556) 
		# clear Button
		clear_button = ttk.Button(self, text="Clear", command=lambda :self.clear_image(label), style="TButton",width=10)
		clear_button.place(relx=0.1, rely=3.5, anchor='center', in_=label3) 
		# Detect Buttons
		prc_button = ttk.Button(self, text="Detect", command=lambda :self.process(label), style="TButton",width=10)
		prc_button.place(relx=0.1, rely=4.0, anchor='center', in_=label3) 
		# Save Button
		save_button = ttk.Button(self, text="Save", command=lambda :self.save_app(), style="TButton",width=10)
		save_button.place(relx=0.1, rely=4.5, anchor='center', in_=label3) 
		# Logo label for ball


	image_path=None # global variable where image load path is saved
	image_path_save=None # global variable where image save path is saved
	resultImg=None # global variable where image load path is saved
	# Create function to open an image
	def open_image(self, label, T):
		try:
			global image_path # global variable where image load path is saved
			file_path = filedialog.askopenfilename() # select path
			image_path=file_path # set global path
			shapeImg=cv2.imread(file_path).shape # get shape of the loaded image
			image = Image.open(file_path) # open the loaded image from path using pillow library
			if shapeImg[1]>800 or shapeImg[0]>400: # check if image size > 400 for width or 800 for height
				image = image.resize((800, 400), Image.ANTIALIAS) # if bigger, resize image to become 800*400
			else:
				image = image.resize((shapeImg[1], shapeImg[0]), Image.ANTIALIAS) # if not bigger, resize image to it's size
			photo = ImageTk.PhotoImage(image) # load image using Image Tkinter to set the label image to view in GUI
			label.config(image=photo) # set the image as label of GUI
			label.place(relx=0.63, rely=0.12, anchor='center') # Set Picture location according to screen
			label.image = photo # set the image as label of GUI
			T.delete("1.0",tk.END) # Delete the place where the path appears in gui
			T.insert(tk.END,file_path)# add the new selected path 
			messagebox.showinfo(title="InfoMessage", message="Image uploaded successfully") # create messagebox with load successful as message for user
		except:
			messagebox.showerror(title="ErrorMessage", message="Error while loading") # create messagebox with error while loading as message for user

	# Create function to open an image
	def open_image1(self, T1):
		global image_path_save # global variable where image saved path is saved
		file_path = filedialog.askdirectory() # select path
		image_path_save=file_path # set the global save path 
		T1.delete("1.0",tk.END)# Delete place where the path appears in gui
		T1.insert(tk.END,file_path) # add new selected path
		

	# Create function to clear image
	def clear_image(self, label):
		global image_path,resultImg
		label.image=None # set the image to none 
		image_path=None # set the load path to none 
		image_path_save=None # set the save path to none 
		resultImg=None # set the result image variable to none

	def exit_app(self):
		self.destroy()

	def process(self, label):
		try:
			global resultImg
			f = apply(image_path) # call apply function with loaded selected path
			resultImg=f # set global result image to the image after applying algorithm
			image=Image.fromarray(f) # load result image to Image pillow object
			shapeImg=cv2.imread(image_path).shape # save shape of image in the shapeImg variable
			photo = ImageTk.PhotoImage(image) # load image using Image Tkinter to set the label image to view in GUI
			label.config(image=photo)
			label.image = photo # set the label image to result image
			messagebox.showinfo(title="InfoMessage", message="Player detection successful")# create messagebox with detect successful as message for user
		except:
			messagebox.showerror(title="ErrorMessage", message="Error while detecting")# create messagebox with error while detection for user


	# Function to save the images
	def save_app(self):
		global resultImg
		try:
			resultImg = cv2.cvtColor(resultImg, cv2.COLOR_BGR2RGB) # convert image to RGB because algorithm returns it in BGR format
			cv2.imwrite(image_path_save+"/savedImg.jpg", resultImg) # save image in selected path
			messagebox.showinfo(title="InfoMessage", message="Image saved successfully") # create messagebox with saved successful as message for user
		except:
			messagebox.showerror(title="ErrorMessage", message="Error while saving")# create messagebox with error while saving for user




# Driver Code
app = ImageApp()
app.mainloop()
