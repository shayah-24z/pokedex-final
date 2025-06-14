import customtkinter
from customtkinter import *
import pypokedex
import tkinter as tk
from tkinter import * 
from tkinter.ttk import * 
from tkinter import messagebox
import requests
import pandas as pd
import PIL.Image, PIL.ImageTk
import urllib3
from io import BytesIO
from CTkMessagebox import CTkMessagebox


#Checks to see if csv file exists and creates one if not found
try:
    User_data = pd.read_csv('UserData.csv')
except FileNotFoundError:
    User_data = pd.DataFrame(columns=['Username', 'Password', 'Poké1' ,'Poké2' , 'Poké3', 'Poké4', 'Poké5', 'Poké6','delete'])

#Creates initial pokedex window
window = CTk()
window.geometry("550x650")
window.title("K'shayah - Pokedex" )
window.config(bg='#A0182C',padx=10, pady=10)

#### S T Y L I N G    F U N C T I O N S ####
#creates intital centre frame
def create_center_frame(fg_color = 'white',bg_color='#B04040',corner_radius=32,border_color='#222222',border_width=2, width=999, height=999):
    center_frame = CTkFrame(window, fg_color = fg_color ,bg_color=bg_color, corner_radius=corner_radius,border_color=border_color, border_width=border_width, width=width, height=height)
    center_frame.place(relx=0.5, rely=0.5, anchor='center')
    return center_frame

#creates a label function thats customizes pretty much everything
def create_label(parent, text, size=12,fg_color='#F5F5F5',bg_color ='transparent',text_color='#6E9BAF',corner_radius=32,):
    label = CTkLabel(parent, text=text, font=('calibri', size),fg_color=fg_color,bg_color=bg_color,text_color=text_color,corner_radius=corner_radius,)
    return label

    #so creates a button that uses the window as the parent frame, makes the buttons round and sets a background and hover window

#creates a button function that can be called anywhere 
def create_button(parent, text, command, size=12, corner_radius = 32,fg_color='white',text_color='black',hover_color='#D4A55E',border_color ='#8E1527', border_width = 3, width=100):
    button = CTkButton(parent, text=text, command=command, font=('calibri', size), corner_radius=corner_radius,fg_color=fg_color, text_color=text_color, hover_color=hover_color, border_color=border_color,border_width=border_width, width = width)
    return button

def create_entry(parent, textvariable=None, show=None, size=16):
    entry = CTkEntry(parent, textvariable=textvariable, font=('calibri', size), show=show)
    return entry


######## C L E A R    W I N D O W    F U N C T I O N ######
def clear_window():
    #gets rid of what was previoiusly enterd on window
    for widget in window.winfo_children():
        widget.destroy()

######## S T A R T    W I N D O W     F U N C T I O N    ########
def start_window():
    clear_window()
    window.config(bg='#E0E0E0')

    #creates a centre frame so the title and buttons are in the middle of the window
    center_frame = create_center_frame(fg_color = '#A0182C',bg_color='#E0E0E0',corner_radius=80, border_color='#8E1527', border_width=6)
    
    #adds big pokedex title to center frame
    title = create_label(center_frame, "Pokedex", 24,fg_color='transparent',bg_color='transparent',text_color='#D4A55E', corner_radius=64)
    title.pack(pady=20, padx=35)
    
    #allows user to sign up
    new_user_btn = create_button(center_frame, "Create new user", command=add_user)
    new_user_btn.pack(padx=10)
    
    #allows users to sign in
    old_user_btn = create_button(center_frame, "Existing User", command=get_password)
    old_user_btn.pack(pady=7, padx=15)

    CTkLabel(center_frame,text="By K'shayah", text_color='#D4A55E',bg_color='transparent', ).pack(padx=4, pady=14)

######## E N D    W I N D O W     F U N C T I O N    ########
def end_window():
    clear_window()
    

    center_frame = create_center_frame(fg_color = '#A0182C',bg_color='#E0E0E0',corner_radius=80, border_color='#8E1527', border_width=6)
    
    goodbye = create_label(center_frame, "Goodbye!", 20,fg_color='transparent',bg_color='transparent',text_color='#D4A55E', corner_radius=64)
    goodbye.pack(pady=20,padx=35)
    
    #returns users back to login page
    sign_out= create_button(center_frame, "Sign Out", start_window)
    sign_out.pack(pady=10)



######## G E T     P A S S W O R D     F U N C T I O N  ######
def get_password():
    clear_window()
    #change window colour to green
    window.config(bg='#E0E0E0')

    #Creates center frame so the login form is in the middle of the window
    center_frame = create_center_frame(bg_color='#E0E0E0',fg_color='#A0182C')

    #creates a login form label that fits the background of the frame its in
    title = create_label(center_frame, "Login", 24, fg_color='transparent',bg_color='#A0182C', text_color='#EDE7D9')
    title.pack(pady=20, padx=10)

    #creates a variable for storing the username and password
    uname_var = tk.StringVar()
    passw_var = tk.StringVar()

    #designs the username input section
    uname_label = create_label(center_frame, "Username", 12,fg_color="white",bg_color="#A0182C", text_color="#222222")
    uname_label.pack(pady=5)
    #pack essentially shows it on the page
    uname_entry = create_entry(center_frame, uname_var)
    uname_entry.pack(pady=5,padx=10)

    #designs the password input section
    passw_label = create_label(center_frame, "Password", 12,fg_color="white",bg_color="#A0182C", text_color="#222222")
    passw_label.pack(pady=5)
    passw_entry = create_entry(center_frame, passw_var, show='*')
    passw_entry.pack(pady=5,padx=10)

    # Login button
    login_btn = create_button(center_frame, "Login", lambda: check_password(uname_entry, passw_entry),fg_color='white',text_color='black',hover_color='#D4A55E',border_color ='#8E1527', border_width = 3)
    login_btn.pack(pady=20)

