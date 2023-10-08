# Due to the trading212 having different ticker symbols for some tickers for example META is FB. you can use this script to find the correct symbol to use the api
# Some ticker may still not work. for example tickers with a '#' seems to have issues with the request library I will work on getting this sorted
# so use this feature you will have to also download the api_tickerList.csv file.


def find_api_ticker(symbol: str, full_name: str = None, isin: str = None, 
                    countryOfOrigin: str = None, currency: str = None, filePath: str = None) -> str:
    """find the correct ticker for the trading212 platform"""
    
    if filePath == None:
        if name == "nt":
            path = ".\\api_tickers.csv"
        else:
            path = ".\\api_tickers.csv"
    else:
        path = filePath

    data = pd.read_pickle(path)

    search_results = {}

    for i, row in data.iterrows():
        sn = str(data["shortName"].loc[data.index[i]])
        fn = str(data["fullName"].loc[data.index[i]])
        list_isin = str(data["isin"].loc[data.index[i]])
        ticker = str(data["ticker"].loc[data.index[i]])
        country = str(data["countryOfOrigin"].loc[data.index[i]])
        cur = str(data["currency"].loc[data.index[i]])
        if isin:
            if isin == list_isin:
                search_results[sn] = {"fullName" : fn ,"isin": list_isin, "ticker": ticker}
        elif full_name:
            if full_name in fn:
                search_results[sn] = {"fullName" : fn ,"isin": list_isin, "ticker": ticker}
        else:
            if symbol.upper() in sn:
                if countryOfOrigin or currency:
                    if countryOfOrigin == country :
                        search_results[sn] = {"fullName" : fn ,"isin": list_isin, "ticker": ticker}
                    if currency == cur:
                        search_results[sn] = {"fullName" : fn ,"isin": list_isin, "ticker": ticker}
                else:
                    search_results[sn] = {"fullName" : fn ,"isin": list_isin, "ticker": ticker}

    if len(search_results) > 1:
        print("Multiple values found: Try using isin")
        return search_results
    else:
        return search_results

    return
