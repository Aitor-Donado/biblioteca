from recursos import Recurso
from usuarios import Usuario
from datetime import datetime
import re
# ==========================================
# DECORADOR DE REGISTRO (Fase 4.3)
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

    def prestamo(self, recurso, usuario):
        # Buscar el recurso
        # Si está disponible
        # Hacer el préstamo
        pass

    def devolucion(self, recurso, usuario):
        # Buscar el recurso
        # Si no está disponible devolverlo
        # Quitar el título de los recursos prestados del usuario
        # Poner el título en el historial del usuario
        pass

    def crear_usuario(self):
        nombre = input("Introduce el nombre del usuario: ")
        email = Biblioteca.comprueba_email(input("Introduce el email del usuario"))
        usuario_nuevo = Usuario(nombre, email)
        self.usuarios.append(usuario_nuevo)

    def crear_recurso(self):
        print("1: Libro\n2: DVD\n3:Revista")
        tipo = input("¿Que tipo de recurso quieres agregar?: ")
        print(tipo)
        
biblio = Biblioteca()
biblio.crear_usuario()
print(biblio.usuarios)