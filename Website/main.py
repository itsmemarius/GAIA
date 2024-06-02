import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                        password="electric", port=5432)

cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS person (
               id INT PRIMARY KEY,
               name VARCHAR(255),
               age INT,
               gender CHAR
);
""")

cursor.execute("""
                INSERT INTO person(id, name, age, gender) VALUES
               (1, 'Mihai', 21, 'm'),
               (2, 'Ion', 22, 'm'),
               (3, 'Marius', 22, 'm'),
               (4, 'Dina', 45, 'f'),
               (5, 'Catea', 20, 'f')
""")

cursor.execute("""
    SELECT * FROM person WHERE age = 22;
""")

print(cursor.fetchall())

for row in cursor.fetchall():
    print(row)

conn.commit()
cursor.close()
conn.close()
