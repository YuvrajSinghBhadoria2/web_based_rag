import sys
sys.path.append('/Users/apple/Documents/assignement/backend')

from app.services.vector_store import vector_store
from app.services.embeddings import embedding_service
import asyncio

async def check_vector_db():
    # Get stats
    stats = await vector_store.get_stats()
    print(f"Vector DB Stats: {stats}")
    
    # Test query
    query = "Notions of occlusiology in orthodontics"
    print(f"\nQuery: {query}")
    
    # Generate embedding
    query_embedding = embedding_service.embed_text(query)
    print(f"Query embedding dimension: {len(query_embedding)}")
    
    # Search with specific document ID
    doc_id = "494ae2db-bd8e-4b09-9ece-e48dcec25ebf"
    print(f"\nSearching in document: {doc_id}")
    
    results = await vector_store.search(
        query_embedding=query_embedding,
        top_k=5,
        document_ids=[doc_id]
    )
    
    print(f"\nResults found: {len(results)}")
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Page: {result['metadata'].get('page_number', 'N/A')}")
            print(f"Content: {result['text'][:200]}...")
    else:
        print("\nNo results found!")
        
        # Try searching without document filter
        print("\nTrying search without document filter...")
        all_results = await vector_store.search(
            query_embedding=query_embedding,
            top_k=5,
            document_ids=None
        )
        print(f"Results without filter: {len(all_results)}")
        
        if all_results:
            for i, result in enumerate(all_results, 1):
                print(f"\n--- Result {i} ---")
                print(f"Document ID: {result['metadata'].get('document_id', 'N/A')}")
                print(f"Similarity: {result['similarity']:.4f}")
                print(f"Content: {result['text'][:100]}...")

asyncio.run(check_vector_db())
