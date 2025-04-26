from reviewer import Reviewer  # Import the Reviewer class from reviewer.py

def main():
    print("Welcome to the Code Reviewer Application!")
    print("Please enter the code snippet you would like to review:")
    
    code_snippet = input("Code Snippet: ")
    
    
    reviewer = Reviewer()
    feedback = reviewer.analyze_code(code_snippet)
    print("Feedback:")
    print(feedback)
    
    print("Thank you for using the Code Reviewer Application!")

if __name__ == "__main__":
    main()