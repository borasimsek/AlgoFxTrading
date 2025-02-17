from api.oanda_api import OandaAPI
from infrastructure.instrument_collection import InstrumentCollection
from simulation.ma_cross import run_ma_sim


if __name__ == '__main__':
    #api = OandaAPI()
    #instrumentCollection = InstrumentCollection()
    #instrumentCollection.CreateFile(api.get_account_instruments(), "./data")
    #instrumentCollection.loadInstruments("./data")
    #instrumentCollection.PrintInstruments()


    #data = api.get_account_summary()
    #print(data)
    
    #instrumentCollection.loadInstruments("./data")
    #instrumentCollection.PrintInstruments()
    run_ma_sim(curr_list=["EUR","USD","GBP", "JPY", "AUD", "CAD"],)