####### A D D     U S E R     F U N C T I O N #######
def add_user():
    global uname_entry, passw_entry
    clear_window()
    #change window colour to green
    window.config(bg='#E0E0E0')

    #creates a center frame for the signup form
    center_frame = create_center_frame(bg_color='#E0E0E0',fg_color='#A0182C')

    title = create_label(center_frame, "Sign Up", 24,fg_color='transparent',bg_color='#A0182C',text_color='#EDE7D9')
    title.pack(pady=20,padx=10)

    #creates a variable for storing the username and password
    uname_var = tk.StringVar()
    passw_var = tk.StringVar()

    #designs the username input section
    uname_label = create_label(center_frame, "Username", 12,fg_color="white",bg_color="#A0182C", text_color="#222222")
    uname_label.pack(pady=5)
    #pack essentially shows it on the page
    uname_entry = create_entry(center_frame, uname_var)
    uname_entry.pack(pady=5,padx=10)

    #designs the password input section, hides the password
    passw_label = create_label(center_frame, "Password", 12,fg_color="white",bg_color="#A0182C", text_color="#222222")
    passw_label.pack(pady=5)
    passw_entry = create_entry(center_frame, passw_var, show='*')
    passw_entry.pack(pady=5,padx=10)

    #button that saves information entered to a csv
    register_btn = create_button(center_frame, "Register",save_new_info,fg_color='white',text_color='black',hover_color='#D4A55E',border_color ='#8E1527', border_width = 3)
    register_btn.pack(pady=20)

########  S A V E     N E W    U S E R    I N F O   #######
def save_new_info():
    global User_data

    #adds a new row to the UserData csv using the next availiable index
    new_row = {'Username': uname_entry.get(), 'Password': passw_entry.get()}
    User_data = pd.concat([User_data, pd.DataFrame([new_row])], ignore_index=True)

    #saves the info to csv
    User_data.to_csv('UserData.csv', index=False)
    print(User_data)

    #displays succsess message to user
    msg = CTkMessagebox(master=window, title="Success", message=f"Welcome, {uname_entry.get()}! Account created successfully!", icon="check",option_1="Noice",fg_color='#E0E0E0',bg_color='#6B8E72',text_color='#6B8E72', button_color='#E0E0E0', button_text_color='#6B8E72')
    
    #waits for user to press button before loading next window TO STOP CRASHING
    msg.get()
    
    #takes user back to login screen
    get_password()

######## C H E C K    P A S S W O R D    F U N C T I O N ######
def check_password(uname_entry, passw_entry):
    global User_data, username, password

    #Reloads the CSV so it can find new user and password
    User_data = pd.read_csv('UserData.csv')
    print(User_data)

    #gets username and password and makes sure theres no extra whitesapces to cause errors
    username = uname_entry.get().strip()
    password = passw_entry.get().strip()
    
    #checks if password and username entered is in the UserData csv
    if username in User_data['Username'].values:
        #gets password for username entered
        correct_pass = User_data.loc[User_data['Username'] == username, 'Password'].values[0]
        #checks if the password entered is the same as the one saved
        if password == correct_pass:
            welcome = create_label(window, f'Welcome {username}!')
            welcome.pack(pady=10)
            MainMenu()
        else:
            print("Login failed: Wrong password")
            CTkMessagebox(master=window, title="Login error", message="Incorrect Password", icon="cancel",option_1="Ok",sound='on',fg_color='#E0E0E0',bg_color='#2E2E2E',text_color='#A0182C', button_color='#A0182C', button_text_color='#2E2E2E')
    else:
        print("Login failed: Invalid username.")
        CTkMessagebox(master=window, title="Login error", message="Incorrect username", icon="cancel",option_1="Ok",fg_color='#E0E0E0',bg_color='#2E2E2E',text_color='#A0182C', button_color='#A0182C', button_text_color='#2E2E2E')



#######  M A I N    M E N U      O P T I O N     F U N C T I O N #####
def MenuOption(MainChoice1):
    print(MainChoice1)

    if MainChoice1 == "User Management":
         print('user management')
         UserManMenu()
    elif MainChoice1 == "Search Pokémon":
         print('Search pokemon')
         pokeMenu()
    elif MainChoice1 == "View Collection":
         print('View Collection')
         ViewCollection()
    elif MainChoice1 == "Quit":
         print('End')
         end_window()
    else:
        tk.messagebox.showerror("Error", "Invalid choice!\n")

