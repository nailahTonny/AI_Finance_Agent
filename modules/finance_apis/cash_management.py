import requests, os
def get_summary():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol=AAPL&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        report = data['annualReports'][0]
        cash = report['cashAndCashEquivalentsAtCarryingValue']
        return {"total_cash": f"${cash}", "available_cash": f"${cash}"}
    except Exception as e:
        return {"error": str(e)}
