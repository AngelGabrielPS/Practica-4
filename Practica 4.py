#problema 1 
import requests
def precio():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        response.raise_for_status()  
        data = response.json()
        bitcoin_price = data["bpi"]["USD"]["rate_float"]
        return bitcoin_price
    except requests.RequestException as e:
        print("Error making API request:", e)
        return None
def main():
    n = int(input("Ingrese la cantidad de bitcoins: "))
    if n <= 0:
        print("La cantidad de Bitcoins debe ser mayor que cero")
        return
    bitcoin_price = precio()
    if bitcoin_price is not None:
         return
    total_value_usd = n * bitcoin_price
    formatted_total_value = "${:,.4f}".format(total_value_usd)
    print(f"El valor actual de {n} Bitcoins es: {formatted_total_value} USD")

if __name__ == "__main__":
    main()



#problema 3
import requests
url= "https://images.unsplash.com/photo-1583511655826-05700d52f4d9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1888&q=80"
response=requests.get(url)
with open('perrito.jpg','wb') as f:
    f.write(response.content)
    pass


#problema 4
def guardar_tabla(numero):
    with open(f"tabla-{numero}.txt", "w") as file:
        for i in range(1, 11):
            linea = f"{numero} x {i} = {numero * i}\n"
            file.write(linea)

def mostrar_tabla(numero):
    try:
        with open(f"tabla-{numero}.txt", "r") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"El archivo tabla-{numero}.txt no existe.")

def mostrar_linea_tabla(numero, linea):
    try:
        with open(f"tabla-{numero}.txt", "r") as file:
            lines = file.readlines()
            if 1 <= linea <= len(lines):
                print(lines[linea - 1].strip())
            else:
                print("Línea fuera de rango.")
    except FileNotFoundError:
        print(f"El archivo tabla-{numero}.txt no existe.")

def main():
    while True:
        print("1. Guardar tabla de multiplicar")
        print("2. Mostrar tabla de multiplicar completa")
        print("3. Mostrar línea específica de la tabla")
        print("4. Salir")
        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 1:
            numero = int(input("Ingrese un número entre 1 y 10: "))
            if 1 <= numero <= 10:
                guardar_tabla(numero)
                print(f"Tabla de multiplicar del {numero} guardada en tabla-{numero}.txt")
            else:
                print("Número fuera de rango.")
        elif opcion == 2:
            numero = int(input("Ingrese un número entre 1 y 10: "))
            if 1 <= numero <= 10:
                mostrar_tabla(numero)
            else:
                print("Número fuera de rango.")
        elif opcion == 3:
            numero = int(input("Ingrese un número entre 1 y 10: "))
            if 1 <= numero <= 10:
                linea = int(input("Ingrese el número de línea a mostrar: "))
                mostrar_linea_tabla(numero, linea)
            else:
                print("Número fuera de rango.")
        elif opcion == 4:
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")



#problema 5
import requests
import csv

def precio():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        response.raise_for_status() 
        data = response.json()
        bitcoin_price = data["bpi"]["USD"]["rate_float"]
        return bitcoin_price
    except requests.RequestException as e:
        print("Error making API request:", e)
        return None

def guardar_precio_txt(precio):
    with open("precio_bitcoin.txt", "w") as file:
        file.write(str(precio))

def guardar_precio_csv(precio):
    with open("precio_bitcoin.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Fecha", "Precio USD"])
        csv_writer.writerow(["Hoy", precio])

def main():
    bitcoin_price = precio()
    if bitcoin_price is not None:
        guardar_precio_txt(bitcoin_price)
        guardar_precio_csv(bitcoin_price)
        print("Datos de precio de Bitcoin guardados en precio_bitcoin.txt y precio_bitcoin.csv")

if __name__ == "__main__":
    main()


#problema 6
import sqlite3
import requests
from datetime import datetime

def get_bitcoin_prices():
    try:
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        data = response.json()
        prices = {
            "USD": data["bpi"]["USD"]["rate_float"],
            "GBP": data["bpi"]["GBP"]["rate_float"],
            "EUR": data["bpi"]["EUR"]["rate_float"]
        }
        return prices
    except requests.RequestException:
        print("Error al obtener los precios de Bitcoin.")
        return None

def create_database():
    conn = sqlite3.connect("cryptos.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bitcoin (
            id INTEGER PRIMARY KEY,
            date TEXT,
            usd_price REAL,
            gbp_price REAL,
            eur_price REAL
        )
    ''')

    conn.commit()
    conn.close()

def insert_data(prices):
    conn = sqlite3.connect("cryptos.db")
    cursor = conn.cursor()

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO bitcoin (date, usd_price, gbp_price, eur_price)
        VALUES (?, ?, ?, ?)
    ''', (now, prices["USD"], prices["GBP"], prices["EUR"]))

    conn.commit()
    conn.close()

def main():
    bitcoin_prices = get_bitcoin_prices()
    if bitcoin_prices is None:
        return
    create_database()
    insert_data(bitcoin_prices)

    print("Datos insertados correctamente en la base de datos.")

if __name__ == "__main__":
    main()