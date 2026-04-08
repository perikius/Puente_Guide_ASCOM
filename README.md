# 🔭 Puente_Guide_ASCOM

[English version below / Versión en español a continuación]

---

# English Version

This is a personal project intended to reconnect my telescope with the veteran and historical software **Guide 9.1**, which I hold in high regard.

## 🛠️ 1. User Section (Using the Executable)
If you don't code and just want your Guide 9.1 to move the telescope again with modern ASCOM versions, this section is for you.

### How to get started:
1. **Download:** Go to the **[Releases]** section on the right side of this page and download the `.zip` file containing the executable and Manual_Setup.pdf.
2. **Requirement:** Install **com0com** to create a pair of linked virtual ports (e.g., COM10 <-> COM11).
3. **Step-by-step Guide:** Open the `Manual_Setup_EN.pdf` file included in this repository. It contains screenshots to configure Guide and the bridge.

### Manual_Setup
This program acts as a communication bridge to allow Guide software to send and receive commands using the ASCOM 7.1 Device Hub. It connects both to the Device Hub COM object and to a virtual serial port linked to Guide's port. It formats LX200 commands to ensure seamless communication.

<img width="661" height="219" alt="7-Esquema" src="https://github.com/user-attachments/assets/cf66faff-2d99-48e5-9523-6ecf26277828" />
General scheme using example virtual ports COM4 == COM5 

#### 1. Serial Port Emulation :
It is necessary to create two linked virtual ports. Guide will connect to one, and "Puente_Guide_ASCOM" will connect to the other. I have used 'com0com' for this link. You can download version 3.0.0.0 here: :
https://sourceforge.net/projects/com0com/files/com0com/3.0.0.0/
<img width="855" height="225" alt="1-com0com" src="https://github.com/user-attachments/assets/9a8a3447-ee64-42c2-9f63-3b4302a2ac26" />
1. Create a new pair with "Add Pair" and rename them using available ports (e.g., COM4 – COM5). Check the Windows Device Manager to ensure they are not in use. 

2. Enable these options: ‘use Ports class’, ‘emulate baud rate’, and ‘enable buffer overrun’ on both ports.

<img width="443" height="391" alt="2-com0com" src="https://github.com/user-attachments/assets/9dd839bc-8344-48c3-85a1-d499e977ff60" />

Press Apply. Once the ports are created, close ‘com0com’; you won't need to create them again. 

3. Verify in the Device Manager that the ports are active.
<img width="349" height="110" alt="3-Dispositivos" src="https://github.com/user-attachments/assets/93624385-b744-4b84-a5df-105ddf8669ae" />

4. The final scheme will look like this:
<img width="527" height="76" alt="8-EsquemaR" src="https://github.com/user-attachments/assets/efca8c42-8358-41bc-a24a-ddca44c41e8d" />


### 2. Instructions for Use: 

1. ASCOM: Connect your telescope to the Device Hub as you usually do. 

2. Open “Puente_Guide_ASCOM”: A list of detected ports will appear. Select the port that will receive data from the one linked to Guide (in the example, COM5).
<img width="468" height="186" alt="4-Puente_Guide" src="https://github.com/user-attachments/assets/5cd71bb1-98a6-445b-88f3-b517e5f63f40" />

Example: If COM5 is the fourth in the list, type ’4’.

<img width="469" height="232" alt="6-Puente-Guide-espera" src="https://github.com/user-attachments/assets/f09fd624-9044-4af7-8292-e50da9fc5c38" />

Once the port is selected, “Puente_Guide_ASCOM” connects to the Device Hub and waits for commands from Guide 9.1.

3. Configure Guide: Go to Settings -> Telescope Control, select the linked port (in the example, COM4), and choose the LX-200 protocol.
Note: COM ports higher than COM8 did not work for me in Guide 9.1.
<img width="218" height="308" alt="5-ControlTelescopio" src="https://github.com/user-attachments/assets/3205dbfa-2595-4690-ad74-ab60c30acdca" />

4. Ready! You can now use Guide.
The exchanged commands will appear in the “Puente_Guide_ASCOM” terminal window. 
<img width="474" height="486" alt="6-Puente-Guide-comunicacion" src="https://github.com/user-attachments/assets/f5fb555f-953c-49b2-ab55-07d2f2db5818" />

The program manages synchronization and coordinate commands: :Sr..#, :Sd...#, :CM#, :MS#, :GD#, :GR#. 

