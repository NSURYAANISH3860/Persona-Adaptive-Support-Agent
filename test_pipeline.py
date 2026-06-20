from src.classifier import classify_customer_persona
from src.rag_pipeline import LocalRAGPipeline
from src.generator import generate_adaptive_response

def run_tests():
    pipeline = LocalRAGPipeline()
    print("Ingesting data...")
    pipeline.load_and_ingest_all()
    
    queries = [
        "Where is the guide to clear cookies? It's been an hour and nothing is loading on your interface!",
        "What are the header parameter requirements for your bearer token auth implementation?",
        "Our operational uptime is decreasing. We need a timeline of when billing disputes are resolved.",
        "I'm experiencing an issue with your database integration that's causing internal errors.",
        "My billing statement has unexpected duplicate charges. I demand an immediate refund!"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n--- Test Scenario {i} ---")
        print(f"Query: {query}")
        
        classification = classify_customer_persona(query)
        persona = classification.get("persona")
        print(f"Detected Persona: {persona}")
        
        context = pipeline.retrieve_context(query)
        result = generate_adaptive_response(query, persona, context)
        
        if result["escalated"]:
            print("Status: ESCALATED TO HUMAN")
            print(f"Handoff Payload: {result['handoff_summary']}")
        else:
            print("Status: HANDLED")
            print(f"Response: {result['response'][:100]}...")

if __name__ == "__main__":
    run_tests()