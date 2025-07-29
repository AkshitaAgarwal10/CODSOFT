def add(x, y): return x + y
def subtract(x, y): return x - y
def multiply(x, y): return x * y
def divide(x, y): return x / y if y != 0 else "\033[91mError: Can't divide by zero!\033[0m"
def power(x, y): return x ** y

def show_history(history):
    print("\n\033[95m📊 YOUR MATH JOURNEY:\033[0m")
    for i, calc in enumerate(history, 1):
        print(f"{i}. {calc}")

def main():
    history = []
    print("\n\033[96m===✨ WELCOME TO CALC CITY! ✨===")
    print("Where numbers meet magic! 🌟\033[0m")

    while True:
        print("\n\033[93mChoose your math adventure:\033[0m")
        print("1. Add ➕")
        print("2. Subtract ➖")
        print("3. Multiply ✖️")
        print("4. Divide ➗")
        print("5. Power Up 📈")
        print("6. Quit 🚪")

        choice = input("\033[94mYour move (1-6): \033[0m").strip()

        if choice == '6':
            print("\033[96mThanks for visiting Calc City! Come back soon! 👋\033[0m")
            break

        if choice not in ['1','2','3','4','5']:
            print("\033[91m🚫 Oops! Pick between 1-6\033[0m")
            continue

        try:
            x = float(input("First number: "))
            y = float(input("Second number: "))
        except ValueError:
            print("\033[91m💢 Numbers only please!\033[0m")
            continue

        ops = {
            '1': ('➕', add),
            '2': ('➖', subtract),
            '3': ('✖️', multiply),
            '4': ('➗', divide),
            '5': ('📈', power)
        }
        symbol, operation = ops[choice]
        result = operation(x, y)

        equation = f"{x} {symbol} {y} = {result}"
        print(f"\033[92m🎉 Ta-da! {equation}\033[0m")
        history.append(equation)

        show_history(history)

if __name__ == "__main__":
    main()

