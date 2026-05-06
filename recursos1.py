import datetime

class Recurso:
    def __init__(self, titulo, genero):
        self.titulo = titulo
        self.genero = genero
        self.disponible = True
        self.prestado_a = None
        self.duracion_prestamo = 3

    def __registrar_log(self, accion: str):
        """Escribe la acción en el archivo de log con marca de tiempo."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("biblioteca_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {accion} ejecutado sobre '{self.titulo}'\n")

    def prestar(self, usuario):
        if self.disponible:
            self.disponible = False
            self.prestado_a = usuario
            print(f"Se ha prestado el libro a {usuario}")
            self.__registrar_log("prestar")
        else:
            raise PermissionError("El libro no está disponible")

    def devolver(self):
        if not self.disponible:
            self.disponible = True
            self.prestado_a = None
            self.__registrar_log("devolver")
        else:
            raise PermissionError("El libro ya estaba disponible")

    def __str__(self):
        # ✅ Corregido el error de comillas anidadas y ajustado a tu assert
        return f'{self.titulo} ({self.genero}) - {"no " if not self.disponible else ""}disponible'


if __name__ == "__main__":
    r = Recurso("El Hobbit", "Fantasía")
    print(r)          # → "El Hobbit (Fantasía) - disponible"
    assert r.__str__() == "El Hobbit (Fantasía) - disponible", "No imprime bien los datos del libro"
    
    r.prestar("Ana García")
    print(r)          # → "El Hobbit (Fantasía) - no disponible"
    assert r.disponible == False, "El libro no debería estar disponible"
    
    try:
        r.prestar("Carlos López") # → Debe rechazar la operación y avisar
    except PermissionError as e:
        print(e)
        assert e.args == ('El libro no está disponible',), "Error no esperado"
    
    r.devolver()
    print(r)          # → "El Hobbit (Fantasía) - disponible"
    assert r.disponible == True, "El libro debería estar disponible"
    # r.__registrar_log("devolver")
    print("\n✅ Todas las pruebas superadas. Revisa 'biblioteca_log.txt' para ver el registro.")