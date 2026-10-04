import tkinter as tk                # I just renamed it tk to make it easier to write
from staff_member import login

def open_login_window(on_success):  # this part is really important: on_success() function does not have paranthises yet because, if we write it with parantheses it will immediately call the function, but that is not what we want

    window =tk.Tk()                 # creating the actual window - root
    window.title("HashLab - Login") 
    window.geometry("360x260")      # size of window in pixels 

    LABEL_FONT = ("Arial", 13)          # firstly, I was writing them by hand each time, but whenever I tried to change it - it became so hard to change for each text, so I just created variables - make it easier to modify
    BUTTON_FONT = ("Arial", 12)
    ENTRY_FONT = ("Arial", 13)

    tk.Label(window, text = "Username", font = LABEL_FONT).pack(pady=(20,0))   # creates a label - basically label is static and noneditable text, and it is inside window(root). pack is for actually drawing the label 
    username_entry = tk.Entry(window, font = ENTRY_FONT)           # tk.Entry is text box, and we are just saving it into a variable - username_entry
    username_entry.pack()

    tk.Label(window, text = "Password", font = LABEL_FONT).pack(pady=(15, 0))
    password_entry = tk.Entry(window, show="*", font = ENTRY_FONT)             # masking the typed characters - makes it safer
    password_entry.pack()

    error_label = tk.Label(window, text="", fg="red", font = LABEL_FONT)       # empty until there is an error to show - I just created this label beforehand, so there is no need to create new label when error happens everytime
    error_label.pack(pady=(10, 0))

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

    tk.Button(window, text="Login", command = attempt_login, font = BUTTON_FONT, width = 12).pack(pady=20)      # this is button - so this basically says whenever the button pressed it calls the attempt_login() function

    window.mainloop()               # this is the code makes the window stay open until it should get closed


if __name__ == "__main__":          # so the code under this statement will run if the code is run directly
    def show_result(staff):         # I put this statement to test the login window itself without running main.py, so I can see what happens in this login window
        print(f"Logged in as {staff.username} ({staff.role})")

    open_login_window(show_result)