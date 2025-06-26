from functions.get_content import get_file_content

def main():

    print(get_file_content("calculator", "lorem.txt"))
    print()
    print(get_file_content("calculator", "main.py"))
    print()
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()
    print(get_file_content("calculator", "/bin/cat"))

if __name__ == "__main__":
    main()