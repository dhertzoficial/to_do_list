import sqlite3

def conectar():
    conexao = sqlite3.connect("to_do_database_4.db")
    cursor = conexao.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_tarefa TEXT NOT NULL,
        status INTEGER NOT NULL,
        prior INTEGER NOT NULL,
        time FLOAT NOT NULL
    )
    ''')
    conexao.commit()
    return conexao, cursor

def inserir_tarefa():
    conexao, cursor = conectar()
    nome_tarefa = input("\nDigite o nome da tarefa: ")
    while True:
        status = int(input("Digite o status da tarefa: pending(0) ou done(1) "))
        if status == 0 or status == 1:
            break
        else:
            print("Aceitos somente 0 ou 1")
    
    while True:
        prior = int(input("Digite a priority da tarefa: Alta(1), Media(2), Baixa(3)  : "))
        if prior == 1 or prior == 2 or prior == 3:
            break
        else:
            print("Aceitos somente 1, 2 ou 3")
    
    time = float(input("Digite o time (exemplo 8.2 para 8:20): "))
    cursor.execute('''
    INSERT INTO tarefas (nome_tarefa, status, prior, time)
    VALUES (?, ?, ?, ?)
    ''', (nome_tarefa, status, prior, time))
    conexao.commit()
    conexao.close()
    print("\nTarefa inserida com sucesso")

def atualizar_tarefa():
    conexao, cursor = conectar()
    id_tarefa = int(input("Digite o ID da tarefa a ser atualizada: "))
    nome_tarefa = input("Digite o novo nome da tarefa: ")
    status = int(input("Digite o status da tarefa: Pending(0) ou Done(1) "))
    prior = int(input("Digite a nova prior da tarefa: "))
    time = float(input("Digite o novo time: "))
    cursor.execute('''
    UPDATE tarefas
    SET nome_tarefa = ?, status = ?, prior = ?, time = ?
    WHERE id = ?
    ''', (nome_tarefa, status, prior, time, id_tarefa))
    conexao.commit()
    conexao.close()
    print("\nTarefa atualizada com sucesso")

def deletar_tarefa():
    conexao, cursor = conectar()
    id_tarefa = int(input("\nDigite o ID da tarefa a ser deletada: "))
    
    #PEGAR O NOME DA TAREFA
    cursor.execute('SELECT nome_tarefa FROM tarefas WHERE id = ?', (id_tarefa,))
    tarefa = cursor.fetchone()
    
    if tarefa:
        nome_tarefa = tarefa[0]

        # CODIGO COR ANSI PARA AMARELO
        YELLOW = '\033[93m'
        RESET = '\033[0m'

        confirmacao = input(f"{YELLOW}Voce tem certeza que deseja excluir a tarefa '{nome_tarefa}'?  (s/n) {RESET}").lower()
        if confirmacao == 's':
            cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
            conexao.commit()
            print("\nTarefa deletada com sucesso")
        else:
            print("\nExclusao cancelada")
    else:
        print("\nTarefa nao encontrada")
    
    conexao.close()

def exibir_tarefas():
    conexao, cursor = conectar()
    cursor.execute('SELECT * FROM tarefas ORDER BY time')
    tarefas = cursor.fetchall()
    print("")
    
    #CABECALHO DA TABELA
    print(f"{"ID":<4} | {"NOME DA TAREFA":<30} | {"STATUS":<8} | {"PRIORIDADE":<12} | {"TIME":<6}")
    print("-" * 70)
    
    # CODIGO CORES ANSI
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    for tarefa in tarefas:
        id_tarefa, nome_tarefa, status, priority, time = tarefa
        status_string = "Pending" if status == 0 else "Done"
        
        # TRANSFORMANDO PRIORIDADES EM TEXTO
        if priority == 1:
            priority_string = "Alta"
        elif priority == 2:
            priority_string = "Media"
        elif priority == 3:
            priority_string = "Baixa"
        else:
            priority_string = "Não definida"

        color = RED if status == 0 else GREEN
        print(f"{id_tarefa:<4} | {nome_tarefa:<30} | {color}{status_string:<8}{RESET} | {priority_string:<12} | {time:<6}" )
    conexao.close()
    
def update_time_tarefa():
    conexao, cursor = conectar()
    id_tarefa = int(input("Digite o ID da tarefa a ser atualizada: "))
    time = float(input("Digite o novo time: "))
    cursor.execute('''
    UPDATE tarefas
    SET time = ?
    WHERE id = ?
    ''', (time, id_tarefa))
    conexao.commit()
    conexao.close()
    print("\nTarefa atualizada com sucesso")

def main():
    conectar()
    while True:
        print("\nMenu:")
        print("1 - Inserir tarefa")
        print("2 - Atualizar tarefa")
        print("3 - Deletar tarefa")
        print("4 - Exibir tarefas")
        print("5 - Alterar horario tarefa")
        print("6 - Sair")

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
            update_time_tarefa()
        elif escolha == "6":
            break
        else:
            print("Opcao invalida")

if __name__ == "__main__":
    main()


