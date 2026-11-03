import os
import telebot

# Ваши данные (токен и ваш ID)
TOKEN = "9063745005:AAE--XnFmDtvdYBU-hT4KsWovwsBjG44p1s"
ADMIN_ID = 8605597292

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привет! Напиши сюда своё сообщение, и я передам его владельцу.",
  )


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_messages(message):
  # Если сообщение написали ВЫ (админ)
  if message.from_user.id == ADMIN_ID:
    # Проверяем, ответили ли вы на чьё-то пересланное сообщение
    if message.reply_to_message and message.reply_to_message.forward_from:
      target_user_id = message.reply_to_message.forward_from.id
      try:
        bot.send_message(
            target_user_id, f"Ответ от администратора:\n\n{message.text}"
        )
        bot.reply_to(message, "✅ Ответ успешно отправлен пользователю!")
      except Exception as e:
        bot.reply_to(message, f"❌ Не удалось отправить: {e}")
    else:
      bot.reply_to(
          message,
          "Чтобы ответить пользователю, нажмите «Ответить» (Reply) на его"
          " пересланном сообщении.",
      )
  else:
    # Если сообщение написал обычный пользователь — пересылаем вам
    try:
      # Пересылаем сообщение вам с сохранением данных пользователя
      forwarded = bot.forward_message(
          ADMIN_ID, message.chat.id, message.id
      )
      # Подсказка для вас
      bot.send_message(
          ADMIN_ID,
          f"👆 Сообщение от пользователя @{message.from_user.username or 'нет_ника'} (ID: `{message.from_user.id}`). Чтобы ответить, нажмите «Ответить» на сообщение выше.",
          parse_mode="Markdown",
      )
      bot.reply_to(
          message,
          "Ваше сообщение доставлено! Ожидайте ответ.",
      )
    except Exception as e:
      print(f"Ошибка пересылки: {e}")


print("Бот запущен...")
bot.infinity_polling()