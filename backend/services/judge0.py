import asyncio
import random

# Mock Judge0 service - replace with actual Judge0 API integration
async def submit_code_to_judge0(code: str, language: str):
    # Simulate API call delay
    await asyncio.sleep(1)
    
    # Mock response based on simple heuristics
    if len(code.strip()) < 10:
        return {
            "status": "compilation_error",
            "message": "Code too short"
        }
    
    # Simple check for common patterns
    if "return" in code or "print" in code:
        # 80% chance of acceptance for code with return/print
        if random.random() < 0.8:
            return {
                "status": "accepted",
                "message": "All test cases passed"
            }
        else:
            return {
                "status": "wrong_answer",
                "message": "Failed on test case 2"
            }
    
    return {
        "status": "runtime_error",
        "message": "Runtime error occurred"
    }

# Language ID mapping for Judge0
LANGUAGE_IDS = {
    "python": 71,
    "javascript": 63,
    "java": 62,
    "cpp": 54,
    "c": 50
}