def MainMenu():
    #gets rid of previous widgets
    clear_window()
    window.config(bg='#E0E0E0')

    #creates main frame to hold all widgets
    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80,border_color='#8E1527', border_width=6)
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=25, pady=20)

    title = create_label(inner_frame, "Main Menu", 24, fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5',corner_radius=32)
    title.pack(pady=15, padx=19)

    ############## O P T I O N    W I N D O W      C R E A T I O N ############
    option_label = create_label(inner_frame, "Choose an option:", 14,fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5', corner_radius=32)
    option_label.pack(pady=10, padx=10)

    #options for combobox
    options = ["User Management", "Search Pokémon", "View Collection","Quit"]
    #creates a combo box menu that gives users option to enter user management or search for pokemon
    mycombBox = CTkComboBox(inner_frame,values=options,height=40, width=200, corner_radius=32,fg_color='#FFFFFF',text_color='#A0182C', border_width=2, border_color= '#D4A55E',button_color= '#D4A55E', button_hover_color='#B04040',dropdown_hover_color='#A0182C', dropdown_fg_color='#F5F5F5',dropdown_text_color='#D4A55E',command=MenuOption)
    
    mycombBox.pack(pady=25, padx=22)


######### U S E R    M A N A G E M E N T   F U N C T I O N #####
def UserManagement(ManageChoice):
    if ManageChoice == '1':
        print('Change Username')
        UserChange()
    if ManageChoice == '2':
        print('Change Password')
        PassChange()
    if ManageChoice == '3':
        print('Delete Account')
        DeleteUser(User_data, username)
    if ManageChoice == '4':
        MainMenu()

######### U S E R    M A N A G E M E N T   M E N U   ######
def UserManMenu():
    clear_window()

    #creates outer frame to center all widgets
    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80,border_width=2,border_color='#F5F5F5')
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=25, pady=25)

    title = create_label(inner_frame, "User Management", 22,fg_color='#F5F5F5',bg_color='#A0182C', text_color='#A0182C',corner_radius=32)
    title.pack(pady=30,)

    ########### O P T I O N    W I N D O W      C R E A T I O N ###########
    option_label = create_label(inner_frame, "Choose a numbered option:", 15,fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5',corner_radius=32)
    option_label.pack(pady=10, padx=10)

    #gives users  user management options
    options = '''
    1) Change Username
    2) Change Password
    3) Delete Account
    4) Quit
    '''
    options_label = create_label(inner_frame, options, 12,fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5',corner_radius=32)
    options_label.pack(pady=15,padx=20)
    
    #input section for users to enter their option
    option_var = tk.StringVar()
    option_entry1 = CTkEntry(inner_frame,textvariable=option_var, corner_radius=32,bg_color='#A0182C',fg_color='#F5F5F5', border_color='#7C1322', border_width=2, text_color='#A0182C')
    option_entry1.pack(pady=15)

    #Submit button which carries out choice enterd
    submit_btn = create_button(inner_frame, text="Submit", command=lambda: UserManagement(option_var.get()))
    submit_btn.pack(pady=15)   

def PassChange():
    print('changing password')
    clear_window()
    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80,border_width=2,border_color='#F5F5F5')
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=25, pady=25)
    
    title = create_label(inner_frame, "Change Password", 24,fg_color='#F5F5F5',bg_color='#A0182C', text_color='#A0182C',corner_radius=32)
    title.pack(pady=30)

    #Gets Users Username
    uname_var = tk.StringVar()
    uname_label = create_label(inner_frame, "Enter Username:", 12,fg_color='#A0182C',bg_color='#A0182C',text_color='#F5F5F5')
    uname_label.pack(pady=5)
    uname_entry = create_entry(inner_frame, uname_var)
    uname_entry.pack(pady=5)

    #Gets password entry
    passw_var = tk.StringVar()
    passw_label = create_label(inner_frame, "Enter new password:", 12,fg_color='#A0182C',bg_color='#A0182C',text_color='#F5F5F5')
    passw_label.pack(pady=5)
    passw_entry = create_entry(inner_frame, passw_var, show='*')
    passw_entry.pack(pady=5)

    #saves new password entered to the csv
    def SavePass():
        #removes whitespaces to avoid error
        username = uname_entry.get().strip()
        password = passw_entry.get().strip()

        #checks if username enterd is in csv
        if username in User_data['Username'].values:
            #updates password of the username enterd 
            User_data.loc[User_data['Username'] == username, 'Password'] = password
            User_data.to_csv('UserData.csv', index=False)

            #displays sucsefull message to user
            msg = CTkMessagebox(master=window, title="Success", message=f"password successfully changed, {username}!", icon="check",option_1="Noice",fg_color='#E0E0E0',bg_color='#6B8E72',text_color='#6B8E72', button_color='#E0E0E0', button_text_color='#6B8E72')
            #waits for user to press button before loading next window TO STOP CRASHING
            msg.get()
            
            #takes user back to main menu
            MainMenu()
        else:

            tk.messagebox.showerror("Error", "User not found!")
            print('User not found')

    submit_btn = create_button(inner_frame, "Submit", SavePass,corner_radius = 32,fg_color='white',text_color='black',hover_color='#7C1322',border_color ='#7C1322', border_width = 3)
    submit_btn.pack(pady=10)

