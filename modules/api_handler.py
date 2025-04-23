from modules.finance_apis import cash_management, accounting, tax_reporting
def handle_api_call(intent):
    if intent == "get_cashflow_summary":
        return cash_management.get_summary()
    elif intent == "generate_tax_report":
        return tax_reporting.generate_report()
    elif intent == "get_account_balance":
        return accounting.get_balance()
    else:
        return {"error": "Unknown intent"}
