from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo, showerror
from tkinter.messagebox import askyesno
from tkinter import filedialog as fd
from Methods import Methods_List
import csv


import re



"""Classes"""

class Error(Exception):
    pass

class IDInvalid(Error):
    pass

#Frame for the treeview
class DatabaseDisplay(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=('id_no', 'name', 'course', 'year', 'gender'), show="headings", height = 16, style = "Treeview")

        dtbStyle = ttk.Style()
        dtbStyle.configure("Treeview", font=("Lucida Sans", "15"))
        dtbStyle.configure("Treeview.Heading", font=("Lucida Sans", "15"), background="black")


        self.heading('#0', text='', anchor=CENTER)
        self.heading('id_no', text='ID Number')
        self.heading('name', text='Name')
        self.heading('course', text='Course')
        self.heading('year', text='Year')
        self.heading('gender', text='Gender')

        self.column('#0', width=0, stretch=NO)
        self.column('id_no', width=120, minwidth= 100, anchor = CENTER)
        self.column('name', width=252, minwidth= 250, anchor = CENTER)
        self.column('course', width=125, minwidth= 100, anchor = CENTER)
        self.column('year', width=60, minwidth= 20, anchor = CENTER)
        self.column('gender', width=70, minwidth= 20, anchor = CENTER)

        self.grid(row=0, column=0, sticky = "nsew", ipadx = 105, ipady=10)

        scrollbar = ttk.Scrollbar(master, orient=VERTICAL, command=self.yview, cursor='sb_v_double_arrow')
        self.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky='ns',)

    #updates the treeview everytime we call it
    def Treeview_Update(self, student_list):


        for i in self.get_children():
            self.delete(i)

        if self.master.master.filepath == '':
            showinfo("Student Information System", "To start, click on 'File' and choose 'New' or 'Open'.")

        count = 1
        for element in student_list:
            rowid = 'I' + str('{:03}'.format(count))
            self.insert('', END, iid=rowid, values=element)
            count += 1

#Frame for the labels
class UserDataDisplay(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="UserDataDisplay.TFrame", height = 315, width = 410)


        self.grid_propagate(0)

        self.Var_IDNo = StringVar()
        self.Var_FullName = StringVar()
        self.Var_Course = StringVar()
        self.Var_Year = StringVar()
        self.Var_Gender = StringVar()
        self._single_data_input = []

        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("UserDataDisplay.TFrame", background="#8E3E63")
        UserDataDisplay_style.configure("UserDataDisplay.TLabel", background="#8E3E63", foreground="white", font=("Lucida Sans", "16", "bold"), justify=CENTER)
        UserDataDisplay_style.configure("UserDataDisplay.TEntry", foreground="black")
        UserDataDisplay_style.configure("UserDataDisplay.TMenubutton", font=('Lucida Sans', "16", 'bold'))


        Label_IDNo = ttk.Label(self, text="ID No:", style = "UserDataDisplay.TLabel")
        Label_FullName = ttk.Label(self, text="Name:", style = "UserDataDisplay.TLabel")
        Label_Course = ttk.Label(self, text="Course:", style = "UserDataDisplay.TLabel")
        Label_Year = ttk.Label(self, text="Year:", style = "UserDataDisplay.TLabel")
        Label_Gender = ttk.Label(self, text="Gender:", style = "UserDataDisplay.TLabel")






        self.grid(row=0, column=3, rowspan = 5, padx=2, pady=2, ipadx=24, ipady=20, columnspan = 5)

        Label_IDNo.grid(row=1, column=3, pady = 20, sticky = "sw", padx=25)
        Label_FullName.grid(row=2, column=3, pady = 20, sticky = "w", padx=25)
        Label_Course.grid(row=3, column=3, pady = 20, sticky = "w", padx=15)
        Label_Year.grid(row=4, column=3, pady = 20, sticky = "w", padx=30)
        Label_Gender.grid(row=5, column=3, pady = 20, sticky = "w", padx=15)



    @property
    def single_data_input(self):

        self._single_data_input = [str(self.Var_IDNo.get()), str(self.Var_FullName.get()), str(self.Var_Course.get()), str(self.Var_Year.get()), str(self.Var_Gender.get())]
        return self._single_data_input

    @single_data_input.setter
    def single_data_input(self, value):
        self._single_data_input = value

