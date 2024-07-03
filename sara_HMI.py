import customtkinter as custom
import pyfirmata2 as pyfirm
import serial.tools.list_ports



# Initialiser la fenêtre principale
# root_tk = tk.Tk()
root_tk = custom.CTk()
root_tk.geometry("300x500")
root_tk.title("Sara HMI")

is_connected = False
board = None

# Fonctions

def connecter_robot():
    global is_connected, board
    try:
        PORT = 'COM4' # Assurez-vous que ce port est correct pour votre Arduino
        print(f"Trying to connect to {PORT}")
        board = pyfirm.Arduino(PORT)
        is_connected = True
        print("Successfully connected to the robot.")
        status_label.configure(text="STATUS: ON", fg_color="green")
    except Exception as e:
        is_connected = False
        print(f"Failed to connect to {PORT}: {e}")
        status_label.configure(text="STATUS: OFF", fg_color="red")
def check_connexion():
    print("Avalable devices:")
    port_list = serial.tools.list_ports.comports()
    if len(port_list) == 0:
        print("No device found")
    else:
        for port in port_list:
            print(port.device,port.description)


def deconnexion():
    global is_connected,board
    if is_connected:
        board.exit()
        is_connected = False
        status_label.configure(text=" STATUS: OFF ",fg_color="red")
        print("Deconnexion reussie")
    else:
        print("Aucune connexion active")




def move_robot():
    x = axe_x_entry.get()
    y = axe_y_entry.get()
    z = axe_z_entry.get()
    print(f"Move Robot to X: {x}, Y: {y}, Z: {z}")

def open_arm():
    if is_connected:
        print("Open Arm")
    print("Open Arm")

def close_arm():
    print("Close Arm")


def exit():
    print("Fin du programme")
    root_tk.quit()


# Création des labels et des entrées pour les axes
custom.CTkLabel(master=root_tk, text="Axe X").grid(row=0, column=0, padx=10, pady=10)
axe_x_entry = custom.CTkEntry(master=root_tk)
axe_x_entry.grid(row=0, column=1, padx=10, pady=10)

custom.CTkLabel(master=root_tk, text="Axe Y").grid(row=1, column=0, padx=10, pady=10)
axe_y_entry = custom.CTkEntry(master=root_tk)
axe_y_entry.grid(row=1, column=1, padx=10, pady=10)

custom.CTkLabel(master=root_tk, text="Axe Z").grid(row=2, column=0, padx=10, pady=10)
axe_z_entry = custom.CTkEntry(master=root_tk)
axe_z_entry.grid(row=2, column=1, padx=10, pady=10)

# Création des boutons
move_button = custom.CTkButton(master=root_tk, text="Move", command=move_robot)
move_button.grid(row=3, column=0, columnspan=2, pady=20)

open_arm_button = custom.CTkButton(master=root_tk, text="Open Arm", command=open_arm)
open_arm_button.grid(row=4, column=0, pady=10)

close_arm_button = custom.CTkButton(master=root_tk, text="Close Arm", command=close_arm)
close_arm_button.grid(row=4, column=1, pady=10)

connect_button = custom.CTkButton(master=root_tk,text="Connect",command=connecter_robot)
connect_button.grid(row=5,column=0,columnspan=2,pady=10)


# création du label pour le status de la connexion

status_label = custom.CTkLabel(master=root_tk,text="  STATUS: OFF  ",fg_color="red")
status_label.grid(row=6,column=0,columnspan=2,pady=10)

deconnexion_button = custom.CTkButton(master= root_tk,text="Deconnexion",command=deconnexion)
deconnexion_button.grid(row=7,column=0,columnspan=2,pady=10)

# création de la barre de progression
progressbar = custom.CTkProgressBar(root_tk, orientation="horizontal")
progressbar.configure(mode="indeterminate")
progressbar.set(0)
progressbar.grid(row=10,column=0,columnspan=2,pady=10)



check_button = custom.CTkButton(master=root_tk,text="Check connexion",command=check_connexion)
check_button.grid(row=9,column=0,columnspan=2,pady=10)

exit_button = custom.CTkButton(master=root_tk,text="Exit",command=exit)
exit_button.grid(row=11,column=0,columnspan=2,pady=10)


# Lancer la boucle principale de l'interface
root_tk.mainloop()



#
# class SaraHMI:
#     def __init__(self,root):
#         self.root = root
#         self.root.title("Sara HMI")
#         self.root.geometry("800x600")
#         self.root.resizable(False,False)
#         self.root.config(bg="white")
#
#         self.create_widgets()
#
#     def create_widgets(self):
#         # les Widgets
#         customtkinter.CTkLabel(self.root,text="Axe X").grid(row=0,column=0)
#         self.X_entry = customtkinter.CTkEntry(self.root)
#         self.X_entry.grid(row=0,column=1)
#
#         customtkinter.CTkLabel(self.root,text="Axe Y").grid(row=1,column=0)
#         self.Y_entry = customtkinter.CTkEntry(self.root)
#         self.Y_entry.grid(row=1,column=1)
#
#         customtkinter.CTkLabel(self.root,text="Axe Z").grid(row=2,column=0)
#         self.Z_entry = customtkinter.CTkEntry(self.root)
#         self.Z_entry.grid(row=2,column=1)
#
#
#         #boutton pour envoyer les commande
#
#         customtkinter.CTkButton(self.root,text="Move",command=self.move_robot).grid(row=3,column=0, columnspan=2)
#         customtkinter.CTkButton(self.root,text="Open Arm",command=self.open_arm).grid(row=4,column=0,)
#         customtkinter.CTkButton(self.root,text="Close Arm",command=self.close_arm).grid(row=5,column=0,)
#         # customtkinter.CTkButton(self.root,text="Envoyer",command=self.send_command).grid(row=3,column=0)
#
#     def move_robot(self):
#
#         x = self.X_entry.get()
#         y = self.Y_entry.get()
#         z = self.Z_entry.get()
#         print("Move Robot")
#
#     def open_arm(self):
#         print("Open Arm")
#
#     def close_arm(self):
#         print("Close Arm")
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SaraHMI(root)
#     root.mainloop()






#
# root_tk = tk.Tk()  # create the Tk window like you normally do
# root_tk.geometry("400x240")
# root_tk.title("CustomTkinter Test")
#
# def button_function():
#     print("button pressed")
#
# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=root_tk, corner_radius=10, command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
#
# root_tk.mainloop()