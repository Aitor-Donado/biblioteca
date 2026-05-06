# 📘 Práctica de POO en Python: Sistema de Gestión de Biblioteca
## Fase 0: Clase Base `Recurso` (El cimiento del sistema)

### 🎯 Objetivo
Crear la clase base que representará cualquier material bibliotecario. Esta clase definirá el estado compartido, el comportamiento básico de préstamo/devolución y servirá como punto de partida para la composición, herencia y gestión centralizada que se implementarán en fases posteriores.

### 📐 Requisitos Técnicos

#### 1. Atributos de la clase
- `titulo` (`str`): Nombre del material.
- `genero` (`str`): Categoría temática (ej: `"Ficción"`, `"Divulgación"`, `"Ciencia Ficción"`).
- `disponible` (`bool`): Estado inicial `True`. Indica si el recurso puede prestarse.
- `prestado_a` (`str`): **Inicialmente será una cadena** que almacenará el nombre del usuario que lo tiene. Valor inicial: `None` o `"Sin prestar"`. *(Nota para el alumno: en la siguiente fase este atributo cambiará para almacenar un objeto, pero por ahora trabaja con strings)*.
- `duracion_prestamo` (`int`): Número de días que se puede mantener el recurso prestado. Valor por defecto: `3`.

#### 2. Métodos obligatorios
- `__init__(self, titulo, genero, duracion_prestamo=3)`
- `__str__(self)`: Devuelve una representación legible del recurso. Debe mostrar título, género y estado actual (`Disponible` o `Prestado a [nombre]`).
- `prestar(self, nombre_usuario)`:
  - Valida si el recurso está disponible.
  - Si lo está: marca `disponible = False`, guarda el `nombre_usuario` en `prestado_a` y registra la acción.
  - Si no lo está: informa al usuario o lanza una excepción controlada.
- `devolver(self)`:
  - Valida si el recurso estaba efectivamente prestado.
  - Si lo estaba: restaura `disponible = True`, limpia `prestado_a` y registra la acción.
  - Si no estaba prestado: informa del error o lanza una excepción controlada.

#### 3. Registro de actividades (Log)
Tanto en `prestar()` como en `devolver()` debes incluir un bloque que escriba en un archivo de texto llamado `biblioteca_log.txt`. Cada línea debe contener al menos:
- Fecha y hora exacta de la acción.
- Tipo de operación (`prestar` o `devolver`).
- Título del recurso afectado.

*(Utiliza el módulo `datetime` para obtener la marca temporal y abre el archivo en modo append `"a"` con codificación `utf-8`).*

### 🧩 Comportamiento Esperado
```text
r = Recurso("El Hobbit", "Fantasía")
print(r)          # → "El Hobbit (Fantasía) - Disponible"

r.prestar("Ana García")
print(r)          # → "El Hobbit (Fantasía) - Prestado a Ana García"

r.prestar("Carlos López") # → Debe rechazar la operación y avisar
r.devolver()
print(r)          # → "El Hobbit (Fantasía) - Disponible"
```
*(El archivo `biblioteca_log.txt` debe haberse actualizado automáticamente tras cada llamada válida a `prestar` o `devolver`).*

### Fase 1: La clase `Usuario` (Composición)
Ahora que `prestado_a` es un string, hay que convertirlo en un objeto. Esto demuestra composición (una Biblioteca tiene Recursos y Usuarios; un Recurso está prestado a un Usuario).

**Tarea a realizar:**
1. Crear la clase `Usuario` con atributos: `nombre`, `id_usuario` y una lista `prestamos_activos` (que guardará objetos de tipo `Recurso`).
2. Añadir un método `mostrar_prestamos()` que use un bucle `for` para imprimir los libros que tiene.

### Fase 2: Herencia (Libro, Revista, DVD)
El concepto de "Recurso" es perfecto para la herencia. 

Cada tipo de recurso tiene atributos particulares y, lo más importante, **diferentes tiempos de préstamo**.

**Tarea a realizar:**
1. Crear las clases `Libro`, `Revista` y `DVD` que hereden de `Recurso`.
2. Añadir atributos propios (ej: `num_paginas` para Libro, `isbn` para Libro, `duracion_minutos` para DVD, `numero_edicion` para Revista).
3. Sobrescribir el método `__str__` para que incluya la nueva información usando `super()`.
4. **El reto de la lógica:** Modificar el préstamo para que las revistas se presten por 7 días y los DVDs por 2 días (los libros se quedan en 3). *Hay dos maneras de hacerlo, pasar los días al `__init__` de Recurso o sobrescribir el método `prestar` usando `super()`*

### Fase 3: La clase `Biblioteca` (El gestor central)
Aquí es donde entra todo lo aprendido en los temas 02, 03 y 04 (Listas, Bucles, Condicionales).

**Tarea a realizar:**
1. Crear la clase `Biblioteca` que tenga una lista de `recursos` y una lista de `usuarios`.
2. Métodos como `agregar_recurso(recurso)`, `registrar_usuario(usuario)`.
3. **Búsqueda:** Un método `buscar_por_titulo(titulo)` que devuelva una lista con los recursos que coincidan (usando `if titulo.lower() in recurso.titulo.lower()`).
4. **Préstamo seguro:** Un método `realizar_prestamo(id_usuario, titulo_recurso)` que busque al usuario, busque el recurso, y llame a las funciones correspondientes manejando los `try...except` para avisar si el usuario no existe o el recurso no está disponible.

---
### Fase 4: Temas avanzados
Aplicar lo visto en los temas 09, 10 y 11:

**1. Uso de `filter` y `lambda` (Tema 10):**
Añadir un método `buscar_disponibles_por_genero(genero)` que use `filter` y `lambda` para retornar solo los recursos de ese género que tengan `self.disponible == True`.

**2. Funciones Generadoras (Tema 09):**
Añadir un método `generar_informe_general()` que use `yield` para ir devolviendo uno a uno los strings con la información de *todos* los recursos de la biblioteca. (Esto evita cargar una lista gigante en memoria si la biblioteca fuera enorme).

**3. Decorador (Tema 11):**
Fíjate que en tu código actual repites el bloque de escritura en el archivo log en `prestar` y `devolver`. 
Podemos crear un **decorador** llamado `registrar_accion` que capture el nombre de la función (`prestar` o `devolver`) y el objeto sobre el que se ejecuta, y escriba en el log automáticamente. Así podemos limpiar el código de la clase `Recurso`.

### Opcional
**Crear una Interfaz de Usuario:**
- Menú principal con opciones para:
    - Agregar un nuevo material (libro, revista o DVD).
    - Listar todos los materiales en la biblioteca.
    - Mostrar información detallada de un material específico.
    - Salir del programa.