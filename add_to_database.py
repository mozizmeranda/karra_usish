import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

with open("add_to_db.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(" ")  # Разделяем строку по пробелам
        if len(parts) >= 3:
            user_id = int(parts[0])  # ID
            name = parts[1]  # Имя
            phone = parts[2]  # Номер телефона

            # Добавляем пользователя в базу данных (если его ещё нет)
            cursor.execute("INSERT OR IGNORE INTO users (id, name, phone) VALUES (?, ?, ?)",
                           (user_id, name, phone))

conn.commit()
conn.close()

print("Данные успешно добавлены в базу!")
