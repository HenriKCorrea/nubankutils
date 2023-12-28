import copy
import csv
from datetime import datetime
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
        """Autentica o usuário utilizando o QRCode.

        Args:
            cpf (str): CPF do usuário.
            password (str): Senha do usuário.
            uuid (str, optional): UUID do QRCode. Defaults to None.

        Raises:
            Exception: Falha ao autenticar o usuário utilizando QRCode.
        """

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
        if not self.is_authenticated():
            raise Exception(
                """Falha ao autenticar o usuário utilizando QRCode.
Verifique seu usuário, senha e se o QRCode foi escaneado corretamente."""
            )

    def get_past_bills(self, past_count: int = 1):
        """Retorna as faturas anteriores a partir da fatura em aberto.

        Args:
            past_count (int, optional): Quantidade de faturas anteriores a serem retornadas. Defaults to 1.

        Raises:
            Exception: Não foi possível encontrar a fatura em aberto.

        Returns:
            list: Lista de faturas.
        """

        bill_list = list(self.get_bills())
        try:
            open_bill_index = [
                index
                for index, item in enumerate(bill_list)
                if dict(item).get("state") == "open"
            ].pop()
        except Exception as e:
            raise Exception(f"Não foi possível encontrar a fatura em aberto: {e}")

        filtered_bill_list = bill_list[open_bill_index : open_bill_index + past_count]

        return filtered_bill_list

    def get_detailed_bills(self, bills: list):
        """Retonar as faturas com detalhe das compras.

        Args:
            bills (list): Lista de faturas.

        Returns:
            list: Lista de faturas detalhadas."""

        detail_bill_list = [
            dict(self.get_bill_details(bill_summary)) for bill_summary in bills
        ]

        return detail_bill_list

    def generate_str_timestamp(self):
        """Gera uma string timestamp incluindo nome do usuario.

        Returns:
            str: Timestamp gerado no formato <NOME>_<DATA_HORA>.
        """

        return f"{dict(self.get_customer()).get('preferred_name')}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"


def preprocess_detailed_bills(bills: list, fix_amount=False, index_increment=False):
    """Preprocessa as faturas detalhadas para facilitar a visualização.

    Args:
        bills (list): Lista de faturas detalhadas.
        fix_amount (bool, optional): Converte o valor da compra de centavos para reais e inverte sinal. Defaults to False.
        index_increment (bool, optional): Incrementa a parcela atual por + 1. Defaults to False.

    Returns:
        list: Lista de faturas detalhadas preprocessadas.
    """

    def preprocess_line_item(lineItem: dict):
        result = copy.deepcopy(lineItem)
        if fix_amount and "amount" in result and isinstance(result["amount"], int):
            result["amount"] = result["amount"] / -100
        if index_increment and "index" in result and isinstance(result["index"], int):
            result["index"] = result["index"] + 1
        return result

    def preprocess_bill(bill: dict):
        if "line_items" in bill:
            bill = copy.deepcopy(bill)
            bill["line_items"] = [
                preprocess_line_item(item) for item in bill.get("line_items", [])
            ]

        return bill

    return [preprocess_bill(dict(bill).get("bill") or bill) for bill in bills]


def extract_line_items_from_detailed_bills(bills: list, values: list):
    """Extrai os itens de compra das faturas detalhadas.

    Args:
        bills (list): Lista de faturas detalhadas.
        values (list): Lista de valores a serem extraídos. Ex: ["amount", "title"]

    Returns:
        list: Lista de itens de compra.
    """

    def postProcess(key: str, value):
        result = value
        if key == "amount":
            result = str(result).replace(".", ",")
        return result

    extracted_items = []

    for bill in bills:
        bill_data = dict(bill).get("bill", bill)
        line_items = dict(bill_data).get("line_items", [])

        for item in line_items:
            extracted_items.append(
                [postProcess(key, dict(item).get(key, "")) for key in values]
            )

    return extracted_items


def create_csv_file(csv_file_path: str, rows: list):
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sep=,"])
        writer.writerows(rows)
