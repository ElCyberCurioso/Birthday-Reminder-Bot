from telegram import Update
from telegram.ext import ContextTypes
from src.database import add_birthday, get_birthdays, delete_birthday
from datetime import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot de cumpleaños.\n"
        "Usa /add <nombre>, <fecha AAAA-MM-DD>, <días aviso> para agregar.\n"
        "Usa /list para ver los cumpleaños.\n"
        "Usa /delete <id> para borrar uno."
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Expected format: /add Name, YYYY-MM-DD, Days
        text = ' '.join(context.args)
        parts = [p.strip() for p in text.split(',')]
        
        if len(parts) != 3:
            await update.message.reply_text("Formato incorrecto. Usa: /add Nombre, AAAA-MM-DD, Días")
            return

        name = parts[0]
        date_str = parts[1]
        days_before = int(parts[2])

        # Validate date
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            await update.message.reply_text("Fecha inválida. Usa el formato AAAA-MM-DD (ej: 1990-12-31)")
            return

        chat_id = update.effective_chat.id
        add_birthday(chat_id, name, date_str, days_before)
        await update.message.reply_text(f"¡Guardado! Te avisaré {days_before} días antes del cumpleaños de {name}.")
    
    except ValueError:
        await update.message.reply_text("El número de días debe ser un número entero.")
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error: {e}")

async def list_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    birthdays = get_birthdays(chat_id)
    
    if not birthdays:
        await update.message.reply_text("No tienes cumpleaños guardados.")
        return

    msg = "📅 **Cumpleaños Guardados**:\n"
    for b in birthdays:
        # b: (id, name, birth_date, reminder_days)
        msg += f"ID: {b[0]} | {b[1]} | {b[2]} (Aviso: {b[3]} días antes)\n"
    
    await update.message.reply_text(msg)

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usa: /delete <ID>")
        return

    try:
        b_id = int(context.args[0])
        chat_id = update.effective_chat.id
        success = delete_birthday(b_id, chat_id)
        
        if success:
            await update.message.reply_text(f"Cumpleaños ID {b_id} eliminado.")
        else:
            await update.message.reply_text("No se encontró ese ID o no te pertenece.")
    except ValueError:
        await update.message.reply_text("El ID debe ser un número.")
