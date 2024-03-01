#the methods used
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo, showerror
from tkinter.messagebox import askyesno
from tkinter import filedialog as fd
from Methods import Method_List
import re

#base class for costum exceptions
class Error(Exception):
    pass
#used when an invalid ID is passed. used below
class IDInvalid(Error):
    pass

class DatabaseDisplay(ttk.Treeview):
    def __init__(self, master): #initializes an instance in the class
        super().__init__(master, columns=('id_no', 'name', 'course', 'year', 'gender'), show="headings", height = 15, style = "Treeview")#calls the constructor of the parent class with specific parameters

        dtbStyle = ttk.Style()
        dtbStyle.configure("Treeview", font=("Arial", "15")) #Configures the font for all elements with the style "Treeview".
        dtbStyle.configure("Treeview.Heading", font=("Lucida Sans", "12", "bold")) #the font style for the text headers 

       #the headings/headers
        self.heading('#0', text='', anchor=CENTER)
        self.heading('id_no', text='ID Number')
        self.heading('name', text='Name')
        self.heading('course', text='Course')
        self.heading('year', text='Year')
        self.heading('gender', text='Gender')
       #The width of each header
        self.column('#0', width=0, stretch=YES)
        self.column('id_no', width=120, minwidth= 100)
        self.column('name', width=250, minwidth= 250)
        self.column('course', width=125, minwidth= 100)
        self.column('year', width=60, minwidth= 20)
        self.column('gender', width=70, minwidth= 20)

        self.grid(row=0, column=0, sticky = "nsew", ipadx = 105, ipady=10)

        scrollbar = ttk.Scrollbar(master, orient=VERTICAL, command=self.yview, cursor='sb_v_double_arrow') #Creates a vertical scrollbar widget.
        self.configure(yscroll=scrollbar.set) # Configures the y-scrolling behavior of the DatabaseDisplay widget to be controlled by the scrollbar.

        scrollbar.grid(row=0, column=1, sticky='ns',)#places the scrollbar to the right 


    def treeview_update(self, student_list):

        #updates the treeview when i delete a name/automatically reflects the deletion of a name in the treeview and not just in the csv
        for i in self.get_children():
            self.delete(i)
        #displays a  message if no file path is provided
        if self.master.master.filepath == '': 
            showinfo("Student Information System", "To start, click on 'File' and choose 'New' or 'Open'.") 

        count = 1
        for element in student_list:
            rowid = 'I' + str('{:03}'.format(count))
            self.insert('', END, iid=rowid, values=element)
            count += 1

# a class that inherits frame
class UserDataDisplay(ttk.Frame): 
    def __init__(self, master): #initializes an instance of the class
        super().__init__(master, style="UserDataDisplay.TFrame", height = 315, width = 410)


        self.grid_propagate(0) # makes the grid the right size
        
        #used to track changes 
        self.Var_IDNo = StringVar()
        self.Var_FullName = StringVar()
        self.Var_Course = StringVar()
        self.Var_Year = StringVar()
        self.Var_Gender = StringVar()
        self._single_data_input = []
        
        #the style of the widgets, labels and menu buttons
        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("UserDataDisplay.TFrame", background="navy blue")
        UserDataDisplay_style.configure("UserDataDisplay.TLabel", background="navy blue", foreground="orange", font=("Lucida Sans", "16", "bold"), justify=CENTER)
        UserDataDisplay_style.configure("UserDataDisplay.TEntry", foreground="black")
        UserDataDisplay_style.configure("UserDataDisplay.TMenubutton", font=('Arial', "16", 'bold'))

        #the labels  
        Label_IDNo = ttk.Label(self, text="ID No:", style = "UserDataDisplay.TLabel")
        Label_FullName = ttk.Label(self, text="Name:", style = "UserDataDisplay.TLabel")
        Label_Course = ttk.Label(self, text="Course:", style = "UserDataDisplay.TLabel")
        Label_Year = ttk.Label(self, text="Year:", style = "UserDataDisplay.TLabel")
        Label_Gender = ttk.Label(self, text="Gender:", style = "UserDataDisplay.TLabel")
        #places the frame in the specified row and column of its parent widget
        self.grid(row=0, column=3, rowspan = 5, padx=2, pady=2, ipadx=24, ipady=20, columnspan = 5)
        #the specific placement of the labels
        Label_IDNo.grid(row=1, column=3, pady = 20, sticky = "sw", padx=25)
        Label_FullName.grid(row=2, column=3, pady = 20, sticky = "w", padx=25)
        Label_Course.grid(row=3, column=3, pady = 20, sticky = "w", padx=15)
        Label_Year.grid(row=4, column=3, pady = 20, sticky = "w", padx=30)
        Label_Gender.grid(row=5, column=3, pady = 20, sticky = "w", padx=15)


   #property decorator so that we can access this method like an attribute of an object
    @property
    def single_data_input(self):  #acts as a getter for the single_data_input property. returns the current value
       #This line creates a list containing strings representing the current values as strings
        self._single_data_input = [str(self.Var_IDNo.get()), str(self.Var_FullName.get()), str(self.Var_Course.get()), str(self.Var_Year.get()), str(self.Var_Gender.get())]
        return self._single_data_input
    #setter method
    @single_data_input.setter
    def single_data_input(self, value):
        self._single_data_input = value

