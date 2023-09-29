class Summary:
    def __init__(self, data: dict) -> None:
        self.raw = data
        """Dados brutos da fatura"""

        self.due_date = str(data.get("due_date"))
        """Data limite para pagar a fatura"""

        self.close_date = str(data.get("close_date"))
        """Data de fechamento da fatura"""

        self.total_balance = int(str(data.get("total_balance")))
        """Valor total da fatura em centavos"""

        self.open_date = str(data.get("open_date"))
        """Data de abertura da fatura"""


class LineItem:
    def __init__(self, data: dict) -> None:
        self.raw = data
        """Dados brutos da compra"""

        self.amount = int(str(data.get("amount")))
        """Valor da compra em centavos"""

        self.index = int(str(data.get("index")))
        """Indice da parcela da compra (ex.: indice 2 de 10 parcelas)"""

        self.title = str(data.get("title"))
        """Titulo da compra"""

        self.post_date = str(data.get("post_date"))
        """Data da compra"""

        self.id = str(data.get("id"))
        """ID da compra"""

        self.category = str(data.get("category"))
        """Categoria da compra"""

        self.charges = int(str(data.get("charges")))
        """Numero de parcelas da compra"""


class DetailedBill:
    def __init__(self, data: dict) -> None:
        self.raw = data
        """Dados brutos da fatura"""

        self.summary = Summary(data.get("summary") or {})
        """Dados resumidos da fatura"""

        self.line_items = [LineItem(item) for item in data.get("line_items") or []]
        """Compras da fatura"""

