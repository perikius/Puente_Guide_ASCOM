# -*- coding: utf-8 -*-
import serial
import serial.tools.list_ports  # Importante para listar puertos
import win32com.client
import time
import sys

# --- SELECCIÓN AUTOMÁTICA DE PUERTO ---
def seleccionar_puerto():
    puertos = list(serial.tools.list_ports.comports())
    
    if not puertos:
        print("Error: No se detectaron puertos COM disponibles.")
        input("Presiona Enter para salir...")
        sys.exit()

    print("\n--- Puertos COM detectados ---")
    for i, p in enumerate(puertos):
        # Muestra el nombre (COMx) y la descripción del dispositivo
        print(f"{i + 1}: {p.device} - {p.description}")

    while True:
        try:
            seleccion = int(input("\nSelecciona el número del puerto (ej. 1): "))
            if 1 <= seleccion <= len(puertos):
                return puertos[seleccion - 1].device
            else:
                print(f"Por favor, elige un número entre 1 y {len(puertos)}.")
        except ValueError:
            print("Entrada no válida. Introduce solo el número.")

# Asignamos el puerto elegido por el usuario
SERIAL_PORT = seleccionar_puerto()

BAUD_RATE = 9600
ASCOM_DRIVER_ID = "ASCOM.DeviceHub.Telescope" 

# --- VELOCIDADES (Ajustadas a lo que pide tu Driver) ---
VEL_GUIDE = 1.0    
VEL_CENTER = 2.0   
VEL_FIND = 3.0     
VEL_SLEW = 4.0     
velocidad_actual = VEL_CENTER 

