import asyncio
from telethon import TelegramClient, events

try:
    from config import api_id, api_hash, bot_token, source_channel, destination_channel
except ImportError:
    print("❌ Файл config.py не найден!")
    print("📝 Создай config.py на основе config.example.py и заполни своими данными")
    exit(1)

async def main():
    # остальной код без изменений...
    # остальной код без изменений...
async def main():
    print("🔄 Запускаю бота...")
    
    client = TelegramClient('bot_session', api_id, api_hash)
    
    try:
        await client.start(bot_token=bot_token)
        print("✅ Бот авторизован!")
        
        # Проверяем подключение к каналам
        source_channel = await client.get_entity('https://t.me/vakansii_it')
        print(f"✅ Найден исходный канал: {source_channel.title}")
        
        dest_channel = await client.get_entity('https://t.me/vakansui_IT') 
        print(f"✅ Найден целевой канал: {dest_channel.title}")
        
        # Проверяем, что бот - админ в целевом канале
        participants = await client.get_participants(dest_channel)
        bot_me = await client.get_me()
        is_admin = any(p.id == bot_me.id for p in participants)
        print(f"✅ Бот в целевом канале: {'ДА' if is_admin else 'НЕТ'}")
        
        if not is_admin:
            print("❌ ДОБАВЬ БОТА В КАНАЛ КАК АДМИНИСТРАТОРА!")
            return
        
        print("🎯 Бот готов к работе! Ожидаю сообщения...")
        print("💡 Опубликуй тестовое сообщение в @vakansii_it")
        
        # Ждем сообщения
        @client.on(events.NewMessage(chats=source_channel))
        async def handler(event):
            print(f"📨 Получено: {event.text[:50]}...")
            await client.forward_messages(dest_channel, event.message)
            print("✅ Переслано!")
        
        # Бесконечное ожидание
        print("⏳ Бот работает в фоне...")
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())