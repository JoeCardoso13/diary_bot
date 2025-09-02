from rag_tools import process_query

def main():
    """Main function to run the RAG application."""
    print("\nWelcome to your Diary Bot assitant!")
    print("Ask questions about anything that's in your diary! The Diary Bot will remember!")
    print("Type 'quit' at any time to exit.\n")

    while True:
        # Get user question
        question = input("\nWhat would you like to know about? ")
        
        if question.lower() == 'quit':
            print("\nThanks for using the Diary Bot assistant. Helping you remember!")
            break
        
        # Process the query and display response
        response = process_query(question)
        print("\nResponse:")
        print(response)

if __name__ == "__main__":
    main() 
