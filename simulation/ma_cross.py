import pandas as pd
from infrastructure.instrument_collection import instrumentCollection as ic

BUY = 1
SELL = -1
NONE = 0
get_ma_col = lambda x: f"MA_{x}"

class MAResult:
    def __init__(self,df_trades,pair_name,ma_l,ma_s):
        self.df_trades = df_trades
        self.pair_name = pair_name
        self.ma_l = ma_l
        self.ma_s = ma_s
        self.result = self.result_ob()

    def __repr__(self):
        return str(self.result)

    def result_ob(self):
        return dict(
            pair_name=self.pair_name,
            num_trades=self.df_trades.shape[0],
            total_gain=int(self.df_trades["GAIN"].sum()),
            mean_gain= int(self.df_trades["GAIN"].mean()),
            min_gain= int(self.df_trades["GAIN"].min()),
            max_gain= int(self.df_trades["GAIN"].max()),
            ma_l=self.ma_l,
            ma_s=self.ma_s)



def load_price_data(pair, granularity, ma_list):
    df = pd.read_pickle(f"./data/{pair}_{granularity}.pkl")
    for ma in ma_list:
        df[get_ma_col(ma)] = df["mid_c"].rolling(window=ma).mean()
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def is_trade(row):
    if row.DELTA > 0 and row.DELTA_PREV <= 0:
        return BUY
    elif row.DELTA < 0 and row.DELTA_PREV >= 0:
        return SELL
    else:
        return NONE

def assess_pair(price_data, ma_long_col, ma_short_col, instrument):
    df_analysis = price_data.copy()
    df_analysis["DELTA"] = df_analysis[ma_short_col] - df_analysis[ma_long_col]
    df_analysis["DELTA_PREV"] = df_analysis["DELTA"].shift(1)
    df_analysis["TRADE"] = df_analysis.apply(is_trade, axis=1)
    #print(instrument.name,ma_long_col, ma_short_col)
    #print(df_analysis.head(3))
    return get_trades(df_analysis, instrument)

def get_trades(df_analysis, instrument):
    df_trades = df_analysis[df_analysis["TRADE"] != NONE].copy()
    df_trades["DIFF"] = df_trades["mid_c"].diff().shift(-1)
    df_trades.fillna(0, inplace=True)
    df_trades["GAIN"] = df_trades.DIFF / instrument.pipLocation
    df_trades["GAIN"] = df_trades["GAIN"] * df_trades["TRADE"]
    total_gain = df_trades["GAIN"].sum()
    return dict(total_gain =int(total_gain), df_trades = df_trades)

def analyse_pair(instrument, granularity, ma_long, ma_short):

    ma_list = set(ma_long + ma_short) # bunu yaparak aynı değerlerin tekrar tekrar hesaplanmasını engelliyoruz. Örneğin 20 ve 20 alması mantıklı olmazdı.
    pair = instrument.name

    price_data = load_price_data(pair, granularity, ma_list)
    print(pair)
    print(price_data.head(3))
    for ma_l in ma_long:
        for ma_s in ma_short:
            if ma_l <= ma_s:
                continue

            result = assess_pair(
                price_data,
                get_ma_col(ma_l),
                get_ma_col(ma_s),
                instrument
            )

            tg = result["total_gain"]
            nt = result["df_trades"].shape[0]

            print(f"{pair} {granularity} {ma_l}-{ma_s} Total Gain: {tg} Trades: {nt}")

def run_ma_sim(curr_list=["EUR","USD"],
                granularity=["H1"],
                ma_long =[20,40,80],
                ma_short=[10,20]):
    ic.LoadInstruments("./data")
    for g in granularity:
        for p1 in curr_list:
            for p2 in curr_list:
                pair = f"{p1}_{p2}"
                if pair in ic.instruments_dict.keys():
                    analyse_pair(ic.instruments_dict[pair], g, ma_long, ma_short)