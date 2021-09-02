import os

from armamentos.Armamento import Armamento


class DataReader:
    names = {
        'weapon': 'armas',
        'boots': 'botas',
        'helmet': 'cascos',
        'gloves': 'guantes',
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

    reader = None

    def __init__(self, dir_name, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates):
        self.dir_name: str = dir_name
        self.total_weapons: int = total_weapons
        self.total_boots: int = total_boots
        self.total_helmets: int = total_helmets
        self.total_chestplates: int = total_chestplates
        self.total_gloves: int = total_gloves
        self.buffer = {}
        self.totals = {
            'weapon': total_weapons,
            'boots': total_boots,
            'helmet': total_helmets,
            'chestplate': total_chestplates,
            'gloves': total_gloves,
        }

    def get(self, piece, index) -> Armamento:
        if piece not in DataReader.names:
            raise Exception('Invalid armor piece')
        if (index, piece) in self.buffer:
            return self.buffer[(index, piece)]
        file_name = DataReader.names[piece]
        source_dir = os.path.join(self.dir_name, f'{file_name}.tsv')
        file = open(f'{source_dir}', 'r')
        for i, line in enumerate(file):
            if i > self.totals[piece] + 1:
                raise Exception('Index out of range')
            if i == (index + 1):
                stats = line.split('\t')
                stats = [float(x) for x in stats]
                armamento = Armamento(int(stats[0]), piece, float(stats[1]), float(stats[2]), float(stats[3]),
                                      float(stats[4]), float(stats[5]))
                self.buffer[(index, piece)] = armamento
                return armamento
        raise Exception('Index out of range')

    def get_all(self, piece) -> list[Armamento]:
        if piece not in DataReader.names:
            raise Exception('Invalid armor piece')
        file_name = DataReader.names[piece]
        source_dir = os.path.join(self.dir_name, f'{file_name}.tsv')
        file = open(f'{source_dir}', 'r')
        output = []
        for i, line in enumerate(file):
            if i == 0:
                continue
            stats = line.split('\t')
            stats = [float(x) for x in stats]
            armamento = Armamento(int(stats[0]), piece, float(stats[1]), float(stats[2]), float(stats[3]),
                                  float(stats[4]), float(stats[5]))
            output.append(armamento)
        return output

    @staticmethod
    def init_reader(dir_name, total_weapons, total_boots, total_helmets, total_gloves, total_chestplates):
        DataReader.reader = DataReader(dir_name, total_weapons, total_boots, total_helmets, total_gloves,
                                       total_chestplates)
