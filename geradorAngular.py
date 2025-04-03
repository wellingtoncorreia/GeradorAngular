import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import threading

def criar_projeto():
    nome_projeto = entry_nome.get().strip()
    pasta_destino = entry_local.get().strip()
    estilo_css = var_css.get()
    ssr = var_ssr.get()

    if not nome_projeto:
        messagebox.showerror("Erro", "Digite um nome para o projeto!")
        return

    if not pasta_destino:
        messagebox.showerror("Erro", "Selecione um local para salvar o projeto!")
        return

    caminho_projeto = os.path.join(pasta_destino, nome_projeto)

    if os.path.exists(caminho_projeto):
        messagebox.showerror("Erro", "Já existe um projeto com esse nome nesse local!")
        return

    comando = f"ng new {nome_projeto} --style={estilo_css.lower()} {'--ssr' if ssr == 'Sim' else ''} --no-interactive"

    try:
        os.makedirs(caminho_projeto, exist_ok=True)

        janela_progresso = tb.Toplevel(app)
        janela_progresso.title("Instalação das Dependências")
        janela_progresso.geometry("600x300")
        janela_progresso.resizable(False, False)
        janela_progresso.grab_set()

        tb.Label(janela_progresso, text="Instalando dependências... Aguarde", font=("Arial", 12)).pack(pady=5)

        # Área para exibir a saída do terminal
        text_output = tk.Text(janela_progresso, wrap="word", height=12, width=80, bg="black", fg="green")
        text_output.pack(padx=10, pady=5, fill="both", expand=True)

        scrollbar = tk.Scrollbar(janela_progresso, command=text_output.yview)
        scrollbar.pack(side="right", fill="y")
        text_output.config(yscrollcommand=scrollbar.set)

        def executar_comandos():
            process = subprocess.Popen(comando, cwd=pasta_destino, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for linha in iter(process.stdout.readline, ""):
                text_output.insert("end", linha)
                text_output.see("end")
                text_output.update_idletasks()

            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                text_output.insert("end", "\n✅ Instalação concluída com sucesso!\n")
                messagebox.showinfo("Sucesso", f"Projeto '{nome_projeto}' criado com sucesso em {caminho_projeto}!")
                subprocess.Popen(["code", caminho_projeto], shell=True)
                app.quit()
            else:
                text_output.insert("end", "\n❌ Erro ao criar o projeto!\n")
                messagebox.showerror("Erro", "Ocorreu um erro ao criar o projeto.")

        thread = threading.Thread(target=executar_comandos)
        thread.start()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao criar o projeto:\n{e}")

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_local.delete(0, tk.END)
        entry_local.insert(0, pasta)

# Criar a interface principal com ttkbootstrap
app = tb.Window(themename="darkly")
app.title("Gerador de Projetos Angular")
app.geometry("500x420")
app.resizable(False, False)

# Centralizar na tela
largura_tela = app.winfo_screenwidth()
altura_tela = app.winfo_screenheight()
largura_janela = 500
altura_janela = 420
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
app.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

frame = tb.Frame(app)
frame.pack(padx=20, pady=10, fill="x", expand=True, anchor="w")

# Nome do Projeto (100% da largura)
tb.Label(frame, text="Nome do Projeto:", font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
entry_nome = tb.Entry(frame)
entry_nome.pack(pady=5, anchor="w", fill="x", expand=True)

# Local de Salvamento
tb.Label(frame, text="Local de Salvamento:", font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
frame_local = tb.Frame(frame)
frame_local.pack(fill="x", pady=5, anchor="w")
entry_local = tb.Entry(frame_local)
entry_local.pack(side="left", expand=True, fill="x", padx=(0, 5))
btn_pasta = tb.Button(frame_local, text="Selecionar", command=escolher_pasta, bootstyle=PRIMARY) 
btn_pasta.pack(side="left")

# Tipo de CSS (100% da largura)
tb.Label(frame, text="Escolha o tipo de CSS:", font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
var_css = tb.StringVar(value="CSS")
opcoes_css = ["CSS", "SCSS", "SASS", "LESS"]
menu_css = tb.Combobox(frame, textvariable=var_css, values=opcoes_css, state="readonly")
menu_css.pack(pady=5, anchor="w", fill="x", expand=True)

# Ativar SSR
tb.Label(frame, text="Ativar SSR (Server-Side Rendering)?", font=("Arial", 11)).pack(anchor="w", pady=(5, 0))
frame_ssr = tb.Frame(frame)
frame_ssr.pack(pady=5, anchor="w")
var_ssr = tb.StringVar(value="Não")
tb.Radiobutton(frame_ssr, text="Sim", variable=var_ssr, value="Sim", bootstyle="success").pack(side="left", padx=10)
tb.Radiobutton(frame_ssr, text="Não", variable=var_ssr, value="Não", bootstyle="danger").pack(side="left", padx=10)

# Botão Criar Projeto - Centralizado
btn_criar = tb.Button(app, text="Criar Projeto", command=criar_projeto, bootstyle=SUCCESS)
btn_criar.pack(pady=15)

app.mainloop()
