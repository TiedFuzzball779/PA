from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Configura la conexión con Arduino
arduino = serial.Serial('/dev/cu.usbserial-1420', 9600, timeout=1)

def read_arduino():
    while True:
        if arduino.in_waiting > 0:
            try:
                line = arduino.readline().decode().strip()
                if line:
                    values = line.split(",")
                    data = {}
                    for i in range(0, len(values), 2):
                        spot_id = int(values[i])
                        value = int(values[i + 1])
                        estado = "Ocupado" if value > 5 else "Libre"
                        data[spot_id] = estado
                    socketio.emit('update_status', data)  # Enviar datos al frontend
            except Exception as e:
                print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')  # Renderizar la interfaz web

if __name__ == '__main__':
    # Iniciar el hilo para leer datos de Arduino
    threading.Thread(target=read_arduino, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)