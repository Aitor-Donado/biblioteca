class Usuario:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email
        self.id_usuario = id(self)  # Identificador único del usuario
        self.historial_prestamos = []  # Lista de recursos prestados en el pasado
        self.recursos_prestados = []  # Lista de recursos actualmente prestados al usuario

    def __str__(self):
        return f"Usuario: {self.nombre}, Email: {self.email}"
    
    def mostrar_prestamos(self):
        for recurso in self.recursos_prestados:
            print(recurso)

    def mostrar_prestamos_historico(self):
        for recurso in self.historial_prestamos:
            print(recurso)