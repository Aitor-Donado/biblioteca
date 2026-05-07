import datetime
# from functools import wraps

# ==========================================
# DECORADOR DE REGISTRO (Fase 4.3)
# ==========================================
def registrar_accion(func):
    # @wraps(func)
    def wrapper(self, *args, **kwargs):
        # 1. Ejecuta el método original (prestar o devolver)
        resultado = func(self, *args, **kwargs)
        
        # 2. Si no se lanzó ninguna excepción, registra la acción
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("biblioteca_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {func.__name__} ejecutado sobre '{self.titulo}' a {self.prestado_a.nombre if not self.disponible else ""}\n")
            
        return resultado
    return wrapper


# ==========================================
# CLASE BASE RECURSO
# ==========================================
class Recurso:
    def __init__(self, titulo, genero):
        self.titulo = titulo
        self.genero = genero
        self.disponible = True
        self.prestado_a = None
        self.duracion_prestamo = 3
        self.id = id(self)

    @registrar_accion
    def prestar(self, usuario):
        if self.disponible:
            self.disponible = False
            self.prestado_a = usuario
            usuario.recursos_prestados.append(self.titulo)
            print(f"Se ha prestado el libro a {usuario.nombre}")
        else:
            raise PermissionError("El libro no está disponible")

    @registrar_accion
    def devolver(self):
        if not self.disponible:
            self.disponible = True
            self.prestado_a = None
        else:
            raise PermissionError("El libro ya estaba disponible")

    def __str__(self):
        # Se usan comillas simples externas para evitar SyntaxError con las internas
        return f'{self.titulo} ({self.genero}) - {"no " if not self.disponible else ""}disponible'


class Libro(Recurso):
    def __init__(self, titulo, genero, autor, paginas):
        super().__init__(titulo, genero)
        self.autor = autor
        self.paginas = paginas
        self.duracion_prestamo = 7

class DVD(Recurso):
    def __init__(self, titulo, genero, director, duracion):
        super().__init__(titulo, genero)
        self.director = director
        self.duracion = duracion
        self.duracion_prestamo = 5

    def crear_recurso(cls):
        pass

class Revista(Recurso):
    def __init__(self, titulo, genero, numero, editorial):
        super().__init__(titulo, genero)
        self.numero = numero
        self.editorial = editorial

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
        assert e.args == ('El libro no está disponible',), "Error no esperado"
    
    r.devolver()
    print(r)          # → "El Hobbit (Fantasía) - disponible"
    assert r.disponible == True, "El libro debería estar disponible"
    
    print("\n✅ Todas las pruebas superadas. Revisa 'biblioteca_log.txt' para ver el registro.")