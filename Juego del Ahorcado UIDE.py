# PROYECTO FINAL
# JUEGO DEL AHORCADO - FACTURACIÓN UNIVERSITARIA
# Universidad Internacional del Ecuador (UIDE)
# Autor: Miguel Ángel Suárez Prada
# Lenguaje: Python

import random
import os

# VARIABLES GLOBALES Y CONFIGURACIÓN
puntaje = 0
victorias = 0
derrotas = 0
nombre_usuario = ""

# Tupla con el dibujo del ahorcado según los intentos fallidos (0 a 6)
AHORCADO = (
"""
 +---+
 |   |
     |
     |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
     |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
 |   |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|   |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\  |
     |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\  |
/    |
     |
=========
""",
"""
 +---+
 |   |
 O   |
/|\\  |
/ \\  |
     |
=========
"""
)

# Diccionario organizado por categorías de facturación técnica de la UIDE
categorias = {
    "Facturación": [
        "FACTURA", "RECIBO", "DESCUENTO", "PENSION"
    ],
    "Tesorería": [
        "ARANCEL", "CUOTA", "TESORERIA"
    ],
    "Académico": [
        "MATRICULA", "BECA", "CREDITO"
    ]
}

# Diccionario general de definiciones para las pistas
definiciones = {
    "FACTURA": "Documento que respalda una venta.",
    "MATRICULA": "Proceso mediante el cual un estudiante registra sus materias.",
    "RECIBO": "Documento que confirma un pago.",
    "ARANCEL": "Valor económico que debe cancelar el estudiante.",
    "TESORERIA": "Departamento encargado de recaudar pagos.",
    "PENSION": "Pago periódico realizado por el estudiante.",
    "CUOTA": "Parte del valor total cancelada por el estudiante.",
    "DESCUENTO": "Reducción aplicada sobre un valor.",
    "CREDITO": "Número de horas académicas asignadas a una materia.",
    "BECA": "Beneficio económico otorgado al estudiante."
}

# FUNCIONES DE INTERFAZ Y LOGÍSTICA

def mostrar_titulo():
    """Muestra la bienvenida institucional."""
    print("=" * 60)
    print("     JUEGO DEL AHORCADO")
    print(" FACTURACIÓN UNIVERSITARIA - UIDE")
    print("=" * 60)

def seleccionar_palabra():
    """Selecciona una categoría y una palabra aleatoria."""
    categoria = random.choice(list(categorias.keys()))
    palabra = random.choice(categorias[categoria])
    pista = definiciones.get(palabra, "Concepto de facturación universitaria.")
    return palabra, pista, categoria

def mostrar_palabra(palabra, letras_adivinadas):
    """Muestra la palabra utilizando guiones bajos para las letras ocultas."""
    resultado = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            resultado += letra + " "
        else:
            resultado += "_ "
    return resultado

def validar_letra(letra):
    """Valida que el usuario ingrese únicamente una letra del alfabeto."""
    if len(letra) != 1:
        return False
    if not letra.isalpha():
        return False
    return True

def sumar_puntos(intentos_restantes):
    """Calcula el puntaje basado en los intentos salvados."""
    return intentos_restantes * 10


# GESTIÓN DE HISTORIAL Y ESTADÍSTICAS

def obtener_ruta_historial():
    """Genera una ruta absoluta segura en la misma carpeta del script .py"""
    try:
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(ruta_actual, "historial.txt")
    except NameError:
        return "historial.txt"

def guardar_resultado(nombre, resultado, palabra):
    """Registra la partida en un archivo de texto utilizando una ruta absoluta segura."""
    try:
        ruta_archivo = obtener_ruta_historial()
        archivo = open(ruta_archivo, "a", encoding="utf-8")
        archivo.write(f"{nombre} - {resultado} - {palabra}\n")
        archivo.close()
    except Exception as e:
        print("\n⚠ Nota: No se pudo escribir en el historial debido a restricciones del sistema:", e)

def mostrar_historial():
    """Lee y despliega el contenido del historial de partidas."""
    print("\n========== HISTORIAL DE PARTIDAS ==========\n")
    try:
        ruta_archivo = obtener_ruta_historial()
        archivo = open(ruta_archivo, "r", encoding="utf-8")
        print(archivo.read())
        archivo.close()
    except FileNotFoundError:
        print("Aún no existen partidas registradas en el historial.txt.")
    except Exception as e:
        print("No se pudo leer el archivo de historial:", e)

def mostrar_estadisticas():
    """Muestra el rendimiento acumulado del colaborador."""
    print("\n========== ESTADÍSTICAS GLOBALES ==========")
    print(f"Colaborador: {nombre_usuario}")
    print(f"Victorias:   {victorias}")
    print(f"Derrotas:    {derrotas}")
    print(f"Puntaje Total: {puntaje} pts")
    print("===========================================")

