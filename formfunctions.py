from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from formfunctions import *

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = (win.winfo_screenheight() // 2 - win_height // 2) - 50
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def checkIfEmpty(lat, long, mag, depth, num_tst):
    if len(lat) == 0 or len(long) == 0 or len(mag) == 0 or len(depth) == 0 or len(num_tst) == 0:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "There is an empty field, please fill up the missing values.")
        return 1
    else:
        return 0

def checkIfQuantity(lat, long, mag, depth, num_tst):
    try:
        latitude = float(lat)
        longitude = float(long)
        magnitude = float(mag)
        depth = float(depth)
        num_testimonies = int(num_tst)
        # print(str(latitude))
    except:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Only number symbols is accepted as input in the textfields.")
        return 1
    return 0

#https://www.britannica.com/science/latitude
def checkLatitudeRange(lat):
    lat = float(lat)
    if lat > 90 or lat < -90:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Latitude entered is not in the range.")
        return 1
    else:
        return 0

#https://www.britannica.com/science/latitude
def checkLongitudeRange(long):
    long = float(long)
    if long > 180 or long < -180:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Longitude entered is not in the range.")
        return 1
    else:
        return 0

#https://www.mtu.edu/geo/community/seismology/learn/earthquake-measure/magnitude/

def checkMagnitude(magnitude):
    magnitude = float(magnitude)
    if magnitude < 2.5 or magnitude > 9.5:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Magnitude entered is not in the range.")
        return 1
    else:
        return 0


def checkDepth(depth):
    depth = float(depth)
    if depth < 0 or depth > 700:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Depth entered is not in the range.")
        return 1
    else:
        return 0


def checkTestimonies(num_testimonies):
    num_testimonies = int(num_testimonies)
    print(str(num_testimonies))
    if num_testimonies <= 0:
        messagebox.showerror("DOST-PHIVOLCS (Error)", "Testimony number must be a positive and non-zero number")
        return 1
    else:
        return 0


