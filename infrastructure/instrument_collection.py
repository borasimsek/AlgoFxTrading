import json
from models.instrument import Instrument

class InstrumentCollection:
    FILENAME = 'instruments.json'
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation','displayPrecision' ,'tradeUnitsPrecision','marginRate']

    def __init__(self):
        self.instruments_dict = {}

    def LoadInstruments(self, path):
        self.instruments_dict = {}
        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, 'r') as f:
            data = json.loads(f.read())
            for key, value in data.items():
                self.instruments_dict[key] = Instrument.formApiObject(value)

    def CreateFile(self, data, path):
        if data == None:
            print("No data to save")
            return
        instrument_dict = {}
        for i in data:
            key = i['name']
            instrument_dict[key] = {k: i[k] for k in self.API_KEYS}
        
        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, 'w') as f:
            f.write(json.dumps(instrument_dict, indent=2))

    def PrintInstruments(self):
        for key, value in self.instruments_dict.items():
            print(key, value)
            print(len(self.instruments_dict.keys()), " instruments loaded")
    
instrumentCollection = InstrumentCollection()