#Frame for the buttons
class ButtonsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="BF.TFrame", height = 153, width = 171)

        searchvar = StringVar()

        self.grid_propagate(0)

        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("BF.TFrame", background="#8E3E63")
        UserDataDisplay_style.configure("BF.TLabel", background="#8E3E63", foreground="white", font=("Roboto Mono", "10", "bold"))

        self.grid(row=6, column=3, sticky = "nws", rowspan = 5, padx=2, pady=2, ipadx=143, ipady=20, columnspan = 5)

        Add_Button = Button(self, text="Add", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = master.master.master.add)
        Edit_Button = Button(self, text="Edit", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = master.master.master.edit_choice)
        Delete_Button = Button(self, text="Delete", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = master.master.master.delete_choice_popup)
        Search_Entry = ttk.Entry(self, textvariable=searchvar, style="UserDataDisplay.TEntry", width=25, font=('Lucida Sans', "16", 'bold'))

        def search_entry_type(event):
            try:
                cmd.csv_read(master.master.master.filepath)
                master.master.master.search(searchvar.get())
            except FileNotFoundError:
                pass

        Search_Entry.bind("<KeyRelease>", search_entry_type)
        Search_Button = Button(self, text="Search", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: master.master.master.search(searchvar.get()))

        Display_Course_Button = Button(self, text= "Courses", relief=RAISED, fg="white", bg="#8E3E63", height = 1, font=('Lucida Sans', "16", 'bold'), command = lambda: master.master.master.course_window_init())

        Add_Button.grid(row=0, column=0, padx=20, pady=20, sticky = "news")
        Edit_Button.grid(row=0, column=2, padx=48, pady=20, sticky = "news")
        Delete_Button.grid(row=0, column=4, padx=20, pady=20, sticky = "news")
        Search_Entry.grid(row=1, column=0, sticky = "ns", columnspan = 5, pady=10)
        Search_Button.grid(row=2, column=0, sticky="ns", columnspan=2, pady=10)  # Adjusted column to 2
        Display_Course_Button.grid(row=2, column=3, padx=10, columnspan=2)



#the main app to run
class App(Tk):
    def __init__(self):
        super().__init__()
        # Regular expression for validation (e.g., student ID format)
        self.rex = re.compile("^[0-9]{4}[-][0-9]{4}$")

        # Initialize instance variables for storing student information
        self.IDNo = ''       # Student ID number
        self.FullName = ''   # Full name of the student
        self.Course = ''     # Course enrolled
        self.Year = ''       # Year of study
        self.Gender = ''     # Gender of the student

        # Initialize other instance variables
        self.dataread_list = []      # List for storing read data
        self.index = 0               # Index for navigating through data
        self.filepath = ''           # File path for saving/loading data

        # Flags for managing application state
        self.addCheck = False        # Flag to check if adding a new entry
        self.editCheck = False       # Flag to check if editing an entry
        self.ID_removedisplay_check = False  # Flag for display control when ID is removed

        # Set up the main window
        self.title("Student Information System")
        self.geometry("1365x670+0+0")  # Set the window size and position

        # Set minimum and maximum window size
        self.wm_minsize(1365, 670)
        self.wm_maxsize(1365, 670)

        # Start the window in maximized state
        self.state('zoomed')


        style = ttk.Style()
        style.configure("Treeview.Heading", rowheight = 40)
        style.configure("Treeview", rowheight = 40)
        

        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File",menu=file_menu)

        file_menu.add_command(label="New            'Creates a new CSV file and opens it.'", command = self.new_file)
        file_menu.add_command(label="Open           'Opens a CSV file.'", command = self.select_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close          'Closes the program'", command = self.close_file)

        framestyle = ttk.Style()
        framestyle.configure("mainframe.TFrame", background="#D2649A")
        framestyle.configure("secondframe.TFrame", background='#D2649A')
        framestyle.configure("dataFrame.TFrame", background='white')


        mainframe = ttk.Frame(self, style="mainframe.TFrame")
        mainframe.grid(row=0, column=0, sticky = "news", rowspan = 40, columnspan = 3, ipadx=2)
        self.treeview = DatabaseDisplay(mainframe)


        secondframe = ttk.Frame(self, style="secondframe.TFrame")
        secondframe.grid(row=0, column=3, sticky = "news", rowspan = 40, ipadx=8)



        frame1 = ttk.Frame(secondframe, style="dataFrame.TFrame")
        frame1.grid(row=0, column=3, sticky = "news", rowspan=5, ipadx=0, padx = 20, ipady = 0, columnspan = 5, pady = 30)

        frame2 = ttk.Frame(secondframe, style="dataFrame.TFrame", height = 197, width = 461)
        frame2.grid(row=6, column=3, sticky = "nws", ipadx=0, padx = 20, columnspan = 5, pady = 40)

        frame2.grid_propagate(0)

        self.UserDataFrame = UserDataDisplay(frame1)
        UserButtonsFrame = ButtonsFrame(frame2) #needed to make the buttons appear on screen

        self.treeview.Treeview_Update(self.filepath)


        self.Entry_IDNo = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_IDNo, style="UserDataDisplay.TEntry", width=9, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))

        self.course_tuple = Methods_List.read_course_csv('Courses.csv')
        self.Entry_Course = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Course, self.course_tuple[0], *self.course_tuple)
        

        self.year_tuple = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Irregular")
        self.Option_Year = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Year, self.year_tuple[0], *self.year_tuple)

        

        self.gender_tuple = ("-----", "Male", "Female", "Other")
        self.Option_Gender = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Gender, self.gender_tuple[0], *self.gender_tuple)

        self.Button_Done = Button(self.UserDataFrame, text="Done", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = self.doneFunc)

        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)
        self.Entry_Course.grid(row=3, column=4, pady = 20, sticky = "w")
        

        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")

        self.Button_Done.grid(row=5, column=5, sticky="nw")

        self.before_edit_button(self.UserDataFrame)
        self.treeview.bind('<<TreeviewSelect>>', self.item_selected)
