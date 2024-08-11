import requests
from Model.Gol import Gol
from Model.Partida import Partida
from Resources.TraducaoNomesParaSiglas import traducoesParaSigla
from Resources.TraducaoSiglasPaises import traducoesParaNome

class PesquisaController:
    PARTIDAS: list[Partida] = []
    GOLS: list[Gol] = []
    URL: str = "https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_2018"

    def loadDados(self):
        response = requests.get(self.URL)
        dados = response.json()
        rodadas = dados["rounds"]
        for rodada in rodadas:
            faseAux = rodada["name"]
            fase = self.atribuirFaseDaPartida(faseAux)
            partidas = rodada["matches"]
            for partidaAux in partidas:
                numero = partidaAux["num"]
                estadio = partidaAux["stadium"]["name"]
                cidade = partidaAux["city"]
                mandante = partidaAux["team1"]["code"]
                visitante = partidaAux["team2"]["code"]
                gols_mandante = partidaAux["score1"]
                gols_visitante = partidaAux["score2"]

                if fase == "Fase de grupos":
                    grupoAux = partidaAux["group"]
                    grupo = grupoAux.replace("Group", "Grupo")
                else:
                    grupo = ""

                gols: list[Gol] = []
                todosGols: list[dict] = partidaAux["goals1"] + partidaAux["goals2"]
                for gol in todosGols:
                    gols.append(
                        Gol(gol["name"], "", gol["minute"], "")
                    )
                
                partida: Partida = Partida(
                    numero,
                    estadio,
                    cidade,
                    mandante,
                    visitante,
                    gols_mandante,
                    gols_visitante,
                    gols,
                    fase,
                    grupo
                )

                golsTime1: list[dict] = partidaAux["goals1"]
                for gol in golsTime1:
                    self.GOLS.append(
                        Gol(gol["name"], traducoesParaNome[partida.mandante], gol["minute"], repr(partida))
                    )
                golsTime2: list[dict] = partidaAux["goals2"]
                for gol in golsTime2:
                    self.GOLS.append(
                        Gol(gol["name"], traducoesParaNome[partida.visitante], gol["minute"], repr(partida))
                    )

                grupo = ""
                grupoAux = ""
                self.PARTIDAS.append(partida)
        fase = "" 


    def atribuirFaseDaPartida (self, fase: str) -> str:
        if "Matchday" in fase:
            return "Fase de grupos"
        elif fase == "Round of 16":
            return "Oitavas de Final"
        elif fase == "Quarter-finals":
            return "Quartas de Final"
        elif fase == "Semi-finals":
            return "Semifinais"
        elif fase == "Match for third place":
            return "Partida pelo 3º Lugar"
        else:
            return "Final"


    def getGruposParaCombobox (self) -> list[str]:
        grupos : list[str] = []
        grupos.extend(["Grupo A", "Grupo B", "Grupo C", "Grupo D", "Grupo E", "Grupo F", "Grupo G", "Grupo H"])

        return grupos
    
    def getFasesParaCombobox (self) -> list[str]:
        fases : list[str] = []
        fases.extend(["Fase de grupos",
                      "Oitavas de Final",
                      "Quartas de Final",
                      "Semifinais",
                      "Partida pelo 3º Lugar",
                      "Final"])

        return fases

    def getPartidasTradicional(self, codigoTime: str) -> list[Partida]:
        partidas_time: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.contem(codigoTime):
                partidas_time.append(partida)
        return partidas_time

    def getPartidasPorFases(self) -> str:
        for partida in self.PARTIDAS:
            fases = partida.fase + " " + partida.mandante + " " + str(partida.gols_mandante) + " X " + str(partida.gols_visitante) + " " + partida.visitante + "\n"
        return fases

    def getPartidasComFilter(self, codigoTime: str) -> list[Partida]:
        return list(
            filter(
                lambda time: time.contem(codigoTime), 
                self.PARTIDAS
            )
        )

    def getGolsJogador(self, nome_jogador: str) -> list[Gol]:
        gols_jogador: list[dict] = []
        for partida in self.PARTIDAS:
            for gol in partida.gols:
                if gol.jogador == nome_jogador:
                    gols_jogador.append(
                        {
                            "gol": gol,
                            "partida": partida,
                        }
                    )
        return gols_jogador

    def getJogosSelecao(self, codigo_selecao: str) -> list[Partida]:
        jogos_selecao: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.contem(codigo_selecao):
                jogos_selecao.append(partida)
        return jogos_selecao

    def getJogosVitoriaMandante(self) -> list[Partida]:
        jogos_vitoria_mandante: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.gols_mandante > partida.gols_visitante:
                jogos_vitoria_mandante.append(partida)
        return jogos_vitoria_mandante

    def getJogosEmpate(self) -> list[Partida]:
        jogos_empate: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.gols_mandante == partida.gols_visitante:
                jogos_empate.append(partida)
        return jogos_empate

    def getJogosVitoriaVisitante(self) -> list[Partida]:
        jogos_vitoria_visitante: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.gols_mandante < partida.gols_visitante:
                jogos_vitoria_visitante.append(partida)
        return jogos_vitoria_visitante

    def getJogosPorEstadio(self, estadio: str) -> list[Partida]:
        jogosEstadio: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.estadio == estadio:
                jogosEstadio.append(partida)
        return jogosEstadio


    def getJogosPorCidade(self, cidade: str) -> list[Partida]:
        jogosCidade: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.cidade == cidade:
                jogosCidade.append(partida)
        return jogosCidade

    def aplicarAnoDaCompeticao(self, ano: str):
        self.URL = f"https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_{ano}"
        self.loadDados()

    def getJogosPorFase(self, fase: str) -> list[Partida]:
        jogosDaFase: list[Partida] = []
        for partida in self.PARTIDAS:
            if partida.fase == fase:
                jogosDaFase.append(partida)
        return jogosDaFase

    def getJogosPorGrupo(self, grupo: str) -> list[Partida]:
        jogosDoGrupo: list[Partida] = []       
        for partida in self.PARTIDAS:
            if partida.grupo == grupo:
                jogosDoGrupo.append(partida)
        return jogosDoGrupo
    
    def ehNuloOuVazio(self, palavra:str):
        return (palavra is None or not palavra) or palavra == ""
    

    # Funções principais para o funcionamento dos filtros na interface
    def getPartidasParaListagem(self, fase:str, grupo:str, cidade:str, estadio:str,
                                timeMandante:str, timeVisitante:str, resultado:str) -> list[Partida]:
        partidas = self.PARTIDAS
        if not self.ehNuloOuVazio(fase):
            partidas = list(filter(lambda p: p.fase == fase, partidas))

        if not self.ehNuloOuVazio(grupo):
            partidas = list(filter(lambda p: p.grupo == grupo, partidas))
        if not self.ehNuloOuVazio(cidade):
            partidas = list(filter(lambda p: p.cidade == cidade, partidas))
        if not self.ehNuloOuVazio(estadio):
            partidas = list(filter(lambda p: p.estadio == estadio, partidas))
        if not self.ehNuloOuVazio(timeMandante):
            siglaMandante = traducoesParaSigla[timeMandante]
            partidas = list(filter(lambda p: p.mandante == siglaMandante, partidas))
        if not self.ehNuloOuVazio(timeVisitante):
            siglaVisitante = traducoesParaSigla[timeVisitante]
            partidas = list(filter(lambda p: p.visitante == siglaVisitante, partidas))

        if not self.ehNuloOuVazio(resultado):
            if resultado == "Mandante":
                partidas = list(filter(lambda p: p.gols_mandante > p.gols_visitante, partidas))
            elif resultado == "Visitante":
                partidas = list(filter(lambda p: p.gols_visitante > p.gols_mandante, partidas))
            elif resultado == "Empate":
                partidas = list(filter(lambda p: p.gols_mandante == p.gols_visitante, partidas))

        return partidas
    

    def getGolsParaListagem(self, selecao:str, jogador:str) -> list[Gol]:
        gols = self.GOLS
        if not self.ehNuloOuVazio(selecao):
            gols = list(filter(lambda g: g.selecao == selecao, gols))

        if not self.ehNuloOuVazio(jogador):
            gols = list(filter(lambda g: g.jogador == jogador, gols))

        return gols
