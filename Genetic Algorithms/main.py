import geneticAlgs as ga

def print_menu():
    menu = """================================\n
           MENU\n
               ================================\n
               1 - Genetic Knapsack
               9 - Exit                        \n
               ================================\n
           Enter a choice and press enter:"""
    print(menu)

def printAnswer(result, algType):
    print('With a maximum weight of {}. The {} algorithm recommends you take the following items:'.format(result[1], algType))

    totalWeight = 0
    totalValue = 0

    for row in result[2]:
        totalWeight += int(row[1])
        totalValue += int(row[2])
        print(row)

    print('\nWhich results in a total weight of {} and a total value of {}\n\n'.format(totalWeight, totalValue))


def menu():

    print_menu()
    user_input = 0

    while user_input != 9:
        
        user_input = int(input())

        # Genetic Knapsack
        if user_input == 1:
            print('Running the Genetic Knapsack Algorithm')
            print("What is the name of the file in the cases folder that you want to use? (No extension)")
            user_input = input()
            printAnswer(ga.genKnapRunner(user_input), "Genetic Knapsack")

        # Exit
        elif user_input == 9:
            print('Exiting...')
            break
        else:
            print('Response not recognized, please enter your option again')
        print("\nPress enter to continue...")
        clutter = input()
        print('\n\n\n\n\n\n')
        print_menu()

# Run Menu
menu()
