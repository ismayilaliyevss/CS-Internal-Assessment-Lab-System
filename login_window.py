import tkinter as tk                # I just renamed it tk to make it easier to write
from staff_member import login

def open_login_window(on_success):  # this part is really important: on_success() function does not have paranthises yet because, if we write it with parantheses it will immediately call the function, but that is not what we want

    window =tk.Tk()                 # creating the actual window - root
    window.title("HashLab - Login") 
    window.geometry("300x180")      # size of window in pixels 

    tk.Label(window, text = "Username").pack(pady=(15,0))   # creates a label - basically label is static and noneditable text, and it is inside window(root). pack is for actually drawing the label 
    username_entry = tk.Entry(window)           # tk.Entry is text box, and we are just saving it into a variable - username_entry
    username_entry.pack()

    tk.Label(window, text = "Password").pack(pady=(10, 0))
    password_entry = tk.Entry(window, show="*")             # masking the typed characters - makes it safer
    password_entry.pack()

    error_label = tk.Label(window, text="", fg="red")       # empty until there is an error to show - I just created this label beforehand, so there is no need to create new label when error happens everytime
    error_label.pack(pady=(5, 0))

    def attempt_login():
        username = username_entry.get()             # getting the thing written in the box
        password = password_entry.get()
        result = login(username, password)

        if isinstance(result, str):             # above we just called login() function and it can return two things: error string and StaffMember object. This line checks if it string or not
            error_label.config(text="Invalid username or password")
            password_entry.delete(0, tk.END)     # I just deleted the written password so user can rewrite it. The reason I did not deleted the username is because in most cases users make mistake while fillng the password as it is masked
        else:
            window.destroy()                   
            on_success(result)

    tk.Button(window, text="Login", command = attempt_login).pack(pady=15)      # this is button - so this basically says whenever the button pressed it calls the attempt_login() function

    window.mainloop()               # this is the code makes the window stay open until it should get closed