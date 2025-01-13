import customtkinter as ctk
import tkinter as tk
import pyperclip
from tkinter import ttk
from sys import exit
import os
from password_generator import password_crafter
import time
from cryptography.fernet import Fernet
import sqlite3
from PIL import Image, ImageTk
import os

#To make it universal
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#All styling attributes
blue = '#456349'
black = '#100f1a'
color_for_frame = '#04020d'
inside_frame = '#100f1a'
button_colors = '#322473'
border_colors = '#322473'
button_hover_color = '#533ac7'

#all fonts attributes
font_tuple = ("Poppins SemiBold", 13, 'bold')
treeview_header = ("Poppins SemiBold", 10, 'bold')
font_button = ("Poppins Light", 13)
paswd_font = ("Poppins Light", 15)
entry_font = ("Mosterrat Regular", 13)
logo_font = ("MONTSERRAT BLACK ITALIC", 14, 'bold')
#==============================================================

#Creating encrypting key
try:
   key = ''
   with open('key_save.key', 'rb') as f:
       key = f.read()
    
   key_read = Fernet(key)
   
   with open('data.ini', 'rb') as f:
       pin_decrypt = f.read()

   pin = key_read.decrypt(pin_decrypt) 
   pin = pin.decode()
except FileNotFoundError:
    if os.path.exists("cache"):
            os.remove("cache")
            exit()
#===============================================================

#Creating database
datab = sqlite3.connect('cache')
my_cursor = datab.cursor()
datab.commit()

try:
    my_cursor.execute("CREATE TABLE saved_data (website text NOT NULL, username text NOT NULL, password text NOT NULL, id INTEGER PRIMARY KEY)")
except:
    pass
#===============================================================

