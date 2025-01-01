import customtkinter as custom
import serial.tools.list_ports
import threading
import time
from adafruit_motorkit import MotorKit
import board

from sara_HMI import status_label, connect_button, output_log_frame, root_tk, autodetect


class StepperController:
    def __init__(self):
        self.kit = None
        self.current_step = 0
        self._running = False
        self.stepper = None

    def connect(self, port=None):
        try:
            # Initialiser le MotorKit
            self.kit = MotorKit(i2c=board.I2C())
            # Utiliser le stepper 1 (ports M1 et M2) ou stepper 2 (ports M3 et M4)
            self.stepper = self.kit.stepper1
            # Configuration par défaut
            self.stepper.release()
            return True
        except Exception as e:
            print(f"Erreur lors de la connexion au moteur: {e}")
            return False

    def release(self):
        if self.stepper:
            self.stepper.release()

    def move_steps(self, steps, step_style="single"):
        if not self.stepper:
            return False

        self._running = True
        # Définir le style de pas
        if step_style == "single":
            self.stepper.step_style = self.stepper.SINGLE
        elif step_style == "double":
            self.stepper.step_style = self.stepper.DOUBLE
        elif step_style == "interleave":
            self.stepper.step_style = self.stepper.INTERLEAVE
        elif step_style == "microstep":
            self.stepper.step_style = self.stepper.MICROSTEP

        direction = 1 if steps > 0 else -1
        for _ in range(abs(steps)):
            if not self._running:
                break
            self.stepper.onestep(direction=direction)
            self.current_step += direction
            time.sleep(0.01)  # Délai entre les pas

        self.release()  # Relâcher le moteur après le mouvement
        self._running = False

    def stop(self):
        self._running = False
        self.release()


# Créer l'instance du contrôleur de moteur
stepper_controller = StepperController()


class ConnectionMonitor:
    def __init__(self, on_disconnect_callback):
        self._running = False
        self.port = None
        self.on_disconnect = on_disconnect_callback
        self.thread = None

    def start_monitoring(self, port):
        self.port = port
        self._running = True
        self.thread = threading.Thread(target=self._monitor_connection)
        self.thread.daemon = True
        self.thread.start()

    def stop_monitoring(self):
        self._running = False
        if self.thread:
            self.thread.join()

    def _monitor_connection(self):
        while self._running:
            connected_ports = [port.device for port in serial.tools.list_ports.comports()]
            if self.port not in connected_ports:
                print(f"Disconnection detected on port {self.port}")
                self._running = False
                root_tk.after(0, self.on_disconnect)
            time.sleep(1)


def handle_disconnect():
    global is_connected
    print("Déconnexion détectée!")
    is_connected = False
    stepper_controller.release()
    status_label.configure(text="STATUS: OFF", fg_color="red")
    connect_button.configure(text="Connect", state="normal")
    output_log_frame.configure(text="Déconnexion détectée! Câble débranché.", fg_color="red")


def connecter_robot():
    global is_connected, connection_monitor
    try:
        # Connecter le contrôleur de moteur
        if stepper_controller.connect():
            is_connected = True
            print("Successfully connected to the motor.")
            status_label.configure(text="STATUS: ON", fg_color="green")
            connect_button.configure(text="ONLINE", state="disabled")
            output_log_frame.configure(text="Successfully connected to the motor.", fg_color="green")

            # Démarrer la surveillance de la connexion
            PORT = autodetect()
            if PORT:
                connection_monitor.start_monitoring(PORT)
        else:
            raise Exception("Failed to initialize motor controller")

    except Exception as e:
        is_connected = False
        print(f"Failed to connect: {e}")
        status_label.configure(text="STATUS: OFF", fg_color="red")
        output_log_frame.configure(text=f"Failed to connect: {e}", fg_color="red")


def move_motor():
    if is_connected:
        try:
            steps = int(steps_entry.get())  # Nombre de pas
            step_style = step_style_var.get()  # Style de pas

            # Lancer le mouvement dans un thread séparé
            thread = threading.Thread(target=lambda: stepper_controller.move_steps(steps, step_style))
            thread.daemon = True
            thread.start()

            print(f"Moving motor {steps} steps in {step_style} mode")
            output_log_frame.configure(text=f"Moving motor {steps} steps in {step_style} mode", fg_color="green")
        except ValueError as e:
            print(f"Invalid input: {e}")
            output_log_frame.configure(text="Invalid input", fg_color="red")
    else:
        print("Motor not connected")
        output_log_frame.configure(text="Motor not connected", fg_color="red")


def stop_motor():
    if is_connected:
        stepper_controller.stop()
        print("Motor stopped")
        output_log_frame.configure(text="Motor stopped", fg_color="orange")


# Création des contrôles de l'interface
custom.CTkLabel(master=root_tk, text="Nombre de pas").grid(row=0, column=0, padx=10, pady=10)
steps_entry = custom.CTkEntry(master=root_tk, placeholder_text="pas")
steps_entry.grid(row=0, column=1, padx=10, pady=10)

# Menu déroulant pour le style de pas
step_style_var = custom.StringVar(value="single")
custom.CTkLabel(master=root_tk, text="Style de pas").grid(row=1, column=0, padx=10, pady=10)
step_style_menu = custom.CTkOptionMenu(
    master=root_tk,
    values=["single", "double", "interleave", "microstep"],
    variable=step_style_var
)
step_style_menu.grid(row=1, column=1, padx=10, pady=10)

# Boutons de contrôle
move_button = custom.CTkButton(master=root_tk, text="Déplacer moteur", command=move_motor)
move_button.grid(row=2, column=0, columnspan=2, pady=10)

stop_button = custom.CTkButton(master=root_tk, text="Arrêter moteur", command=stop_motor)
stop_button.grid(row=3, column=0, columnspan=2, pady=10)

# Initialisation du moniteur de connexion
connection_monitor = ConnectionMonitor(handle_disconnect)