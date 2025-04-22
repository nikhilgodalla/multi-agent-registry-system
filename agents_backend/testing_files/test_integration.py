# testing_files/test_integration.py
import logging
import requests
import time

logging.basicConfig(level=logging.DEBUG)

def run_test_cases():
    base_url = "http://localhost:8000/submit_problem/"
    
    # Test cases with different scenarios
    test_cases = [
        # Test Case 1: Initial Marketing Strategy
        {
            "parent_id": "parent_marketing_1",
            "problem_statement": "Develop a digital marketing strategy for a new mobile app launch"
        },
        
        # Test Case 2: Similar Marketing Problem (should reuse agent)
        {
            "parent_id": "parent_marketing_2",
            "problem_statement": "Create marketing strategy for mobile application launch campaign"
        },
        
        # Test Case 3: Different Domain - Data Analysis
        {
            "parent_id": "parent_data_1",
            "problem_statement": "Analyze customer behavior patterns in e-commerce data"
        },
        
        # Test Case 4: Similar Data Analysis Problem (should reuse agent)
        {
            "parent_id": "parent_data_2",
            "problem_statement": "Study e-commerce customer behavior and shopping patterns"
        },
        
        # Test Case 5: Completely Different Domain - Technical
        {
            "parent_id": "parent_tech_1",
            "problem_statement": "Design a system architecture for a cloud-based application"
        },
        
        # Test Case 6: Similar Technical Problem (should reuse agent)
        {
            "parent_id": "parent_tech_2",
            "problem_statement": "Create cloud application system architecture design"
        }
    ]
    
    print("\n=== Starting Integration Tests ===\n")
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {idx}:")
        print(f"Parent ID: {test_case['parent_id']}")
        print(f"Problem Statement: {test_case['problem_statement']}")
        
        try:
            response = requests.post(base_url, json=test_case)
            result = response.json()
            
            print("\nResponse:")
            print(f"Status Code: {response.status_code}")
            print(f"Message: {result.get('message', 'No message')}")
            print(f"Agent ElementId: {result.get('agent', {}).get('elementId', 'No elementId')}")
            print(f"Agent Role: {result.get('agent', {}).get('role', 'No role')}")
            
            # Add a small delay between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in test case {idx}: {str(e)}")
        
        print("\n" + "="*50)

def verify_results():
    """
    Print instructions for manual verification of results
    """
    print("\n=== Verification Steps ===")
    print("\n1. Check Neo4j Browser (http://localhost:7474):")
    print("   Run this Cypher query:")
    print("   MATCH (p)-[r:DEPENDS_ON]->(c) RETURN p, r, c;")
    print("\n   Expected results:")
    print("   - Should see 6 DummyAgent nodes")
    print("   - Should see 3 Agent nodes (one for each domain)")
    print("   - Should see 6 DEPENDS_ON relationships")
    
    print("\n2. Check ChromaDB:")
    print("   Run list_chroma.py to verify stored agents")
    print("   Expected results:")
    print("   - Should see 3 unique agents")
    print("   - Each agent should have proper metadata")

if __name__ == "__main__":
    print("\nStarting Integration Tests...")
    print("Make sure your FastAPI server is running (uvicorn main:app --reload)")
    
    input("\nPress Enter to continue...")
    
    try:
        run_test_cases()
        verify_results()
        
    except Exception as e:
        print(f"\nTest suite failed: {str(e)}")
    
    print("\nTests completed. Please verify results in Neo4j and ChromaDB.")
