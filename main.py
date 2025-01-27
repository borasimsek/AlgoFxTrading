from api.oanda_api import OandaAPI



if __name__ == '__main__':
    api = OandaAPI()

    data = api.get_account_summary()
    print(data)