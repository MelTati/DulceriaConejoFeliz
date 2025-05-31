# 🐇 Conejo Feliz - Sistema de Ventas y Compras

**Tecnologías:** Python 3.8+ · MySQL 8.0+ · PyQt6

## 📦 Requisitos previos

- Python 3.8 o superior
- MySQL Server 8.0 o superior
- Git (opcional)

## 🛠️ Instalación paso a paso

1. **Clonar el repositorio:**

   ```bash
   git clone [text](https://github.com/MelTati/ProyectoConejoFeliz.git)
   cd Mel-Tati
   ```

2. **Configurar entorno virtual:**

   ```bash
   python -m venv 23270676
   ```

   Para activar:

   - **Windows:** `23270676\Scripts\activate`
   - **Linux/Mac:** `source 23270676/bin/activate`

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

## 📄 Estructura del proyecto

```
PROYECTOFINALS4A2/
├── __pycache__/
├── config/
├── controllers/
├── db/
├── icons/
├── models/
├── PROYECTOFINALS4A2/
├── views/
├── login.py
├── main.py
├── prueba1.pdf
├── readme.md
└── requirements.txt

🖥️ INICIAR EL SISTEMA
python login.py


```

## ✨ Características clave del proyecto

- 🔑 **Login:** Pantalla de inicio de sesión para acceso seguro al sistema.
- 👤 **Gestión de usuarios:** Login seguro y control de acceso por roles (Supervisor, Cajero).
- 👥 **Gestión de clientes:** Alta, baja y modificación de clientes.
- 🏢 **Gestión de proveedores:** Alta, baja y modificación de proveedores.
- 🛒 **Gestión de ventas y compras:** Registro, consulta y actualización de ventas y compras.
- 🧾 **Generación de tickets:** El sistema emite un comprobante detallado por cada venta realizada.
- 📦 **Control de inventario:** Manejo de artículos, stock, categorías y marcas.
- 🖥️ **Interfaz gráfica amigable:** Desarrollada con PyQt6 para facilitar el uso.
- 🗄️ **Persistencia de datos:** Uso de MySQL para almacenar toda la información.
- 🔒 **Seguridad:** Validación de credenciales y manejo de errores.
- 🛠️ **Modularidad:** Código organizado en modelos, controladores y vistas (MVC).
- 📑 **Detalles de compras:** Consulta y gestión de los productos adquiridos en cada compra, permitiendo ver información específica de cada transacción de compra.
- 🏷️ **Gestión de categorías:** Organización y clasificación de artículos para facilitar su búsqueda y control.
- 🏷️ **Gestión de marcas:** Organización y clasificación de artículos por marca para facilitar su búsqueda y control.
