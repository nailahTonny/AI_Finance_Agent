import requests, os
def get_balance():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=AAPL&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        report = data['annualReports'][0]
        balance = report['cashAndCashEquivalentsAtCarryingValue']
        return {"account_balance": f"${balance}"}
    except Exception as e:
        return {"error": str(e)}
