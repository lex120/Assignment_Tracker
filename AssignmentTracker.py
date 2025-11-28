import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os
import sys


def resource_path(filename):
    """_summary_

    Args:
        filename (string): the name of the file

    Returns:
        string:the path to the file
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename


class Cls: 
    def __init__(self, name, file_name):
        """Creates an instance of the Cls class
        Along with the given parameters, it also creates an empty assignment list, then calls open_class() to fill it

        Args:
            name (string): the string name of the class to be used as a label
            file_name (_type_): the filename associated with the class (ex: class1.csv)
        """
        self.name = name
        self.file_name = file_name
        self.assignment_list = []
        self.open_class()

    def open_class(self):
        """
        Opens the file name for the class and reads the csv file
        into a list of Assignment objects
        """
        try:
            with open(resource_path(self.file_name), 'r', newline='') as file:
                for item in csv.reader(file):
                    if len(item) == 7:
                        self.assignment_list.append(Assignment(*item))
        except FileNotFoundError:
            open(resource_path(self.file_name), 'w').close()
            self.assignment_list = []

    def add(self, assignment):
        """
        Adds the given assignment object to the list of
        Assignment objects for the Cls
        :param assignment: an Assignment object
        """
        self.assignment_list.append(assignment)
    
    def save_class(self):
        """
        Saves the currently opened class to the associated file
        """
        with open(resource_path(self.file_name), 'w', newline='') as curr_file:
            csv_writer = csv.writer(curr_file)
            for assignment in self.assignment_list:
                csv_writer.writerow([
                    assignment.status,
                    assignment.name,
                    assignment.due_date_string,
                    assignment.due_time,
                    assignment.type_of_assignment,
                    assignment.days_until_due,
                    assignment.description
                ])


class Assignment:
    def __init__(self, status, name, due_date, due_time, type_of_assignment, days_until_due, description):
        self.status = status if status.strip() != "" else "Not Started"
        self.name = name
        self.due_date_string = due_date
        self.due_date = self.parse_date(due_date)
        self.due_time = due_time
        self.type_of_assignment = type_of_assignment
        self.description = description
        self.days_until_due = self.compute_days_until_due()
        self.complete = (self.status == "Complete")

    def parse_date(self, s):
        try:
            parts = s.split("/")
            if len(parts) != 3:
                return None
            month = int(parts[0])
            day = int(parts[1])
            year = int(parts[2])
            return date(year, month, day)
        except:
            return None

    def compute_days_until_due(self):
        if self.due_date is None:
            return ""
        return (self.due_date - date.today()).days


def on_select(event):
    """
    Updates class names based on the changes made
    """
    global current_table_frame, current_class
    selected = event.widget.get()

    if current_table_frame is not None:
        current_table_frame.destroy()
        current_table_frame = None

    for cls_obj in [class1, class2, class3, class4, class5, class6, class7]:
        if cls_obj.name == selected:
            current_class = cls_obj
            break

    current_table_frame = create_assignment_table(frame)
    current_table_frame.pack(fill=tk.BOTH, expand=True)
    window.update_idletasks()

def valid_date(s):
    if s.strip() == "":
        return True
    try:
        parts = s.split("/")
        if len(parts) != 3:
            return False
        month = int(parts[0])
        day = int(parts[1])
        year = int(parts[2])
        date(year, month, day)
        return True
    except:
        return False

def add_assignment():
    global current_class

    def sync(event=None):
        global current_table_frame
        if current_table_frame is not None:
            current_table_frame.destroy()

        temp_assignment = Assignment(
            "Not Started",
            name_entry.get(),
            date_entry.get(),
            time_entry.get(),
            type_entry.get(),
            "",
            desc_entry.get()
        )
        current_class.add(temp_assignment)
        current_class.save_class()

        current_table_frame = create_assignment_table(frame)
        popup.destroy()

    if current_class is None:
        return

    popup = tk.Toplevel(window)
    popup.title("Add an Assignment")

    assignment_label = tk.Label(popup, text="Assignment:")
    assignment_label.grid(row=1, column=1, sticky=tk.E)
    name_entry = ttk.Entry(popup)
    name_entry.grid(row=1, column=2)
    name_entry.focus()

    date_label = tk.Label(popup, text="Due Date:")
    date_label.grid(row=2, column=1, sticky=tk.E)
    date_entry = ttk.Entry(popup)
    date_entry.grid(row=2, column=2)

    time_label = tk.Label(popup, text="Due Time:")
    time_label.grid(row=3, column=1, sticky=tk.E)
    time_entry = ttk.Entry(popup)
    time_entry.grid(row=3, column=2)

    type_label = tk.Label(popup, text="Type:")
    type_label.grid(row=4, column=1, sticky=tk.E)
    type_entry = ttk.Entry(popup)
    type_entry.grid(row=4, column=2)

    desc_label = tk.Label(popup, text="Description:")
    desc_label.grid(row=5, column=1, sticky=tk.E)
    desc_entry = ttk.Entry(popup)
    desc_entry.grid(row=5, column=2)

    save_button = ttk.Button(
        popup,
        text="Save",
        style="Buttons.TButton",
        command=sync
    )
    save_button.grid(row=6,column=1,columnspan=2,pady=5)
    entries = [name_entry, date_entry, time_entry, type_entry, desc_entry]

    name_entry.focus()

    def focus_next(event):
        widget = event.widget
        try:
            index = entries.index(widget)
            next_widget = entries[index + 1]
            next_widget.focus()
        except IndexError:
            pass
        return "break"


    for entry in entries:
        entry.bind("<Return>", focus_next)


def delete_assignment():
    """
    Deletes selected Assignment(s) from the currently selected
    Cls and updates the table
    """
    global current_table_frame

    tree = current_table_frame.winfo_children()[0]
    selected_items = tree.selection()

    if not selected_items:
        messagebox.showerror("showerror", "No assignment selected to delete")
        return

    for item_id in selected_items:
        values = tree.item(item_id, "values")
        for assignment in current_class.assignment_list:
            if (
                assignment.status == values[0]
                and assignment.name == values[1]
                and assignment.due_date_string == values[2]
                and assignment.due_time == values[3]
                and assignment.type_of_assignment == values[4]
                and str(assignment.days_until_due) == values[5]
                and assignment.description == values[6]
            ):
                current_class.assignment_list.remove(assignment)
                break

    current_class.save_class()

    current_table_frame.destroy()
    current_table_frame = create_assignment_table(frame)


def create_assignment_table(root):
    """
    Creates the assignment table
    """
    table = ttk.Frame(root)
    table.pack(fill=tk.BOTH, expand=True)

    columns = ("status", "name", "due_date", "due_time", "type", "days until due", "description")
    tree = ttk.Treeview(
        table,
        columns=columns,
        show="headings",
        height=10,
        style="Custom.Treeview"
    )
    tree.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(table, orient=tk.VERTICAL, command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscroll=scrollbar.set)

    table.columnconfigure(0, weight=1)
    table.rowconfigure(0, weight=1)

    headers = ["Status", "Name", "Due Date", "Due Time", "Type", "Days Until Due", "Description"]
    for col, text in zip(columns, headers):
        tree.heading(col, text=text)

    base_widths = [120, 120, 100, 80, 120, 150, 250]
    total_base = sum(base_widths)
    proportions = [w / total_base for w in base_widths]

    for col, width in zip(columns, base_widths):
        tree.column(col, width=width, minwidth=50, stretch=True)

    for assignment in current_class.assignment_list:
        tree.insert("", tk.END, values=(
            assignment.status,
            assignment.name,
            assignment.due_date_string,
            assignment.due_time,
            assignment.type_of_assignment,
            assignment.days_until_due,
            assignment.description
        ))

    def resize_columns(event):
        total_width = max(event.width - 18, 400)
        for col, prop in zip(columns, proportions):
            new_width = int(total_width * prop)
            tree.column(col, width=new_width)

    tree.bind("<Configure>", resize_columns)
    return table


def settings():
    """
    Creates the setings menu and calls associated
    functions based on button clicks
    """
    popup = tk.Toplevel(window)
    popup.title("Settings")
    popup.geometry("250x150")

    tk.Label(popup, text="Settings", font=("Arial", 14, "bold")).pack()

    manage_button = tk.Button(
        popup,
        text="Manage Classes",
        bg=current_theme[0],
        fg="black",
        relief="flat",
        command=manage_classes
    )
    manage_button.pack()

    theme_button = tk.Button(
        popup,
        text="Manage Theme",
        bg=current_theme[0],
        fg="black",
        relief="flat",
        command=manage_theme
    )
    theme_button.pack()

    edit_button = tk.Button(
        popup,
        text="Edit Assignment",
        bg=current_theme[0],
        fg="black",
        relief="flat",
        command=edit_assignment
    )


def edit_assignment():
    global current_table_frame
    tree = current_table_frame.winfo_children()[0]
    selected_items = tree.selection()

    if not selected_items:
        messagebox.showerror("showerror", "No assignment selected to edit")
        return

    first_item = selected_items[0]
    values = tree.item(first_item, "values")

    if current_class is None:
        return

    popup = tk.Toplevel(window)
    popup.title("Edit Assignment")
    
    STATUS_LIST = ["Not Started", "In Progress", "Complete"]
    status_label = tk.Label(popup, text="Status:")
    status_label.grid(row=1, column=1, sticky=tk.E)
    status_options = tk.StringVar()
    status_choice = ttk.Combobox(
        popup,
        textvariable=status_options,
        style="Custom.TCombobox",
        state="readonly",
        values= STATUS_LIST)
    status_choice.set(values[0])
    status_choice.grid(row=1,column=2)
    
    assignment_label = tk.Label(popup, text="Assignment:")
    assignment_label.grid(row=2, column=1, sticky=tk.E)
    name_entry = ttk.Entry(popup)
    name_entry.grid(row=2, column=2)
    name_entry.insert(0, values[1])
    name_entry.focus()

    date_label = tk.Label(popup, text="Due Date:")
    date_label.grid(row=3, column=1, sticky=tk.E)
    date_entry = ttk.Entry(popup)
    date_entry.grid(row=3, column=2)
    date_entry.insert(0, values[2])

    time_label = tk.Label(popup, text="Due Time:")
    time_label.grid(row=4, column=1, sticky=tk.E)
    time_entry = ttk.Entry(popup)
    time_entry.grid(row=4, column=2)
    time_entry.insert(0, values[3])

    type_label = tk.Label(popup, text="Type:")
    type_label.grid(row=5, column=1, sticky=tk.E)
    type_entry = ttk.Entry(popup)
    type_entry.grid(row=5, column=2)
    type_entry.insert(0, values[4])

    desc_label = tk.Label(popup, text="Description:")
    desc_label.grid(row=6, column=1, sticky=tk.E)
    desc_entry = ttk.Entry(popup)
    desc_entry.grid(row=6, column=2)
    desc_entry.insert(0, values[6])

    
    def sync(event=None):
        global current_table_frame

        captured_rows = []
        for item_id in selected_items:
            captured_rows.append(tree.item(item_id, "values"))

        if current_table_frame is not None:
            current_table_frame.destroy()

        for row_vals in captured_rows:
            for assignment in current_class.assignment_list:
                if (
                    assignment.status == row_vals[0]
                    and assignment.name == row_vals[1]
                    and assignment.due_date_string == row_vals[2]
                    and assignment.due_time == row_vals[3]
                    and assignment.type_of_assignment == row_vals[4]
                    and assignment.description == row_vals[6]
                ):
                    assignment.status = status_choice.get()
                    assignment.name = name_entry.get()
                    assignment.due_date_string = date_entry.get()
                    assignment.due_date = assignment.parse_date(assignment.due_date_string)
                    assignment.due_time = time_entry.get()
                    assignment.type_of_assignment = type_entry.get()
                    assignment.description = desc_entry.get()
                    assignment.days_until_due = assignment.compute_days_until_due()
                    break

        current_class.save_class()
        current_table_frame = create_assignment_table(frame)
        popup.destroy()


    save_button = ttk.Button(
            popup,
            text="Save",
            style="Buttons.TButton",
            command=sync
        )
    save_button.grid(row=7,column=1,columnspan=2,pady=5)
    
    entries = [name_entry, date_entry, time_entry, type_entry, desc_entry]

    name_entry.focus()

    def focus_next(event):
        widget = event.widget
        try:
            index = entries.index(widget)
            next_widget = entries[index + 1]
            next_widget.focus()
        except IndexError:
            pass
        return "break"

    for entry in entries:
        entry.bind("<Return>", focus_next)


def manage_theme():
    """
    Creates popup that lets user select the current theme for the interface
    """
    popup = tk.Toplevel(window)
    popup.title("Manage Classes")

    tk.Label(popup, text="Pick a Theme:", font=("Arial", 12, "bold")).grid(
        row=0, column=3, columnspan=2, pady=10
    )
    tk.Button(popup, highlightbackground="#FF6EBE", highlightthickness=5, relief="solid",
                command=lambda: set_theme("pink")).grid(row=2, column=1)
    tk.Button(popup, highlightbackground="#FFF892", highlightthickness=5, relief="solid",
                command=lambda: set_theme("yellow")).grid(row=2, column=2)
    tk.Button(popup, highlightbackground="#00BB77", highlightthickness=5, relief="solid",
                command=lambda: set_theme("green")).grid(row=2, column=3)
    tk.Button(popup, highlightbackground="#56C4FF", highlightthickness=5, relief="solid",
              command=lambda: set_theme("blue")).grid(row=2, column=4)
    tk.Button(popup, highlightbackground="#BC8FF7", highlightthickness=5, relief="solid",
                command=lambda: set_theme("purple")).grid(row=2, column=5)
    tk.Button(popup, highlightbackground="#FFFFFF", highlightthickness=5, relief="solid",
                border=5, command=lambda: set_theme("white")).grid(row=2, column=6, pady=2)


def get_theme_colors(theme):
    """
    Returns list that contains hex codes for the colors within the chosen theme
    """
    WHITE = ["#FFFFFF", "#000000", "#000000FF"]
    PINK = ["#FF6EBE", "#000000", "#FF249C"]
    YELLOW = ["#FFFCCC", "#000000", "#FFF894"]
    GREEN = ["#00BB77", "#000000", "#01754B"]
    BLUE = ["#56C4FF", "#000000", "#19A0EA"]
    PURPLE = ["#BC8FF7", "#000000", "#9C52FC"]
    match theme:
        case "white":
            return WHITE
        case "pink":
            return PINK
        case "yellow":
            return YELLOW
        case "green":
            return GREEN
        case "blue":
            return BLUE
        case "purple":
            return PURPLE


def apply_theme():
    """
    Applys the theme to the styles throughout the program
    """
    bg, fg, border = current_theme
    menu_frame.config(bg=bg)
    frame.config(bg=bg)
    style.configure(
        "Custom.TCombobox",
        fieldbackground="#FFFFFF",
        background=bg,
        bordercolor=bg,
        arrowsize=14,
    )
    style.configure(
        "Buttons.TButton",
        background=bg,
        foreground=fg,
        bordercolor=border,
        highlightbackground=fg,
        highlightthickness=5,
        focusthickness=0,
        padding=6,
        relief="solid"
    )
    add_button.configure(style="Buttons.TButton")
    delete_button.configure(style="Buttons.TButton")
    settings_button.configure(style="Buttons.TButton")
    style.configure("Custom.Treeview.Heading",
                    background=bg,
                    foreground="black",
                    relief="flat")
    window.update_idletasks()


def set_theme(theme):
    """
    Selects the given theme as the current theme
    """
    global current_theme, current_theme_name
    current_theme_name = theme
    current_theme = get_theme_colors(theme)

    try:
        with open(resource_path("setup.csv"), "r", newline='') as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        rows = []

    if rows:
        row = rows[0]
        if len(row) == 0:
            row = [current_theme_name]
        else:
            row[-1] = current_theme_name
    else:
        row = [current_theme_name]

    with open(resource_path("setup.csv"), "w", newline='') as f:
        csv.writer(f).writerow(row)

    apply_theme()


def manage_classes():
    """
    Creates popup for the User to change the name of the
    classes and then updates the program
    """
    popup = tk.Toplevel(window)
    popup.title("Manage Classes")

    entry_widgets = []
    class_objects = [class1, class2, class3, class4, class5, class6, class7]

    tk.Label(popup, text="Edit Class Names:", font=("Arial", 12, "bold")).grid(
        row=0, column=0, columnspan=2, pady=10
    )

    for idx, cls_obj in enumerate(class_objects):
        tk.Label(popup, text=f"Class {idx+1}:").grid(row=idx+1, column=0, sticky=tk.E)
        entry = ttk.Entry(popup, width=20)
        entry.insert(0, cls_obj.name)
        entry.grid(row=idx+1, column=1, padx=5, pady=2)
        entry_widgets.append(entry)

    def save_changes(event=None):
        """
        Saves the new names of the classes to the csv and across then program
        """
        global current_theme_name
        new_names = []

        for entry, cls_obj in zip(entry_widgets, class_objects):
            name = entry.get().strip()
            if len(name) > 0:
                cls_obj.name = name
                new_names.append(name)

        with open(resource_path("setup.csv"), "w", newline='') as f:
            csv.writer(f).writerow(new_names + [current_theme_name])

        class_choice.config(values=new_names)

        if current_class.name not in new_names:
            class_choice.set(new_names[0] if new_names else "")
        else:
            class_choice.set(current_class.name)

        popup.destroy()

    popup.bind("<Return>", save_changes)

    save_button = tk.Button(
        popup,
        text="Save",
        command=save_changes,
        bg=current_theme[0],
        fg="black",
        relief="flat",
        width=10
    )
    save_button.grid(row=9, column=0, columnspan=2, pady=10)


def save_geometry(event=None):
    """
    Saves window size so that it does not resize between actions
    """
    window.minsize(window.winfo_width(), window.winfo_height())


window = tk.Tk()
window.update_idletasks()
window.minsize(window.winfo_width(), window.winfo_height())
window.bind("<Configure>", save_geometry)
window.title("Assignment Tracker")

current_theme_name = "green"
current_theme = get_theme_colors(current_theme_name)

names = []
try:
    with open(resource_path("setup.csv"), 'r', newline='') as file:
        for row in csv.reader(file):
            if row:
                if len(row) >= 1:
                    current_theme_name = row[-1]
                    for name in row[:-1]:
                        if name.strip() != "":
                            names.append(name)
                break
except FileNotFoundError:
    default_names = ["Class 1", "Class 2", "Class 3", "Class 4", "Class 5", "Class 6", "Class 7"]
    with open(resource_path("setup.csv"), "w", newline='') as f:
        csv.writer(f).writerow(default_names + [current_theme_name])
    names = default_names

current_theme = get_theme_colors(current_theme_name)

class1 = Cls("Class 1", "class1.csv")
class2 = Cls("Class 2", "class2.csv")
class3 = Cls("Class 3", "class3.csv")
class4 = Cls("Class 4", "class4.csv")
class5 = Cls("Class 5", "class5.csv")
class6 = Cls("Class 6", "class6.csv")
class7 = Cls("Class 7", "class7.csv")

classes = [class1, class2, class3, class4, class5, class6, class7]
for cls_obj, stored_name in zip(classes, names):
    cls_obj.name = stored_name


menu_frame = tk.Frame(window, bg=current_theme[0])
menu_frame.pack(side=tk.TOP, fill=tk.X)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Custom.TCombobox",
    fieldbackground="#FFFFFF",
    background=current_theme[0],
    bordercolor=current_theme[0],
    arrowsize=14,
)

class_options = tk.StringVar()
class_choice = ttk.Combobox(
    menu_frame,
    textvariable=class_options,
    style="Custom.TCombobox",
    state="readonly",
    values=names)
class_choice.set("Pick a Class")
class_choice.pack(side=tk.LEFT, padx=10, pady=5)
class_choice.bind("<<ComboboxSelected>>", on_select)

style.configure(
    "Buttons.TButton",
    background=current_theme[0],
    foreground=current_theme[1],
    bordercolor=current_theme[2],
    highlightbackground=current_theme[1],
    highlightthickness=5,
    focusthickness=0,
    padding=6,
    relief="solid"
)

add_button = ttk.Button(
    menu_frame,
    text="Add Assignment",
    style="Buttons.TButton",
    command=add_assignment
)
add_button.pack(side=tk.LEFT, padx=5, pady=5)

edit_button = ttk.Button(
    menu_frame,
    text="Edit Assignment",
    style = "Buttons.TButton",
    command=edit_assignment
)
edit_button.pack(side=tk.LEFT, padx=5, pady=5)

delete_button = ttk.Button(
    menu_frame,
    text="Delete Assignment",
    style="Buttons.TButton",
    command=delete_assignment
)
delete_button.pack(side=tk.LEFT, padx=5, pady=5)

settings_button = ttk.Button(
    menu_frame,
    text="Settings",
    style="Buttons.TButton",
    command=settings
)
settings_button.pack(side=tk.LEFT, padx=5, pady=5)

style.configure("Custom.Treeview.Heading",
                background=current_theme[0],
                foreground="black",
                relief="flat")

frame = tk.Frame(window, borderwidth=3, bg=current_theme[0])
frame.pack(fill=tk.BOTH, expand=True)

current_class = class1
current_table_frame = create_assignment_table(frame)

apply_theme()

window.mainloop()
#TODO: re-add strikethrough