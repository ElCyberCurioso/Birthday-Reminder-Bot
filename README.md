# 🎂 Bot de Cumpleaños para Telegram

Esta es una aplicación contenerizada en Docker que gestiona recordatorios de cumpleaños a través de un bot de Telegram. Permite agregar personas, fechas de nacimiento y configurar con cuántos días de anticipación deseas recibir una notificación.

## 🚀 Características

*   **Gestión por Chat**: Cada usuario/grupo gestiona su propia lista de cumpleaños.
*   **Recordatorios Personalizables**: Tú decides cuántos días antes quieres que te avise.
*   **Notificación el Día del Evento**: También recibes un aviso el mismo día del cumpleaños.
*   **Persistencia de Datos**: Utiliza SQLite para guardar la información, persistiendo aunque se reinicie el contenedor.
*   **Docker Ready**: Listo para desplegar en cualquier entorno con Docker.

## 📋 Requisitos Previos

*   [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados.
*   Un Token de Bot de Telegram (obtenido de [@BotFather](https://t.me/botfather)).

## 🛠️ Instalación y Despliegue

1.  **Clonar o descargar** este repositorio.

2.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en la raíz del proyecto basándote en el ejemplo:
    ```bash
    cp .env.example .env
    ```
    Edita el archivo `.env` y coloca tu token de Telegram:
    ```ini
    TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
    ```

3.  **Ejecutar con Docker Compose**:
    ```bash
    docker-compose up -d --build
    ```
    El bot se iniciará y la base de datos se guardará automáticamente en la carpeta `./data`.

## 🤖 Comandos del Bot

Una vez iniciado, busca tu bot en Telegram y usa los siguientes comandos:

| Comando | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `/start` | Inicia el bot y muestra el mensaje de bienvenida. | `/start` |
| `/add` | Agrega un nuevo cumpleaños. <br>Formato: `/add Nombre, AAAA-MM-DD, DíasAviso` | `/add Juan, 1995-05-20, 3` |
| `/list` | Muestra la lista de todos los cumpleaños guardados en el chat actual. | `/list` |
| `/delete` | Elimina un cumpleaños usando su ID (visible en `/list`). | `/delete 1` |

### Ejemplo de uso
1.  **Agregar**: `/add Maria, 1990-12-25, 7` (Avisará 7 días antes del 25 de diciembre).
2.  **Ver lista**: `/list` (Te mostrará que Maria tiene el ID 1).
3.  **Borrar**: `/delete 1` (Elimina el recordatorio de Maria).

## ⚙️ Configuración Avanzada

*   **Hora de Notificación**: Por defecto, el bot verifica los cumpleaños todos los días a las **09:00 AM**.
*   **Zona Horaria**: Configurada en `docker-compose.yml` como `America/Argentina/Buenos_Aires`. Puedes cambiarla modificando la variable `TZ`.

## 📂 Estructura del Proyecto

*   `src/`: Código fuente Python.
*   `data/`: Directorio donde se monta el volumen de la base de datos (se crea al iniciar).
*   `Dockerfile`: Definición de la imagen.
*   `docker-compose.yml`: Orquestación del contenedor.
