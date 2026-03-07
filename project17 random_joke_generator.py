import pyjokes
import time

def get_joke(category='neutral'):
    try:
        joke = pyjokes.get_joke(category=category)
        return joke
    except Exception as e:
        return f"Error: {e}"

def main():
    print("RANDOM JOKE GENERATOR")
    print("=" * 30)
    print("1. Get a joke")
    print("2. Exit")
    print("=" * 30)
    
    while True:
        choice = input("Enter your choice (1-2): ").strip()
        
        if choice == "1":
            print("\nSelect Joke Category:")
            print("a. Programming (Neutral)")
            print("b. Chuck Norris (Programming)")
            print("c. Any")
            
            cat_choice = input("Enter category (a/b/c): ").strip().lower()
            
            category = 'neutral'
            if cat_choice in ['b', 'chuck', 'chuck norris']:
                category = 'chuck'
            elif cat_choice in ['c', 'any', 'all']:
                category = 'all'
                
            print("\nYour joke is loading...")
            time.sleep(2)
            joke = get_joke(category)
            print("\n" + joke)
            print("\n" + "=" * 30)
        elif choice == "2":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice! Please select 1-2.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()