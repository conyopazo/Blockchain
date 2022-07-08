from threading import Thread, Lock
import threading
import datetime
import json
from typing import final
from bitcoin import *
from hashlib import sha256
import time as t
import random

#Variables globales
prefix_zeros = 3
prefix_str='0'*prefix_zeros
chain = []
nodos_accept = 0
cant_nodos = 6
bloque = ''
nonce_winner = ''
hash_winner = ''
ganador = ''
termine = False
cant_bloques = 3
#Creamos variable para bloquear
flag = False
#Generamos lista con posibles nodos
# nodos_total = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
nodos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
random.shuffle(nodos)
ts = ''
#Funcion para crear bloque
def create_block(previous_hash, transacciones):
    global chain
    data = {'index': len(chain) + 1,
                'transacciones' : transacciones,
                'timestamp': ts,
                'previous_hash': previous_hash}
    return data

# This is the function for proof of work and used to successfully mine the block
def proof_of_work(block, prefix_zeros):
    global flag
    begin=t.time()
    prefix_str='0'*prefix_zeros
    MAX_NONCE=10000000
    time.sleep(random.random())
    for nonce in range(MAX_NONCE):
        if not flag:         
            block['nonce'] = nonce
            hash = hash256(block)
            if hash.startswith(prefix_str):
                flag = True
                print("Bitcoin mined with nonce value :",nonce)
                time_taken=t.time()- begin
                print("The mining process  took ",time_taken,"seconds") 
                return block,nonce,hash
    print("No pude encontrar el nonce")
    return False

#Esta función comprueba que sea correcto el nonce encontrado
def concenso(block,nonce,hash_entregado):
    block['nonce'] = nonce
    hash = hash256(block)
    print(hash)
    print(hash_entregado)
    if (hash == hash_entregado) and (hash.startswith(prefix_str)):
        return True  
    else:
        return False    

# This function check a new block
def append_block(final_block):
    global chain
    hash = hash256(final_block)
    if hash.startswith(prefix_str):
        chain.append(final_block)
    else:
        raise Exception("Bloque no válido")

# This function is created to display the previous block
def print_previous_block():
    return chain[-1]

#Genero hash
def hash256(block):
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

#Obtengo cadena
def get_chain():
    return chain

#Crear lista de transacciones aleatorias
def transactions_list():
    global nodos
    transactions= []
    for i in range (random.randint(1,4)):
        valor_transaction = random.randint(0,50)
        lista_nodos = nodos.copy()
        nodo1 = random.choice(lista_nodos)
        lista_nodos.remove(nodo1)
        tr = nodo1 + "->" + random.choice(lista_nodos) + "->" + str(valor_transaction)
        transactions.append(tr)
    return transactions

#Clase que define un hilo
class Node(threading.Thread):
    def __init__(self, threadID, name, transactions):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.transactions = transactions
        self.lock = Lock()
    #Lo que corre cada hilo
    def run(self):
        global bloque
        global hash_winner
        global nonce_winner
        global ganador
        global termine
        global nodos_accept
        # print("hola, soy ", self.name)
        # Created new block
        previous_block = print_previous_block()
        previous_hash = hash256(previous_block)
        data = create_block(previous_hash,self.transactions)
        block = proof_of_work(data, prefix_zeros)
        if block:
            bloque = block[0]
            nonce_winner = block[1]
            hash_winner = block[2]
            ganador = self.name
            print("El ganador es", self.name)
            # print(block)
            # print(hash256(block))
            termine = True
        if ganador != self.name:
            while True:
                if termine:
                    validacion = concenso(data,nonce_winner,hash_winner)
                    if validacion:
                        self.lock.acquire()
                        nodos_accept+=1
                        self.lock.release()
                    break
        else:
            print('Yo el ganador ', self.name, ' no voto')
#Main
def main():    
    global chain
    global flag
    global nodos_accept
    global cant_nodos
    global ts
    #Created a new chain
    ts = str(datetime.datetime.now())
    primero = create_block(previous_hash='0',transacciones = "")
    inicial_block = proof_of_work(primero,prefix_zeros)
    append_block(inicial_block[0])
    print(chain)
    for j in range(cant_bloques):
        #Modfico variables
        flag = False
        transactions = transactions_list()
        ts = str(datetime.datetime.now())
        # Create new threads
        threads = []
        print('Cnt nodos: ', len(nodos))
        for i in range(cant_nodos):
            thread = Node(i + 1, nodos[i] , transactions)
            thread.start()
            threads.append(thread)
        # Wait for all threads to complete
        for t in threads:
            t.join()
        #Valido concenso
        print("Los nodos que dijeron que sí fueron: ",nodos_accept)
        #Arreglar
        if (nodos_accept >= (cant_nodos-1) * 0.8):
            append_block(bloque)
        print (chain)
        nodos_accept = 0
if __name__ == "__main__":
    main()
