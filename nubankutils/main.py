import json
import click
from qrcode.main import QRCode
from pynubank import Nubank


class NubankEx(Nubank):
    """Extensão da classe Nubank para adicionar novas funcionalidades."""

    def is_authenticated(self):
        """Verifica se o usuário está autenticado."""

        return "Authorization" in self._client._headers and isinstance(
            self._client._headers["Authorization"], str
        )

    def authenticate_with_qr_code(self, cpf, password, uuid: str | None = None):
        """Autentica o usuário utilizando o QRCode."""

        if uuid is None:
            qr_code: QRCode
            uuid, qr_code = self.get_qr_code()
            qr_code.print_ascii(invert=True)
            input(
                """Necessário autorizar o acesso pelo app do celular.
Abra o aplicaivo Nubank e acesse Perfil > Segurança > Acesso no navegador.
Após escanear o QRCode pressione enter para continuar"""
            )

        super().authenticate_with_qr_code(cpf, password, uuid)

    def get_past_bills(self, bills: int = 1):
        """Retorna as faturas anteriores a partir da fatura em aberto."""

        bill_list = list(self.get_bills())
        try:
            open_bill_index = [
                index
                for index, item in enumerate(bill_list)
                if dict(item).get("state") == "open"
            ].pop()
        except Exception as e:
            raise Exception(f"Não foi possível encontrar a fatura em aberto: {e}")

        filtered_bill_list = bill_list[open_bill_index : open_bill_index + bills]
        detail_bill_list = [
            dict(self.get_bill_details(bill_summary)).get("bill")
            for bill_summary in filtered_bill_list
        ]

        return detail_bill_list


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
        pass
        nu.authenticate_with_qr_code(user, password)
        click.echo("Usuário autenticado com sucesso")
        json.dump(nu.get_past_bills(bills), open("past_bills.json", "w"))
        click.echo("Faturas salvas com sucesso")

    finally:
        if nu.is_authenticated():
            click.echo("Revogando token de acesso.")
            nu.revoke_token()


if __name__ == "__main__":
    main()
