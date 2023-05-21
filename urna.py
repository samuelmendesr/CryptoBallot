import phe
from phe import paillier
import json
import blockchain
import random

# ------------------------------------------------------------

with open("public_key", "r") as f:
     public_key_jwk = f.read()

rec_public_key = json.loads(public_key_jwk)
public_key_n = phe.util.base64_to_int(rec_public_key['n'])
public_key = paillier.PaillierPublicKey(public_key_n)

# ------------------------------------------------------------

def cedula_modelo():
    return [0, 0, 0]

embaralhamento = 3

blockchain = blockchain.Blockchain()
blockchain.importar_json("blockchain.json", public_key)

candidatos = blockchain.blocos[0].dados

urna_ativada = True
index_voto = 0
votos = []

while (urna_ativada):
    print("Eleições CA 2023")

    i = 1
    for candidato in candidatos:
        print(candidato, ":", i)
        i += 1

    voto = input("Voto: ")

    cedula = cedula_modelo()

    if (voto == "exit"):
        urna_ativada = False
    elif (voto != 0):
        try:
            cedula[int(voto) - 1] = 1
        except:
            cedula = cedula_modelo()

    cedula_encriptada = cedula

    j = 0
    for i in cedula:
        cedula_encriptada[j] = str(public_key.encrypt(i).ciphertext())
        j += 1

    votos.append(cedula_encriptada)

    print("FIM")

    if (index_voto == embaralhamento) or (urna_ativada == False):
        index_voto = 0
        random.shuffle(votos)

        for voto in votos:
            blockchain.adicionar_bloco(voto, 'voto')

        votos = []

    index_voto += 1


blockchain.exportar_json("blockchain.json")


if (blockchain.checar_blocos()):
    print("Blockchain ok")
else:
    print("Blockchain corrompida")


