# Assignment Tracker

## Overview

This is an assignment tracker originally designed for personal use, but I wanted to make it publically available as well!

---

## Technologies Used

- Python version:  3.13.7
- GUI framework: Tkinter  
- Data storage: CSV files  
- Packaging method: PyInstaller

---

## Project Structure

```bash
/your-project
│── AssignmentTracker.py 
│── setup.csv
│── class1.csv ... class7.csv
│── resources/ 
│── README.md 
```

### Description of Files

| File | Purpose |
|------|---------|
| `AssignmentTracker.py` | Main application code |
| `setup.csv` | Stores class names + selected theme |
| `classX.csv` | Stores assignments for each class |
| `AppIcon.icns` | The app icon|

---

## Features

- Add, edit, delete assignments
- Up to 7 classes supported
- Theme selection
- Days until due auto-calculation
- Status of Assignment Tracking with auto strikethrough on completion
- Highlighting of Assignments when they are close to or past due and not complete

---

## 🧠 Core Classes

### `Cls`

**Handles:** one class and its assignments

**Attributes:**

- name
- file_name
- assignment_list

**Important Methods:**

- `open_class()` – loads assignments from CSV  
- `add(assignment)` – adds new assignment  
- `save_class()` – writes assignments to CSV  

---

### `Assignment`

**Represents:** a single assignment

**Attributes:**

- status
- name
- due_date_string
- due_time
- type_of_assignment
- description
- days_until_due

**Internal Methods:**

- `parse_date()` — converts string → date  
- `compute_days_until_due()` — recalculates based on today  

---

## 🖥️ User Interface

### Main Window

- Dropdown: selects current class
- Table: displays assignments
- Buttons:
  - Add Assignment
  - Must have class selected to use:
    - Edit Assignment
    - Delete Assignment
  - Settings

### Pop-ups

#### Add Assignment

Fields included:

- name
- date
- time
- type
- description

#### Edit Assignment

- Fields pre-filled from selected row. Fields included:
- status
- name
- date
- time
- type
- description

---

## 💾 Data Format

### Assignment CSV Format

```python
status,
name,
due_date_string,
due_time,
type_of_assignment,
days_until_due,
description
```

### Example Row

```txt
Not Started, "Essay 1", "02/14/2025", "11:59 PM", "Writing", 3, "Intro draft"
```

---

## 🧪 Known Issues / Future Improvements

- Currently no way to sort assignments
- Date validation is limited

---

## 🚀 How to Run

### From source

```bash
python AssignmentTracker.py
```

### Packaged App Notes

- Include CSV files in same directory
- macOS may require folder permissions
- First launch may prompt for access

---

## 🙋 Troubleshooting

| Issue | Cause | Fix |
|------|-------|-----|
| No assignments appear | No class selected | Pick a class from dropdown |
| CSV not saving | OS permission blocked | Move app to Documents folder |
| Crashes on edit | Missing CSV column | Check file formatting |
|Popup on open saying that it cannot be opened|Apple Gatekeep|Go to Settings-->Privacy & Security-->Scroll to the bottom and click the option to allow Assignment Tracker to open|

---

## 📄 License

MIT

---

## ✍️ Author

- Alexa Berman
- Github: @lex120
- Contact: <aberman120@gmail.com>
