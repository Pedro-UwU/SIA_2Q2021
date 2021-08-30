import os

from armamentos.Armamento import Armamento


class DataReader:
    names = {
        'weapon': 'armas',
        'boot': 'botas',
        'helmet': 'cascos',
        'glove': 'guantes',
        'chestplate': 'pecheras'
    }

    indices = {
        'id': 0,
        'Fu': 1,
        'Ag': 2,
        'Ex': 3,
        'Re': 4,
        'Vi': 5
    }

    def __init__(self, dir_name, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates):
        self.dir_name: str = dir_name
        self.total_weapons: int = total_weapons
        self.total_boots: int = total_boots
        self.total_helmets: int = total_helmets
        self.total_chestplates: int = total_chestplates
        self.total_gloves: int = total_gloves
        self.buffer = {}

    def get(self, piece, index) -> Armamento:
        if piece not in DataReader.names:
            raise Exception('Invalid armor piece')
        if index in self.buffer:
            return self.buffer[index]
        file_name = DataReader.names[piece]
        source_dir = os.path.join(self.dir_name, f'{file_name}.tsv')
        file = open(f'{source_dir}', 'r')
        for i, line in enumerate(file):
            if i == (index + 1):
                stats = line.split('\t')
                stats = [float(x) for x in stats]
                armamento = Armamento(int(stats[0]), piece, float(stats[1]), float(stats[2]), float(stats[3]),
                                      float(stats[4]), float(stats[5]))
                self.buffer[index] = armamento
                return armamento
