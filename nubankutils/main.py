import click

from nubankutils.utils import (
    NubankEx,
    create_csv_file,
    extract_line_items_from_detailed_bills,
    preprocess_detailed_bills,
)


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
        detailed_bills = preprocess_detailed_bills(
            nu.get_detailed_bills(past_bills), fix_amount=True, index_increment=True
        )
        # Purcharces contains data from bills sorted by date
        # The first row is the header to export into CSV file
        purcharses = [
            [
                "Data",
                "Categoria",
                "Descrição",
                "Comentário",
                "Valor",
                "Parcelas",
                "Parcela",
            ],
            *sorted(
                extract_line_items_from_detailed_bills(
                    detailed_bills,
                    [
                        "post_date",
                        "category",
                        "title",
                        "comment",
                        "amount",
                        "charges",
                        "index",
                    ],
                ),
                reverse=True,
                key=lambda x: x[0],
            ),
        ]
        create_csv_file(f"nubank_card_{nu.generate_str_timestamp()}.csv", purcharses)
        click.echo("Faturas salvas com sucesso!")

    finally:
        if nu.is_authenticated():
            click.echo("Revogando token de acesso.")
            nu.revoke_token()


if __name__ == "__main__":
    main()
