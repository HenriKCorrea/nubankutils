Extrato de Cartão de Crédito - Análise Financeira em Planilha

Este projeto Python está sendo desenvolvido como objetivo de facilitar a validação, extração de informações e organização do extrato do cartão de crédito em planilhas mensais e anuais para proporcionar uma análise financeira eficaz e melhorar o controle das suas finanças pessoais.

Funcionalidades

* Validação de Extrato: Este aplicativo permite a importação e validação de extratos de cartão de crédito, garantindo a integridade dos dados.

* Extração de Dados: O projeto extrai informações cruciais do extrato, incluindo data da transação, descrição, valor e categoria de gastos.

* Categorização Automática: As transações são categorizadas automaticamente com base na descrição da transação, economizando tempo na organização.

* Organização em Planilhas Mensais e Anuais: Os dados são organizados em planilhas mensais e anuais para oferecer uma visão clara dos gastos ao longo do tempo.

* Análise Mensal e Anual: O aplicativo gera resumos mensais e anuais dos seus gastos, mostrando o total gasto em cada categoria e o saldo disponível.

* Exportação para Planilhas: Você pode exportar os dados diretamente para planilhas, como Excel ou CSV, para uma análise mais detalhada.


Requisitos
Python 3.11


Contribuições
Contribuições são bem-vindas! Se você deseja melhorar ou adicionar recursos a este projeto, sinta-se à vontade para enviar um pull request.

Aviso Legal
Este projeto é apenas para fins educacionais e pessoais. Não é uma ferramenta financeira oficial e não deve ser usado para tomar decisões financeiras críticas. Sempre consulte um profissional financeiro antes de tomar decisões importantes relacionadas às suas finanças pessoais.

Autor
Este projeto foi desenvolvido por @HenriKCorrea e @rafaloliveira.


# Dicas para debug

## Armazenar credencias em uma variável de shell

```powershell
$code = Get-Credential -Verbose:$false
poetry run nubankutils --user="$($code.GetNetworkCredential().Username)" --password="$($code.GetNetworkCredential().Password)"
```