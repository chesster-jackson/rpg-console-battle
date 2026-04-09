#Juego RPG
import random
import time

class Personaje:
    def __init__(self, nombre=None, rol=None, fuerza=0, resistencia=0):
        self.nombre = nombre
        self.rol = rol
        self.fuerza = fuerza
        self.resistencia = resistencia
        self.arma = None

    def asignar(self, nombre, rol, fuerza, resistencia):
        self.nombre = nombre
        self.rol = rol
        self.fuerza = fuerza
        self.resistencia = resistencia

    def esta_vivo(self):
        return self.resistencia > 0

    def recibir_daño(self, cantidad):
        self.resistencia = max(0, self.resistencia - cantidad)

    def __str__(self):
        arma_txt = f" con {self.arma.nombre} (daño base {self.arma.daño})" if self.arma else ""
        return f"{self.nombre} [{self.rol}] FUE:{self.fuerza} RES:{self.resistencia}{arma_txt}"


class Arma:
    def __init__(self):
        self.pool = {
            "Espada": (4, 7),
            "Mazo": (6, 9),
            "Lanza": (3, 8)
        }
        self.nombre = None
        self.daño = 0

    def aleatoria(self, bonificacion_fuerza=0):
        self.nombre = random.choice(list(self.pool.keys()))
        rango = self.pool[self.nombre]
        base = random.randint(*rango)
        self.daño = base + max(0, bonificacion_fuerza // 3)


def elegir_personaje_usuario():
    pj = Personaje()
    while True:
        print("Elige tu personaje")
        print("1. Héroe")
        print("2. Orco")
        opcion = input("Ingrese el número o el nombre de su personaje: ").strip().lower()
        opcion = opcion.replace("é", "e")  # soportar 'heroe' sin tilde

        if opcion in ("1", "heroe"):
            pj.asignar("Héroe", "Héroe", fuerza=10, resistencia=24)
            break
        elif opcion in ("2", "orco"):
            pj.asignar("Orco", "Orco", fuerza=8, resistencia=28)
            break
        else:
            print("Opción no válida, intenta nuevamente.\n")
    return pj


def crear_enemigo(oponente_del_usuario):
    enemigo = Personaje()
    if oponente_del_usuario.rol == "Héroe":
        enemigo.asignar("Orco", "Orco", fuerza=8, resistencia=28)
    else:
        enemigo.asignar("Héroe", "Héroe", fuerza=10, resistencia=24)
    return enemigo


def asignar_arma(personaje):
    arma = Arma()
    arma.aleatoria(bonificacion_fuerza=personaje.fuerza)
    personaje.arma = arma
    print(f"{personaje.nombre} obtuvo {arma.nombre} con daño base {arma.daño}.")


def calcular_daño_golpe(atacante):
    if atacante.arma is None:
        return 0, "fallo"

    base = atacante.arma.daño + atacante.fuerza // 4
    variacion = random.randint(-2, 2)
    daño = max(0, base + variacion)

    # Fallo (10%)
    if random.random() < 0.10:
        return 0, "fallo"

    # Crítico (15%)
    critico = False
    if random.random() < 0.15:
        daño = int(daño * 1.5)
        critico = True

    return daño, ("crítico" if critico else "normal")


def batalla_por_turnos(jugador, enemigo):
    print("\n=== ¡Comienza la batalla! ===")
    print(jugador)
    print(enemigo)
    print()

    turno_jugador = True
    ronda = 1

    while jugador.esta_vivo() and enemigo.esta_vivo():
        print(f"— Ronda {ronda} —")

        atacante = jugador if turno_jugador else enemigo
        defensor = enemigo if turno_jugador else jugador

        daño, tipo = calcular_daño_golpe(atacante)

        if tipo == "fallo":
            print(f"{atacante.nombre} ataca con {atacante.arma.nombre}... y falla! No causa daño.")
        elif tipo == "crítico":
            print(f"Golpe CRÍTICO {atacante.nombre} usa {atacante.arma.nombre} y causa {daño} de daño.")
            defensor.recibir_daño(daño)
        else:
            print(f"{atacante.nombre} ataca con {atacante.arma.nombre} y causa {daño} de daño.")
            defensor.recibir_daño(daño)

        print(f"Estado: {jugador.nombre} Resistencia={jugador.resistencia} | {enemigo.nombre} Resistencia={enemigo.resistencia}\n")

        turno_jugador = not turno_jugador
        ronda += 1
        time.sleep(0.5)  # pausa breve para que sea más legible

    if jugador.esta_vivo():
        print(f"{jugador.nombre} ha ganado la batalla. {enemigo.nombre} ha sido derrotado.")
    else:
        print(f"{jugador.nombre} ha sido derrotado. {enemigo.nombre} gana la batalla.")


if __name__ == "__main__":
    # random.seed(42)  # descomenta si quieres resultados repetibles
    jugador = elegir_personaje_usuario()
    enemigo = crear_enemigo(jugador)
    print("\nAsignando armas...")
    asignar_arma(jugador)
    asignar_arma(enemigo)
    batalla_por_turnos(jugador, enemigo)