#class for the ButtonsFrame
class ButtonsFrame(ttk.Frame): #This method initializes an instance of the ButtonsFrame class.
    def __init__(self, master):
        super().__init__(master, style="BF.TFrame", height = 153, width = 171)

        searchvar = StringVar() #creates a string variable for storing text entered into the search entry widget

        self.grid_propagate(0) #makes the grid the right size
        #style for the label and frame
        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("BF.TFrame", background="navy blue")
        UserDataDisplay_style.configure("BF.TLabel", background="navy blue", foreground="orange", font=("Roboto Mono", "10", "bold"))
        
        self.grid(row=6, column=3, sticky = "nws", rowspan = 5, padx=2, pady=2, ipadx=143, ipady=20, columnspan = 5)
        
        #the buttons
        Add_Button = Button(self, text="Add", relief=RAISED, fg="orange", bg="Blue", height = 1, width = 6, font=('Roboto Mono', "16", 'bold'), command = master.master.master.add)
        Edit_Button = Button(self, text="Edit", relief=RAISED, fg="orange", bg="Blue", height = 1, width = 6, font=('Roboto Mono', "16", 'bold'), command = master.master.master.edit_choice)
        Delete_Button = Button(self, text="Delete", relief=RAISED, fg="orange", bg="Blue", height = 1, width = 6, font=('Roboto Mono', "16", 'bold'), command = master.master.master.delete_choice_popup)
        Search_Entry = ttk.Entry(self, textvariable=searchvar, style="UserDataDisplay.TEntry", width=25, font=('Lucida Sans', "16", 'bold'))
       #reads the csv file then performs a search operation using the content of the entry widget searchvar
        def search_entry_type():
            try:
                cmd.csv_read(master.master.master.filepath)
                master.master.master.search(searchvar.get())
            except FileNotFoundError:
                pass
        #binds the keyrelease event to the search entry type function which allows for real time search functionality
        Search_Entry.bind("<KeyRelease>", search_entry_type)
        
        #the placement of the buttons
        Add_Button.grid(row=0, column=0, padx=20, pady=20, sticky = "news")
        Edit_Button.grid(row=0, column=2, padx=48, pady=20, sticky = "news")
        Delete_Button.grid(row=0, column=4, padx=20, pady=20, sticky = "news")
        Search_Entry.grid(row=1, column=0, sticky = "ns", columnspan = 5, pady=10)
        

