import subprocess
import customtkinter as custom
import pyfirmata2 as pyfirm
import serial.tools.list_ports
import random
import time
from PIL import Image, ImageTk


RAMDOM_COLOR = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

# Initialiser la fenêtre principale
# root_tk = tk.Tk()
root_tk = custom.CTk()
root_tk.geometry("1500x700")
root_tk.title("Sara HMI")



is_connected = False
board = None
PORT = None



# Fonctions

def autodetect():
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        PORT = port[0]
    return PORT


def connecter_robot():
    global is_connected, board
    try:
        PORT = autodetect() # # nous avons  cree  une fonction autodetect qui permet de detecter le port automatiquement
        print(f"Trying to connect to {PORT}")
        board = pyfirm.Arduino(PORT)
        is_connected = True
        print("Successfully connected to the robot.")
        status_label.configure(text="STATUS: ON", fg_color="green")
        connect_button.configure(text="ONLINE",state="disabled")
        output_log_frame.configure(text="Successfully connected to the robot.",fg_color="green")

    except Exception as e:
        is_connected = False
        print(f"Failed to connect to {PORT}: {e}")
        status_label.configure(text="STATUS: OFF", fg_color="red")
def check_connexion():
    print("Avalable devices:")
    port_list = serial.tools.list_ports.comports()
    if len(port_list) == 0:
        print("No device found")
        status_label.configure(text="STATUS: OFF", fg_color="red")
        output_log_frame.configure(text="No device found",fg_color="red")
    else:
        for port in port_list:
            print(port.device,port.description)
            output_log_frame.configure(text=f"{port.device} - {port.description}",fg_color="green")



def deconnexion():
    global is_connected,board
    if is_connected:
        board.exit()
        is_connected = False
        status_label.configure(text=" STATUS: OFF ",fg_color="red")
        connect_button.configure(text="Connect",state="normal")
        print("Deconnexion reussie")
        output_log_frame.configure(text="Deconnexion reussie",fg_color="red")
    else:
        print("Aucune connexion active")
        output_log_frame.configure(text="Aucune connexion active",fg_color="red")




def move_robot():
    if is_connected:
        x:int = axe_x_entry.get()
        y:int = axe_y_entry.get()
        z:int = axe_z_entry.get()
        print(f"Move Robot to X: {x}, Y: {y}, Z: {z}")
        output_log_frame.configure(text=f"Move Robot to X: {x}, Y: {y}, Z: {z}")
    else:
        print("Robot not connected")
        output_log_frame.configure(text="Robot not connected",fg_color="red")

def open_arm():
    if is_connected:
        print("Open Arm")
        output_log_frame.configure(text="Open Arm")
    else:
        print("Robot not connected")
        output_log_frame.configure(text="Robot not connected",fg_color="red")

def close_arm():
    if is_connected:
        print("Close Arm")
        output_log_frame.configure(text="Close Arm")
    else:
        print("Robot not connected")
        output_log_frame.configure(text="Robot not connected",fg_color="red")



def exit():
    print("Fin du programme")
    root_tk.quit()

def choix():
    print("choix")
    # option = option_menu.get()
    # print(option)

def upload_firmware():
    if is_connected:
        file_path = custom.filedialog.askopenfilename(filetypes=[("Firmware files", "*.hex")])
        if file_path :

            print("Upload firmware")
            output_log_frame.configure(text="Upload started....")
            progressbar.start()

            #  on utilise avrdude pour uploader le firmware
            # command = f"avrdude -v -patmega328p -carduino -P{PORT} -b115200 -D -Uflash:w:{file_path}:i"
            # subprocess.run(command,check=True,shell=True)

            time.sleep(5)
            progressbar.stop()
            print("Firmware uploaded")
            output_log_frame.configure(text="Firmware uploaded")
    else:
        print("Robot not connected")
        output_log_frame.configure(text="Robot not connected",fg_color="red")

    # //TODO: implementer l'upload du firmware et le progress bar


def upload_image():
    file_path = custom.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        image = Image.open(file_path)
        image = image.resize((400, 300),)
        image_tk = ImageTk.PhotoImage(image)

        view_frame.configure(image=image_tk)
        view_frame.image = image_tk



def led():

    while is_connected:
        try:
            board.digital[13].write(True)
            print("LED ON")
            time.sleep(5)
            board.digital[13].write(False)
            print("LED OFF")
        except Exception as e :
            print(f'Error: {e}')
        return 0

    else:
        print("Robot not connected")
    # // TODO: implementer le controle de la led




# Création des labels et des entrées pour les axes

custom.CTkLabel(master=root_tk, text="Axe X").grid(row=0, column=0, padx=10, pady=10)
axe_x_entry = custom.CTkEntry(master=root_tk,placeholder_text="mm")
axe_x_entry.grid(row=0, column=1, padx=10, pady=10)

custom.CTkLabel(master=root_tk, text="Axe Y").grid(row=1, column=0, padx=10, pady=10)
axe_y_entry = custom.CTkEntry(master=root_tk,placeholder_text="mm")
axe_y_entry.grid(row=1, column=1, padx=10, pady=10)

custom.CTkLabel(master=root_tk, text="Axe Z").grid(row=2, column=0, padx=10, pady=10)
axe_z_entry = custom.CTkEntry(master=root_tk,placeholder_text="mm")
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



check_button = custom.CTkButton(master=root_tk,text="Check connexion",command=check_connexion)
check_button.grid(row=8,column=0,columnspan=2,pady=10)

# Button upload firmware

option_menu_var = custom.StringVar(value="Type de robot")
option_menu = custom.CTkOptionMenu(master=root_tk,values=["SCARA"],command=choix(),variable=option_menu_var)
option_menu.grid(row=9,column=0,columnspan=2,pady=10)


upload_firmware_button = custom.CTkButton(master=root_tk,text="Upload Firmware",command=upload_firmware)
upload_firmware_button.grid(row=10,column=0,columnspan=2,pady=10)




# création de la barre de progression
progressbar = custom.CTkProgressBar(root_tk, orientation="horizontal",determinate_speed=50)
progressbar.configure(mode="determinate")
progressbar.set(0)
progressbar.grid(row=11,column=0,columnspan=2,pady=10)


# Création de la zone de texte pour afficher les logs
view_frame = custom.CTkLabel(master=root_tk,text="",width=600,height=600)
view_frame.grid(row=0,column=3,rowspan=12,padx=10,pady=10)








# Moniteur de sortie

output_log_frame = custom.CTkLabel(master=root_tk,text="COMMAND",width=300,height=50,fg_color="orange",bg_color="white")
output_log_frame.grid(row=12,column=3,rowspan=12,padx=10,pady=10)

upload_image_button = custom.CTkButton(master=root_tk,text="Upload Image",command=upload_image)
upload_image_button.grid(row=12,column=4,columnspan=2,pady=10)


led_button = custom.CTkButton(master=root_tk,text="LED",command=led)
led_button.grid(row=11,column=4,columnspan=2,pady=10)


exit_button = custom.CTkButton(master=root_tk,text="Exit",command=exit)
exit_button.grid(row=12,column=0,columnspan=2,pady=10)


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