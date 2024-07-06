import customtkinter
import random
import serial.tools.list_ports

PORT = None
list_port = []





def autodetect():
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        PORT = port[0]
    return PORT


PORT = autodetect()

print(PORT)

print(type(PORT))




# def button_callback():
#     global PORT,list_port
#     port_list = serial.tools.list_ports.comports()
#     if len(port_list) == 0:
#         print("No fund")
#     else:
#         for port in port_list:
#             print(port)
#             PORT = port[0]



# print(PORT)

#
#
#
# app = customtkinter.CTk()
# app.geometry("400x150")
#
# button = customtkinter.CTkButton(app, text="my button", command=button_callback)
# button.pack(padx=20, pady=20)
#
# app.mainloop()