import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_db_connection():
    """Create a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER'),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
    )

def generate_embedding(text):
    """Generate embedding for the given text using OpenAI's API."""
    if not text:
        print("Warning: No diary text - skipping entry")
        return None
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        print(f"Text that failed: {text[:200]}...")
        return None

def search_similar_entries(query, limit=5):
    """Search for similar diary entries based on the query."""
    # Generate embedding for the query
    query_embedding = generate_embedding(query)
    
    # Connect to the database
    conn = get_db_connection()
    
    try:
        with conn.cursor() as cur:
            # Perform the similarity search
            cur.execute("""
                SELECT 
                    date,
                    entry,
                    1 - (embedding <=> %s::vector) as similarity
                FROM diary
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (query_embedding, query_embedding, limit))
            
            results = cur.fetchall()
            
            # Format the results
            formatted_results = []
            for row in results:
                formatted_results.append({
                    'date': row[0],
                    'entry': row[1],
                    'similarity': row[2]
                })
            
            return formatted_results
            
    finally:
        conn.close()

def format_rag_prompt(relevant_entries):
    """Format the RAG prompt with context and question."""
    # Start with system instructions
    prompt = "You are a diary management assistant. You will answer the user based on the most relevants entries from his diary. These entries are provided to you below. If the entries aren't relevant to the question, feel free to say that you aren't sure about that question."

    # Add the relevant diary entries as context
    prompt += "\n\nRelevant diary entries:\n"
    for relevant_entry in relevant_entries:
        prompt += f"\nDate: {relevant_entry['date']}\n"
        prompt += f"Content: {relevant_entry['entry']}\n"
        prompt += "---"

    return prompt

def get_llm_response(prompt, question):
    """Get response from OpenAI's API."""
    response = client.responses.create(
        model="gpt-3.5-turbo",
        input=[
            { "role": "developer", "content": prompt },
            { "role": "user", "content": question }
        ],
    )
    return response.output_text

def generate_random_question():
    """Generate a random question about your diary."""
    prompt = """Pick a random question from this list:

- When was the last time I called my Brother?
- Is there any homework due?
- When was the last night I had fun with friends?
- Who was I with during my walk on May 16th?
- What did I do on May 1st?
- When was the last time I called Grandma?
- When was the last time I called Mom?

"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            { "role": "user", "content": prompt }
        ],
        temperature=1.3,
    )
    return response.output_text

def process_query(question):
    """Process a query and return the response."""
    if not question.strip():
        return "Please enter a question about your diary."
    
    # Search for relevant entries
    relevant_entries = search_similar_entries(question, limit=3)
    
    if not relevant_entries:
        return "I couldn't find any relevant diary entries for your question."
    
    # Format the RAG prompt
    prompt = format_rag_prompt(relevant_entries)
    
    # Get the response
    response = get_llm_response(prompt, question)
    
    return response

