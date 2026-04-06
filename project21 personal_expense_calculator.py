import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_PATH = 'expenses.csv'

def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_csv(FILE_PATH)
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
            return df
        except Exception as e:
            print(f"Error loading data: {e}. Starting with a fresh list.")
    
    return pd.DataFrame(columns=['date', 'amount', 'category', 'description'])

def save_data(df):
    try:
        df.to_csv(FILE_PATH, index=False)
    except Exception as e:
        print(f"Error saving data: {e}")

def get_expense_input():
    print('='*30)
    print('ADD NEW EXPENSE')
    date_str = input('Enter the date (DD-MM-YYYY) [Leave empty for today]-: ')
    if not date_str:
        date = pd.Timestamp.now().normalize()
    else:
        try:
            date = pd.to_datetime(date_str, dayfirst=True)
        except ValueError:
            print("Invalid date format. Using today's date.")
            date = pd.Timestamp.now().normalize()

    try:
        amount = float(input('Enter the amount-: '))
    except ValueError:
        print('Invalid amount. Please enter a number.')
        return None
        
    category = input('Enter the category (entertainment, food, shopping, transport, etc.)-: ').lower()
    description = input('Enter the description-: ')
    
    return {'date': date, 'amount': amount, 'category': category, 'description': description}

def view_expenses(df):
    if df.empty:
        print("\nNo expenses recorded yet.")
        return
    
    print('\n' + '='*30)
    view_df = df.sort_values(by='date', ascending=False).copy()
    view_df['date'] = view_df['date'].dt.strftime('%d-%m-%Y')
    print(view_df.to_string(index=True))
    print('='*30)
    print(f"Total Expenses: {df['amount'].sum():.2f}")

def delete_expense(df):
    if df.empty:
        print("\nNo expenses to delete.")
        return
    
    view_expenses(df)
    try:
        idx = int(input('\nEnter the Index (leftmost column) of the expense to delete-: '))
        if idx in df.index:
            removed = df.loc[idx]
            df = df.drop(idx)
            print(f"Removed expense: {removed['description']} ({removed['amount']})")
            return df
        else:
            print("Invalid index.")
    except ValueError:
        print("Please enter a valid numeric index.")
    return df

def visualize_expenses(df):
    if df.empty:
        print("\nNo expenses to visualize.")
        return
    
    plt.style.use('ggplot')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    category_totals = df.groupby('category')['amount'].sum()
    category_totals.plot(kind='pie', ax=ax1, autopct='%1.1f%%', startangle=140, title='Breakdown by Category')
    ax1.set_ylabel('')

    daily_totals = df.groupby('date')['amount'].sum().sort_index()
    daily_totals.plot(kind='bar', ax=ax2, color='skyblue', title='Spending Trend (Daily)')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Amount')
    plt.xticks(rotation=45)

    plt.tight_layout()
    print("\nDisplaying visualization window...")
    plt.show()

def main():
    expenses_df = load_data()
    
    while True:
        print('\n' + '='*30)
        print('PERSONAL EXPENSE CALCULATOR (PANDAS VERSION)')
        print('1. Add expense')
        print('2. View expenses')
        print('3. Delete expense')
        print('4. Visualize expenses')
        print('5. Exit')
        
        choice = input('Enter your choice (1-5)-: ')

        if choice == '1':
            new_expense = get_expense_input()
            if new_expense:
                expenses_df = pd.concat([expenses_df, pd.DataFrame([new_expense])], ignore_index=True)
                save_data(expenses_df)
                print("Expense added successfully!")
        elif choice == '2':
            view_expenses(expenses_df)
        elif choice == '3':
            expenses_df = delete_expense(expenses_df)
            save_data(expenses_df)
        elif choice == '4':
            visualize_expenses(expenses_df)
        elif choice == '5':
            save_data(expenses_df)
            print("Exiting... goodbye!")
            break
        else:
            print('Invalid choice, please try again.')

if __name__ == '__main__':
    main()