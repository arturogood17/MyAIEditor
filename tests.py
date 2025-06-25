from functions.get_files import get_files_info

def main():

    print(get_files_info("calculator", "."))
    print()
    print(get_files_info("calculator", "pkg"))
    print()
    print(get_files_info("calculator", "/bin"))
    print()
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()