############ U S E R N A M E     C H A N G E   F U N C T I O N ###
def UserChange():
    print('changing password')
    clear_window()

    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80,border_width=2,border_color='#F5F5F5')
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=25, pady=25)

    title = create_label(inner_frame, "Change Username", 24,fg_color='#F5F5F5',bg_color='#A0182C', text_color='#A0182C',corner_radius=32)
    title.pack(pady=30)

    #Gets Users password and stores it
    passw_var = tk.StringVar()
    uname_label = create_label(inner_frame, "Enter password:", 12,fg_color='#A0182C',bg_color='#A0182C',text_color='#F5F5F5')
    uname_label.pack(pady=5)
    uname_entry = create_entry(inner_frame, passw_var, show='*')
    uname_entry.pack(pady=5)

    #Gets Users New Username and stores it
    uname_var = tk.StringVar()
    passw_label = create_label(inner_frame, "Enter new Username:", 12,fg_color='#A0182C',bg_color='#A0182C',text_color='#F5F5F5')
    passw_label.pack(pady=5)
    passw_entry = create_entry(inner_frame, uname_var)
    passw_entry.pack(pady=5)

    #saves new password entered to the csv
    def SaveUser():
        username = uname_entry.get().strip()
        password = passw_entry.get().strip()

        #checks if username enterd is in csv
        if password in User_data['Password'].values:
            #updates username of the password enterd 
            User_data.loc[User_data['Password'] == password, 'Username'] = username
            User_data.to_csv('UserData.csv', index=False)
            
            #displays sucsefull message to user
            msg = CTkMessagebox(master=window, title="Success", message=f"password successfully changed, {username}!", icon="check",option_1="Noice",fg_color='#E0E0E0',bg_color='#6B8E72',text_color='#6B8E72', button_color='#E0E0E0', button_text_color='#6B8E72')
            #waits for user to press button before loading next window TO STOP CRASHING
            msg.get()

            MainMenu()
        else:
            tk.messagebox.showerror("Error", "User not found!")
            print('User not found')
    submit_btn = create_button(inner_frame, "Submit", SaveUser)
    submit_btn.pack(pady=10)

########### D E L E T E      U S E R      D I S P L A Y #####
def DeleteUser(User_data, username):
    print('deleting user')
    clear_window()

    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80,border_width=2,border_color='#F5F5F5')
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=25,pady=25)
    title = create_label(inner_frame, "Delete Account", 24,fg_color='#F5F5F5',bg_color='#A0182C', text_color='#A0182C',corner_radius=32)
    title.pack(pady=20)

    #stores users entry
    del_var = tk.StringVar()

    #Gets password for authentication
    del_label = create_label(inner_frame, "Enter password to delete user",12,fg_color='#A0182C',bg_color='#A0182C',text_color='#F5F5F5')
    del_label.pack(pady=5)
    del_entry = create_entry(inner_frame, del_var, show='*')
    del_entry.pack(pady=5)

    #Delete button that calls function
    delete_btn = create_button(inner_frame, "Delete Account", lambda: DeleteRow(username, del_entry.get()),corner_radius = 32,fg_color='white',text_color='black',hover_color='#7C1322',border_color ='#7C1322', border_width = 3)
    delete_btn.pack(pady=10)

    back_btn = create_button(inner_frame, "Back", MainMenu,)
    back_btn.pack(pady=5)

########## D E L E T E      U S E R     F U N C T I O N #####
def DeleteRow(username, password):
    global User_data
    #reads the csv
    User_data = pd.read_csv('UserData.csv')

    #Find the location (index) where username matches in the csv
    index = User_data[User_data['Username'] == username].index[0]
    #Removes that user's row from the database
    User_data.drop(index, inplace=True)
    User_data.to_csv('UserData.csv', index=False)

    #displays sucsefull message to user
    msg = CTkMessagebox(master=window, title="Success", message="Account succsessfully deleted", icon="check",option_1="Noice",fg_color='#E0E0E0',bg_color='#6B8E72',text_color='#6B8E72', button_color='#E0E0E0', button_text_color='#6B8E72')
    msg.get()

    #Returns to start screen
    start_window()


