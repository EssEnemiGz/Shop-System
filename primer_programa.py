from getpass import getpass
import json

username = input("Introduzca su usuario: ")
password = getpass("Introduzca su contraseña: ")
info = None

def render():
    with open("products.json", "r") as products: # Listado de productos
        products_list = json.load(products)
        info = products_list
        for i in products_list:
            ID = i["id"]
            name = i["name"]
            price = i["price"]
            cant = i["cant"]
            print(f"{ID} - {name}, precio: {price}. Quedan: {cant}")
            
    return info

with open("users.json", "r") as file: # Esto es solo la verificacion del usuario
    json_object = json.load(file)
    
    for el in json_object:
        if el.get("username") == username and el.get("password") != password:
            exit()
            
info = render() # Listado de productos inicial
        
print("\nPara comprar introduzca el numero de la opcion que desea.\n Si quiere salir, escriba exit.")
reset = 0
while 1:
    if reset: 
        info = render()
        reset = 0
        
    response = input("Opcion: ")
    if response == "exit": break
    
    try: 
        response = int(response)
    except:
        print("Introduzca una opcion valida")
    finally:
        print("Gracias por preferirnos")
        
    no_existe = 1
    actual_product = None
    for cont in info: # Verificando que el ID existe
        if cont.get("id") == response: 
            actual_product = cont # Definiendo el producto actual en base a la iteracion
            no_existe = 0
            break
            
    if no_existe: 
        print("El ID no existe")
        reset = 1
        continue
        
    print("\033[2J")
    print(f"¿Está seguro de que quiere comprar el producto {actual_product.get('name')} por {actual_product.get('price')}?")
    option = input("si o no:")
    if option.lower() == "si": # Restando la cantidad al producto
        with open("products.json", "w") as changer: 
            position = None 
            for cont, j in enumerate(info): # [0, {...}]
                if j.get("id") == response:
                    position = cont
            
            if info[position]["cant"] == 0: 
                print("YA NO QUEDAN EXISTENCIAS!") 
                reset = 1
                continue
            
            info[position]["cant"] = info[position]["cant"]-1
            json.dump(info, changer, indent=4)
    else: 
        reset = 1
        continue