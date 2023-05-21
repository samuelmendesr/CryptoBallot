import hashlib
import json
from datetime import datetime
from phe import paillier

class Bloco:
    def __init__(self, dados, tipo):
        self.tipo = tipo
        self.dados = dados
        self.hash_anterior = None
        self.hash_atual = None

    def calcular_hash(self):
        dados_serializados = ''.join([i for i in self.dados])
        return hashlib.sha256(dados_serializados.encode()).hexdigest()

    def to_dict(self):
        return {
            'tipo': self.tipo,
            self.tipo: self.dados,
            'hash_anterior': self.hash_anterior,
            'hash': self.calcular_hash()
        }

class Blockchain:
    def __init__(self):
        self.blocos = []

    def adicionar_bloco(self, voto, tipo):
        bloco = Bloco(voto, tipo)
        if len(self.blocos) > 0:
            bloco.hash_anterior = self.blocos[-1].calcular_hash()

        bloco.hash_atual = bloco.calcular_hash()
        self.blocos.append(bloco)

    def mostrar_blocos(self):
        for bloco in self.blocos:
            print(f'Hash anterior: {bloco.hash_anterior}')
            print(f'Voto: {bloco.dados}')
            print(f'Hash: {bloco.calcular_hash()}\n')

    def checar_blocos(self):
        for i in range(1, len(self.blocos)):
            bloco_atual = self.blocos[i]
            bloco_anterior = self.blocos[i-1]

            print(bloco_atual.hash_atual, "==", bloco_atual.calcular_hash())

            if bloco_atual.hash_anterior != bloco_anterior.calcular_hash():
                return False
            if bloco_atual.hash_atual != bloco_atual.calcular_hash():
                return False
        return True

    def exportar_json(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            blocos_dict = [bloco.to_dict() for bloco in self.blocos]
            json.dump(blocos_dict, arquivo, indent=4)

    def importar_json(self, nome_arquivo, public_key = None):
        with open(nome_arquivo, 'r') as arquivo:
            blocos_dict = json.load(arquivo)
            self.blocos = []
            for bloco_dict in blocos_dict:
                if (bloco_dict['tipo'] == 'voto'):
                    cedula = []
                    for voto in bloco_dict['voto']:
                        cedula.append(voto)
                    bloco = Bloco(cedula, bloco_dict['tipo'])
                elif (bloco_dict['tipo'] == 'candidatos'):
                    bloco = Bloco(bloco_dict['candidatos'], bloco_dict['tipo'])
                else:
                    bloco = Bloco(bloco_dict['dados'], bloco_dict['tipo'])

                bloco.hash_atual = bloco_dict['hash']
                bloco.hash_anterior = bloco_dict['hash_anterior']
                self.blocos.append(bloco)




