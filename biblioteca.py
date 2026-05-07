from recursos import Libro, Revista, DVD
from usuarios import Usuario
from datetime import datetime
import re

import questionary
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

# ==========================================
# DECORADOR DE REGISTRO
# ==========================================
def registrar_accion(func):
    def wrapper(self, recurso, usuario):
        # 1. Ejecuta el método original (prestar o devolver)
        resultado = func(self, recurso, usuario)
        
        # 2. Si no se lanzó ninguna excepción, registra la acción
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            console.print(f"❌ Recurso '{titulo_recurso}' no encontrado.")
            return
        if not usuario:
            console.print(f"❌ Usuario '{nombre_usuario}' no encontrado.")
            return

        try:
            recurso.prestar(usuario)
            console.print(f"✅ Préstamo realizado: {recurso.titulo} a {usuario.nombre}")
        except PermissionError as e:
            console.print(f"❌ {e}")

    def devolucion(self, titulo_recurso, nombre_usuario):
        # 1. Buscar el recurso
        recurso = next((r for r in self.recursos if r.titulo == titulo_recurso), None)
        usuario = next((u for u in self.usuarios if u.nombre == nombre_usuario), None)

        if not recurso or not usuario:
            console.print("❌ Recurso o Usuario no encontrado.")
            return

        try:
            recurso.devolver()
            if recurso.titulo in usuario.recursos_prestados:
                usuario.recursos_prestados.remove(recurso.titulo)
                usuario.historial_prestamos.append(recurso.titulo)
            console.print(f"✅ Devolución realizada: {recurso.titulo} por {usuario.nombre}")
        except PermissionError as e:
            console.print(f"❌ {e}")

    def crear_usuario(self):
        nombre = Prompt.ask("Introduce el nombre del usuario")
        while True:
            try:
                email_input = Prompt.ask("Introduce el email del usuario").strip()
                email_valido = Biblioteca.comprueba_email(email_input)
                break
            except ValueError as e:
                console.print(f"❌ {e}. Inténtalo de nuevo.")
        usuario_nuevo = Usuario(nombre, email_valido)
        self.usuarios.append(usuario_nuevo)


    def crear_recurso(self):
        console.print("\n--- Crear nuevo recurso ---")
        console.print("1: Libro | 2: DVD | 3: Revista")
        opcion = Prompt.ask("Selecciona tipo", choices=["1", "2", "3"])

        titulo = Prompt.ask("Título")
        genero = Prompt.ask("Género")

        # Lógica específica por tipo
        if opcion == "1":
            autor = Prompt.ask("Autor")
            paginas = IntPrompt.ask("Páginas")
            nuevo = Libro(titulo, genero, autor, paginas)
        elif opcion == "2":
            director = Prompt.ask("Director")
            duracion = Prompt.ask("Duración (min)")
            nuevo = DVD(titulo, genero, director, duracion)
        elif opcion == "3":
            numero = Prompt.ask("Número")
            editorial = Prompt.ask("Editorial")
            nuevo = Revista(titulo, genero, numero, editorial)
        else:
            console.print("❌ Opción no válida.")
            return

        self.recursos.append(nuevo)
        console.print(f"✅ Recurso '{titulo}' añadido correctamente.")

    def mostrar_recursos(self):
        table = Table(title="Recursos Disponibles")
        table.add_column("Título", style="cyan")
        table.add_column("Género", style="magenta")
        table.add_column("Estado", style="green")

        for r in self.recursos:
            estado = "Disponible" if r.disponible else "Prestado"
            table.add_row(r.titulo, r.genero, estado)
        console.print(table)

    def mostrar_usuarios(self):
        table = Table(title="Usuarios Registrados")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="magenta")
        table.add_column("Email", style="green")

        for u in self.usuarios:
            table.add_row(str(u.id), u.nombre, u.email)
        console.print(table)

    def menu(self):
        while True:
            console.print(Panel("[bold blue]Gestión de Biblioteca[/bold blue]", subtitle="Selecciona una opción"))
            console.print("1. Crear Usuario")
            console.print("2. Crear Recurso")
            console.print("3. Realizar Préstamo")
            console.print("4. Realizar Devolución")
            console.print("5. Listar Recursos")
            console.print("6. Salir")

            opcion = Prompt.ask("Selecciona una opción", choices=["1", "2", "3", "4", "5", "6"])

            if opcion == "1":
                self.crear_usuario()
            elif opcion == "2":
                self.crear_recurso()
            elif opcion == "3":
                titulo = Prompt.ask("Título del recurso")
                usuario = Prompt.ask("Nombre del usuario")
                self.prestamo(titulo, usuario)
            elif opcion == "4":
                titulo = Prompt.ask("Título del recurso")
                usuario = Prompt.ask("Nombre del usuario")
                self.devolucion(titulo, usuario)
            elif opcion == "5":
                self.mostrar_recursos()
            elif opcion == "6":
                break

if __name__ == "__main__":  
    biblio = Biblioteca()
    # Datos de prueba
    biblio.usuarios.append(Usuario("Pedro", "pedro@example.com"))
    biblio.recursos.append(Revista("¡Hola!", "cotilleos", 300, "Bruguera"))

    biblio.menu()