#closes the APP
    def close_file(self): #ward
        close_window = askyesno("Close Student Information System?", "Are you sure you want to exit?")
        if close_window:
            self.destroy()

#creates a new student csv file
    def new_file(self):
        temp = self.filepath
        filetypes = (('CSV Files', '*.csv'),)

        filename = fd.asksaveasfilename(title='Create a new file', initialdir='*', filetypes=filetypes, initialfile = "New CSV", defaultextension = ".csv")

        self.filepath = filename

        if self.filepath == '':
            self.filepath = temp
        else:
            cmd.csv_create(self.filepath)

        self.treeview.Treeview_Update(cmd.csv_read(self.filepath))

    def select_file(self):
        filetypes = (('CSV Files', '*.csv'),)
        filename = fd.askopenfilename(title='Open a file', initialdir='*', filetypes=filetypes)
        self.filepath = filename
        self.treeview.Treeview_Update(cmd.csv_read(self.filepath))

    # updates the corresponding display widgets in the UI, and returns the selected student's data as a list. 
    def item_selected(self, event):
        try:
            for student_selected in self.treeview.selection():
                item = self.treeview.item(student_selected)
                student_data = item['values']

                self.IDNo, self.FullName, self.Course, self.Year, self.Gender = student_data
                self.IDNo = str(self.IDNo)
                self.FullName = str(self.FullName)


                self.Course = str(self.Course)
                self.Year = str(self.Year)
                self.Gender = str(self.Gender)
                student_data = [self.IDNo, self.FullName, self.Course, self.Year, self.Gender]

                self.IDNo_DataDisplay.config(text=self.IDNo)
                self.FullName_DataDisplay.config(text=self.FullName)
                self.Course_DataDisplay.config(text=self.Course)
                self.Year_DataDisplay.config(text=self.Year)
                self.Gender_DataDisplay.config(text=self.Gender)


                return student_data

        except TclError:
            pass



    #the function for the course window, everytime we click the course button this pops up
    def course_window_init(self): 
        course_window = Toplevel(self, bg="#D2649A")
        course_window.geometry("500x500")
        course_window.grid_propagate(0)

        course_window.grid_columnconfigure(0, weight=1)
        course_window.grid_rowconfigure(0, weight=1)

        self.cinput = StringVar()

        self.course_treeview = ttk.Treeview(course_window, columns=('course_code', 'course_name'), show="headings", height = 5, style = "Treeview")


        self.course_treeview.heading('#0', text='', anchor=CENTER)
        self.course_treeview.heading('course_code', text='Code')
        self.course_treeview.heading('course_name', text='Name')


        self.course_treeview.column('#0', width=0, stretch=NO)
        self.course_treeview.column('course_code', width=5, minwidth= 1)
        self.course_treeview.column('course_name', width=250, minwidth= 1)


        self.course_treeview.grid(row=0, column=0, sticky = "nsew")

        scrollbars = ttk.Scrollbar(course_window, orient=VERTICAL, command=self.course_treeview.yview, cursor='sb_v_double_arrow')
        self.course_treeview.configure(yscroll=scrollbars.set)

        scrollbars.grid(row=0, column=1, sticky='ns',)

        course_buttons_frame = Frame(course_window, width = 100, height = 500, bg = "#243447")
        course_buttons_frame.grid(row = 0, column = 2)
        course_buttons_frame.pack_propagate(False)

        Label(course_buttons_frame, bg = "#243447", text = '').pack(pady=20)
        Button(course_buttons_frame, text = "Add", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.addcourse(course_window)).pack(padx = 10, pady = 20)
        Button(course_buttons_frame, text = "Edit", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.editcourse(course_window)).pack(padx = 10, pady = 20)
        Button(course_buttons_frame, text = "Delete", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.delcourse(course_window)).pack(padx = 10, pady = 20)
        
        


        self.course_treeview.bind('<<TreeviewSelect>>', self.course_selected)

        self.courseDisplay()



    def courseDisplay(self):
        course_list = []

        # Clear current items in the Treeview
        for i in self.course_treeview.get_children():
            self.course_treeview.delete(i)

        # Read data from the CSV file
        try:
            with open('Courses.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                # Assuming the CSV has headers and skipping the header row
                next(reader)
                for row in reader:
                    course_list.append(row)

            # Insert each course into the Treeview with a unique row ID
            count = 1
            for element in course_list:
                rowid = 'I' + str('{:03}'.format(count))
                self.course_treeview.insert('', END, iid=rowid, values=element)
                count += 1
        except FileNotFoundError:
            # Handle the case where the file is not found
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
        except Exception as e:
            # Handle other potential exceptions
            print(f"An error occurred: {e}")


    def course_selected(self, event):
        course_row = ''
        for items in self.course_treeview.selection():
            course_row = self.course_treeview.item(items)
            course_row = course_row['values']

        return course_row


    def editcourse(self, course_window):
        coursename_entry = StringVar()
        coursecode_entry = StringVar()

        editcourse_selected = self.course_selected("<<TreeviewSelect>>")
        initial_ccode = editcourse_selected[0]

        editcourse_Toplevel = Toplevel(self, bg="#243447")
        editcourse_Toplevel.geometry("400x200")
        editcourse_Toplevel.pack_propagate(False)

        rowa = Frame(editcourse_Toplevel, bg="#243447", width=400, height=50)
        rowa.pack(anchor="w")
        rowa.pack_propagate(False)
        rowb = Frame(editcourse_Toplevel, bg="#243447", width=400, height=50)
        rowb.pack(anchor="w")
        rowb.pack_propagate(False)
        rowc = Frame(editcourse_Toplevel, bg="#243447", width=400, height=50)
        rowc.pack(anchor="w")
        rowc.pack_propagate(False)
        rowd = Frame(editcourse_Toplevel, bg="#243447", width=400, height=50)
        rowd.pack(anchor="w")
        rowd.pack_propagate(False)

        Label(rowa, fg="white", bg="#243447", text='Edit Course', font=('Lucida Sans', "16", 'bold')).pack(side=LEFT, padx=10)
        Label(rowb, fg="white", bg="#243447", text='Course Code: ', font=('Lucida Sans', "14", 'bold')).pack(side=LEFT, padx=10)
        Label(rowc, fg="white", bg="#243447", text='Course Name:', font=('Lucida Sans', "14", 'bold')).pack(side=LEFT, padx=10)

        Entry(rowb, width=5, font=('Lucida Sans', "16", 'bold'), textvariable=coursecode_entry).pack(side=LEFT, padx=10, anchor="w")
        Entry(rowc, width=15, font=('Lucida Sans', "16", 'bold'), textvariable=coursename_entry).pack(side=LEFT, padx=10, anchor="w")

        coursecode_entry.set(editcourse_selected[0])
        coursename_entry.set(editcourse_selected[1])

        Button(rowd, text="Edit", relief=RAISED, fg="white", bg="#8E3E63", height=1, width=6, font=('Lucida Sans', "16", 'bold'),
               command=lambda: self.editcourse_confirm(editcourse_Toplevel, coursecode_entry, coursename_entry, course_window, initial_ccode)).pack(side=LEFT, padx=10)

    def editcourse_confirm(self, courseedit, ccode, cname, course_window, initial_ccode):
        try:
            courseedit.destroy()

            ccode = ccode.get().strip()
            cname = cname.get().strip()

            if not ccode or not cname:
                raise ValueError("Course code and name cannot be empty.")

            updated_courses = []
            course_updated = False

            # Read the existing courses from the CSV
            with open('Courses.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Read the header
                for row in reader:
                    if row[0] == initial_ccode:
                        row[0] = ccode
                        row[1] = cname
                        course_updated = True
                    updated_courses.append(row)

            # Check for duplicate course code
            if not course_updated:
                for row in updated_courses:
                    if row[0] == ccode and row[0] != initial_ccode:
                        raise ValueError("The course code that you entered already exists.")

            # Write the updated courses back to the CSV
            with open('Courses.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)  # Write the header
                writer.writerows(updated_courses)

            # Update students with the old course code
            updated_students = []
            with open(self.filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                student_header = next(reader)  # Read the header
                for row in reader:
                    if row[2] == initial_ccode: 
                        row[2] = ccode
                    updated_students.append(row)

            with open(self.filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(student_header)  # Write the header
                writer.writerows(updated_students)

            self.treeview.Treeview_Update(cmd.csv_read(self.filepath))

            showinfo("Success", f"'{initial_ccode}' has been successfully edited.")
            course_window.focus()
            self.courseDisplay()
        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            course_window.focus()
        except ValueError as e:
            showwarning("Invalid Input", str(e))
            course_window.focus()
        except Exception as e:
            print(f"An error occurred: {e}")
            showwarning("Error", "An error occurred while editing the course.")
            course_window.focus()

    def delcourse(self, course_window):
        course_delete_warn = askyesno(title = "Delete?", message = "Are you sure you want to delete the selected row?")

        if course_delete_warn:
            self.delcourse_confirm(course_window)
            

    def delcourse_confirm(self, course_window):
        try:
            selected_course = self.course_selected("<<TreeviewSelect>>")
            if not selected_course:
                showwarning("No Selection", "Please select a course to delete.")
                return

            course_code_to_delete = selected_course[0]

            # List to hold updated courses
            updated_courses = []
            # Flag to check if the course was deleted
            course_deleted = False

            # Read the existing courses from the CSV
            with open('Courses.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Read the header
                for row in reader:
                    if len(row) > 0 and row[0] != course_code_to_delete:
                        updated_courses.append(row)
                    else:
                        if len(row) > 0:
                            course_deleted = True

            if not course_deleted:
                showwarning("Not Found", "The selected course was not found.")
                return

            # Write the updated courses back to the CSV
            with open('Courses.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)  # Write the header
                writer.writerows(updated_courses)

            # Update the student CSV file to replace occurrences of the deleted course code with 'N/A'
            with open(self.filepath, 'r', newline='') as studentfile:
                student_reader = csv.reader(studentfile)
                student_data = list(student_reader)

            updated_student_data = []
            for row in student_data:
                if len(row) > 2 and row[2] == course_code_to_delete:
                    row[2] = 'N/A'  # Replace the course code with 'N/A'
                updated_student_data.append(row)

            # Write the updated student data back to the CSV file
            with open(self.filepath, 'w', newline='') as studentfile:
                student_writer = csv.writer(studentfile)
                student_writer.writerows(updated_student_data)

            self.treeview.Treeview_Update(cmd.csv_read(self.filepath))

            showinfo("Success", f"The course '{course_code_to_delete}' has been successfully removed from the courses.")
            course_window.focus()
            self.courseDisplay()

        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            course_window.focus()
        except IndexError as e:
            print(f"IndexError occurred: {e}")
            showwarning("Error", "Index out of range for courses.")
            course_window.focus()
        except Exception as e:
            print(f"An error occurred: {e}")
            showwarning("Error", "An error occurred while deleting the course.")
            course_window.focus()


    def addcourse(self, course_window):


        coursename_entry = StringVar()
        coursecode_entry = StringVar()

        addcourse_Toplevel = Toplevel(self, bg="#243447")
        addcourse_Toplevel.geometry("400x200")
        addcourse_Toplevel.pack_propagate(False)

        rowa = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowa.pack(anchor = "w")
        rowa.pack_propagate(False)
        rowb = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowb.pack(anchor = "w")
        rowb.pack_propagate(False)
        rowc = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowc.pack(anchor = "w")
        rowc.pack_propagate(False)
        rowd = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowd.pack(anchor = "w")
        rowd.pack_propagate(False)


        Label(rowa, fg = "white", bg = "#243447", text = 'Add Course', font=('Lucida Sans', "16", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowb, fg = "white", bg = "#243447", text = 'Course Code: ', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowc, fg = "white", bg = "#243447", text = 'Course Name:', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)

        Entry(rowb, width = 5, font=('Lucida Sans', "16", 'bold'), textvariable = coursecode_entry).pack(side = LEFT, padx = 10, anchor = "w")
        Entry(rowc, width = 15, font=('Lucida Sans', "16", 'bold'), textvariable = coursename_entry).pack(side = LEFT, padx = 10, anchor = "w")

        Button(rowd, text = "Add", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.addcourse_confirm(addcourse_Toplevel, coursecode_entry, coursename_entry, course_window)).pack(side = LEFT, padx = 10)

    def addcourse_confirm(self, coursetop, ccode, cname, course_window):
        try:
            coursetop.destroy()

            new_course_code = ccode.get()
            new_course_name = cname.get()

            # Read existing courses from the CSV
            existing_courses = set()
            with open('Courses.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip the header
                for row in reader:
                    existing_courses.add(row[0])

            # Check if the new course code already exists
            if new_course_code in existing_courses:
                raise ValueError("The course code that you entered already exists.")

            # Add the new course to the CSV file
            with open('Courses.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([new_course_code, new_course_name])

            showinfo("Success", f"'{new_course_code}' has been successfully added to the courses.")
            course_window.focus()
            self.courseDisplay()
        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            course_window.focus()
        except ValueError as e:
            showwarning("Invalid Input", str(e))
            course_window.focus()
        except Exception as e:
            print(f"An error occurred: {e}")
            showwarning("Error", "An error occurred while adding the course.")
            course_window.focus()


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


    def get_input(self):
        # Assuming self.filepath holds the path to the CSV file
        if not self.filepath:
            showwarning("File Error", "No CSV file selected.")
            return

        # Read the CSV file to check for duplicates
        with open(self.filepath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row
            for row in reader:
                
                if row[0] == self.UserDataFrame.Var_IDNo.get():
                    showwarning("Duplicate Entry", "A student with the same ID already exists in the CSV file.")
                    return

        # Proceed to add the student to the CSV file
        x = self.UserDataFrame.single_data_input
        with open(self.filepath, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(x)

        # Update the display and reset input fields as needed
        self.update_list()
        self.before_edit_button(self.UserDataFrame)
        self.IDNo_DataDisplay.config(text=self.UserDataFrame.Var_IDNo.get())
        self.FullName_DataDisplay.config(text=self.UserDataFrame.Var_FullName.get())
        self.Course_DataDisplay.config(text=self.UserDataFrame.Var_Course.get())
        self.Year_DataDisplay.config(text=self.UserDataFrame.Var_Year.get())
        self.Gender_DataDisplay.config(text=self.UserDataFrame.Var_Gender.get())



    def update_list(self):
        self.treeview.Treeview_Update(cmd.csv_read(self.filepath))

    def doneFunc(self, check):
        try:
            if not self.rex.match(self.UserDataFrame.Var_IDNo.get()) and not self.rex.match(self.UserDataFrame.Var_Course.get()):
                raise IDInvalid
        except IDInvalid:
            showerror("Invalid Input for ID or Course code already exists", "Invalid Input. \nID must be in \nYYYY-NNNN format.")
            return
        
        if check == "add":
            self.addCheck = False
            self.editCheck = False
            self.ID_removedisplay_check = False
            self.get_input()

        elif check == "edit":
            # Fetch the new ID that the user wants to set
            new_id = self.UserDataFrame.Var_IDNo.get()
            current_id = self.dataread_list[self.index][0]

            # Check if the ID is actually being changed
            if new_id != current_id:
                # Check if the new ID already exists in the CSV
                if self.is_id_existing(new_id):
                    showerror("Error", "Student ID already exists.")
                    return

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

    def is_id_existing(self, student_id):
        with open(self.filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == student_id:
                    return True
        return False

    def after_edit_button(self, classObj, type=""):

        self.IDNo_DataDisplay.destroy()
        self.FullName_DataDisplay.destroy()
        self.Course_DataDisplay.destroy()
        self.Year_DataDisplay.destroy()
        self.Gender_DataDisplay.destroy()


        self.Entry_IDNo = ttk.Entry(classObj, textvariable=classObj.Var_IDNo, style="UserDataDisplay.TEntry", width=10, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(classObj, textvariable=classObj.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))
        self.Entry_Course = ttk.OptionMenu(classObj, classObj.Var_Course, self.course_tuple[0],*self.course_tuple, style = "UserDataDisplay.TMenubutton")

        self.Option_Year = ttk.OptionMenu(classObj, classObj.Var_Year, self.year_tuple[0], *self.year_tuple, style = "UserDataDisplay.TMenubutton")
        self.Option_Gender = ttk.OptionMenu(classObj, classObj.Var_Gender, self.gender_tuple[0], *self.gender_tuple, style = "UserDataDisplay.TMenubutton")
        self.Button_Done = Button(classObj, text="Done", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.doneFunc(type))

        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)
        self.Entry_Course.grid(row=3, column=4, pady = 20, sticky = "w")
    

        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")

        #code for preinserting of YYYY-NNNN format when clicking add button
        if type == "add":
            classObj.Var_IDNo.set("YYYY-NNNN")
            def ID_removedisplay(event):
                if not self.ID_removedisplay_check:
                    if classObj.Var_IDNo.get() == "YYYY-NNNN":
                        event.widget.delete(0, END)
                    self.ID_removedisplay_check = True
            self.Entry_IDNo.bind("<Button-1>", ID_removedisplay)

        self.Button_Done.grid(row=5, column=5, sticky="e")



    def before_edit_button(self, classObj):

        self.Entry_IDNo.destroy()
        self.Entry_FullName.destroy()
        self.Entry_Course.destroy()
        self.Option_Year.destroy()
        self.Option_Gender.destroy()
        self.Button_Done.destroy()

        self.IDNo_DataDisplay = ttk.Label(classObj, text=self.IDNo, style = "UserDataDisplay.TLabel")
        self.FullName_DataDisplay = ttk.Label(classObj, text=self.FullName, style = "UserDataDisplay.TLabel")
        self.Course_DataDisplay = ttk.Label(classObj, text=self.Course, style = "UserDataDisplay.TLabel")
        self.Year_DataDisplay = ttk.Label(classObj, text=self.Year, style = "UserDataDisplay.TLabel")
        self.Gender_DataDisplay = ttk.Label(classObj, text=self.Gender, style = "UserDataDisplay.TLabel")

        self.IDNo_DataDisplay.grid(row=1, column=4, pady = 20, sticky = "ew", padx=5)
        self.FullName_DataDisplay.grid(row=2, column=4, pady = 20, sticky = "ew", padx=5)
        self.Course_DataDisplay.grid(row=3, column=4, pady = 20, sticky = "ew", padx=5)
        self.Year_DataDisplay.grid(row=4, column=4, pady = 20, sticky = "ew", padx=5)
        self.Gender_DataDisplay.grid(row=5, column=4, pady = 20, sticky = "ew", padx=5)


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


    def search(self, search_input):
        try:
            # Read data from CSV
            self.dataread_list = cmd.csv_read(self.filepath)

            if search_input == '':
                # Update treeview if search input is empty
                self.treeview.Treeview_Update(self.dataread_list)
            else:
                # Initialize an empty list to store search results
                search_display = []

                # Clear current selection in the treeview
                self.treeview.selection_set()

                # Search through the CSV data
                for index, item in enumerate(self.dataread_list):
                    if search_input in item[0] or search_input in item[1]:
                        search_display.append(item)

                # Update the treeview with search results
                self.treeview.Treeview_Update(search_display)

                try:
                    # Set the selection to the first item, if available
                    self.treeview.selection_set('I001')
                except TclError:
                    # Handle the case where the item might not exist
                    pass
        except FileNotFoundError:
            # Handle the case where the file is not found
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
        except Exception as e:
            # Handle other potential exceptions
            print(f"An error occurred: {e}")
        finally:
            # Any cleanup code can be added here
            pass


if __name__ == '__main__':
    cmd = Methods_List()
    app = App()
    app.mainloop()
