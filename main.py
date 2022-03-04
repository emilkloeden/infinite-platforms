import game


def restart():
    main(first_run=False)

def main(first_run=False):
    game.Game(first_run)

if __name__ == "__main__":
    main(first_run=True)