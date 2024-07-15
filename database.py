import sqlite3

def conectar():
    conexao = sqlite3.connect("to_do_database_3.db")
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_tarefa TEXT NOT NULL,
        status INTEGER NOT NULL,
        prior INTEGER NOT NULL
    )
    ''')
    conexao.commit()
    return conexao, cursor

def inserir_tarefa():
    conexao, cursor = conectar()
    nome_tarefa = input("Digite o nome da tarefa: ")
    status = int(input("Digite o status da tarefa: pending(0) ou done(1) "))
    prior = int(input("Digite a prior da tarefa: "))
    cursor.execute('''
    INSERT INTO tarefas (nome_tarefa, status, prior)
    VALUES (?, ?, ?)
    ''', (nome_tarefa, status, prior))
    conexao.commit()
    conexao.close()
    print("\nTarefa inserida com sucesso")

def atualizar_tarefa():
    conexao, cursor = conectar()
    id_tarefa = int(input("Digite o ID da tarefa a ser atualizada: "))
    nome_tarefa = input("Digite o novo nome da tarefa: ")
    status = int(input("Digite o status da tarefa: pending(0) ou done(1) "))
    prior = int(input("Digite a nova prior da tarefa: "))
    cursor.execute('''
    UPDATE tarefas
    SET nome_tarefa = ?, status = ?, prior = ?
    WHERE id = ?
    ''', (nome_tarefa, status, prior, id_tarefa))
    conexao.commit()
    conexao.close()
    print("\nTarefa atualizada com sucesso")


def deletar_tarefa():
    pass

def exibir_tarefas():
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM tarefas ORDER BY prior')
    tarefas = cursor.fetchall()
    print("Tarefas")
    for tarefa in tarefas:
        print(tarefa)
    conexao.close()
    

def main():
    conectar()
    while True:
        print("\nMenu:")
        print("1 - Inserir tarefa")
        print("2 - Atualizar tarefa")
        print("3 - Deletar tarefa")
        print("4 - Exibir tarefas")
        print("5 - Sair")

        escolha = input("Digite a opcao desejada: ")
        if escolha == "1":
            inserir_tarefa()
        elif escolha == "2":
            atualizar_tarefa()
        elif escolha == "3":
            deletar_tarefa()
        elif escolha == "4":
            exibir_tarefas()
        elif escolha == "5":
            break
        else:
            print("Opcao invalida")

if __name__ == "__main__":
    main()
