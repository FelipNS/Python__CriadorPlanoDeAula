PRIMARY_BG_COLOR = '#282c34'
SECOND_BG_COLOR = '#181a1f'
DEFAULT_FG_COLOR = 'white'
DEFAULT_WINDOW_POSITION = 'tk::PlaceWindow . center'

def center(win, width=None, height=None):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    if width == None:
        width = win.winfo_reqwidth()   
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    if height == None:
        height = win.winfo_reqheight()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry(f'{width}x{height}+{x}+{y}')
    win.deiconify()