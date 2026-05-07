from dataclasses import dataclass, field
from typing import List

@dataclass
class Usuario:
    nombre: str
    email: str
    id: int = field(init=False)
    historial_prestamos: List[str] = field(default_factory=list)  # Lista de recursos prestados en el pasado
    recursos_prestados: List[str] = field(default_factory=list)  # Lista de recursos actualmente prestados al usuario

    def __post_init__(self):
        self.id = id(self)  # Identificador único del usuario
    def __str__(self):
        return f"Usuario: {self.nombre}, Email: {self.email}"
    
    def mostrar_prestamos(self):
        print(f"Prestamos actuales de {self.nombre}: {self.recursos_prestados}")
    def mostrar_prestamos_historico(self):
        print(f"Historial de {self.nombre}: {self.historial_prestamos}")