#the main window
class Main_App_Window(Tk):
    def __init__(self): #initializes an instance of the App class
        super().__init__()

        self.rex = re.compile("^[0-9]{4}[-][0-9]{4}$") #the specific format for ID number
        
        #initialize values to empty strings
        self.IDNo = ''
        self.FullName = ''
        self.Course = ''
        self.Year = ''
        self.Gender = ''
        #initialized first as an empty list
        self.dataread_list = []
        #counter
        self.index = 0
        #stores the filepath
        self.filepath = ''
        
        self.addCheck = False
        self.editCheck = False
        self.ID_removedisplay_check = False
        #title
        self.title("Student Information System")
        self.geometry("1365x670+0+0")
        #size of the frame
        self.wm_minsize(1365, 670)
        self.wm_maxsize(1365, 670)

        self.state('zoomed')

        #style of the treeview headings and rows
        style = ttk.Style()
        style.configure("Treeview.Heading", rowheight = 40)
        style.configure("Treeview", rowheight = 40)
       
        #creates a menubar and associates the menubar with the main window
        menubar = Menu(self)
        self.config(menu=menubar)
        
        #adds a file menu as a cascade item under the file label in the menu bar
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File",menu=file_menu)
        
        #label text and description of the each command and then a function to execute
        file_menu.add_command(label="New            'Creates a new CSV file and opens it.'", command = self.new_file)
        file_menu.add_command(label="Open           'Opens a CSV file.'", command = self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close          'Closes the program'", command = self.close_file)
        
        #style of the frame
        framestyle = ttk.Style()
        framestyle.configure("mainframe.TFrame", background="blue")
        framestyle.configure("secondframe.TFrame", background='blue')
        framestyle.configure("dataFrame.TFrame", background='white')

        #the maine frame used to display the table
        mainframe = ttk.Frame(self, style="mainframe.TFrame")
        mainframe.grid(row=0, column=0, sticky = "news", rowspan = 40, columnspan = 3, ipadx=2)
        self.treeview = DatabaseDisplay(mainframe)

        #another frame which holds the two widgets
        secondframe = ttk.Frame(self, style="secondframe.TFrame")
        secondframe.grid(row=0, column=3, sticky = "news", rowspan = 40, ipadx=8)


        #the styling and size of the frames
        frame1 = ttk.Frame(secondframe, style="dataFrame.TFrame")
        frame1.grid(row=0, column=3, sticky = "news", rowspan=5, ipadx=0, padx = 20, ipady = 0, columnspan = 5, pady = 30)

        frame2 = ttk.Frame(secondframe, style="dataFrame.TFrame", height = 197, width = 461)
        frame2.grid(row=6, column=3, sticky = "nws", ipadx=0, padx = 20, columnspan = 5, pady = 40)
        #positioning
        frame2.grid_propagate(0)
        
        #the two widgets on the right
        self.UserDataFrame = UserDataDisplay(frame1)
        UserButtonsFrame = ButtonsFrame(frame2)
        
        #updates the treeview widget with the filepath
        self.treeview.treeview_update(self.filepath)

        #creates the entry widget when we press add
        self.Entry_IDNo = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_IDNo, style="UserDataDisplay.TEntry", width=9, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))
        self.course_tuple = Method_List.read_csv_to_tuples('Courses.csv')
        self.Entry_Course = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Course, self.course_tuple[0], *self.course_tuple)
        self.year_tuple = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Irregular")
        self.Option_Year = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Year, self.year_tuple[0], *self.year_tuple)
        self.gender_tuple = ("-----", "Male", "Female", "Other")
        self.Option_Gender = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Gender, self.gender_tuple[0], *self.gender_tuple)
        self.Button_Done = Button(self.UserDataFrame, text="Done", relief=RAISED, fg="orange", bg="blue", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = self.doneFunc)
        
        #positions
        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)
        self.Entry_Course.grid(row=3, column=4, pady = 20, sticky = "w")
        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")
        self.Button_Done.grid(row=5, column=5, sticky="nw")
       
        self.before_edit_button(self.UserDataFrame)
        self.treeview.bind('<<TreeviewSelect>>', self.item_selected)

   #when the close file option is chosen prompts the user whether he means to close it or not
    def close_file(self):
        close_window = askyesno("Close Student Information System?", "Are you sure you want to exit?")
        if close_window:
            self.destroy()
    #creates a new file when we choose to create one
    def new_file(self):
        temp = self.filepath
        filetypes = (('CSV Files', '*.csv'),)

        filename = fd.asksaveasfilename(title='Create a new file', initialdir='*', filetypes=filetypes, initialfile = "New CSV", defaultextension = ".csv")

        self.filepath = filename

        if self.filepath == '':
            self.filepath = temp
        else:
            cmd.csv_create(self.filepath)

        self.treeview.treeview_update(cmd.csv_read(self.filepath))
    #selects a file from a folder
    def select_file(self):
        filetypes = (('CSV Files', '*.csv'),)
        filename = fd.askopenfilename(title='Open a file', initialdir='*', filetypes=filetypes)
        self.filepath = filename
        self.treeview.treeview_update(cmd.csv_read(self.filepath))
    #handles the selection of items in the treeview widget
    def item_selected(self, event):
        try:
            for student_selected in self.treeview.selection():
                item = self.treeview.item(student_selected)
                student_data = item['values']
                
                #converts data into a string
                self.IDNo, self.FullName, self.Course, self.Year, self.Gender = student_data
                self.IDNo = str(self.IDNo)
                self.FullName = str(self.FullName)
                self.Course = str(self.Course)
                self.Year = str(self.Year)
                self.Gender = str(self.Gender)
                student_data = [self.IDNo, self.FullName, self.Course, self.Year, self.Gender]
                
                #updates the display
                self.IDNo_DataDisplay.config(text=self.IDNo)
                self.FullName_DataDisplay.config(text=self.FullName)
                self.Course_DataDisplay.config(text=self.Course)
                self.Year_DataDisplay.config(text=self.Year)
                self.Gender_DataDisplay.config(text=self.Gender)

                return student_data

        except TclError:
            pass
   #handle the functionality of adding new data to the GUI application. 
    def add(self):
        if not self.addCheck:
            if not self.editCheck:
                self.UserDataFrame.Var_IDNo.set('')
                self.UserDataFrame.Var_FullName.set('')
                self.UserDataFrame.Var_Course.set('')
                self.UserDataFrame.Var_Year.set('')
                self.UserDataFrame.Var_Gender.set('')


                self.after_edit_button(self.UserDataFrame, "add")
                self.addCheck = True


    # this method handles user input, save it to a CSV file, update the UI accordingly, and handle file-related exceptions gracefully.
    def get_input(self):
        try:
            x = self.UserDataFrame.single_data_input


            cmd.csv_data_add(self.filepath, x)
            self.before_edit_button(self.UserDataFrame)
            self.update_list()
            self.IDNo_DataDisplay.config(text=self.UserDataFrame.Var_IDNo.get())
            self.FullName_DataDisplay.config(text=self.UserDataFrame.Var_FullName.get())
            self.Course_DataDisplay.config(text=self.UserDataFrame.Var_Course.get())
            self.Year_DataDisplay.config(text=self.UserDataFrame.Var_Year.get())
            self.Gender_DataDisplay.config(text=self.UserDataFrame.Var_Gender.get())
        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            self.before_edit_button(self.UserDataFrame)
