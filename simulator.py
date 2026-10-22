import time
import random
import requests

# Configuración
API_URL = "http://127.0.0.1:8000/api/readings/"
SENSOR_ID = "c92fdf03-ce07-48ad-b043-9043341e026d"  

def run_simulation():
    water_level = 80.0  # Nivel inicial seguro (en cm)
    battery = 100
    
    print(f"🌊 Iniciando simulación IoT para el sensor: {SENSOR_ID}")
    print("Presiona Ctrl + C para detener.\n")
    
    try:
        while True:
            # Simulamos lluvia: el agua sube entre 10 y 30 cm por ciclo (con ligeras variaciones)
            variation = random.uniform(10.0, 30.0)
            water_level = round(water_level + variation, 2)
            
            # Si supera los 280 cm, reiniciamos el ciclo para simular que bajó el nivel
            if water_level > 280.0:
                print("🔄 Nivel máximo de prueba alcanzado. Reiniciando cauce a nivel normal...")
                water_level = 80.0

            # Simulamos descarga lenta de batería
            if random.random() < 0.2 and battery > 15:
                battery -= 1

            payload = {
                "sensor_id": SENSOR_ID,
                "water_level_cm": water_level,
                "battery_level": battery
            }

            response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                estado = "🟢 NORMAL"
                if water_level >= 220.0:
                    estado = "🔴 CRÍTICO (Alerta generada)"
                elif water_level >= 150.0:
                    estado = "🟡 ADVERTENCIA (Alerta generada)"
                    
                print(f"[{estado}] Nivel enviado: {water_level} cm | Batería: {battery}%")
            else:
                print(f"⚠️ Error al enviar lectura ({response.status_code}): {response.text}")

            # Espera 5 segundos antes de la siguiente lectura
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Simulación detenida por el usuario.")

if __name__ == "__main__":
    run_simulation()