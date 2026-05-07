from recursos import Libro, Revista, DVD
from usuarios import Usuario
from datetime import datetime
import re

# ==========================================
# DECORADOR DE REGISTRO
# ==========================================
def registrar_accion(func):
    def wrapper(self, recurso, usuario):
        # 1. Ejecuta el método original (prestar o devolver)
        resultado = func(self, recurso, usuario)
        
        # 2. Si no se lanzó ninguna excepción, registra la acción
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("biblioteca_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {func.__name__} ejecutado sobre '{recurso}' a {usuario}\n")
            
        return resultado
    return wrapper


class Biblioteca:
    def __init__(self):
        self.recursos = []
        self.usuarios = []

    @staticmethod
    def comprueba_email(email):
        patron_email = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        if re.fullmatch(patron_email, email):
            return email
        else:
            raise ValueError("El email no es correcto")

    def prestamo(self, titulo_recurso, nombre_usuario):
        # 1. Buscar el recurso
        recurso = next((r for r in self.recursos if r.titulo == titulo_recurso), None)
        # 2. Buscar el usuario
        usuario = next((u for u in self.usuarios if u.nombre == nombre_usuario), None)

        if not recurso:
            print(f"❌ Recurso '{titulo_recurso}' no encontrado.")
            return
        if not usuario:
            print(f"❌ Usuario '{nombre_usuario}' no encontrado.")
            return

        try:
            recurso.prestar(usuario)
            print(f"✅ Préstamo realizado: {recurso.titulo} a {usuario.nombre}")
        except PermissionError as e:
            print(f"❌ {e}")

    def devolucion(self, titulo_recurso, nombre_usuario):
        # 1. Buscar el recurso
        recurso = next((r for r in self.recursos if r.titulo == titulo_recurso), None)
        usuario = next((u for u in self.usuarios if u.nombre == nombre_usuario), None)

        if not recurso or not usuario:
            print("❌ Recurso o Usuario no encontrado.")
            return

        try:
            recurso.devolver()
            if recurso.titulo in usuario.recursos_prestados:
                usuario.recursos_prestados.remove(recurso.titulo)
                usuario.historial_prestamos.append(recurso.titulo)
            print(f"✅ Devolución realizada: {recurso.titulo} por {usuario.nombre}")
        except PermissionError as e:
            print(f"❌ {e}")

    def crear_usuario(self):
        nombre = input("Introduce el nombre del usuario: ")
        while True:
            try:
                email_input = input("Introduce el email del usuario: ").strip()
                email_valido = Biblioteca.comprueba_email(email_input)
                break
            except ValueError as e:
                print(f"❌ {e}. Inténtalo de nuevo.")
        usuario_nuevo = Usuario(nombre, email_valido)
        self.usuarios.append(usuario_nuevo)


    def crear_recurso(self):
        print("\n--- Crear nuevo recurso ---")
        print("1: Libro | 2: DVD | 3: Revista")
        opcion = input("Selecciona tipo: ")

        titulo = input("Título: ")
        genero = input("Género: ")

        # Lógica específica por tipo
        if opcion == "1":
            autor = input("Autor: ")
            paginas = int(input("Páginas: "))
            nuevo = Libro(titulo, genero, autor, paginas)
        elif opcion == "2":
            director = input("Director: ")
            duracion = input("Duración (min): ")
            nuevo = DVD(titulo, genero, director, duracion)
        elif opcion == "3":
            numero = input("Número: ")
            editorial = input("Editorial: ")
            nuevo = Revista(titulo, genero, numero, editorial)
        else:
            print("❌ Opción no válida.")
            return

        self.recursos.append(nuevo)
        print(f"✅ Recurso '{titulo}' añadido correctamente.")


if __name__ == "__main__":  
    biblio = Biblioteca()
    """
    biblio.crear_usuario()
    print(biblio.usuarios)
    biblio.crear_recurso()
    """
    # Crear datos de prueba
    u = Usuario("Pedro", "pedro@example.com")
    biblio.usuarios.append(u)
    biblio.recursos.append(Revista("¡Hola!", "cotilleos", 300, "Bruguera"))
    print("Recursos antes:", biblio.recursos)
    biblio.prestamo("¡Hola!", "Pedro")
    print("Prestados usuario:", u.recursos_prestados)
    biblio.devolucion("¡Hola!", "Pedro")
    print("Historial usuario:", u.historial_prestamos)