#updates the treeview with the latest data obtained from the csv file.
    def update_list(self):
        self.treeview.treeview_update(cmd.csv_read(self.filepath))
# this method handles the completion of adding or editing data in the GUI application, 
# performing input validation, updating the data source (CSV file), and refreshing the UI components.
    def doneFunc(self, check):
        try:
            if not self.rex.match(self.UserDataFrame.Var_IDNo.get()):
                raise IDInvalid
        except IDInvalid:
                showerror("Invalid Input for ID", "Invalid Input. \nID must be in \nYYYY-NNNN format.")
                return
        if check == "add":
            self.addCheck = False
            self.editCheck = False
            self.ID_removedisplay_check = False
            self.get_input()

        elif check == "edit":
            self.addCheck = False
            self.editCheck = False
            self.ID_removedisplay_check = False
            x = self.UserDataFrame.single_data_input
            self.dataread_list[self.index] = x

            cmd.csv_data_edit(self.filepath, self.dataread_list)
            self.before_edit_button(self.UserDataFrame)

            self.update_list()
            self.IDNo_DataDisplay.config(text=self.UserDataFrame.Var_IDNo.get())
            self.FullName_DataDisplay.config(text=self.UserDataFrame.Var_FullName.get())
            self.Course_DataDisplay.config(text=self.UserDataFrame.Var_Course.get())
            self.Year_DataDisplay.config(text=self.UserDataFrame.Var_Year.get())
            self.Gender_DataDisplay.config(text=self.UserDataFrame.Var_Gender.get())

