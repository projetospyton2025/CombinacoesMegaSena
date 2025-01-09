import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .combinacoes import gerar_combinacoes, validar_numeros, verificar_resultado
import pandas as pd

class MegaSenaApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mega Sena - Gerador de Combinações")
        self.root.geometry("800x600")
        self.combinacoes_geradas = None
        self.setup_interface()

    def setup_interface(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Entrada de números
        ttk.Label(frame, text="Digite os números (7-60, separados por vírgula):").grid(row=0, column=0, sticky=tk.W)
        self.entrada_numeros = ttk.Entry(frame, width=50)
        self.entrada_numeros.grid(row=0, column=1, padx=5, pady=5)

        # Botão de upload
        ttk.Button(frame, text="Upload Arquivo", command=self.upload_arquivo).grid(row=1, column=0, columnspan=2, pady=5)

        # Seleção de dezenas
        ttk.Label(frame, text="Dezenas por jogo:").grid(row=2, column=0, sticky=tk.W)
        self.dezenas_var = tk.StringVar(value="6")
        dezenas_combo = ttk.Combobox(frame, textvariable=self.dezenas_var, values=list(range(6, 21)))
        dezenas_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Botões de ação
        ttk.Button(frame, text="Gerar Jogos", command=self.gerar_jogos).grid(row=3, column=0, pady=5)
        ttk.Button(frame, text="Resetar", command=self.resetar).grid(row=3, column=1, pady=5)
        
        # Frame para botões de download
        self.frame_download = ttk.Frame(frame)
        self.frame_download.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Área de resultados
        self.resultado_text = tk.Text(frame, height=20, width=60)
        self.resultado_text.grid(row=5, column=0, columnspan=2, pady=5)
        self.resultado_text.config(state='disabled')

        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def upload_arquivo(self):
        arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", "*.txt"), ("Arquivos Excel", "*.xlsx")]
        )
        if arquivo:
            try:
                if arquivo.endswith('.txt'):
                    with open(arquivo, 'r') as f:
                        numeros = f.read().strip()
                else:
                    df = pd.read_excel(arquivo)
                    numeros = ','.join(map(str, df.iloc[0].tolist()))
                self.entrada_numeros.delete(0, tk.END)
                self.entrada_numeros.insert(0, numeros)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo: {str(e)}")

    def mostrar_botoes_download(self):
        for widget in self.frame_download.winfo_children():
            widget.destroy()
        
        ttk.Button(self.frame_download, text="Download TXT", 
                  command=lambda: self.download('txt')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_download, text="Download XLSX", 
                  command=lambda: self.download('xlsx')).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.frame_download, text="Verificar Resultado", 
                  command=self.verificar_resultado).pack(side=tk.LEFT, padx=5)

    def gerar_jogos(self):
        numeros_texto = self.entrada_numeros.get().strip()
        try:
            numeros = [int(n.strip()) for n in numeros_texto.split(',')]
            if not validar_numeros(numeros):
                raise ValueError("Números inválidos")
            
            dezenas = int(self.dezenas_var.get())
            self.combinacoes_geradas = gerar_combinacoes(numeros, dezenas)
            
            self.resultado_text.config(state='normal')
            self.resultado_text.delete(1.0, tk.END)
            self.resultado_text.insert(tk.END, f"Total de combinações: {len(self.combinacoes_geradas)}\n\n")
            
            for i, combo in enumerate(self.combinacoes_geradas, 1):
                self.resultado_text.insert(tk.END, f"Jogo {i}: {sorted(combo)}\n")
            
            self.resultado_text.config(state='disabled')
            self.mostrar_botoes_download()
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def download(self, formato):
        if not self.combinacoes_geradas:
            return
            
        if formato == 'txt':
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivo de texto", "*.txt")]
            )
            if arquivo:
                with open(arquivo, 'w') as f:
                    for combo in self.combinacoes_geradas:
                        f.write(f"{sorted(combo)}\n")
        
        else:  # xlsx
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Arquivo Excel", "*.xlsx")]
            )
            if arquivo:
                df = pd.DataFrame(self.combinacoes_geradas)
                df.to_excel(arquivo, index=False)

    def verificar_resultado(self):
        if not self.combinacoes_geradas:
            return
            
        try:
            resultado = verificar_resultado(self.combinacoes_geradas)
            
            self.resultado_text.config(state='normal')
            self.resultado_text.delete(1.0, tk.END)
            
            self.resultado_text.insert(tk.END, f"Resultado do Concurso {resultado['concurso']}\n")
            self.resultado_text.insert(tk.END, f"Data: {resultado['data']}\n")
            self.resultado_text.insert(tk.END, f"Números sorteados: {resultado['numeros']}\n\n")
            
            for jogo in resultado['jogos']:
                self.resultado_text.insert(tk.END, 
                    f"Jogo: {jogo['combinacao']} - Acertos: {jogo['acertos']}\n")
            
            self.resultado_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar resultado: {str(e)}")

    def resetar(self):
        self.entrada_numeros.delete(0, tk.END)
        self.dezenas_var.set("6")
        self.resultado_text.config(state='normal')
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state='disabled')
        self.combinacoes_geradas = None
        for widget in self.frame_download.winfo_children():
            widget.destroy()

    def iniciar(self):
        self.root.mainloop()