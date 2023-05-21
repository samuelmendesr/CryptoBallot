import phe
from phe import paillier
import json

import blockchain

with open("public_key", "r") as f:
     public_key_jwk = f.read()

rec_public_key = json.loads(public_key_jwk)
public_key_n = phe.util.base64_to_int(rec_public_key["n"])
public_key = paillier.PaillierPublicKey(public_key_n)

with open("private_key", "r") as f:
     private_key_jwk = f.read()

rec_private_key = json.loads(private_key_jwk)
private_key_p = phe.util.base64_to_int(rec_private_key["p"])
private_key_q = phe.util.base64_to_int(rec_private_key["q"])
private_key = paillier.PaillierPrivateKey(public_key, private_key_p, private_key_q)


blockchain_votos = blockchain.Blockchain()

blockchain_votos.importar_json("blockchain.json", public_key)

cedulas = []
for bloco in blockchain_votos.blocos:
     cedulas.append(bloco.dados)

candidatos = cedulas[0]
cedulas = cedulas[1:]

resultados = {}

i = 0
for candidato in candidatos:
     resultado = 0
     for cedula in cedulas:
          resultado += paillier.EncryptedNumber(public_key, int(cedula[i]))

     resultados[candidato] = private_key.decrypt(resultado)
     print(candidato, ":", resultados[candidato])
     i += 1