#this method effectively updates the GUI interface to allow the user to edit or add new data entries, 
#providing appropriate entry fields and controls for the specified action type.
    def after_edit_button(self, classObj, type=""):
      #destroys the existing display elements
        self.IDNo_DataDisplay.destroy()
        self.FullName_DataDisplay.destroy()
        self.Course_DataDisplay.destroy()
        self.Year_DataDisplay.destroy()
        self.Gender_DataDisplay.destroy()

      #styling of the widgets
        self.Entry_IDNo = ttk.Entry(classObj, textvariable=classObj.Var_IDNo, style="UserDataDisplay.TEntry", width=10, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(classObj, textvariable=classObj.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))
        self.Entry_Course = ttk.OptionMenu(classObj, classObj.Var_Course, self.course_tuple[0],*self.course_tuple, style = "UserDataDisplay.TMenubutton")
        self.Option_Year = ttk.OptionMenu(classObj, classObj.Var_Year, self.year_tuple[0], *self.year_tuple, style = "UserDataDisplay.TMenubutton")
        self.Option_Gender = ttk.OptionMenu(classObj, classObj.Var_Gender, self.gender_tuple[0], *self.gender_tuple, style = "UserDataDisplay.TMenubutton")

      #button creation
        self.Button_Done = Button(classObj, text="Done", relief=RAISED, fg="orange", bg="blue", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.doneFunc(type))
       #grid placements
        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)
        self.Entry_Course.grid(row=3, column=4, pady = 20, sticky = "w")
        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")

        #The user can input a new ID without manually deleting the placeholder text
        if type == "add":
            classObj.Var_IDNo.set("YYYY-NNNN")
            def ID_removedisplay(event):
                if not self.ID_removedisplay_check:
                    if classObj.Var_IDNo.get() == "YYYY-NNNN":
                        event.widget.delete(0, END)
                    self.ID_removedisplay_check = True
            self.Entry_IDNo.bind("<Button-1>", ID_removedisplay)

        self.Button_Done.grid(row=5, column=5, sticky="e")


    #this method effectively reverts the GUI interface to its original state
    def before_edit_button(self, classObj):
       #destroys the widgets before hand
        self.Entry_IDNo.destroy()
        self.Entry_FullName.destroy()
        self.Entry_Course.destroy()
        self.Option_Year.destroy()
        self.Option_Gender.destroy()
        self.Button_Done.destroy()
       #the styles of the label
        self.IDNo_DataDisplay = ttk.Label(classObj, text=self.IDNo, style = "UserDataDisplay.TLabel")
        self.FullName_DataDisplay = ttk.Label(classObj, text=self.FullName, style = "UserDataDisplay.TLabel")
        self.Course_DataDisplay = ttk.Label(classObj, text=self.Course, style = "UserDataDisplay.TLabel")
        self.Year_DataDisplay = ttk.Label(classObj, text=self.Year, style = "UserDataDisplay.TLabel")
        self.Gender_DataDisplay = ttk.Label(classObj, text=self.Gender, style = "UserDataDisplay.TLabel")
       #grid positioning
        self.IDNo_DataDisplay.grid(row=1, column=4, pady = 20, sticky = "ew", padx=5)
        self.FullName_DataDisplay.grid(row=2, column=4, pady = 20, sticky = "ew", padx=5)
        self.Course_DataDisplay.grid(row=3, column=4, pady = 20, sticky = "ew", padx=5)
        self.Year_DataDisplay.grid(row=4, column=4, pady = 20, sticky = "ew", padx=5)
        self.Gender_DataDisplay.grid(row=5, column=4, pady = 20, sticky = "ew", padx=5)

