import os


class DataReader:
    names = {
        'weapons': 'armas',
        'boots': 'botas',
        'helmets': 'cascos',
        'gloves': 'guantes',
        'chestplates': 'pecheras'
    }

    def __init__(self, dir_name, total_weapons, total_boots, total_helmets, total_chestplates, total_gloves):
        self.dir_name: str = dir_name
        self.total_weapons: int = total_weapons
        self.total_boots: int = total_boots
        self.total_helmets: int = total_helmets
        self.total_chestplates: int = total_chestplates
        self.total_gloves: int = total_gloves

    def get(self, piece, index):
        if piece not in DataReader.names:
            raise Exception('Invalid armor piece')
        piece = DataReader.names[piece]
        source_dir = os.path.join(self.dir_name, f'{piece}.tsv')
        print(f'{source_dir = }')
        file = open(f'{source_dir}', 'r')
        for i, line in enumerate(file):
            if i == (index+1):
                print(line)