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




> **Note:** This program is provided "as is". I cannot offer technical support or updates, but I'm sharing it because it works for me.

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
