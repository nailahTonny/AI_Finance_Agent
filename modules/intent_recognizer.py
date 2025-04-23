from sentence_transformers import SentenceTransformer, util
import re
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

intent_map = {
    "check account balance": "get_account_balance",
    "generate tax report": "generate_tax_report",
    "upload and process invoice": "upload_invoice",
    "fetch cashflow summary": "get_cashflow_summary"
}
keyword_map = {
    "balance": "get_account_balance",
    "tax": "generate_tax_report",
    "invoice": "upload_invoice",
    "cashflow": "get_cashflow_summary",
    "cash flow": "get_cashflow_summary"
}
def get_intent(user_query):
    queries = list(intent_map.keys())
    embeddings = model.encode(queries + [user_query], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embeddings[-1], embeddings[:-1])
    best_idx = similarity.argmax()
    best_score = similarity[0][best_idx].item()
    if best_score >= 0.5:
        return intent_map[queries[best_idx]]
    lowered = user_query.lower()
    for keyword, intent in keyword_map.items():
        if re.search(rf"\\b{keyword}\\b", lowered):
            return intent
    return "unknown_intent"
