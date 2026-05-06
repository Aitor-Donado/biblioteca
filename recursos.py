class Recurso:
    def __init__(self, titulo, genero):
        self.titulo = titulo
        self.genero = genero
        self.disponible = True
        # Datos que no se modificarán

    def prestar(self, usuario):
        if self.disponible:
            self.disponible = False
            print("Se ha prestado el libro a {usuario}")
        else:
            raise PermissionError("El libro no está disponible")

    def devolver(self):
        self.disponible = True

    def __str__(self):
        return f"{self.titulo} ({self.genero}) - {"No" if not self.disponible else ""} disponible"

if __name__ == "__main__":
    r = Recurso("El Hobbit", "Fantasía")
    print(r)          # → "El Hobbit (Fantasía) - Disponible"

    r.prestar("Ana García")
    print(r)          # → "El Hobbit (Fantasía) - Prestado a Ana García"
    assert r.disponible==False, "El libro no debería estar disponible"
    try:
        r.prestar("Carlos López") # → Debe rechazar la operación y avisar
    except PermissionError as e:
        print(e)
        # assert e.args==('El libro no está disponible',), "Error no esperado"
    
    r.devolver()
    print(r)          # → "El Hobbit (Fantasía) - Disponible"
    assert r.disponible==True, "El libro debería estar disponible"