from dataclasses import dataclass, field
from typing import Optional
import datetime
# ==========================================
# DECORADOR DE REGISTRO (Fase 4.3)
# ==========================================
def registrar_accion(func):
    def wrapper(self, *args, **kwargs):
        resultado = func(self, *args, **kwargs)
        
        # Obtenemos el nombre del usuario si está disponible, o "Disponible"
        nombre_usuario = self.prestado_a.nombre if self.prestado_a else "Disponible"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("biblioteca_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {func.__name__} ejecutado sobre '{self.titulo}' a {nombre_usuario}\n")
            
        return resultado
    return wrapper


# ==========================================
# CLASE BASE RECURSO (Dataclass)
# ==========================================
@dataclass
class Recurso:
    titulo: str
    genero: str
    disponible: bool = True
    prestado_a: Optional[object] = None
    duracion_prestamo: int = 3
    id: int = field(init=False)

    def __post_init__(self):
        self.id = id(self)

    @registrar_accion
    def prestar(self, usuario):
        if self.disponible:
            self.disponible = False
            self.prestado_a = usuario
            usuario.recursos_prestados.append(self.titulo)
            print(f"Se ha prestado {self.titulo} a {usuario.nombre}")
        else:
            raise PermissionError("El recurso no está disponible")

    @registrar_accion
    def devolver(self):
        if not self.disponible:
            self.disponible = True
            self.prestado_a = None
        else:
            raise PermissionError("El recurso ya estaba disponible")

    def __str__(self):
        # Se usan comillas simples externas para evitar SyntaxError con las internas
        return f'{self.titulo} ({self.genero}) - {"no " if not self.disponible else ""}disponible'

@dataclass
class Libro(Recurso):
    autor: str = ""
    paginas: int = 0
    def __post_init__(self):
        super().__post_init__()
        self.duracion_prestamo = 7

@dataclass
class DVD(Recurso):
    director: str = ""
    duracion: int = 0
    def __post_init__(self):
        super().__post_init__()
        self.duracion_prestamo = 5

@dataclass
class Revista(Recurso):
    numero: int = 0
    editorial: str = ""

    
# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":

    r = Libro("El Hobbit", "Fantasía", "Tolkien", 1000)
    print(r)          # → "El Hobbit (Fantasía) - disponible"
    assert r.__str__() == "El Hobbit (Fantasía) - disponible", "No imprime bien los datos del libro"
    
    from usuarios import Usuario
    u1 = Usuario("Ana García", "ana@gmail.com")
    u2 = Usuario("Carlos López", "carlos@hotmail.com")
    
    r.prestar(u1)
    print(r)          # → "El Hobbit (Fantasía) - no disponible"
    assert r.disponible == False, "El libro no debería estar disponible"
    u1.mostrar_prestamos()
    assert u1.recursos_prestados[-1]==r.titulo, "El último préstamo no coincide"
    try:
        r.prestar("Carlos López") # → Debe rechazar la operación y avisar
    except PermissionError as e:
        print(e)
        assert e.args == ('El recurso no está disponible',), "Error no esperado"
    
    r.devolver()
    print(r)          # → "El Hobbit (Fantasía) - disponible"
    assert r.disponible == True, "El libro debería estar disponible"
    
    print("\n✅ Todas las pruebas superadas. Revisa 'biblioteca_log.txt' para ver el registro.")