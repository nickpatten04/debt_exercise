from module.debts import Debts


def output_debts():
    return Debts.build_from_api().to_json()


if __name__ == "__main__":
    [print(line) for line in output_debts()]