#Main Program
class Pass_gen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x700+140+100')
        #self.iconbitmap('D:\Programming (D)\(B)Materials\Devlo\All\p_password_manager\icon.ico')
        self.iconbitmap("icon.ico")

        #adding images from local directroy
        adding_save_image = ctk.CTkImage(Image.open("saved_password_icon.png").resize((23, 24), Image.LANCZOS))
        #adding_save_image = ctk.CTkImage(Image.open("D:\Programming (D)\(B)Materials\Devlo\All\p_password_manager\saved_password_icon.png").resize((23, 24), Image.LANCZOS))
        adding_exit_image = ctk.CTkImage(Image.open("exit_icon.png").resize((23, 24), Image.LANCZOS))
        adding_copy_button = ctk.CTkImage(Image.open("icon_for_copy.png").resize((23, 24), Image.LANCZOS))  
        adding_insert_button = ctk.CTkImage(Image.open("insert_icon.png").resize((23, 24), Image.LANCZOS))
        adding_generate_button = ctk.CTkImage(Image.open("generate_button.png").resize((23, 24), Image.LANCZOS))
        adding_enter_button = ctk.CTkImage(Image.open("enter_icon.png").resize((23, 24), Image.LANCZOS))
        adding_delete_selected = ctk.CTkImage(Image.open("delete_selected.png").resize((23, 24), Image.LANCZOS))
        adding_delete_all = ctk.CTkImage(Image.open("delete_all.png").resize((23, 24), Image.LANCZOS))
      
        x = 200
        self.count = 0 

        #the g gets the password label password 
        self.g = False

        #log of how many sames in name_list
        self.indexing = 0

        self.log_out = ctk.CTkFrame(self, fg_color=black)
        self.log_out.place(relx=0, rely=0, relwidth=1, relheight=1)

        #Password gen frame
        self.password = ctk.CTkFrame(self, fg_color=color_for_frame, border_color = border_colors, border_width=3, corner_radius=0)
        self.password.place(relx=0.20, rely=0, relwidth=0.8, relheight=1)

        #side frame---------
        self.menu_frame = ctk.CTkFrame(self, fg_color=black, border_width=0, border_color=border_colors, corner_radius=0)
        self.menu_frame.place(relx=0,rely=0,relwidth=0.2, relheight=1)

        #middle frame(password generation Frame)-------
        self.entry_frame = ctk.CTkFrame(self.password, fg_color=inside_frame, corner_radius=10)
        self.entry_frame.place(relx=0.5, rely=0.054, relwidth=0.95, relheight=0.42, anchor='n')

        #bottom frame(password genertion frame)--------
        self.info_frame = ctk.CTkFrame(self.password, fg_color=inside_frame, corner_radius=10)
        self.info_frame.place(relx=0.5, rely=0.53, relwidth=0.95, relheight=0.42, anchor='n')
        
        #Save password frame
        self.saves_frame = ctk.CTkFrame(self, fg_color=color_for_frame, border_color=border_colors, border_width=3, corner_radius=0)
        self.saves_frame.place(relx=0.20, rely=0, relwidth=0.8, relheight=1)
        
        

        #--------------------------------------------------------------------------------------------------------
        
        #ask for password window
        self.check_pin = ''
        self.save_pin = ''
        self.single_pin = ctk.CTkToplevel()
        self.single_pin.geometry('500x200+400+340')
        self.entry_inside_top = ctk.CTkEntry(self.single_pin,
                                             placeholder_text='Enter pin',
                                             width=100,
                                             height=30)
        self.entry_inside_top.place(relx=0.25, rely=0.25, anchor='center')
        self.entry_inside_top.focus_set()
        self.entry_inside_top.bind('<Return>', self.focus_on)
        self.entry_inside_top.configure(font=entry_font)

        self.entry_inside_top1 = ctk.CTkEntry(self.single_pin,
                                             placeholder_text='Confirm pin',
                                             width=100,
                                             height=30)
        self.entry_inside_top1.place(relx=0.75, rely=0.25, anchor='center')
        self.entry_inside_top1.bind('<Return>', self.confirm)
        self.entry_inside_top1.configure(font=entry_font)
        

        self.top_button1 = ctk.CTkButton(self.single_pin,
                                    text='Confirm',
                                    width=60,
                                    height=40,
                                    fg_color=black,
                                    hover_color=button_hover_color,
                                    command=self.close_pop)
        self.top_button1.place(relx=0.6, rely=0.85, anchor='center')
        self.top_button1.bind('<Button-1>', self.confirm)
        self.top_button2 = ctk.CTkButton(self.single_pin,
                                    text='Cancel',
                                    width=60,
                                    height=40,
                                    fg_color=black,
                                    hover_color=button_hover_color,
                                    command=self.close_pop)
        self.top_button2.place(relx=0.45, rely=0.85, anchor='center')
        self.top_button2.bind('<Button-1>', self.cancel)
        
        #Window kills the entire program
        self.single_pin.protocol('WM_DELETE_WINDOW', self.full_exit)
        self.single_pin.resizable(False, False)

        #errors in password creation
        self.universal_frame = ctk.CTkFrame(master=self.single_pin, fg_color=black, border_color=border_colors, border_width=3, corner_radius=0)
        self.universal_frame.place(relx=0.50, rely=0.5, relwidth=0.7, relheight=0.7, anchor='center')
        
        self.universal_button = ctk.CTkButton(self.universal_frame,
                                    text='Close',
                                    width=60,
                                    height=40,
                                    fg_color=black,
                                    hover_color=button_hover_color,
                                    command=self.kill_uni_frame)
        self.universal_button.place(relx=0.5, rely=0.84, anchor='center')
        self.universal_button.configure(font=font_button)

        self.uni_label = ctk.CTkLabel(master=self.universal_frame, anchor='center', text='', fg_color=black)
        self.uni_label.place(relx=0.5, rely=0.4, anchor='center')
        self.uni_label.configure(font=paswd_font)
        self.uni_label.configure(text='Restart after pin creation')
        #---------------------------------------------------------------------------------

        #frame to ask for website or username
        self.pop_frame = ctk.CTkFrame(self, fg_color=black, border_color=button_colors, border_width=7)
        pop_button1 = ctk.CTkButton(self.pop_frame,
                                    text='Close',
                                    width=60,
                                    height=40,
                                    fg_color=button_colors,
                                    hover_color=button_hover_color,
                                    command=self.close_pop)
        pop_button1.place(relx=0.5, rely=0.85, anchor='center')
        pop_button1.configure(font=font_button)

        pop_label = ctk.CTkLabel(master=self.pop_frame, anchor='center', text='Please provide atleast the website or username', fg_color=black)
        pop_label.configure(font=paswd_font)
        pop_label.place(relx=0.5, rely=0.4, anchor='center')
        
        

        # Menu button-----
        button = ctk.CTkButton(master=self.menu_frame,
                               text='Password generator',
                               anchor='w',
                               width=194,
                               height=30,
                               command=self.password_gen_frame,
                               image=adding_generate_button,
                               hover_color=button_hover_color,
                               fg_color=button_colors)
        button.place(relx=0.01, rely=0.085)
        button.configure(font=font_button)

        button1 = ctk.CTkButton(master=self.menu_frame,
                                text='Saved password',
                                anchor='w',
                                width=194,
                                height=30,
                                image=adding_save_image,
                                hover_color=button_hover_color,
                                command=self.saved_password,
                                fg_color=button_colors)
        button1.place(relx=0.01, rely=0.16)
        button1.configure(font=font_button)

       #log = ctk.CTkButton(master=self.menu_frame,
       #                    text='log out',
       #                    anchor='w',
       #                    width=194,
       #                    height=30,
       #                    command=self.log,
       #                    hover_color=button_hover_color,
       #                    fg_color=button_colors)
       #log.place(relx=0.01, rely=0.8)
       #log.configure(font=font_button)

        close = ctk.CTkButton(master=self.menu_frame,
                             text='Exit',
                             anchor='w',
                             width=194,
                             height=30,
                             image=adding_exit_image,
                             hover_color=button_hover_color,
                             command=lambda: exit(),
                             fg_color=button_colors)
        close.place(relx=0.01, rely=0.87)
        close.configure(font=font_button)
        #------------------------------------------------------------------------
        
        #middle frame----
        generate = ctk.CTkButton(master=self.entry_frame,
                                 text='Generate',
                                 width=700,
                                 height=30,
                                 fg_color = button_colors,
                                 border_color=black,
                                 border_width=2,
                                 corner_radius=10,
                                 hover_color=button_hover_color,
                                 image=adding_generate_button,
                                 command=self.generate)
        generate.place(relx=0.5, rely=0.12, anchor='center')
        generate.configure(font=font_button)

        #button to copy password
        self.copy_button = ctk.CTkButton(master=self.entry_frame,
                             text='',
                             anchor='m',
                             state='disabled',
                             width=35,
                             height=35,
                             fg_color=button_colors,
                             image=adding_copy_button,
                             hover_color=button_hover_color,
                             command=self.copy)
        self.copy_button.place(relx=0.5, rely=0.88, anchor='center')
        self.copy_button.configure(font=font_button)
        
        #Buttons of saves_frame
        self.copy_in_frame = ctk.CTkButton(master=self.saves_frame,
                             text='Copy',
                             anchor='m',
                             width=85,
                             height=35,
                             fg_color=button_colors,
                             hover_color=button_hover_color,
                             image=adding_copy_button)
        self.copy_in_frame.place(relx=0.07, rely=0.9, anchor='center')
        self.copy_in_frame.bind('<Button-1>', self.select)
        self.copy_in_frame.configure(font=font_button)

        self.delete_selected = ctk.CTkButton(master=self.saves_frame,
                             text='Delete Selected',
                             anchor='m',
                             width=65,
                             height=35,
                             fg_color=button_colors,
                             hover_color=button_hover_color,
                             image=adding_delete_selected)
        self.delete_selected.place(relx=0.22, rely=0.9, anchor='center')
        self.delete_selected.bind('<Button-1>', self.delete_stuff)
        self.delete_selected.configure(font=font_button)

        self.delete_all = ctk.CTkButton(master=self.saves_frame,
                             text='Delete all',
                             anchor='m',
                             width=87,
                             height=35,
                             fg_color=button_colors,
                             hover_color=button_hover_color,
                             image=adding_delete_all)
        self.delete_all.place(relx=0.91, rely=0.9, anchor='center')
        self.delete_all.bind('<Button-1>', self.delete_all_func)
        self.delete_all.configure(font=font_button)
        #-----------------------------------------------------------------------

        #LABELS--

        #Password----
        self.snippet_label = ctk.CTkLabel(self.password,
                                          text='Password Generator',
                                          fg_color='transparent')
        self.snippet_label.place(relx=0.5, rely=0.0345, anchor='center')
        self.snippet_label.configure(font=font_tuple)

        self.snippet_label1 = ctk.CTkLabel(self.password,
                                           text='Info of Website',
                                           fg_color='transparent')
        self.snippet_label1.place(relx=0.5, rely=0.51, anchor='center')
        self.snippet_label1.configure(font=font_tuple)

        #HEADING OF MENU FRAME--
        self.heading = ctk.CTkLabel(self.menu_frame,
                                    text='Password Manager',
                                    fg_color='transparent')
        self.heading.place(relx=0.5, rely=0.025, anchor='center')
        self.heading.configure(font=logo_font)

        self.password_text = ctk.CTkLabel(self.entry_frame,
                                text='',
                                fg_color="transparent")
        self.password_text.place(relx=0.5, rely=0.5, anchor='center')
        self.password_text.configure(font=paswd_font)
        
        #website name label----
        self.website_name = ctk.CTkLabel(self.info_frame,
                                         text='Website:',
                                         fg_color='transparent')
        self.website_name.place(relx=0.03, rely=0.4, anchor='w')
        self.website_name.configure(font=font_tuple)

        self.username = ctk.CTkLabel(self.info_frame,
                                         text='Username:',
                                         fg_color='transparent')
        self.username.place(relx=0.5, rely=0.4, anchor='center')
        self.username.configure(font=font_tuple)

        self.password_name = ctk.CTkLabel(self.info_frame,
                                         text='Password:',
                                         fg_color='transparent')
        self.password_name.place(relx=0.86, rely=0.4, anchor='e')
        self.password_name.configure(font=font_tuple)

        #Coloumn labels--
        self.website_coloumn = ctk.CTkLabel(self.info_frame,
                                         text='',
                                         fg_color='transparent')
        self.website_coloumn.place(relx=0.03, rely=0.6, anchor='w')
        self.website_coloumn.configure(font=font_button)

        self.username_coloumn = ctk.CTkLabel(self.info_frame,
                                         text='',
                                         fg_color='transparent')
        self.username_coloumn.place(relx=0.5, rely=0.6, anchor='center')
        self.username_coloumn.configure(font=font_button)

        self.password_name_coloumn = ctk.CTkLabel(self.info_frame,
                                         text='',
                                         fg_color='transparent')
        self.password_name_coloumn.place(relx=0.85, rely=0.6, anchor='center')
        self.password_name_coloumn.configure(font=font_button)
        #LABELS END HERE------------------------------------------------------------------------

  
        #Button to insert to database
        self.insert_button = ctk.CTkButton(master=self.info_frame,
                             text='',
                             anchor='m',
                             width=35,
                             height=35,
                             fg_color=button_colors,
                             image=adding_insert_button,
                             hover_color=button_hover_color,
                             command=self.insert_into)
        self.insert_button.place(relx=0.5, rely=0.89, anchor='center')
        self.insert_button.configure(font=font_button)
        #self.info_frame.bind('<Return>', self.insert_into)
        
        
        #log entry
        self.pin_entry = ctk.CTkEntry(self.log_out,
                                      placeholder_text='Enter pin',
                                      takefocus=True,
                                      width=200,
                                      height=65,
                                      justify='center',
                                      show='*')
        self.pin_entry.place(relx=0.5, rely=0.35, anchor='center')
        self.pin_entry.bind('<Return>', self.pin_is_right)
        self.pin_entry.configure(font=paswd_font)
        
        #Log button
        self.log_in_button = ctk.CTkButton(master=self.log_out,
                                           text='Enter',
                                           width=100,
                                           height=30,
                                           hover_color=button_hover_color,
                                           compound='left',
                                           anchor='center',
                                           image=adding_enter_button,
                                           fg_color=button_colors)
        self.log_in_button.place(relx=0.5, rely=0.6, anchor='center')
        self.log_in_button.bind('<Button-1>', command=self.pin_is_right)
        self.log_in_button.configure(font=font_button)

        #entry
        self.website_entry = ctk.CTkEntry(self.info_frame, placeholder_text='Website', width=200, takefocus=True)
        self.website_entry.place(relx=0.03, rely=0.15)
        self.website_entry.bind('<Return>', self.take_website)
        self.website_entry.configure(font=entry_font)
        #self.website_entry.bind('<Right>', self.username_entry.focus_set())

        #username entry from bottom frame
        self.username_entry = ctk.CTkEntry(self.info_frame, placeholder_text='Username', width=200, takefocus=True)
        self.username_entry.place(relx=0.7, rely=0.15)
        self.username_entry.bind('<Return>', self.take_username)
        self.username_entry.configure(font=entry_font)

        self.website_entry.bind('<Right>', self.whatever)


        #Search button on second frame
        self.search_entry = ctk.CTkEntry(self.saves_frame, placeholder_text='Search', width=200, takefocus=True)
        self.search_entry.place(relx=0.5, rely=0.035, anchor='center')
        self.search_entry.bind('<Return>', self.search)
        self.search_entry.configure(font=entry_font)

        #Treeveiw(for the info slection)
        self.saved_info = ttk.Treeview(self.saves_frame, columns=('Website','Username','Password'))

        #coloumn for the Treeview
        self.saved_info.column('#0', width=15, stretch= 'NO')
        self.saved_info.column('#1', stretch=tk.YES)
        self.saved_info.column('#2', stretch=tk.YES)
        self.saved_info.column('#3', stretch=tk.YES)

        #Heading for the treeveiw
        self.saved_info.heading('#0', text='')
        self.saved_info.heading('#1', text='Website', anchor='w')
        self.saved_info.heading('#2', text='Username', anchor='w')
        self.saved_info.heading('#3', text='Password', anchor='w')
        self.saved_info.place(relx=0.5, rely=0.46, width=765, height=550, anchor='center')

        self.saved_info.bind('<Return>', self.dont_delete_same)
        self.saved_info.bind('<Control-c>', self.select)
        self.saved_info.bind('<Control-d>', self.delete_stuff)

        #changing style of treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=inside_frame,
                        foreground="white",
                        rowheight = 25,
                        fieldbackground=inside_frame)
        style.map("Treeview", background=[("selected", button_colors)])
        style.map("Treeview", border_colors='green')
        style.map("Treeview.Heading", background=[('active', button_colors)])
        style.configure("Treeview.Heading", background=inside_frame, font=treeview_header, foreground="white", relief="flat")
        #--------------------------------------------------------------------------------------

        #Here because of priority bias
        #if pin is incorrect
        self.wrong_pin = ctk.CTkFrame(self.log_out, fg_color=black, border_color=button_colors, border_width=7)
        wrong_pin_b1 = ctk.CTkButton(self.wrong_pin,
                                    text='Close',
                                    width=60,
                                    height=40,
                                    fg_color=button_colors,
                                    hover_color=button_hover_color,
                                    command=self.close_pin_frame)
        wrong_pin_b1.place(relx=0.5, rely=0.85, anchor='center')
        wrong_pin_b1.configure(font=font_button)

        self.wrong_label = ctk.CTkLabel(master=self.wrong_pin, text='', anchor='center')
        self.wrong_label.configure(font=paswd_font)
        self.wrong_label.place(relx=0.5, rely=0.4, anchor='center')
        #========================================================================================

        #function to be ran with the program
        self.check_for_file()
        self.data_adder()
        self.log_out.tkraise()
        
    def kill_uni_frame(self):
        self.universal_frame.place_forget()
    
    def close_pin_frame(self):
        self.wrong_pin.place_forget()

    def full_exit(self):
        exit()

    #def log(self):
    #    self.log_out.tkraise()

    def focus_on(self, event):
        self.entry_inside_top1.focus_set()

    def pin_is_right(self, event):
        if self.pin_entry.get() != pin:
            self.wrong_label.configure(text='Wrong Pin')
            self.wrong_pin.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.4, anchor='center')
            self.clear_entry()
        else:
            time.sleep(0.15)
            self.log_out.place_forget()

    def clear_entry(self):
        self.website_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.pin_entry.delete(0, 'end')

    def search(self, event):
        a = self.search_entry.get()
        make_it_str = ''
        t = []
        
        for items in self.saved_info.get_children():
            make_it_str = ''.join(str(self.saved_info.item(items)['values'][0:3]))
            if a in make_it_str:
                print(self.saved_info.item(items))
                t.append(items)
            print(make_it_str)
        self.saved_info.selection_set(t)

    def data_adder(self):
        my_cursor.execute("SELECT * FROM saved_data")
    
        for items in my_cursor:
            self.saved_info.insert(parent='', index='end', iid=self.count, text='', values=(items[0], items[1], items[2]))
            self.count += 1
        #Treeveiw ends here---------------------
    
    def password_gen_frame(self):
        time.sleep(0.11)
        self.password.tkraise()

    def generate(self):
        #global g
        self.password_text.configure(text=password_crafter(17))
        self.copy_button.configure(state='enabled')
        self.g = self.password_text.cget('text')
    
    def whatever(self, event):
        self.username_entry.focus_set()

    def copy(self):
        self.website_entry.focus_set()
        pyperclip.copy(self.g)
        self.password_name_coloumn.configure(text=self.g)
        self.password_text.configure(text='')
    
    def take_website(self, event):
        if '.' not in self.website_entry.get():
            self.website_coloumn.configure(text=self.website_entry.get()+'.com')
        else:
            self.website_coloumn.configure(text=self.website_entry.get())
        self.username_entry.focus_set()
    
    def take_username(self, event):
        self.username_coloumn.configure(text=self.username_entry.get())
        self.info_frame.focus()

    def saved_password(self):
       time.sleep(0.11)
       self.saves_frame.tkraise()
        
    def insert_into(self):
        for items in self.name_list():
            if self.website_coloumn.cget('text') == items:    
                self.indexing = self.indexing+1   
                self.website_coloumn.configure(text=self.website_coloumn.cget('text')+str(self.indexing))

        if self.website_coloumn.cget('text') != '' or self.username_coloumn.cget('text') != '':
            my_cursor.execute("INSERT INTO saved_data(website, username, password) VALUES (?,?,?)", ((self.website_coloumn.cget('text'), self.username_coloumn.cget('text'), self.password_name_coloumn.cget('text'))))
        else:
           self.pop_frame.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.4, anchor='center')
           self.pop_frame.tkraise()

        datab.commit()
        self.saved_info.delete(*self.saved_info.get_children())
        
        self.data_adder()
        self.password_name_coloumn.configure(text='')
        self.website_coloumn.configure(text='')
        self.username_coloumn.configure(text='')
        self.entry_frame.focus()
        self.clear_entry()
        
    def name_list(self):
        name = []
        for items in self.saved_info.get_children():
            a = self.saved_info.item(items)['values'][0]
            name.append(a)
        return(name)

    def dont_delete_same(self, event):
        may_work = self.saved_info.selection()
        for item in may_work:
            print(self.saved_info.item(may_work))

    def select(self, event):
        a = ''
        save = self.saved_info.focus()
        a = ', '.join(self.saved_info.item(save)['values'])
        pyperclip.copy(a)
    
    def delete_stuff(self, event):
        t = self.saved_info.selection()

        try:
            for items in t:
                a = (self.saved_info.item(t)['values'][0])
                if a == '':
                    a = (self.saved_info.item(t)['values'][1])
                self.saved_info.delete(t)
                my_cursor.execute('DELETE FROM saved_data WHERE website=? OR username=?', (a, a,))
                datab.commit()
        except:
            pass   

    def delete_all_func(self,event):
        f = self.saved_info.get_children()
        for items in f:
            self.saved_info.delete(items)

        my_cursor.execute('DELETE FROM saved_data')
        datab.commit()
        self.data_adder()

    def close_pop(self):
        self.pop_frame.place_forget()
    
    #top level functions
    def check_for_file(self):
        try:
            with open("data.ini", "r") as f:
                f.readline()
            self.single_pin.destroy()
        except:
            pass
            
    def cancel(self, event):
        self.saves_frame.focus()
        exit()
    
    def confirm(self, event):
        if self.entry_inside_top.get() == '':
            self.universal_frame.place(relx=0.50, rely=0.5, relwidth=0.7, relheight=0.7, anchor='center')
            self.uni_label.configure(text='Please create a pin')
        elif self.entry_inside_top1.get() == '':
            self.universal_frame.place(relx=0.50, rely=0.5, relwidth=0.7, relheight=0.7, anchor='center')
            self.uni_label.configure(text='Password dose not match')
        elif self.entry_inside_top.get() != self.entry_inside_top1.get():
            self.universal_frame.place(relx=0.50, rely=0.5, relwidth=0.7, relheight=0.7, anchor='center')
            self.uni_label.configure(text='Password dose not match')
        else:
            self.check_pin = True
            with open("focus.ini", "w") as f:
                pin = self.entry_inside_top.get()
                f.write(pin)
            
            key = Fernet.generate_key()
            with open('key_save.key', 'wb') as file:
                file.write(key)
           
            read_key = ''
            with open('key_save.key', 'rb') as f:
                read_key = f.read()

            #read data
            encrypt_data = ''
            with open('focus.ini', 'rb') as files:
                encrypt_data = files.read()
            
            encryption_key = Fernet(read_key)

            main_data = encryption_key.encrypt(encrypt_data)

            with open('data.ini', 'wb') as filess:
                filess.write(main_data)
             
        if os.path.exists("focus.ini"):
            os.remove("focus.ini")
            exit()
        else:
            pass


#Initializing program
screen = Pass_gen()
if __name__ == '__main__':
    screen.resizable(False, False)
    screen.bind('<Escape>', exit)
    screen.mainloop()


