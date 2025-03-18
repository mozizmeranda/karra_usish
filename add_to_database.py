import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

with open("add_to_db.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split(" ")
        if len(parts) >= 3:
            user_id = int(parts[0])
            name = parts[1]
            phone = parts[2]


            cursor.execute("INSERT OR IGNORE INTO users (id, name, phone) VALUES (?, ?, ?)",
                           (user_id, name, phone))

conn.commit()
conn.close()

print("Saved :)")