# LÓGICA PRINCIPAL DEL JUEGO

def jugar():
    """Mecánica interna del juego utilizando estructuras clave."""
    global puntaje, victorias, derrotas
    
    # Selección de datos iniciales
    palabra, pista, categoria = seleccionar_palabra()
    letras_adivinadas = []
    letras_intentadas = []
    fallos = 0
    max_fallos = 6

    print(f"\n[Categoría]: {categoria}")
    print(f"[Pista]: {pista}")
    print(f"La palabra contiene {len(palabra)} letras.")

    # Bucle de partida controlado dinámicamente hasta un máximo de 6 fallos
    for intento in range(100): 
        
        print(AHORCADO[fallos])
        print("Palabra: ", mostrar_palabra(palabra, letras_adivinadas))
        
        # Mostrar letras usadas si existen
        if letras_intentadas:
            print("Letras intentadas: ", ", ".join(letras_intentadas))

        letra_ingresada = input("\nDigite una letra: ").upper()

        # Filtro 1: Validación de formato
        if not validar_letra(letra_ingresada):
            print("⚠ Advertencia: Ingrese solo una letra válida (A-Z). Sin números ni símbolos.")
            continue

        # Filtro 2: Validación de repetición
        if letra_ingresada in letras_intentadas:
            print(f"⚠ Ya intentaste con la letra '{letra_ingresada}'. Elige otra.")
            continue

        # Registrar el intento válido en la lista de control
        letras_intentadas.append(letra_ingresada)

        # Filtro 3: Comprobación de existencia en la palabra (IF / ELIF / ELSE)
        if letra_ingresada in palabra:
            print(f"¡Buen trabajo! La letra '{letra_ingresada}' es correcta.")
            letras_adivinadas.append(letra_ingresada)
            
            # Verificar si ya se completó la palabra completa
            palabra_completa = True
            for l in palabra:
                if l not in letras_adivinadas:
                    palabra_completa = False
                    break
            
            if palabra_completa:
                print("\n" + "*" * 41)
                print("¡¡ FELICITACIONES !!")
                print(f"Descubriste la palabra técnica: {palabra}")
                print("*" * 41)
                
                puntos_ganados = sumar_puntos(max_fallos - fallos)
                puntaje += puntos_ganados
                victorias += 1
                print(f"Puntaje obtenido en esta ronda: +{puntos_ganados} pts")
                
                guardar_resultado(nombre_usuario, "GANÓ", palabra)
                break
        else:
            print(f"Lo siento, la letra '{letra_ingresada}' no está en la palabra.")
            fallos += 1

        # Control de pérdida por alcanzar el límite de fallos
        if fallos == max_fallos:
            print(AHORCADO[fallos])
            print("\n" + "*" * 41)
            print("HAS PERDIDO")
            print("La palabra correcta era:", palabra)
            print("*" * 41)
            
            derrotas += 1
            guardar_resultado(nombre_usuario, "PERDIÓ", palabra)
            break

    # Resumen ordenado de letras utilizadas al finalizar la partida usando enumerate()
    print("\nResumen ordenado de letras utilizadas:")
    for numero, letrita in enumerate(letras_intentadas, start=1):
        print(f"{numero} - {letrita}")

# MENÚ GENERAL Y EJECUCIÓN DEL PROGRAMA

def menu():
    """Controlador principal del flujo del sistema."""
    global nombre_usuario
    
    mostrar_titulo()
    nombre_usuario = input("Estimado colaborador por favor ingrese su nombre para iniciar: ").strip()
    if not nombre_usuario:
        nombre_usuario = "Colaborador_UIDE"
    print(f"\n¡Bienvenido {nombre_usuario} al sistema didáctico de facturación!")

    while True:
        print("\nMENÚ PRINCIPAL ")
        print("1. Jugar una partida")
        print("2. Ver historial general (.txt)")
        print("3. Ver mis estadísticas acumuladas")
        print("4. Salir del sistema")
              
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            jugar()
        elif opcion == "2":
            mostrar_historial()
        elif opcion == "3":
            mostrar_estadisticas()
        elif opcion == "4":
            print("\nGracias por utilizar el")
            print("JUEGO DEL AHORCADO")
            print("FACTURACIÓN UNIVERSITARIA")
            print("Universidad Internacional del Ecuador")
            print("### FIN DEL JUEGO")
            
            # Pausa requerida para evitar que se cierre la consola de golpe al terminar
            input("\nPresione ENTER para cerrar la ventana...")
            break
        else:
            print("⚠ Opción incorrecta. Por favor, digite un número del 1 al 4.")

# Punto de entrada para arrancar la aplicación de forma segura
if __name__ == "__main__":
    menu()