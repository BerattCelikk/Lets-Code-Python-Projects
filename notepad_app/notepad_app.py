#NOTEPAD APP
#APP = TKINTER

#libraries
from tkinter import *
from tkinter import filedialog , messagebox

#functions

def save_file():
    try:
        open_file=filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=[("Text Files","*.txt")])
        if open_file is None: # if the user cancels,the operation stops
            return
        text=entry.get(1.0,END) #retrieves all content from the text area
        open_file.write(text) #writes the content to the file
        open_file.close() #closes the file
        messagebox.showinfo("Success","File saved successfully!") #shows a success message
    except Exception as e:
        messagebox.showerror("Error",f"Could not save file : {e}")

#save_file end.

def open_file():
    try:
        #prompts the user to choose a file
        file=filedialog.askopenfile(mode="r",filetypes=[("Text Files","*.txt")])
        if file is not None:
            content=file.read() #reads the file content
            entry.delete(1.0,END) #clears existing content in the next area
            entry.insert(INSERT,content) #Inserts the file content into the text area
    except Exception as e:
        messagebox.showerror("Error",f"Could not save file : {e}")

#open_file end

def undo_action():
    try:
        entry.edit_undo() #undoes the last action
    except:
        pass #if there is nothing to undo, it does nothing

#undo_action end.

def redo_action():
    try:
        entry.edit_redo() #redoes the last undone action
    except:
        pass #if there is nothing to redo, it does nothing

#redo_action end.

def toggle_mode():
    global dark_mode
    dark_mode=not dark_mode
    if dark_mode:
        #dark mode is activated.
        root.config(bg="#000000") #changes the window bg to black
        entry.config(bg="#1E1E1E",fg="#E0E0E0") #changes the text area to dark gray and text color to light gray.
        b1.config(bg="#000080",fg="#E0E0E0") #changes the text area to dark gray and text color to light gray
        b2.config(bg="#000080",fg="#E0E0E0") 
        b3.config(bg="#000080",fg="#E0E0E0") 
        b4.config(bg="#000080",fg="#E0E0E0") 
        mode_button.config(bg="#000080",fg="#E0E0E0",text="Switch to Light Mode") #changes button text to "switch to light mode"
    else:
        #light mode is activated.
        root.config(bg="#E0FFFF") #changes the window bg to light cyan
        entry.config(bg="#F5F5F5",fg="#000000") #changes the text area to white and text color to black.
        b1.config(bg="#87CEFA",fg="#000000") #changes the text area to light blue and text color to black
        b2.config(bg="#87CEFA",fg="#000000") 
        b3.config(bg="#87CEFA",fg="#000000") 
        b4.config(bg="#87CEFA",fg="#000000") 
        mode_button.config(bg="#87CEFA",fg="#000000",text="Switch to Dark Mode") #changes button text to "switch to Dark mode"


#toggle_mode end.
        


root=Tk() # creates the main window
root.geometry("700x600") #sets the window size to 700x600 pixels
root.title("Notepad") #sets the window title
root.config(bg="#E0FFFF") #sets the window background color to light cyan
root.resizable(False,False) #disables window resizing

dark_mode=False #dark mode is initially disabled

#Buttons
button_width=15
button_height=2

b1=Button(root,width=button_width,height=button_height,bg="#87CEFA",text="Save File",command=save_file) # Save button
b1.place(x=50,y=10) #sets the button position

b2=Button(root,width=button_width,height=button_height,bg="#87CEFA",text="Open File",command=open_file) # Open button
b2.place(x=170,y=10) #sets the button position

b3=Button(root,width=button_width,height=button_height,bg="#87CEFA",text="Undo",command=undo_action) # Undo button
b3.place(x=290,y=10) #sets the button position

b4=Button(root,width=button_width,height=button_height,bg="#87CEFA",text="Redo",command=redo_action) # Redo button
b4.place(x=410,y=10) #sets the button position

mode_button=Button(root,width=button_width,height=button_height,bg="#87CEFA",text="Switch to Dark Mode",command=toggle_mode) # toggle_mode button
mode_button.place(x=530,y=10) #sets the button position

#Text Area
entry=Text(root,height=35,width=80,bg="#F5F5F5",font=("Arial",12),undo=True) #creates the text area with undo feature enabled 
entry.place(x=10,y=60) #sets the text area position


root.mainloop() #runs the main loop to keep the window open and interactive