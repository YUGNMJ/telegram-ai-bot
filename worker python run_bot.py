import subprocess
import time

bot_file = "F:\\zbot\\bot.py"

while True:
    try:
        print("🚀 Запуск бота...")
        subprocess.run(["python", bot_file])
    except KeyboardInterrupt:
        print("❌ Остановка вручную.")
        break
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
    
    print("🔁 Перезапуск через 3 секунды...")
    time.sleep(3)
