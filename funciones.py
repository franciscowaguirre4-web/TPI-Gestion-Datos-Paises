import csv

ARCHIVO_CSV = "paises.csv"
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


def cargar_datos():
    """Lee el CSV y devuelve una lista de diccionarios de países."""
    paises = []

    try:
        with open(ARCHIVO_CSV, "r", newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)

            # Verifica que el archivo tenga las columnas necesarias.
            if lector.fieldnames is None or not all(campo in lector.fieldnames for campo in CAMPOS):
                print("Error: el CSV no contiene las columnas requeridas.")
                return paises

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    poblacion = int(fila["poblacion"])
                    superficie = int(fila["superficie"])
                    continente = fila["continente"].strip()

                    if not nombre or not continente:
                        print(f"Aviso: fila {numero_fila} omitida por tener campos vacíos.")
                        continue
                    if poblacion <= 0 or superficie <= 0:
                        print(f"Aviso: fila {numero_fila} omitida por valores no positivos.")
                        continue

                    pais = {
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente.title(),
                    }
                    paises.append(pais)

                except (ValueError, TypeError, KeyError):
                    print(f"Aviso: fila {numero_fila} omitida por datos inválidos.")

    except FileNotFoundError:
        print(f"No se encontró el archivo {ARCHIVO_CSV}. Se iniciará una lista vacía.")
    except OSError as error:
        print(f"No se pudo leer el CSV: {error}")

    return paises


def guardar_datos(lista):
    """Guarda la lista de países en el archivo CSV."""
    try:
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(lista)
        return True
    except OSError as error:
        print(f"Error al guardar los datos: {error}")
        return False