def start_translator():
    mount = None
    ser = None
    global velocidad_actual

    try:
        # 1. CONECTAR ASCOM
        print(f"Conectando a ASCOM: {ASCOM_DRIVER_ID}...")
        mount = win32com.client.Dispatch(ASCOM_DRIVER_ID)
        if not mount.Connected:
            mount.Connected = True
        print("Montura ASCOM conectada.")

        # 2. ABRIR PUERTO SERIE
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        print(f"Escuchando en {SERIAL_PORT} para Guide 9.1...")

        buffer = ""
        
        while True:
            time.sleep(0.01) 
            if ser.in_waiting > 0:
                # 1. Leemos todo lo que haya llegado (pueden ser varios comandos)
                datos_nuevos = ser.read(ser.in_waiting).decode('ascii', errors='ignore')
                buffer += datos_nuevos
                
                # 2. Mientras haya un '#' en el buffer, hay al menos un comando completo
                while '#' in buffer:
                    pos_hash = buffer.find('#')
                    # Extraemos desde el principio hasta el primer '#'
                    cmd = buffer[:pos_hash + 1].strip()
                    # Dejamos el resto en el buffer para la siguiente vuelta
                    buffer = buffer[pos_hash + 1:]

                    # --- LECTURA DE COORDENADAS ---
                    if ":GR#" in cmd:
                        try:
                            ra_decimal = float(mount.RightAscension)
                            h = int(ra_decimal); m = int((ra_decimal * 60) % 60); s = int((ra_decimal * 3600) % 60)
                            resp = f"{h:02d}:{m:02d}:{s:02d}#"
                            ser.write(resp.encode('ascii'))
                            print(f"<- RA: {resp}", flush=True)
                        except: pass

                    elif ":GD#" in cmd:
                        try:
                            dec_decimal = float(mount.Declination)
                            signo = "+" if dec_decimal >= 0 else "-"
                            abs_dec = abs(dec_decimal)
                            d = int(abs_dec); m = int((abs_dec * 60) % 60); s = int((abs_dec * 3600) % 60)
                            resp = f"{signo}{d:02d}*{m:02d}'{s:02d}#"
                            ser.write(resp.encode('ascii'))
                            print(f"<- DEC: {resp}", flush=True)
                        except: pass

                    # --- SET TARGETS (GOTO) ---
                    elif cmd.startswith(":Sr"):
                        try:
                            # 1. Limpieza: ":Sr05:31:02#" -> "05:31:02"
                            raw = cmd[3:-1].strip()
                            print(f"DEBUG Sr Recibido: '{raw}'")
                            
                            # 2. Separar por dos puntos
                            parts = raw.split(':')
                            
                            # Horas (siempre las primeras)
                            h = float(parts[0])
                            
                            # Minutos y Segundos
                            if len(parts) > 1:
                                m = float(parts[1])
                                s = float(parts[2]) if len(parts) > 2 else 0.0
                            else:
                                # Caso raro: Guide manda solo horas decimales
                                m = (h % 1) * 60
                                s = (m % 1) * 60
                                h = int(h)
                                
                            ra_to_set = h + (m / 60.0) + (s / 3600.0)
                            
                            # 3. Enviar a ASCOM (RA debe estar entre 0 y 24)
                            if 0 <= ra_to_set < 24:
                                mount.TargetRightAscension = ra_to_set
                                ser.write(b"1")
                                print(f"-> Target RA OK: {ra_to_set:.4f}")
                            else:
                                raise ValueError(f"RA fuera de rango: {ra_to_set}")
                                
                        except Exception as e:
                            ser.write(b"0")
                            print(f"Error procesando Sr: {e}")




                    elif cmd.startswith(":Sd"):
                        try:
                            # 1. Ver qué recibe Python exactamente
                            raw = cmd[3:-1].strip() # Recibe '+4601:18'
                            print(f"DEBUG Sd Recibido: '{raw}'")

                            # 2. Extraer signo
                            signo = -1 if "-" in raw else 1
                            # Quitamos signo para procesar números: '4601:18'
                            val = raw.replace('+', '').replace('-', '')
                            
                            # 3. Procesar por posiciones fijas según tu debug:
                            # '46' son los grados (posiciones 0 y 1)
                            # '01:18' son los minutos y segundos (desde posición 2 en adelante)
                            d = float(val[:2])
                            
                            # Limpiamos los minutos de los dos puntos para que sea float: '01.18'
                            m_raw = val[2:].replace(':', '.') 
                            m = float(m_raw)
                            
                            dec_to_set = signo * (d + (m / 60.0))
                            
                            # 4. Enviar a ASCOM
                            if -90 <= dec_to_set <= 90:
                                mount.TargetDeclination = dec_to_set
                                ser.write(b"1")
                                print(f"-> Target DEC OK: {dec_to_set:.4f}")
                            else:
                                print(f"RANGO EXCEDIDO: {dec_to_set}")
                                ser.write(b"0")
                                
                        except Exception as e:
                            ser.write(b"0")
                            print(f"Error procesando Sd: {e}")


                    # --- MOVIMIENTOS Y GOTO ---
                    elif cmd == ":MS#":
                        try:
                            # Importante: ASCOM requiere SlewToTargetAsync para no bloquear
                            mount.SlewToTargetAsync()
                            ser.write(b"0") # '0' en LX200 significa "Aceptado, iniciando"
                            print("!!! GOTO INICIADO")
                        except Exception as e:
                            ser.write(b"1Obstruido#")
                            print(f"Error MS: {e}")

                    elif cmd == ":CM#":
                        try:
                            mount.SyncToTarget()
                            ser.write(b"M31#") # Respuesta genérica de éxito en Sync
                            print("!!! SYNC OK")
                        except:
                            ser.write(b"0#")


                    # --- FLECHAS DE MOVIMIENTO MANUAL ---
                    elif cmd in [":Mn#", ":Ms#", ":Me#", ":Mw#"]:
                        try:
                            eje = 1 if cmd in [":Mn#", ":Ms#"] else 0
                            sentido = velocidad_actual if cmd in [":Mn#", ":Me#"] else -velocidad_actual
                            mount.MoveAxis(eje, sentido)
                            print(f"-> Moviendo {cmd} a v={velocidad_actual}", flush=True)
                        except Exception as e: print(f"Error MoveAxis: {e}")

                    elif cmd in [":Qn#", ":Qs#", ":Qe#", ":Qw#", ":Q#"]:
                        try:
                            if cmd == ":Q#": mount.AbortSlew()
                            else:
                                eje = 1 if cmd in [":Qn#", ":Qs#"] else 0
                                mount.MoveAxis(eje, 0.0)
                            print(f"<- Parada: {cmd}", flush=True)
                        except: pass

                    # --- CAMBIO DE VELOCIDADES ---
                    elif cmd == ":RG#": velocidad_actual = VEL_GUIDE; print("Vel: GUIA")
                    elif cmd == ":RC#": velocidad_actual = VEL_CENTER; print("Vel: CENTRADO")
                    elif cmd == ":RM#": velocidad_actual = VEL_FIND; print("Vel: BUSQUEDA")
                    elif cmd == ":RS#": velocidad_actual = VEL_SLEW; print("Vel: MAXIMA")

    except Exception as e:
        print(f"Error fatal: {e}")

    finally:
        # CIERRE MÍNIMO Y SEGURO
        if mount is not None:
            try:
                # Solo paramos si el telescopio se está moviendo rápido (GOTO)
                if mount.Slewing:
                    mount.AbortSlew()
                # Nos desconectamos nosotros, pero dejamos el ASCOM Hub encendido
                mount.Connected = False
            except:
                pass
        if ser is not None:
            ser.close()
        print("Puente Guide finalizado.")

if __name__ == "__main__":
    start_translator()
