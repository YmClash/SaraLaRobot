import customtkinter
import random
import serial.tools.list_ports
import pyfirmata2 as pyfirm



import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import platform



print(platform.machine())
print(platform.version())
print(platform.platform())
print(platform.processor())
print(platform.system())
devices = serial.tools.list_ports.comports()


print()
if len(devices) !=0 :
    for device in  devices:
        print(device.name , device.description)
else:
        print("No devices connected to the system")

print(len(devices))



print("Hello World")
