from app.embedder import model, embed_texts
from app.vector_store import VectorStore
from app.data_loader import load_data
from openai import OpenAI
import os

# Get API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

# Initialize these only when needed, not on import
data_df = None
store = None

def initialize():
    global data_df, store
    if data_df is None:
        data_df = load_data()
        store = VectorStore(dim=384)
        
        descriptions = data_df['explanation'].tolist()
        metadata = data_df.to_dict(orient='records')
        embeddings = embed_texts(descriptions)
        store.add(embeddings, metadata)

def query_rag(user_input):
    # Initialize data and store if not already done
    if 'store' not in globals() or store is None:
        initialize()
        
    input_emb = embed_texts([user_input])[0]
    top_matches = store.search(input_emb)

    context = "\n".join([
        f"{m['term']}: {m['explanation']} (Analogy: {m['analogy']}, Use-case: {m['use_case']})"
        for m in top_matches
    ])

    prompt = f'''
User asked: "{user_input}"

Similar terms:
{context}

Using this context, explain "{user_input}" in:
1. Plain English
2. A real-world analogy
3. A short use case
    '''

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content