def pedir_texto(mensaje):
    """Solicita texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El campo no puede quedar vacío.")


def pedir_entero_positivo(mensaje):
    """Solicita un número entero mayor que cero."""
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if numero > 0:
                return numero
            print("Ingrese un número mayor que cero.")
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")


def mostrar_paises(lista):
    """Muestra los países de la lista."""
    if not lista:
        print("No hay países para mostrar.")
        return

    for pais in lista:
        print(
            f"Nombre: {pais['nombre']} | Población: {pais['poblacion']} | "
            f"Superficie: {pais['superficie']} km² | Continente: {pais['continente']}"
        )


def agregar_pais(lista):
    """Solicita los datos, agrega un país y guarda el CSV."""
    nombre = pedir_texto("Nombre: ")

    # Evita agregar dos veces el mismo país (sin distinguir mayúsculas).
    for pais in lista:
        if pais["nombre"].casefold() == nombre.casefold():
            print("Error: ese país ya existe.")
            return

    poblacion = pedir_entero_positivo("Población: ")
    superficie = pedir_entero_positivo("Superficie en km²: ")
    continente = pedir_texto("Continente: ").title()

    nuevo = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }

    lista.append(nuevo)
    if guardar_datos(lista):
        print("País agregado correctamente.")
    else:
        lista.pop()
        print("No se pudo agregar porque no se guardaron los datos.")


def actualizar_pais(lista):
    """Actualiza población y superficie de un país existente."""
    if not lista:
        print("No hay países cargados.")
        return

    nombre = pedir_texto("Ingrese el nombre del país: ")

    for pais in lista:
        if pais["nombre"].casefold() == nombre.casefold():
            poblacion_anterior = pais["poblacion"]
            superficie_anterior = pais["superficie"]

            pais["poblacion"] = pedir_entero_positivo("Nueva población: ")
            pais["superficie"] = pedir_entero_positivo("Nueva superficie: ")

            if guardar_datos(lista):
                print("País actualizado correctamente.")
            else:
                pais["poblacion"] = poblacion_anterior
                pais["superficie"] = superficie_anterior
                print("No se guardaron los cambios.")
            return

    print("No se encontró el país.")


def buscar_pais(lista):
    """Busca países por coincidencia parcial o exacta del nombre."""
    nombre = pedir_texto("Ingrese el nombre del país a buscar: ").casefold()
    encontrados = []

    for pais in lista:
        if nombre in pais["nombre"].casefold():
            encontrados.append(pais)

    if encontrados:
        print("\nPaíses encontrados:")
        mostrar_paises(encontrados)
    else:
        print("No se encontró ningún país.")


def filtrar_continente(lista):
    """Muestra los países que pertenecen al continente ingresado."""
    continente = pedir_texto("Ingrese el continente: ").casefold()
    encontrados = []

    for pais in lista:
        if pais["continente"].casefold() == continente:
            encontrados.append(pais)

    if encontrados:
        mostrar_paises(encontrados)
    else:
        print("No hay países de ese continente.")


def filtrar_por_rango(lista, campo, descripcion):
    """Filtra países por un rango inclusivo de población o superficie."""
    if not lista:
        print("No hay países cargados.")
        return

    minimo = pedir_entero_positivo(f"{descripcion} mínimo: ")
    maximo = pedir_entero_positivo(f"{descripcion} máximo: ")

    while maximo < minimo:
        print("El máximo no puede ser menor que el mínimo.")
        minimo = pedir_entero_positivo(f"{descripcion} mínimo: ")
        maximo = pedir_entero_positivo(f"{descripcion} máximo: ")

    encontrados = []
    for pais in lista:
        if minimo <= pais[campo] <= maximo:
            encontrados.append(pais)

    if encontrados:
        mostrar_paises(encontrados)
    else:
        print("No se encontraron países en ese rango.")


def filtrar_poblacion(lista):
    """Filtra países por rango de población."""
    filtrar_por_rango(lista, "poblacion", "Población")


def filtrar_superficie(lista):
    """Filtra países por rango de superficie."""
    filtrar_por_rango(lista, "superficie", "Superficie")


def ordenar_nombre(lista):
    """Ordena alfabéticamente por nombre y muestra el resultado."""
    lista.sort(key=lambda pais: pais["nombre"].casefold())
    mostrar_paises(lista)


def ordenar_poblacion(lista):
    """Ordena por población, permitiendo ascendente o descendente."""
    opcion = input("A - Ascendente / D - Descendente: ").strip().upper()

    if opcion == "A":
        lista.sort(key=lambda pais: pais["poblacion"])
    elif opcion == "D":
        lista.sort(key=lambda pais: pais["poblacion"], reverse=True)
    else:
        print("Opción inválida.")
        return

    mostrar_paises(lista)


def ordenar_superficie(lista):
    """Ordena por superficie, ascendente o descendente."""
    opcion = input("A - Ascendente / D - Descendente: ").strip().upper()

    if opcion == "A":
        lista.sort(key=lambda pais: pais["superficie"])
    elif opcion == "D":
        lista.sort(key=lambda pais: pais["superficie"], reverse=True)
    else:
        print("Opción inválida.")
        return

    mostrar_paises(lista)


def estadisticas(lista):
    """Muestra país mayor/menor población, promedios y cantidad por continente."""
    if not lista:
        print("No hay países cargados para calcular estadísticas.")
        return

    mayor = max(lista, key=lambda pais: pais["poblacion"])
    menor = min(lista, key=lambda pais: pais["poblacion"])
    promedio_poblacion = sum(pais["poblacion"] for pais in lista) / len(lista)
    promedio_superficie = sum(pais["superficie"] for pais in lista) / len(lista)

    continentes = {}
    for pais in lista:
        continente = pais["continente"].title()
        if continente in continentes:
            continentes[continente] += 1
        else:
            continentes[continente] = 1

    print("\n----- ESTADÍSTICAS -----")
    print(f"País con mayor población: {mayor['nombre']} - {mayor['poblacion']:,}")
    print(f"País con menor población: {menor['nombre']} - {menor['poblacion']:,}")
    print(f"Promedio de población: {promedio_poblacion:,.2f}")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km²")

    print("\nCantidad de países por continente:")
    for continente, cantidad in sorted(continentes.items()):
        print(f"{continente}: {cantidad}")
