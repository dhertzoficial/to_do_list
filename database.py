import sqlite3


conexao = sqlite3.connect("todo_database.db")
cursor = conexao.cursor()

#CRIANDO TABELA E COLUNAS NA DATABSE

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)
''')
conexao.commit()

cursor.execute('''
INSERT INTO usuarios (nome,idade)
VALUES (?, ?)   
''',('maria', 25))

cursor.execute('''
INSERT INTO usuarios (nome,idade)
VALUES (?, ?)   
''',('Joao', 30))

conexao.commit()

cursor.execute('SELECT * FROM usuarios')
usuarios = cursor.fetchall()

# Exibindo os dados
for usuario in usuarios:
    print(usuario)

conexao.close()
