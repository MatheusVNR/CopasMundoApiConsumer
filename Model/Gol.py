from dataclasses import dataclass

@dataclass     
class Gol:
    jogador: str
    selecao: str
    minuto: int
    partida: str

    def __repr__(self) -> str:
        return self.jogador + " " + str(self.minuto)