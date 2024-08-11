from dataclasses import dataclass
from Model.Gol import Gol
from Resources.TraducaoSiglasPaises import traducoesParaNome

@dataclass
class Partida:
    numero: int
    estadio: str
    cidade: str
    mandante: str
    visitante: str
    gols_mandante: int
    gols_visitante: int
    gols: list[Gol]
    fase: str
    grupo: str

    def contem(self, codigo_time: str) -> bool:
        return self.mandante == codigo_time or self.visitante == codigo_time

    def __repr__(self) -> str:
        mandante = traducoesParaNome[self.mandante]
        visitante = traducoesParaNome[self.visitante]
        partida = f"{mandante} {self.gols_mandante} X {self.gols_visitante} {visitante}"
        return partida
