import atexit

def my_exit_function(some_argument):
    # Your exit code goes here
    print(some_argument)


if __name__ == '__main__':
    atexit.register(my_exit_function, 'some argument', )




    