#this method facilitates the process of editing selected items in the GUI interface by populating entry widgets with the data of the selected item and updating the interface to enable editing.
    def edit_choice(self):
        if not self.editCheck:
            if not self.addCheck:
                try:
                    edit_list = self.item_selected('<<TreeviewSelect>>')


                    self.dataread_list = cmd.csv_read(self.filepath)
                    for index, item in enumerate(self.dataread_list):
                        if item == edit_list:

                            self.index = index
                            break

                    try:
                        self.UserDataFrame.Var_IDNo.set(edit_list[0])
                        self.UserDataFrame.Var_FullName.set(edit_list[1])
                        self.UserDataFrame.Var_Course.set(edit_list[2])

                        self.after_edit_button(self.UserDataFrame, "edit")

                        self.UserDataFrame.Var_Year.set(edit_list[3])
                        self.UserDataFrame.Var_Gender.set(edit_list[4])
                        self.editCheck = True

                    except TypeError:
                        showwarning("Error", "Choose a row first before clicking 'Edit'.")

                except FileNotFoundError:
                    showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")

                except TclError:
                    pass
#this method provides a popup confirmation for deleting selected items in the GUI interface, ensuring that deletion is performed only when confirmed by the user.
    def delete_choice_popup(self):
        if not self.editCheck and not self.addCheck:
            try:
                delete_list = self.item_selected('<<TreeviewSelect>>')
                self.UserDataFrame.Var_IDNo.set(delete_list[0])

                delete_warn_widget = askyesno(title = "Delete?", message = "Are you sure you want to delete the selected row?")

                if delete_warn_widget:
                    self.delete_choice()


            except FileNotFoundError:
                showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            except TypeError:
                showwarning("Error", "Choose a row first before clicking 'Delete'.")
            except TclError:
                pass



#this method handles the complete process of deleting a selected item from the GUI interface, including updating the CSV file and refreshing the displayed data.
    def delete_choice(self):
        delete_list = self.item_selected('<<TreeviewSelect>>')

        self.dataread_list = cmd.csv_read(self.filepath)

        for index, item in enumerate(self.dataread_list):
            if item == delete_list:

                self.index = index
                break

        cmd.csv_data_delete(self.filepath, self.index)
        self.IDNo_DataDisplay.config(text='')
        self.FullName_DataDisplay.config(text='')
        self.Course_DataDisplay.config(text='')
        self.Year_DataDisplay.config(text='')
        self.Gender_DataDisplay.config(text='')
        self.update_list()

# this method provides the functionality to search for specific items in the CSV data and display only the matching items in the GUI interface.
    def search(self, search_input):
        if search_input == '':
            self.treeview.treeview_update(cmd.csv_read(self.filepath))
        try:
            self.dataread_list = cmd.csv_read(self.filepath)

            did_break = False
            search_display = []
            self.treeview.selection_set()
            for index, item in enumerate(self.dataread_list):
                if search_input in item[0] or search_input in item[1]:
                    search_display.append(item)


            self.treeview.treeview_update(search_display)
            try:
                self.treeview.selection_set('I001')
            except TclError:
                pass

        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")

#creates an instance of Method_List, Main_App_Window, then starts the GUI Loop
if __name__ == '__main__':
    cmd = Method_List()
    app = Main_App_Window()
    app.mainloop()
