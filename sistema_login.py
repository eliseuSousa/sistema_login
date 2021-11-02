from tkinter import*
import sqlite3
from typing import ContextManager
from tkinter import messagebox

def message_erro(msg):
    messagebox.showerror('Erro', msg)

def succesfully(title, msg):
    messagebox.showinfo(title, msg)


def update_database(user_name, password):
    """"Adiciona um novo registro no banco de dados."""
    # Conectando com o banco de dados
    conn = sqlite3.connect('logins_book.db')

    # Criando um cursor
    c = conn.cursor()

    c.execute("INSERT INTO logins VALUES(:name, :password)",
        {
            'name': user_name.get(),
            'password': password.get()
        })

    # Realizando as mudanças no banco de dados
    conn.commit()

    # Fechando a cnexão com o banco de dados
    conn.close()

def query_database(user_name, password):
    """Verificar se um registro já existe no banco de dados."""
    registro_existente = False
    # Conectando com o banco de dados
    conn = sqlite3.connect('logins_book.db')

    # Criar um cursor 
    c = conn.cursor()

    c.execute("SELECT *FROM logins")

    items = c.fetchall()

    for item in items:
        if (item[0] == user_name.get()) and (item[1] == password.get()):
            registro_existente = True

    # Realizar as alterações
    conn.commit()

    # Fechar o banco de dados
    conn.close()

    return registro_existente

def validate_user(user_name, password):
    """Válida os dados informados pelo usuário."""
    if len(user_name.get()) == 0:
        message_erro('Crie um nome de usário.')

    elif len(password.get()) == 0:
        message_erro('Crie uma senha.')

    elif user_name.get() == password.get():
        message_erro('Nome de usário e Senha não podem ser iguais.')
    
    elif not query_database(user_name, password):
        message_erro('Usário não encontrado!')

    else:
        succesfully('Login usuário', 'Seja bem vindo novamente '+user_name.get()+'!')
        user_name.delete(0, END)
        password.delete(0, END)

def validate_new_user(user_name, password, confirm_password):
    """Válida os dados informados para o registro de um novo usuário no banco de dados."""
    if len(user_name.get()) == 0:
        message_erro('Crie um nome de usuário.')

    elif len(password.get()) == 0:
        message_erro('Crie uma senha.')

    elif user_name.get() == password.get():
        message_erro('Nome de usário e Senha não podem ser iguais.')

    elif len(confirm_password.get()) == 0:
        message_erro('Confirme sua senha.')

    elif password.get() != confirm_password.get():
        message_erro('As senhas não são correspondentes.')

    elif query_database(user_name, password):
        user_name.delete(0, END)
        password.delete(0, END)
        confirm_password.delete(0, END)
        message_erro('Usário existente.')

    else:
        update_database(user_name, password)
        succesfully('Novo usuário', 'Novo usuário cadastrado com sucesso!\nSeja bem vindo '+user_name.get())
        user_name.delete(0, END)
        password.delete(0, END)
        confirm_password.delete(0, END)

def new_login():
    """Cria uma tela para a o cadastro de um novo usuário."""
    new_root = Tk()
    new_root.title('New login')
    new_root.call('wm', 'iconphoto', new_root._w, PhotoImage(file='./img/registro.png'))

    # Caixas de diálogo
    user_name = Entry(new_root, width=25)
    user_name.grid(row=0, column=1, padx=15, pady=10)
    
    password = Entry(new_root, width=25)
    password.grid(row=1, column=1, padx=15, pady=10)

    confirm_password = Entry(new_root, width=25)
    confirm_password.grid(row=2, column=1, padx=15, pady=10)

    # Rótulos
    user_name_label = Label(new_root, text='Nome de usuário')
    user_name_label.grid(row=0, column=0, padx=5)

    password_label = Label(new_root, text='Senha')
    password_label.grid(row=1, column=0)

    confirm_password_label = Label(new_root, text='Confirne sua senha.')
    confirm_password_label.grid(row=2, column=0, padx=5)

    # Botões
    submit_btn = Button(new_root, text='Submit', command=lambda:validate_new_user(user_name, password, confirm_password))
    submit_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    exit_btn = Button(new_root, text='Voltar', command=lambda:[new_root.destroy(), main()])
    exit_btn.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    new_root.mainloop()



def main():
    """Cria a tela inicial."""
    root = Tk()
    root.title("Login")
    root.call('wm', 'iconphoto', root._w, PhotoImage(file='./img/enter.png'))
    # Caixas de diálogo para a coleta de dados
    user_name = Entry(root, width=25)
    user_name.grid(row=0, column=1, padx=15,
    pady=10)
    password = Entry(root, width=25)
    password.grid(row=1, column=1, padx=15, pady=10)

    # Rótulos
    user_name_label = Label(root, text='Nome de usuário')
    user_name_label.grid(row=0, column=0, padx=5)
    password_label = Label(root, text="Senha")
    password_label.grid(row=1, column=0, padx=5)

    # Botão de login
    login_btn = Button(root, text='Login', command=lambda:validate_user(user_name, password))
    login_btn.grid(row=3, column=0, padx=5, pady=5)

    # Botão de novo usuário
    new_user_btn = Button(root, text='Novo usário', command=lambda:[root.destroy(), new_login()])
    new_user_btn.grid(row=3, column=1, padx=5, pady=5)

    # Botão de saída
    exit_btn = Button(root, text='Sair', command=root.destroy)
    exit_btn.grid(row=3, column=2, padx=5, pady=5)

    root.mainloop()

main()