########## P O K E M O N    S E A R C H I N G    M E N U    D I S P L A Y #####
def pokeMenu():
    clear_window()

    outer_frame = create_center_frame(fg_color='#A0182C', bg_color='#E0E0E0', corner_radius=80)
    inner_frame = CTkFrame(outer_frame,fg_color='#A0182C',corner_radius=64,)
    inner_frame.pack(padx=10, pady=20)

    title = create_label(inner_frame, "Pokemon Searching Menu", 24,fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5',corner_radius=32)
    title.pack(padx=25, pady=20)

    ############## O P T I O N    W I N D O W      C R E A T I O N ############
    option_label = create_label(inner_frame, "Choose a Searching Method:", 14,fg_color='#A0182C',bg_color='#A0182C', text_color='#F5F5F5', corner_radius=32)
    option_label.pack(pady=15, padx=19)

    #displays pokemon searching options
    pokeoptions = ["Search via Name", "Search via ID", "Search via Type", "Quit"]
    #creates a combo box menu that gives users option to enter user management or search for pokemon
    mycombBox = CTkComboBox(inner_frame,values=pokeoptions,height=40, width=200, corner_radius=32,fg_color='#FFFFFF',text_color='#A0182C', border_width=2, border_color= '#D4A55E',button_color= '#D4A55E', button_hover_color='#B04040',dropdown_hover_color='#A0182C', dropdown_fg_color='#F5F5F5',dropdown_text_color='#D4A55E',command=PokeSearchOpt)
    mycombBox.pack(pady=25, padx=22)

########### P O K E M O N    S E A R C H I N G    M E N U    F U N C T I O N ####
def PokeSearchOpt(pokemonOption):
    if pokemonOption == "Search via Name":  
        print('Search by name')
        SearchPoke()
    elif pokemonOption == "Search via ID":  
        print('Search by ID')
        SearchPoke()
    elif pokemonOption == "Search via Type": 
        SearchType() 
        print('Search by Type')
    elif pokemonOption == "Quit":  
        MainMenu()
    else:
        print("Invalid option. Please try again.")

######### L O A D    P O K E   U S I N G   N A M E    O R    I D    F U N C T  I O N #######
def SearchPoke():
    clear_window()

    #Creates outer frame to store widgets
    outer_frame = create_center_frame(fg_color="#A0182C", bg_color='#E0E0E0',border_color='#F5F5F5')

    pokedex_lab = create_label(outer_frame, "Find Pokemon", 23, bg_color='transparent',fg_color="#F5F5F5", text_color='#6E9BAF')
    pokedex_lab.pack(pady=20)
    #creates frame to store the pokemon image aswell as the pokemon name
    poke_frame = CTkFrame(outer_frame, fg_color="#6E9BAF", border_color="#57899E", border_width=4)
    poke_frame.pack(pady=5, padx=25)
                    
    #placeholder for image, stores it within the pokemon frame
    poke_img = CTkLabel(poke_frame, bg_color='#6E9BAF', text=" ", text_color="#6E9BAF")
    poke_img.pack(pady=10, padx=40)

    #shows pokemon name and type information in specific frames
    poke_name_disp = create_label(poke_frame, "", 15)
    poke_name_disp.pack(pady=5, padx=20)

    type_frame = CTkFrame(outer_frame,fg_color="#F5F5F5", bg_color="transparent",border_color="#6E9BAF", border_width=3)
    type_frame.pack(pady=5,padx=20)

    poke_type1 = create_label(type_frame, "", 12)
    poke_type1.pack(padx=5,pady=5,side=LEFT)

    poke_type2 = create_label(type_frame," ",12)
    poke_type2.pack(pady=5, padx=5,side=RIGHT)

    ##### L O A D S    P O K E M O N     I M A G E   #####
    def load_pokemon(poke_img, username): 
        global pokemon_name

        #gets pokemon from API and stores it so all info is accessable   
        pokemon = pypokedex.get(name=user_entry.get(1.0, "end-1c"))
        
        pokemon_name = pokemon.name
        ptype = pokemon.types
        print(pokemon_name, ptype)
                    
        #gets the image from the pypokedex api 
        http = urllib3.PoolManager()
        response = http.request('GET', pokemon.sprites.front.get('default'))
        #turns image into bytes then pillow image
        image = PIL.Image.open(BytesIO(response.data))

        img = CTkImage(image, size=(140,140))
        poke_img.configure(image=img)
        poke_img.image = img

        #shows all info about pokemon
        poke_name_disp.configure(text=f"#{pokemon.dex} - {pokemon.name.capitalize()}")
        poke_type1.configure(bg_color="#F5F5F5",text=f"Type: {', '.join(pokemon.types)}\n"
                             f"Height: {pokemon.height/10}m\n"
                             f"Weight: {pokemon.weight/10}kg\n")
                             
        poke_type2.configure(bg_color='#F5F5F5' ,text=f"Base Stats:\n"
                             f"HP: {pokemon.base_stats.hp}\n"
                             f"Attack: {pokemon.base_stats.attack}\n"
                             f"Defense: {pokemon.base_stats.defense}\n"
                             f"Speed: {pokemon.base_stats.speed}")

    info_frame = CTkFrame(outer_frame,fg_color='#6E9BAF', border_color='#F5F5F5', border_width=3)
    info_frame.pack(pady=5,padx=20)
    
    #input for pokemon Name or ID
    label_id_name = create_label(info_frame, "Enter Pokemon Name!", 12)
    label_id_name.pack(pady=20)

    user_entry = CTkTextbox(info_frame, height=5, width=100, font=('calibri', 12), fg_color='#57899E', activate_scrollbars=False)
    user_entry.pack(pady=5)

    #creates a frame for the load and add button
    button_frame = CTkFrame(info_frame, bg_color='#6E9BAF', fg_color='#6E9BAF')
    button_frame.pack(pady=10, padx=20)

    #loads pokemon image
    btn_load = create_button(button_frame, "Load Pokemon", lambda: load_pokemon(poke_img, username),fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    btn_load.pack(side=tk.LEFT, padx=5)

    #allows user to add pokemon to party
    add_btn = create_button(button_frame, "Add to Collection", lambda: AddPokemon(username, pokemon_name),fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    add_btn.pack(side=tk.LEFT, padx=5)

    #creates a main menu btn within the center frame
    main_menu_btn = create_button(outer_frame, "Main Menu", MainMenu,fg_color='#6E9BAF',text_color='#F5F5F5',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    main_menu_btn.pack(pady=10)

########## A D D     P O K E M O N    F U N C T I O N ######
def AddPokemon(username, pokemon_name):
    global User_data

    #Reloads CSV 
    User_data = pd.read_csv('UserData.csv')

    #Finds the index of the user in the dataframe using username
    UserIndex = User_data[User_data['Username'] == username].index

    #checks if each pokemon coloum is empty
    if not UserIndex.empty:
        #uses a for loop to iterate through pokemon list and find first availible slot
        for column in ['Poké1', 'Poké2', 'Poké3', 'Poké4', 'Poké5', 'Poké6']:
            #Stores current pokemon names e  
            value = User_data.loc[UserIndex[0], column]
            #checks if the slot is empty or not a number
            if pd.isna(value) or str(value).strip() == '':
                #saves the Pokémon to the first available slot
                User_data.loc[UserIndex[0], column] = pokemon_name
                print(f"Added {pokemon_name} to {username}'s team in {column}.")
                break
        else:
            full_msg = CTkMessagebox(master=window, title="Pokedex Full", message="you have too many pokemon, Choose one to replace", icon="cancel",option_1="Ok",fg_color='#E0E0E0',bg_color='#2E2E2E',text_color='#A0182C', button_color='#A0182C', button_text_color='#2E2E2E')
            full_msg.get()
            ViewCollection()

        User_data.to_csv('UserData.csv', index=False)
    else:
        print(f"Error: User {username} not found.")

########## V I E W     C O L L E C T I O N####
def ViewCollection():
    clear_window()
    pd.read_csv('UserData.csv')

    outer_frame = create_center_frame(fg_color="#A0182C", bg_color='#E0E0E0',border_color='#F5F5F5', corner_radius=80)

    #Displays 'your pokemon collection'
    pokedex_lab = CTkLabel(outer_frame, text=f"{username}'s Pokemon Collection", font=('Arial', 18), bg_color='transparent', fg_color='transparent', text_color='#EBEBEB')
    pokedex_lab.pack(pady=10)

    #Frame for Pokémon collection so everthing is stored together
    collection_frame = CTkFrame(outer_frame, fg_color='#BDD2DB', corner_radius=40)
    collection_frame.pack(pady=10, padx=15)

    #Creates a list to collect garabage and stop pokemon from being overwritten
    global imagelist
    imagelist = []  

    #Find the user index
    UserIndex = User_data[User_data['Username'] == username].index

    #Track rows to allow multiple pokemon to be displed on one row
    max_columns = 3
    GridColumn = 0
    GridRow = 0

    #iterates through each pokemon coloumn to get the names of pokemon
    for column in ['Poké1', 'Poké2', 'Poké3', 'Poké4', 'Poké5', 'Poké6']:
        #stores pokemon names
        value = User_data.loc[UserIndex[0], column]
        #Skip empty or NaN entries for asthetics
        if not value or pd.isna(value):  
            continue

        #debiggin
        print(f"Fetching data for: {value}")

        try:
            #Gets Pokémon data using the API
            pokemon = pypokedex.get(name=value)
            pokemon_name = pokemon.name
            print(f"Fetched: {pokemon_name}")

            #Gets the Pokémon image
            image_url = pokemon.sprites.front.get('default')
            http = urllib3.PoolManager()
            response = http.request('GET', image_url)

            #Convert the image into bytes, then to a PhotoImage
            image = PIL.Image.open(BytesIO(response.data))
            img = CTkImage(image,size=(100,100))

            #Prevents garbage collection so all images load
            imagelist.append(img) 

            #Create a frame for each Pokémon and makes it the background blue
            poke_frame = CTkFrame(collection_frame, border_width=2,fg_color='#7BA5B7' ,bg_color='transparent',corner_radius=32, border_color='#A3C0CC')
            poke_frame.grid(row=GridRow, column=GridColumn, padx=10, pady=10, sticky="nsew")

            #Display Pokémon name, makes backgournd grey 
            collection_label = CTkLabel(poke_frame, text=pokemon_name, font=("calibre", 14), bg_color='transparent', text_color='#F5F5F5')
            collection_label.pack(pady=5)

            #Display Pokémon image
            poke_img_label = CTkLabel(poke_frame, image=img, text=' ', fg_color='#7BA5B7', corner_radius=32)
            poke_img_label.pack(pady=5)

            #calls my delete function using the username and pokemon name
            del_btn = CTkButton(poke_frame, text='Delete Poke', command=lambda p=pokemon_name: DeletePoke(username, p),fg_color='#D1A054', hover_color='#DDB77E', border_color='#6B8E72',border_width=2)
            del_btn.pack(pady=5, padx=5)

            #Calls my switch pokemon function
            swtch_btn = CTkButton(poke_frame, text='Switch Poke', command=lambda p=pokemon_name: SwitchPoke(username, p),border_color='#698C70', border_width=2, fg_color='#6B8E72', hover_color='#8BA790')
            swtch_btn.pack(pady=10, padx=10)

            GridColumn += 1
            #checks to see if there are more than 3 pokemon stored on each row, creates a new one if so
            if GridColumn >= max_columns:
                GridColumn = 0
                GridRow += 1 

        #displays if pokemon data couldnt load usig the API
        except Exception as e:
            print(f"Error loading Pokémon {value}: {e}")
    CTkButton(outer_frame, text="Main Menu", command=MainMenu,fg_color='#6E9BAF',text_color='#F5F5F5',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3).pack(pady=5)

##########  D E L E T E   P O K E M O N    P O S I T I O N ###
def DeletePoke(username, p):
    global User_data  # Add this to ensure we're modifying the global variable
    print(f"Deleting Pokémon: {p}")
   
    #Reloads CSV 
    User_data = pd.read_csv('UserData.csv')

    #Finds the location of the user in the dataframe using username
    UserIndex = User_data[User_data['Username'] == username].index

    #goes through the pokemon list
    for column in ['Poké1', 'Poké2', 'Poké3', 'Poké4', 'Poké5', 'Poké6']:
        #Stores current pokemon names   
        value = User_data.loc[UserIndex[0], column]

        #checks to see if pokemon name (p), is same as one stored in party
        if p == value:
            User_data.loc[UserIndex[0], column] = None  #sets the column to nothing if the same
            print(f'{p} deleted from {column}')
            break
            
    User_data.to_csv('UserData.csv', index=False)
    
    #displays success message 
    tk.messagebox.showinfo("Success", f"Successfully deleted {p}!")
    
    #Clear the window before reloading the collection function
    clear_window()
    ViewCollection()

########## S H O W     R E P L A C E D     P O K E M O N    #######
def SwitchPoke(username, current_poke):
    #gets rid of all previous widgets from window
    clear_window()

    outer_frame = create_center_frame(fg_color="#A0182C", bg_color='#E0E0E0',border_color='#F5F5F5')

    title = create_label(outer_frame, f"Swap {current_poke} with...", 24,bg_color='transparent',fg_color="#F5F5F5", text_color='#6E9BAF')
    title.pack(pady=15, padx=25)

    #placeholder for image, stores it within the pokemon frame
    poke_img = CTkLabel(outer_frame, bg_color='#6E9BAF',text=None, corner_radius=32)
    poke_img.pack(pady=10, padx=40)

    ##shows pokeomon info = name, type
    poke_info = CTkLabel(outer_frame, 15)
    poke_info.pack(pady=10)

    def PokePhoto():
        try:
            #tries to find the name of the pokemon the user entered
            EntryName = text_id_name.get(1.0, "end-1c").strip().lower()
            #if name entered cant be found
            if not EntryName:
                tk.messagebox.showerror("Error", "Please enter a Pokemon name or ID")
                return
            
            #finds the data for the pokemon entered in text box
            pokemon = pypokedex.get(name=EntryName)

            #Display Pokémon name and types
            poke_info.configure(
                text=f"#{pokemon.dex} - {pokemon.name.capitalize()}\n"
                     f"Types: {', '.join(pokemon.types)}"
            )
                    
            #gets the image from the pypokedex api 
            http = urllib3.PoolManager()
            response = http.request('GET', pokemon.sprites.front.get('default'))
            #tursn image into bytes then pillow image
            image = PIL.Image.open(BytesIO(response.data))

            #converts to image so CTkinter can use
            img = CTkImage(image, size=(140,140))
            poke_img.configure(image=img)
            poke_img.image = img

            #saves Pokémon name so it can be accessed when ReplacePoke is called
            global new_pokemon_name
            new_pokemon_name = pokemon.name

        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load Pokémon. Please check the name.\n{e}")

    info_frame = CTkFrame(outer_frame,fg_color='#6E9BAF', border_color='#F5F5F5', border_width=3)
    info_frame.pack(pady=5,padx=20)

    #creates entry for pokemon name
    name_label = create_label(info_frame, "Enter Pokemon Name or ID:", 12)
    name_label.pack(pady=10)

    text_id_name = CTkTextbox(info_frame, height=1, width=80, font=('calibri', 12),activate_scrollbars=False)
    text_id_name.pack(pady=5)
    
    #creates a button frame for aesthetics
    button_frame = CTkFrame(info_frame, bg_color='#6E9BAF', fg_color='#6E9BAF')
    button_frame.pack(pady=10, padx=20)

    #loads  pokemon image they want to swap with
    load_btn = create_button(button_frame, "Load Pokemon", PokePhoto,fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    load_btn.pack(side=tk.LEFT, padx=5)

    #allows user to add pokemon to party
    switch_btn = create_button(button_frame, "Switch Pokemon", lambda: ReplacePoke(username, current_poke, new_pokemon_name),fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    #puts button to a specific side
    switch_btn.pack(side=tk.LEFT, padx=5)

    #bring user back to main menu
    main_menu_btn = create_button(outer_frame, "Main Menu", MainMenu,fg_color='#6E9BAF',text_color='#F5F5F5',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    main_menu_btn.pack(pady=10)

##########  S A V E   R E P L A C E D   P O K E M O N  ###
def ReplacePoke(username, current_poke, new_pokemon_name):
    #print(p, pokemon_name)
    #Finds the location of the user in the dataframe using username
    UserIndex = User_data[User_data['Username'] == username].index

    #goes through the pokemon list
    for column in ['Poké1', 'Poké2', 'Poké3', 'Poké4', 'Poké5', 'Poké6']:
        #checks to see if pokemon matches the one that needs to be replaced
        if User_data.loc[UserIndex[0], column] == current_poke:
            #replaces old pokemon with the new one chosen
            User_data.loc[UserIndex[0], column] = new_pokemon_name
            break
            
    User_data.to_csv('UserData.csv', index=False)
    #show success message to user
    tk.messagebox.showinfo("Success", f"{current_poke} replaced with {new_pokemon_name}.")
    ViewCollection()

########## L O A D   P  O K E    U S I N G   T Y P E    O P T I O N  #####
def SearchType():
    clear_window()

    outer_frame = create_center_frame(fg_color="#A0182C", bg_color='#E0E0E0',border_color='#F5F5F5', corner_radius=40)

    # Input field for type
    type_label = CTkLabel(outer_frame, text="Enter Pokémon type (e.g., fire, water):", font=('Arial', 18), bg_color='transparent', fg_color='transparent', text_color='#EBEBEB')
    type_label.pack(pady=10)

    #Frame for Pokémon collection so everthing is stored together
    inner_frame = CTkFrame(outer_frame, fg_color='#BDD2DB', corner_radius=40)
    inner_frame.pack(pady=10, padx=15)

    type_entry = create_entry(inner_frame)
    type_entry.pack(pady=5)

    def ShowPokeType():
        #gets pokemon type entered
        pokemon_type = type_entry.get().strip().lower()

        results_label = create_label(inner_frame, f"Showing {pokemon_type} Pokemon:", 17, bg_color='transparent', fg_color='transparent', text_color='#EBEBEB')
        results_label.pack(pady=10)

        #creates a frame for asthetics
        collection_frame = CTkFrame(inner_frame,fg_color='#BDD2DB', corner_radius=40)
        collection_frame.pack(pady=10, padx=15)

        #Global list to store PhotoImage objects
        global imagelist
        #stops images being garbage collected
        imagelist = []  


        #values to store 3 pokemon on the same row so non get cut off
        max_columns = 5
        grid_column = 0
        grid_row = 0

        #Placeholder for a list of first 10 Pokémon based on a type
        url = f'https://pokeapi.co/api/v2/type/{pokemon_type.lower()}'
        response = requests.get(url)

        #checks if the request was succsessful + connection established
        if response.status_code == 200:
            data = response.json()
            #Gets first 10 Pokémon of this type
            pokemon_list = data['pokemon'][:10] 
            poke_names = [pokemon['pokemon']['name'] for pokemon in pokemon_list]
            
            print(poke_names)
            
            #goes through each pokemon in the csv and tries to ge the image
            for poke_name in poke_names:
                try:
                    #gets pokemon info from API
                    pokemon = pypokedex.get(name=poke_name)
                    image_url = pokemon.sprites.front.get('default')

                    #if pokemon image URL cant be found
                    if not image_url:
                        print(f"No image available for: {poke_name}")
                        continue

                    #Gets pokemons image
                    http = urllib3.PoolManager()
                    response = http.request('GET', image_url)

                    #converts image into bytes then to a PhotoImage
                    image = PIL.Image.open(BytesIO(response.data))
                    img = CTkImage(image,size=(80,80))

                    #prevents garbage collection so all images load
                    imagelist.append(img)

                    #creates a frame for each Pokémon 
                    poke_frame = CTkFrame(collection_frame,fg_color='#7BA5B7' ,bg_color='transparent',corner_radius=32, border_color='#A3C0CC')
                    poke_frame.grid(row=grid_row, column=grid_column, padx=10, pady=10, sticky="nsew")

                    #displays each pokemons name within the frame
                    collection_label = CTkLabel(poke_frame, text=poke_name.capitalize(), bg_color='transparent', text_color='#F5F5F5')
                    collection_label.pack(pady=5)

                    #display Pokémon image inside the frame
                    poke_img_label = CTkLabel(poke_frame, image=img,text=' ', fg_color='#7BA5B7', corner_radius=32)
                    poke_img_label.pack(pady=5,padx=5)

                    #allows user to add pokemon to collection button
                    add_btn = CTkButton(poke_frame, text="Add to Collection", command=lambda p=poke_name: AddPokemon(username, p),border_color='#698C70', fg_color='#6B8E72', hover_color='#8BA790')
                    add_btn.pack(pady=10, padx=10)

                    #greates rows and columns to stop pokemon getting cut off
                    grid_column += 1
                    #stores pokemon on the next row after max_columns
                    if grid_column >= max_columns:
                        grid_column = 0
                        grid_row += 1

                #displays an error if pokemon info cant be fetched from API
                except Exception as e:
                    print(f"Error loading Pokémon {poke_name}: {e}")
        else:
            tk.messagebox.showerror("Error", f"Failed to fetch data for type: {pokemon_type}")

    #creates a button frame
    button_frame = tk.Frame(inner_frame, bg='#BDD2DB')
    button_frame.pack(pady=10, padx=15)

    #button to show pokemon types
    search_btn = create_button(button_frame, "Show Pokemon", ShowPokeType,fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    search_btn.pack(side=tk.LEFT, padx=5)
    #main menu button
    menu_btn = create_button(button_frame, "Main Menu", MainMenu,fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    menu_btn.pack(side=tk.LEFT, padx=5)
    #view pokemon collection button
    coll_btn = create_button(button_frame, "View collection", ViewCollection,fg_color='#F5F5F5',text_color='#57899E',hover_color='#96B7C5',border_color="#6E9BAF", border_width=3)
    coll_btn.pack(side=tk.LEFT, padx=5)

start_window()
window.mainloop()