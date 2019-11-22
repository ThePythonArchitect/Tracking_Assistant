import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText as Scrollbox
from tkinter.filedialog import askopenfilename as openfile
import webbrowser
import os
from threading import Thread
import subprocess

import pickle


class Gui:

    def __init__(self, debug):

        self.app = tk.Tk()
        self.app.geometry("1000x600")
        self.app.title("Tracking Assistant")
        self.app.resizable(False, False)
        self.app.iconbitmap("icon.ico")
        self.light_theme_colors = {
            "fg": "black",
            "bg": "gray90",
            "bg2": "white"
            }
        self.dark_theme_colors = {
            "fg": "white",
            "bg": "gray15",
            "bg2": "black"
            }
        self.custom_theme_colors = self.get_custom_colors()
        self.fg_color = self.light_theme_colors["fg"]
        self.bg_color = self.light_theme_colors["bg"]
        self.bg2_color = self.light_theme_colors["bg2"]
        self.app.configure(bg="hot pink") #should never show
        self.font = "Calibri"
        self.font_size = 11
        self.title_font_size = 14
        self.frames = []
        self.titles = []
        self.widgets = []

        self.time_window = 1

        self.thread_lock = False

        self.archive_file = None
        self.json_file = None
        self.locations = []

        self.debug = debug

        return

    def build_menu(self):
        #creates the menu bar at the top of the window i.e. File, About...

        if self.debug: print("Building menu bar")

        #create menu bar

        self.menubar = tk.Menu(
            self.app,
            fg=self.fg_color,
            bg=self.bg_color
            )

        #create options that will be under "File"

        self.file_options = tk.Menu(
            self.menubar,
            tearoff=False
            )

        #add option to select months to calculate

        self.file_options.add_command(
            label="Months to Report",
            command=self.set_months,
            )

        #add option to select a zip file

        self.file_options.add_command(
            label="Save Report To Excel",
            command=self.write_to_excel
            )

        #add option to select a zip file

        self.file_options.add_command(
            label="Select Zip File",
            command=self.open_archive
            )

        #add option to select a .json file

        self.file_options.add_command(
            label="Select Json File",
            command=self.open_json
            )

        #add option to exit the app

        self.file_options.add_command(
            label="Exit",
            command=self.quit
            )

        #add the file_options to the menu bar

        self.menubar.add_cascade(
            label="File",
            menu=self.file_options
            )

        #create options that will be under Settings

        self.setting_options = tk.Menu(
            self.menubar,
            tearoff=False
            )
        #add option to select Light Theme

        self.setting_options.add_command(
            label="Light Theme  •",
            command=self.light_theme
            )

        #add option to selet Dark Theme

        self.setting_options.add_command(
            label="Dark Theme",
            command=self.dark_theme
            )

        #add option to selet Forst Theme

        self.setting_options.add_command(
            label="Custom Theme",
            command=self.custom_theme
            )

        #add the setting_options to the menu bar

        self.menubar.add_cascade(
            label="Settings",
            menu=self.setting_options
            )

        #create a list of options that will be under "Help"

        self.help_options = tk.Menu(
            self.menubar,
            tearoff=False
            )

        #create the option to view the tutorial to "Help"

        self.help_options.add_command(
            label="Tutorial",
            command=self.tutorial
            )

        #add the help options to the menu bar

        self.menubar.add_cascade(
            label="Help",
            menu=self.help_options
            )

        #add the fully created menu bar to our window

        self.app.config(menu=self.menubar)

        return

    def build_app(self):

        if self.debug: print("Building main app window")

        #build frames

        self.l_frame = tk.Frame(
            self.app,
            bg=self.bg_color
            )

        self.r_frame = tk.Frame(
            self.app,
            bg=self.bg_color
            )

        #build widgets

        self.l_title = tk.Label(
            self.l_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            text="Custom Locations",
            font=(
                self.font,
                self.title_font_size
                )
            )

        self.l_scrollbox = Scrollbox(
            self.l_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            font=(
                self.font,
                self.font_size
                )
            )

        self.save_button = tk.Button(
            self.l_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            text="Save Locations",
            font=(
                self.font,
                self.font_size
                ),
            command=self.click_save_button
            )

        self.r_title = tk.Label(
            self.r_frame,
            bg=self.bg_color,
            fg=self.fg_color,
            text="Report",
            font=(
                self.font,
                self.title_font_size
                )
            )

        self.r_scrollbox = Scrollbox(
            self.r_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            font=(
                self.font,
                self.font_size
                )
            )

        self.download_button = tk.Button(
            self.r_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            text="Download Data",
            font=(
                self.font,
                self.font_size
                ),
            command=self.download_archive
            )

        self.calculate_button = tk.Button(
            self.r_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            text="Calculate Timeline",
            font=(
                self.font,
                self.font_size
                ),
            command=self.click_calculate_button
            )

        self.expense_button = tk.Button(
            self.r_frame,
            bg=self.bg2_color,
            fg=self.fg_color,
            text="Expense Report",
            font=(
                self.font,
                self.font_size
                ),
            command=self.click_expense_button
            )

        #place frames

        self.l_frame.place(
            relheight = 1.0,
            relwidth = 0.5,
            relx = 0.0,
            rely = 0.0
            )

        self.r_frame.place(
            relheight = 1.0,
            relwidth = 0.5,
            relx = 0.5,
            rely = 0.0
            )

        #place widgets

        self.l_title.place(
            relheight = 0.07,
            relwidth = 0.75,
            relx = 0.125,
            rely = 0.01
            )

        self.l_scrollbox.place(
            relheight = 0.82,
            relwidth = 0.98,
            relx = 0.001,
            rely = 0.09
            )

        self.save_button.place(
            relheight = 0.07,
            relwidth = 0.5,
            relx = 0.25,
            rely = 0.92
            )

        self.r_title.place(
            relheight = 0.07,
            relwidth = 0.75,
            relx = 0.125,
            rely = 0.01
            )

        self.r_scrollbox.place(
            relheight = 0.82,
            relwidth = 0.98,
            relx = 0.01,
            rely = 0.09
            )

        self.download_button.place(
            relheight = 0.07,
            relwidth = 0.29,
            relx = 0.04,
            rely = 0.92
            )

        
        self.calculate_button.place(
            relheight = 0.07,
            relwidth = 0.29,
            relx = 0.36,
            rely = 0.92
            )

        """
        #removed because functionality hasn't been completed.
        self.expense_button.place(
            relheight = 0.07,
            relwidth = 0.29,
            relx = 0.68,
            rely = 0.92
            )
        """

        #add frames to self.frames

        self.frames.append(self.l_frame)
        self.frames.append(self.r_frame)

        #add all the widgets we created to self.widgets
        #so we can reference all of them simultaneously later

        self.titles.append(self.l_title)
        self.titles.append(self.r_title)
        self.widgets.append(self.l_scrollbox)
        self.widgets.append(self.save_button)
        self.widgets.append(self.r_scrollbox)
        self.widgets.append(self.download_button)
        self.widgets.append(self.calculate_button)
        self.widgets.append(self.expense_button)

        return

    def light_theme(self):

        if self.debug: print("switching to light theme")

        with open("theme_default.txt", "w") as file:
            file.write("light theme")

        self.fg_color = self.light_theme_colors["fg"]
        self.bg_color = self.light_theme_colors["bg"]
        self.bg2_color = self.light_theme_colors["bg2"]
        self.setting_options.entryconfigure(0, label="Light Theme  •")
        self.setting_options.entryconfigure(1, label="Dark Theme")
        self.setting_options.entryconfigure(2, label="Custom Theme")
        self.l_scrollbox.config(insertbackground=self.light_theme_colors["bg"])
        self.r_scrollbox.config(insertbackground=self.light_theme_colors["bg"])
        self.update_colors()

        return

    def dark_theme(self):

        if self.debug: print("switching to dark theme")

        with open("theme_default.txt", "w") as file:
            file.write("dark theme")

        self.fg_color = self.dark_theme_colors["fg"]
        self.bg_color = self.dark_theme_colors["bg"]
        self.bg2_color = self.dark_theme_colors["bg2"]
        self.setting_options.entryconfigure(0, label="Light Theme")
        self.setting_options.entryconfigure(1, label="Dark Theme  •")
        self.setting_options.entryconfigure(2, label="Custom Theme")
        self.l_scrollbox.config(insertbackground=self.dark_theme_colors["bg"])
        self.r_scrollbox.config(insertbackground=self.dark_theme_colors["bg"])
        self.update_colors()

        return

    def custom_theme(self):

        if self.debug: print("switching to custom theme")

        with open("theme_default.txt", "w") as file:
            file.write("custom theme")

        self.fg_color = self.custom_theme_colors["fg"]
        self.bg_color = self.custom_theme_colors["bg"]
        self.bg2_color = self.custom_theme_colors["bg2"]
        self.setting_options.entryconfigure(0, label="Light Theme")
        self.setting_options.entryconfigure(1, label="Dark Theme")
        self.setting_options.entryconfigure(2, label="Custom Theme  •")
        self.l_scrollbox.config(insertbackground=self.custom_theme_colors["bg"])
        self.r_scrollbox.config(insertbackground=self.custom_theme_colors["bg"])
        self.update_colors()

        return

    def update_colors(self):

        for frame in self.frames:
            frame.configure(
                background=self.bg_color
                )

        for title in self.titles:
        	title.configure(
        		background=self.bg_color,
                foreground=self.fg_color
        		)

        for widget in self.widgets:
            widget.configure(
                background=self.bg2_color,
                foreground=self.fg_color
                )

        self.app.update()

        return

    def get_locations(self):

        if self.thread_lock: return

        if self.debug: print("retrieving locations from left scrollbox")

        #this is used to get the custom locations from the 
        #scrollbox on the left frame

        return self.l_scrollbox.get(1.0, tk.END)

    def set_locations(self):

        if self.thread_lock: return

        if self.debug: print("reading locations from txt file and printing")

        self.custom_locations = self.reader.read_txt()
        
        self.clear_lscrollbox()

        lines = []
        for x in self.custom_locations:
            self.update_lscrollbox(str(x.name)+": "+str(x.address))
        self.app.update()

        return

    def click_save_button(self):

        if self.thread_lock: return

        if self.debug: print("saving custom locations")

        #Read all locations from the left frame scrollbox
        #then save to disk
        custom_locations = self.get_locations()
        with open("Locations.txt", "w") as file:
            file.write(custom_locations)

        self.set_locations()

        return

    def download_archive(self):

        if self.debug: print("opening download archive link")

        #download the archive from Google Takout
        takeout_url = (
            "https://takeout.google.com/" +
            "settings/takeout/custom/location_history"
            )
        webbrowser.open(
            takeout_url,
            new=2,
            autoraise=False
            )

        return

    def open_archive(self):

        if self.thread_lock: return

        if self.debug: print("opening zip file")

        #only works on windows
        user_folder = os.environ.get("USERPROFILE")
        if user_folder != None:
            downloads_folder = user_folder + "/Downloads"
        else:
            downloads_folder = "C:/"
        filename = openfile(
            initialdir=downloads_folder,
            filetypes=(("Google Takeout File", "*.zip"),
                ("All File Types", "*.*")),
            title="Choose a Google Takeout File"
            )

        self.archive_file = filename

        return

    def open_json(self):

        if self.thread_lock: return

        if self.debug: print("opening json file")

        self.update_rscrollbox("Reading json file...")

        #only works on windows; get the file path from
        #the user via windows file prompt
        user_folder = os.environ.get("USERPROFILE")

        if user_folder != None:
            downloads_folder = user_folder + "/Downloads"
        else:
            downloads_folder = "C:/"
        filename = openfile(
            initialdir=downloads_folder,
            filetypes=(("Google Takeout File", "*.json"),
                ("All File Types", "*.*")),
            title="Choose a Google Takeout File"
            )

        if self.debug: print(f"file found: {user_folder}")

        if filename != None:
            self.json_file = filename

        return

    def tutorial(self):

        if self.debug: print("displaying tutorial")

        #show a popup of the tutorial
        with open("Tutorial.txt", "r") as file:
            tutorial = file.read()
        messagebox.showinfo("Tutorial",
            tutorial
            )

        return

    def default_theme(self):

        #reads a theme name from default_theme.txt and
        #set it accordingly, if file doesn't exists or
        #containts an invalid theme, light theme is chosen

        if self.debug: print("setting theme from default_theme.txt")

        if not os.path.isfile("theme_default.txt"):
            self.light_theme()
            return

        with open("theme_default.txt", "r") as file:
            line = file.read()

        theme = line
            
                
        if theme == "light theme":
            self.light_theme()
        elif theme == "dark theme":
            self.dark_theme()
        elif theme =="custom theme":
            self.custom_theme()
        else:
            self.light_theme()

        return

    def get_custom_colors(self):

        custom_colors = {}

        with open("custom_theme_colors.txt", "r") as file:
            lines = file.readlines()

        fg = lines[0][lines[0].index(":")+2
        :-1]
        bg = lines[1][lines[1].index(":")+2:-1]
        bg2 = lines[2][lines[2].index(":")+2:]
        if bg2[-1] == "\n":
            bg2 = bg2[:-1]

        custom_colors["fg"] = fg
        custom_colors["bg"] = bg
        custom_colors["bg2"] = bg2

        print(f"custom colors: {custom_colors}")

        return custom_colors

    def call_calculate_button(self):

        if self.debug: print("calculating timeline")

        self.clear_rscrollbox()

        #verify that custom locations are set and
        #that a json file or an archive file have
        #been chosen.  If not file has been chosen,
        #then force the user to choose one.  Returns
        #"break" if no custom locations are set
        return_value = self.verify_parameters()

        if self.debug: print(f"return value in calc button: {return_value}")

        if return_value == "break custom":
            self.update_rscrollbox("No custom locations set")
            self.update_rscrollbox("Please enter custom locations")
            return
        elif return_value == "break json":
            self.update_rscrollbox("No json file was selected")
            self.update_rscrollbox("Please select a json file downloaded from Google Takeout")
            return

        elif return_value == "no connection":
            self.update_rscrollbox("No internet connection detected.")
            self.update_rscrollbox("Please connect to the internet and try again.")
            return

        try:

            self.update_rscrollbox("Loading json file from disk.  This may take a few minutes...")
            self.custom_locations = self.addr_translator.convert(self.custom_locations)
            if self.debug: print(f"custom locations: {len(self.custom_locations)}")
            self.locations = self.reader.read_json(self.json_file)
            if self.debug: print(f"json file entries: {len(self.locations)}")
            self.cleaner.set_time_window(given_months=self.time_window)
            self.update_rscrollbox("Trimming data")
            self.locations = self.cleaner.trim_data(self.locations, self.custom_locations)
            if self.debug: print(f"trimmed data: {len(self.locations)}")
            self.update_rscrollbox("Cleaning data")
            self.locations = self.cleaner.clean_data(self.locations)
            if self.debug: print(f"cleaned data: {len(self.locations)}")
            self.update_rscrollbox("Removing false positives")
            self.locations = self.cleaner.clean_data_min(self.locations)
            if self.debug: print(f"data removed false positives: {len(self.locations)}")
            self.update_rscrollbox("Translating time stamps to human readable")
            try:
                self.locations = self.time_translator.translate(self.locations)
            except Exception as e:
                print(e)
                self.update_rscrollbox("Failed to connect to the internet...")
                return
            if self.debug: print(f"data time translated: {len(self.locations)}")
            

            if len(self.locations) == 0:
                self.update_rscrollbox("No entries found within the given time window")
                self.thread_lock = False
                return
            else:
                self.update_rscrollbox("Done.  Displaying results\n")

            #display the results
            for x in self.locations:

                self.update_rscrollbox(str(x.name))
                self.update_rscrollbox("Arrival Time: " + str(x.arr_time))
                self.update_rscrollbox("Departure Time: " + str(x.dep_time))
                self.update_rscrollbox()

        except Exception as e:
            #in case there is an error, release the thread lock
            print(e)
            self.thread_lock = False
            return

        with open("debug_self.locations.pickle", "wb") as f:
            pickle.dump(self.locations, f)

        self.thread_lock = False

        return

    def click_calculate_button(self):

        self.thread_lock = True

        subthread = Thread(target=self.call_calculate_button)
        subthread.start()

        self.thread_lock = False

        return

    def click_expense_button(self):

        if self.thread_lock: return

        if self.debug: print("calculating expense report")

        #check internet connection

        #! Delete this !
        with open("debug_self.locations.pickle", "rb") as f:
            self.locations = pickle.load(f)

        #calculate expense report
        expense_report = self.ex_report.generate(self.locations)

        #write expense report to the right scrollbox
        for x in expense_report:
            print(x)
            self.update_rscrollbox(x)

        return

    def write_to_excel(self):

        if self.debug: print("writing to excel")

        if len(self.locations) == 0:
            self.update_rscrollbox("You need to run the report first")
            self.update_rscrollbox("Click on 'Calculate Timeline' below")
            return

        #set file path
        root_app_dir = os.path.dirname(__file__)
        excel_folder = root_app_dir + "\\Excel Reports"
        if not os.path.isdir(excel_folder):
            os.mkdir(excel_folder)
        print(f"excel folder: {excel_folder}")

        #write to excel file
        self.ex_writer.write_file(self.locations, excel_folder)

        #open containing folder
        
        subprocess.call(f"explorer {excel_folder}", shell=True)

        return

    def update_lscrollbox(self, data=""):

        line = str(data) + "\n"
        self.l_scrollbox.insert(tk.INSERT, line)

        return

    def update_rscrollbox(self, data=""):

        line = str(data) + "\n"
        self.r_scrollbox.insert(tk.INSERT, line)

        return

    def clear_lscrollbox(self):

        self.l_scrollbox.delete('1.0', tk.END)

        return

    def clear_rscrollbox(self):

        self.r_scrollbox.delete('1.0', tk.END)

        return

    def verify_parameters(self):

        if self.debug:
            print(f"custom locations: {len(self.custom_locations)}")

        if len(self.custom_locations) == 0:
            return "break custom"

        if subprocess.call("ping -n 2 google.com") == 1:
            #no internet connection
            return "no connection"


        if self.json_file == None:
            if self.debug: print("no json file")
            if self.archive_file == None:
                if self.debug: print("no archive file")
                self.open_json()
                if self.json_file == "":
                    return "break json"
            else:
                if self.debug: print("extracting archive")
                self.json_file = self.reader.extract_archive(self.archive_file)

        


        return

    def set_months(self):
        #creates a pop up window to get a number
        #from the user

        class pop_up:

            def __init__(self, parent):

                self.parent = parent

                self.message = ("Please enter the amount of months " +
                    "to report on.")
                self.pop_up = tk.Toplevel(self.parent.app)
                self.pop_up.geometry("325x100")
                self.pop_up.title("Set Months")
                self.pop_up.resizable(False, False)
                self.display_text = tk.Label(
                    self.pop_up,
                    text=self.message
                    )

                self.text_box = tk.Entry(self.pop_up)

                self.submit_button = tk.Button(
                    self.pop_up,
                    text="Submit",
                    command=self.get_text,
                    )

                self.display_text.pack()
                self.text_box.pack()
                self.submit_button.pack()

            def get_text(self):
                self.parent.time_window = int(self.text_box.get())
                self.pop_up.destroy()
                return

        self.sub_window = pop_up(self)

        return

    def pop_up(self):

        return

    def quit(self):

        if self.debug: print("exiting app")

        self.app.destroy()

        return

    def run(self):

        if self.debug: print("initialing app...")

        self.build_menu()
        self.build_app()
        self.set_locations()
        self.default_theme()
        self.app.mainloop()

        return


if __name__ == "__main__":
    Gui(debug=True).run()
