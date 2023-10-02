import copy
from pynubank import Nubank
from qrcode.main import QRCode


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


def preprocess_detailed_bills(bills: list, fix_amount=True):
    """Preprocessa as faturas detalhadas para facilitar a visualização.

    Args:
        bills (list): Lista de faturas detalhadas.
        fix_amount (bool, optional): Converte o valor da compra de centavos para reais. Defaults to True.

    Returns:
        list: Lista de faturas detalhadas preprocessadas.
    """

    def preprocess_line_item(lineItem: dict):
        result = copy.deepcopy(lineItem)
        if fix_amount and "amount" in result and isinstance(result["amount"], int):
            result["amount"] = result["amount"] * 0.01
        return result

    def preprocess_bill(bill: dict):
        if "line_items" in bill:
            bill = copy.deepcopy(bill)
            bill["line_items"] = [
                preprocess_line_item(dict(item)) for item in bill.get("line_items", [])
            ]

        return bill

    return [preprocess_bill(bill) for bill in bills]
