from funciones import *

# Carga los países desde el archivo CSV al iniciar el programa.
paises = cargar_datos()

while True:
    print("\n===== MENÚ =====")
    print("1 - Mostrar países")
    print("2 - Agregar país")
    print("3 - Actualizar país")
    print("4 - Buscar país")
    print("5 - Filtrar por continente")
    print("6 - Filtrar por población")
    print("7 - Filtrar por superficie")
    print("8 - Ordenar por nombre")
    print("9 - Ordenar por población")
    print("10 - Ordenar por superficie")
    print("11 - Estadísticas")
    print("0 - Salir")

    opcion = input("Ingrese una opción: ").strip()

    if opcion == "1":
        mostrar_paises(paises)
    elif opcion == "2":
        agregar_pais(paises)
    elif opcion == "3":
        actualizar_pais(paises)
    elif opcion == "4":
        buscar_pais(paises)
    elif opcion == "5":
        filtrar_continente(paises)
    elif opcion == "6":
        filtrar_poblacion(paises)
    elif opcion == "7":
        filtrar_superficie(paises)
    elif opcion == "8":
        ordenar_nombre(paises)
    elif opcion == "9":
        ordenar_poblacion(paises)
    elif opcion == "10":
        ordenar_superficie(paises)
    elif opcion == "11":
        estadisticas(paises)
    elif opcion == "0":
        print("Programa finalizado.")
        break
    else:
        print("Opción incorrecta. Ingrese un número del 0 al 11.")
