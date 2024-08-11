import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from Model.Gol import Gol
from Model.Partida import Partida
from PesquisaController import PesquisaController

class CopaAPI_app:
    controller = PesquisaController()
    ListaDePartidas: list[Partida] = []

    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Dados - Copa do Mundo")
        self.root.resizable(False, False)
        self.centralizarJanela(self.root, largura=400, altura=230)
        self.style = Style(theme="solar")
        self.listaPartidas = None 
        self.listaGols = None

        # Configuração de estilos personalizados
        self.style.configure("TButton", padding=10, font=("Arial", 12, "bold"))
        self.style.configure("Error.TLabel", font=("Arial", 9, "bold"))

        ttk.Label(self.root, text="SELECIONE UMA EDIÇÃO DO CAMPEONATO:", font=("Helvetica", 12, "bold")).pack(pady=30)

        self.comboVar = tk.StringVar()
        edicoes = ["2014", "2018"]
        combobox = ttk.Combobox(self.root, values=edicoes, textvariable=self.comboVar, state="readonly", font=("Helvetica", 12))
        combobox.pack(pady=5)

        msgErro = ttk.Label(self.root, text="", foreground="#Ffd500", style="Error.TLabel")
        msgErro.pack(pady=5)

        ttk.Button(self.root, text="CONTINUAR", command=lambda: self.verificaEdicao(msgErro), style="Amarelo.TButton", cursor="hand2").pack(pady=10)


    def verificaEdicao(self, msgErro):
        anoSelecionado = self.comboVar.get()
        if not anoSelecionado:
            msgErro.config(text="Por favor, selecione uma edição.")
        else:
            msgErro.config(text="")
            self.controller.aplicarAnoDaCompeticao(anoSelecionado)
            self.abrirModalFiltros()


    def abrirModalFiltros(self):
        modal = tk.Toplevel(self.root)
        modal.title("Filtros")
        modal.resizable(False, False)
        self.centralizarJanela(modal, largura=400, altura=230)
        
        frameBotoes = ttk.Frame(modal)
        frameBotoes.pack(pady=30)

        ttk.Label(frameBotoes, text="FILTRAR POR:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=25)
        ttk.Button(frameBotoes, text="PARTIDAS", command=self.abrirModalFiltrosPartida, cursor="hand2").grid(row=3, column=0, padx=30)
        ttk.Button(frameBotoes, text="GOLS", command=self.abrirModalFiltrosGols, cursor="hand2").grid(row=3, column=1, padx=30)


    def abrirModalFiltrosPartida(self):
        modal = tk.Toplevel(self.root)
        modal.title("Filtrar por partidas")
        modal.resizable(False, False)
        self.centralizarJanela(modal, largura=1150, altura=650)

        frameFiltros = ttk.Frame(modal)
        frameFiltros.pack(side="top", pady=10)

        ttk.Label(frameFiltros, text="LISTA DE PARTIDAS", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        ttk.Label(frameFiltros, text="Fase:", font=("Arial", 11, "bold"), justify="left").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        faseCombobox = ttk.Combobox(frameFiltros, values=self.getFases())
        faseCombobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Grupo:", font=("Arial", 11, "bold")).grid(row=2, column=2, padx=5, pady=5, sticky="e")
        grupoCombobox = ttk.Combobox(frameFiltros, values=self.getGrupos())
        grupoCombobox.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Cidade:", font=("Arial", 11, "bold")).grid(row=2, column=4, padx=5, pady=5, sticky="e")
        cidadeEntry = ttk.Entry(frameFiltros)
        cidadeEntry.grid(row=2, column=5, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Estádio:", font=("Arial", 11, "bold")).grid(row=2, column=6, padx=5, pady=5, sticky="e")
        estadioEntry = ttk.Entry(frameFiltros)
        estadioEntry.grid(row=2, column=7, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Time Mandante:", font=("Arial", 11, "bold")).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        timeMandanteEntry = ttk.Entry(frameFiltros)
        timeMandanteEntry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Time Visitante:", font=("Arial", 11, "bold")).grid(row=3, column=2, padx=5, pady=5, sticky="e")
        timeVisitanteEntry = ttk.Entry(frameFiltros)
        timeVisitanteEntry.grid(row=3, column=3, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Resultado:", font=("Arial", 11, "bold")).grid(row=3, column=6, padx=5, pady=5, sticky="e")
        resultado = tk.StringVar()
        ttk.Radiobutton(frameFiltros, text="Vitória Mandante", variable=resultado, value="Mandante").grid(row=4, column=5, padx=5, pady=5)
        ttk.Radiobutton(frameFiltros, text="Empate", variable=resultado, value="Empate").grid(row=4, column=6, padx=5, pady=5)
        ttk.Radiobutton(frameFiltros, text="Vitória Visitante", variable=resultado, value="Visitante").grid(row=4, column=7, padx=5, pady=5)

        frameResultados = ttk.Frame(modal)
        frameResultados.pack(side="top", pady=10, fill="both", expand=True)

        headers = ["Nº", "Fase", "Grupo", "Partida", "Cidade", "Estádio"]
        self.listaPartidas = ttk.Treeview(frameResultados, columns=headers, show="headings", height=50)
        for header in headers:
            self.listaPartidas.heading(header, text=header)
        self.listaPartidas.grid(row=0, column=0, sticky="nsew")

        ttk.Button(frameFiltros, text="Limpar Resultados", style="primary.TButton",
                   command=lambda: self.limparResultadosPartidas(faseCombobox, grupoCombobox, cidadeEntry, estadioEntry,
                                        timeMandanteEntry, timeVisitanteEntry, resultado)).grid(row=6, column=0, rowspan=4, padx=10, pady=15)
        
        ttk.Button(frameFiltros, text="Buscar", command=lambda:self.buscarPartidas(faseCombobox.get(), grupoCombobox.get(), cidadeEntry.get(), estadioEntry.get(),
                                        timeMandanteEntry.get(), timeVisitanteEntry.get(), resultado.get()), style="primary.TButton").grid(row=6, column=1, rowspan=4, padx=10, pady=15)



    def abrirModalFiltrosGols(self):
        modal = tk.Toplevel(self.root)
        modal.title("Filtrar por gols")
        modal.resizable(False, False)
        self.centralizarJanela(modal, largura=805, altura=450)

        frameFiltros = ttk.Frame(modal)
        frameFiltros.pack(side="top", pady=10)

        ttk.Label(frameFiltros, text="LISTA DE GOLS", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        ttk.Label(frameFiltros, text="Seleção:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        selecaoEntry = ttk.Entry(frameFiltros)
        selecaoEntry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(frameFiltros, text="Jogador:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        jogadorEntry = ttk.Entry(frameFiltros)
        jogadorEntry.grid(row=2, column=1, padx=5, pady=5)

        frameResultados = ttk.Frame(modal)
        frameResultados.pack(fill="both", expand=True)

        headers = ["Jogador", "Seleção", "Partida", "Minuto"]
        self.listaGols = ttk.Treeview(frameResultados, columns=headers, show="headings", height=70)
        for header in headers:
            self.listaGols.heading(header, text=header)
        self.listaGols.grid(row=0, column=0, sticky="nsew")

        ttk.Button(frameFiltros, text="Limpar Resultados", command=lambda: self.limparResultadosGols(jogadorEntry, selecaoEntry), style="primary.TButton").grid(row=5, column=1, rowspan=4, padx=10, pady=15)
        ttk.Button(frameFiltros, text="Buscar", command=lambda:self.buscarGols(selecaoEntry.get(), jogadorEntry.get()), style="primary.TButton").grid(row=5, column=2, rowspan=4, padx=10, pady=15)


    def centralizarJanela(self, janela, largura, altura):
        larguraTela = janela.winfo_screenwidth()
        alturaTela = janela.winfo_screenheight()

        x = (larguraTela - largura) // 2
        y = (alturaTela - altura) // 2

        janela.geometry(f"{largura}x{altura}+{x}+{y}")


    def getFases(self) -> list[str]:
        fases : list[str] = []
        fases = self.controller.getFasesParaCombobox()
        return fases


    def getGrupos(self) -> list[str]:
        grupos : list[str] = []
        grupos = self.controller.getGruposParaCombobox()
        return grupos

# Operações para PARTIDAS
    def limparResultadosPartidas(self, faseCombobox, grupoCombobox, cidadeEntry, estadioEntry,
                      timeMandanteEntry, timeVisitanteEntry, vitoriaVar):
            faseCombobox.set('')
            grupoCombobox.set('')
            cidadeEntry.delete(0, tk.END)
            estadioEntry.delete(0, tk.END)
            timeMandanteEntry.delete(0, tk.END)
            timeVisitanteEntry.delete(0, tk.END)
            vitoriaVar.set('')

            if self.listaPartidas is not None:
                for item in self.listaPartidas.get_children():
                    self.listaPartidas.delete(item)

    def atualizarResultadosPartidas(self, partidas):
        if self.listaPartidas is not None:
            for item in self.listaPartidas.get_children():
                self.listaPartidas.delete(item)

            partidasAdicionadas: list[int] = []
            for partida in partidas:
                if partida.numero not in partidasAdicionadas:
                    partidasAdicionadas.append(partida.numero)
                    self.listaPartidas.insert("", "end", values=(partida.numero, partida.fase, partida.grupo, repr(partida),
                                                                partida.cidade, partida.estadio))

    def buscarPartidas(self, fase, grupo, cidade, estadio,
                       timeMandante, timeVisitante, resultado):

        partidas = self.controller.getPartidasParaListagem(fase, grupo, cidade, estadio,
                                                        timeMandante, timeVisitante, resultado)
        
        self.atualizarResultadosPartidas(partidas)


# Operações para GOLS
    def limparResultadosGols(self, jogadorEntry, selecaoEntry):
        selecaoEntry.delete(0, tk.END)
        jogadorEntry.delete(0, tk.END)

        if self.listaGols is not None:
                for item in self.listaGols.get_children():
                    self.listaGols.delete(item)

    def atualizarResultadosGols (self, gols):
        if self.listaGols is not None:
            for item in self.listaGols.get_children():
                self.listaGols.delete(item)

            golsAdicionados: list[Gol] = []
            for gol in gols:
                if gol not in golsAdicionados:
                    golsAdicionados.append(gol)
                    self.listaGols.insert("", "end", values=(gol.jogador, gol.selecao, gol.partida, gol.minuto))


    def buscarGols(self, selecao, jogador):
        gols = self.controller.getGolsParaListagem(selecao, jogador)
        
        self.atualizarResultadosGols(gols)


if __name__ == "__main__":
    root = tk.Tk()
    app = CopaAPI_app(root)
    root.mainloop()
