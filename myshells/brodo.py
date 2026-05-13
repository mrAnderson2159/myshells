import click
from typing import Union


def compute(litri_brodo: float, grammi_carne: int, grammi_pollo: int) -> dict[str, int]:
    bottiglie = litri_brodo / 0.5

    porzione_carne = grammi_carne / bottiglie
    porzione_pollo = grammi_pollo / bottiglie

    return {"carne": round(porzione_carne), "pollo": round(porzione_pollo)}


@click.command()
@click.option("-l", "--litri", type=float, default=None, help="Litri di brodo")
@click.option("-c", "--carne", type=int, default=None, help="Grammi di carne")
@click.option("-p", "--pollo", type=int, default=None, help="Grammi di pollo")
def main(litri, carne, pollo):
    # Se mancano parametri → usa i prompt
    if litri is None:
        litri = float(input("Inserisci la quantità di litri di brodo: "))

    if carne is None:
        carne = int(input("Inserisci la quantità di carne (in grammi): "))

    if pollo is None:
        pollo = int(input("Inserisci la quantità di pollo (in grammi): "))

    result = compute(litri, carne, pollo)

    print()
    print(f"Carne: {result['carne']} g")
    print(f"Pollo: {result['pollo']} g")
    print("------------------")
    print(f"Totale: {result['carne'] + result['pollo']} g")
    print()


if __name__ == "__main__":
    main()
