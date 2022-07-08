from my_blockchain import *
import random
# # Create the object of the class blockchain
blockchain = Blockchain()


#Escribimos ihnformación del bloque
for i in range (2):
    #Generar transacciones aleatorias
    transactions= []
    for i in range (random.randint(1,4)):
        valor_transaction = random.randint(0,50)
        lista_nodos = ["A", "B", "C", "D", "E", "F"]
        nodo1 = random.choice(lista_nodos)
        lista_nodos.remove(nodo1)
        tr = nodo1 + "->" + random.choice(lista_nodos) + "->" + str(valor_transaction)
        transactions.append(tr)
    # print(transactions)
    
    # Mining a new block
    previous_block = blockchain.print_previous_block()
    previous_hash = blockchain.hash256(previous_block)
    block = blockchain.create_block(previous_hash,transactions)

blockchain_final = blockchain.get_chain()
print("-------------------------------------------------")
print("Blockchain final \n",blockchain_final)
print("-------------------------------------------------")