Note on speeds: Although the bridge recognizes movement and guide rate commands (:RG#, :RC#,...  :Mn#, :Ms#,... etc.), it is recommended to use the arrow keys and speed controls from other software or the ASCOM Device Hub for better precision. 


* Troubleshooting: If ‘com0com’ or the executable fails to register ports, try "Run as administrator". 

5. How to close correctly (IMPORTANT): 

To prevent ports from becoming blocked or "hanging," do not close the window using the "X". Press Ctrl + C inside the “Puente_Guide_ASCOM” terminal window to finish the process safely.

It is best to close “Puente_Guide_ASCOM” before other programs. 



> **Note:** This program is provided "as is". I cannot offer technical support or updates.

## 💻 2. Developer Information (Technical Overview)
This project acts as a *middleware* between the legacy serial protocol of Guide 9.1 and the ASCOM 7.1 COM interface.

### 🏗️ Link Architecture
* **Command Transport:** Requires a pair of virtual ports (via com0com). Port A is assigned to Guide (LX200) and Port B to the Python script.
* **Command Translation:** The script acts as a serial server, processes requests, and redirects them to the ASCOM Device Hub via COM objects.

### 🛠️ Script Details (`Puente_Guide_ASCOM.py`)
* **Stack:** Python 3.x.
* **Dependencies:** `pyserial` (Port B management) and `pywin32` (ASCOM communication).
* **Port Selection:** Automatic enumeration routine for available COM ports.
* **Command Logic (Parsing):** Accumulative buffer with `#` delimiter to ensure LX200 command integrity.
* **Coordinate Conversion:** Sanitization of sexagesimal strings and normalization to `float` for ASCOM.
* **Movement Control:** Use of `SlewToTargetAsync` for real-time interruption (Abort).
* **Safety:** Implements `AbortSlew` on close and exception handling via a `finally` block (*Graceful Shutdown*).

### 📦 Build
If you wish to generate your own executable, the exact command used is:
`pyinstaller --onefile --hidden-import=win32timezone --icon=icono.ico Puente_Guide_ASCOM.py`

---

# Versión en Español

Este es un proyecto personal, con la intención de volver a conectar mi telescopio al veterano e histórico programa **Guide 9.1**, al que le tengo un especial aprecio.

## 🛠️ 1. Sección para Usuarios (Uso del Ejecutable)
Si no programas y solo quieres que tu Guide 9.1 vuelva a mover el telescopio con las versiones modernas de ASCOM, esta es tu sección.

### Cómo ponerlo en marcha:
1. **Descarga:** Ve al apartado **[Releases]** a la derecha de esta página y descarga el archivo `.zip` que contiene el ejecutable.
2. **Requisito:** Instala **com0com** para crear un par de puertos virtuales enlazados (ej. COM10 <-> COM11).
3. **Guía paso a paso:** Abre el archivo `Manual_Configuracion_ES.pdf` incluido en este repositorio.

### Manual_Instalación
El programa hace un puente de comunicación para permitir que el software Guide envíe y reciba los comandos con Device Hub de ASCOM 7.1. Se conecta tanto al objeto COM del Device Hub como a un puerto serie virtual vinculado al puerto de Guide. Para ello formatea los comandos LX200 que se envían para realizar la comunicación.
<img width="661" height="219" alt="7-Esquema" src="https://github.com/user-attachments/assets/525c1322-56ef-48c2-8c0b-b3d652e90fcd" />
Este sería el esquema general usando los puertos virtuales de ejemplo COM4==COM5

#### 1. Emulación de puertos serie:
Es necesario crear 2 puertos virtuales y vinculados. Guide se conectará a uno de ellos y “Puente_Guide_ASCOM” se conectará al otro.  Para realizar este enlace he usado el programa ‘com0com’. Hay que descargar la versión 3.0.0.0 de aquí:
https://sourceforge.net/projects/com0com/files/com0com/3.0.0.0/
<img width="855" height="225" alt="1-com0com" src="https://github.com/user-attachments/assets/2973bc9a-d4e4-47a6-a198-035b64c0193f" />
1. Crea un nuevo par con Add Pair, cambia los nombres con puertos que tengas libres (ej. COM4 – COM5). Consulta el Administrador de dispositivos de Windows para asegurarte que no están en uso.

2. Activa opciones: ‘use Ports class’, ‘emulate baud rate’ y ‘enable buffer overrun’ en ambos.
<img width="443" height="391" alt="2-com0com" src="https://github.com/user-attachments/assets/26517aba-58cc-469d-a0f2-37a1dc538553" />

Pulsa Apply. Creados los puertos cierra ‘como0com’, no necesitarás volver a crearlos.

3. Verifica en el Administrador de dispositivos que los puertos están activos.
<img width="349" height="110" alt="3-Dispositivos" src="https://github.com/user-attachments/assets/01a4bcb6-5bbf-450d-9795-70940aa76cb6" />

4. Ahora el esquema quedaría así
<img width="527" height="76" alt="8-EsquemaR" src="https://github.com/user-attachments/assets/1ed644dc-d5ce-450b-a989-e861c4947d0f" />

#### 2. Instrucciones de uso

1. ASCOM: Conecta el telescopio al Device Hub como lo haces habitualmente.

2. Abre “Puente_Guide_ASCOM”. Aparecerá la lista de los puertos detectados; selecciona el que usarás para recibir los datos del puerto que enlaza con el que usa Guide, en el ejemplo el COM5.
<img width="468" height="186" alt="4-Puente_Guide" src="https://github.com/user-attachments/assets/b1df1723-20ab-4cf7-b889-628612d8501b" />

Ejemplo: si el COM5 es el cuarto de la lista, introducimos el número ’4’

<img width="469" height="232" alt="6-Puente-Guide-espera" src="https://github.com/user-attachments/assets/bcb2a3c0-ca32-431c-a690-7e2251ebe7ee" />

Seleccionado el puerto, “Puente_Guide_ASCOM” se conecta al DeviceHub y queda a la espera de los comandos de Guide 9.1

3. Configurar Guide: En Ajustes -> Control Telescopio, selecciona el puerto vinculado (en el ejemplo, COM4) y utiliza el protocolo LX200.
Nota: Los puertos superiores a COM8 no me han funcionado en Guide 9.1.
<img width="218" height="308" alt="5-ControlTelescopio" src="https://github.com/user-attachments/assets/229985b2-ab12-4575-867e-391db5f83429" />

4. ¡Listo! Ya puedes usar Guide.

Los comandos que se intercambien irán apareciendo en la ventana del programa Puente_Guide_ASCOM.

<img width="474" height="486" alt="6-Puente-Guide-comunicacion" src="https://github.com/user-attachments/assets/c1aec2f7-254a-4ea0-b725-ca71bf1dc7b5" />

El programa gestiona los comandos de sincronización y coordenadas:
 :Sr..#, :Sd...#, :CM#, :MS#, :GD#, :GR#.

Nota sobre velocidades: Aunque el puente reconoce los comandos de movimiento y tasa de guía (:RG#, :RC#..., :Mn#, :Ms#... etc.), se recomienda usar las flechas y controles de velocidad desde otro software o los de Device Hub de ASCOM para mayor precisión.

* Si notas que “com0com” o el ejecutable fallan al registrar puertos, prueba "Ejecutar como administrador"

5. Cómo cerrar correctamente (IMPORTANTE)

Para evitar que los puertos queden bloqueados o "colgados", no cierres la ventana del programa  con la X. Presiona Ctrl + C dentro de la ventana de la terminal de “Puente_Guide_ASCOM” para finalizar el proceso de forma segura.

Es conveniente cerrar primero “Puente_Guide_ASCOM” antes que el resto de programas.



> **Nota:** Este programa se entrega "tal cual" (*as is*). No puedo ofrecer soporte técnico ni actualizaciones.

## 💻 2. Información para Desarrolladores (Technical Overview)

Este proyecto funciona como un *middleware* entre el protocolo serie heredado de Guide 9.1 y la interfaz COM de ASCOM 7.1.

### 🏗️ Arquitectura del Enlace
*   **Transporte Comandos:** Requiere un par de puertos virtuales (vía com0com). El puerto A se asigna a Guide (LX200) y el puerto B al script de Python.
*   **Traducción Comandos:** El script actúa como servidor serie, procesa las peticiones y las redirige al ASCOM Device Hub mediante objetos COM.

### 🛠️ Detalles del Script (`Puente_Guide_ASCOM.py`)
*   **Stack:** Python 3.x.
*   **Dependencias:** `pyserial` (gestión del puerto B) y `pywin32` (comunicación con ASCOM).
*   **Selección de Puertos:** Rutina de enumeración automática de puertos COM disponibles.
*   **Lógica de Comandos (Parsing):** Buffer acumulativo con delimitador `#` para garantizar la integridad de los comandos LX200.
*   **Conversión de Coordenadas:** Limpieza de strings sexagesimales y normalización a `float` para ASCOM.
*   **Control de Movimiento:** Uso de `SlewToTargetAsync` para permitir la interrupción (Abort) en tiempo real.
*   **Seguridad:** Implementa `AbortSlew` en el cierre y gestión de excepciones mediante un bloque `finally` (*Graceful Shutdown*) para liberar el puerto serie y el objeto COM.

### 📦 Compilación (Build)
Si deseas generar tu propio ejecutable, el comando exacto utilizado es:

`pyinstaller --onefile --hidden-import=win32timezone --icon=icono.ico Puente_Guide_ASCOM.py`

---

### ⚠️ Important Notes / Notas Importantes

**English:**
* **No Support:** I am not a professional programmer. This is a personal "workaround". No technical support or inquiries will be provided.
* **Open Source:** Provided "as is". Feel free to fork or improve it.
* **Responsibility:** Use at your own risk.

**Español:**
* **Sin soporte:** No soy programador profesional. Es un "apaño" personal. No se ofrecerá soporte técnico ni respuesta a consultas.
* **Código abierto:** Se entrega "tal cual". Siéntete libre de clonar o mejorar el código.
* **Responsabilidad:** El uso de este software es bajo tu propia responsabilidad.

**Clear Skies! / ¡Cielos Despejados!**
