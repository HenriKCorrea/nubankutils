import json
import click

from nubankutils.utils import NubankEx, preprocess_detailed_bills


@click.command()
@click.option(
    "--user", "user", prompt="CPF", required=True, help="Identificador do usuário."
)
@click.option(
    "--password",
    prompt="Senha",
    hide_input=True,
    required=True,
    help="Senha do usuário.",
)
@click.option(
    "--bills",
    type=int,
    default=1,
    help="Quantas faturas devem ser baixadas a partir da fatura em aberto.",
)
def main(
    user: str,
    password: str,
    bills: int,
):
    nu = NubankEx()

    try:
        nu.authenticate_with_qr_code(user, password)
        click.echo("Usuário autenticado com sucesso!")
        past_bills = nu.get_past_bills(bills)
        detailed_bills = preprocess_detailed_bills(nu.get_detailed_bills(past_bills))
        #TODO: Salvar as faturas em um arquivo .csv
        json.dump(
            detailed_bills,
            open("past_bills.json", "w"),
        )
        click.echo("Faturas salvas com sucesso!")

    finally:
        if nu.is_authenticated():
            click.echo("Revogando token de acesso.")
            nu.revoke_token()


if __name__ == "__main__":
    main()
