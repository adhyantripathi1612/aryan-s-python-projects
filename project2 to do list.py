<<<<<<< HEAD
task = []

def start():
    print('this is the to do list ')
    print('what do you want to do?')
    print('1. add a task')
    print('2. view tasks')
    print('3. exit')
    
def add_task():
    task_name = input('enter the task: ')
    task.append(task_name)
    print('task added successfully')



def view_tasks():
    if len(task) == 0:
        print('no tasks to show')
    else:
        print('your tasks are: ')
        for i in range(len(task)):
            print(f'{i+1}. {task[i]}')

def main():
    while True:
        start()
        choice = input('enter your choice: ')
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            print('goodbye!')
            break
        else:
            print('invalid choice, please try again')

if __name__ == '__main__':
    main()




=======
task = []

def start():
    print('this is the to do list ')
    print('what do you want to do?')
    print('1. add a task')
    print('2. view tasks')
    print('3. exit')
    
def add_task():
    task_name = input('enter the task: ')
    task.append(task_name)
    print('task added successfully')



def view_tasks():
    if len(task) == 0:
        print('no tasks to show')
    else:
        print('your tasks are: ')
        for i in range(len(task)):
            print(f'{i+1}. {task[i]}')

def main():
    while True:
        start()
        choice = input('enter your choice: ')
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            print('goodbye!')
            break
        else:
            print('invalid choice, please try again')

if __name__ == '__main__':
    main()




>>>>>>> 3f7e543e3da3f338aae73938f5603f57c2c87d25
