import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine
from backend.models import Base, Problem
import json

# Create tables
Base.metadata.create_all(bind=engine)

def seed_problems():
    db = SessionLocal()
    
    # Check if problems already exist
    existing_problems = db.query(Problem).count()
    if existing_problems > 0:
        print(f"Database already has {existing_problems} problems. Skipping seed.")
        db.close()
        return
    
    problems = [
        {
            "title": "Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
            "input_format": "First line: array of integers separated by commas\nSecond line: target integer",
            "output_format": "Two integers representing the indices, separated by space",
            "test_cases": json.dumps([
                {"input": "[2,7,11,15]\n9", "output": "0 1"},
                {"input": "[3,2,4]\n6", "output": "1 2"},
                {"input": "[3,3]\n6", "output": "0 1"}
            ]),
            "difficulty": "easy"
        },
        {
            "title": "Reverse String",
            "description": "Write a function that reverses a string. The input string is given as an array of characters s.\n\nYou must do this by modifying the input array in-place with O(1) extra memory.",
            "input_format": "Array of characters",
            "output_format": "Reversed array of characters",
            "test_cases": json.dumps([
                {"input": "['h','e','l','l','o']", "output": "['o','l','l','e','h']"},
                {"input": "['H','a','n','n','a','h']", "output": "['h','a','n','n','a','H']"}
            ]),
            "difficulty": "easy"
        },
        {
            "title": "Valid Parentheses",
            "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.",
            "input_format": "A string containing only parentheses characters",
            "output_format": "true if valid, false otherwise",
            "test_cases": json.dumps([
                {"input": "()", "output": "true"},
                {"input": "()[]{}", "output": "true"},
                {"input": "(]", "output": "false"},
                {"input": "([)]", "output": "false"},
                {"input": "{[]}", "output": "true"}
            ]),
            "difficulty": "easy"
        },
        {
            "title": "Maximum Subarray",
            "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.\n\nA subarray is a contiguous part of an array.",
            "input_format": "Array of integers",
            "output_format": "Single integer representing the maximum sum",
            "test_cases": json.dumps([
                {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
                {"input": "[1]", "output": "1"},
                {"input": "[5,4,-1,7,8]", "output": "23"}
            ]),
            "difficulty": "medium"
        },
        {
            "title": "Binary Tree Inorder Traversal",
            "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.\n\nInorder traversal visits nodes in this order: left subtree, root, right subtree.",
            "input_format": "Binary tree represented as array (level order)",
            "output_format": "Array of integers in inorder sequence",
            "test_cases": json.dumps([
                {"input": "[1,null,2,3]", "output": "[1,3,2]"},
                {"input": "[]", "output": "[]"},
                {"input": "[1]", "output": "[1]"}
            ]),
            "difficulty": "medium"
        }
    ]
    
    for problem_data in problems:
        problem = Problem(**problem_data)
        db.add(problem)
    
    db.commit()
    print(f"Successfully seeded {len(problems)} problems!")
    db.close()

if __name__ == "__main__":
    seed_problems()
