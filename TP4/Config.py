import configparser


class Config:

    config = None

    def __init__(self, config_name: str):
        parser = configparser.ConfigParser()
        parser.read(config_name)

        self.ex2_noise_probability = parser.getfloat('ex2', 'NOISE_PROB')
        self.ex2_total_tests = parser.getint('ex2', 'TOTAL_TESTS')
        self.ex2_patterns = parser.get('ex2', 'PATTERNS').split(',')
        self.ex2_show_steps = parser.getboolean('ex2', 'SHOW_STEPS')
        self.ex2_show_saved_patterns = parser.getboolean('ex2', 'SHOW_SAVED_PATTERNS')


    @staticmethod
    def init_config(config_name: str):
        Config.config = Config(config_name)
