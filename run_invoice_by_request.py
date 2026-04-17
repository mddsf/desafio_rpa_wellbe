import sys
import os
from src.invoice_challenge.invoice_request import InvoiceChallengeRequest
from src.config import logger


def format_list(data: list):
    list_formatted = []
    for item in data:
        tmp = item['invoice'].split("/")[-1]
        tmp = tmp.split(".")[0]
        list_formatted.append(tmp)

    return list_formatted

def interactive_mode(options: list):
    print("Modo Interativo")
    print("Opções:")
    choices = []
    choice = None
    options_list = format_list(options)
    try:
        options_list.sort(key=int)
    except:
        pass
    while choice != 0:
        op_list = ['0']
        for i, option in enumerate(options_list):
            print(f"{i+1} - invoice-{option}")
            op_list.append(str(i+1))
        if len(choices) > 0:
            print("L - Limpar")
            op_list.append("L")
        print("0 - Finalizar escolhas")

        choice = input("Escolha uma opção: ")
        if choice.upper() not in op_list:
            print("Opção inválida. Tente novamente.")
            continue

        if choice == "0":
            print("Escolhas finalizadas")
            return choices
        elif choice.upper() == "L":
            print("Resetando escolhas")
            choices = []
            options_list = format_list(options)
            continue
        else:
            print(f"Opção {choice} selecionada")
            choices.append(choice)
            print(f"Escolhas: {choices}")
            del options_list[int(choice)-1]

def main_invoice(input_str):
    logger.info("Iniciando extração de invoices por requisição")
    ic = InvoiceChallengeRequest()
    ic.get_invoices()
    
    if input_str.lower() == "i":
        logger.info("Iniciando modo interativo")
        choices = interactive_mode(ic.invoices)
        if len(choices) == 0:
            logger.info("Nenhuma invoice selecionada, saindo...")
            sys.exit(0)
    else:
        choices = input_str.split(",")
        logger.info("Verificando se invoices existem nos dados")
        ic.check_invoice_list(choices)
    
    invoices_files = []
    for invoice_number in choices:
        logger.info(f"Baixando invoice {invoice_number}")
        img_path = ic.download_invoice(invoice_number)
        invoices_files.append(img_path)
    
    logger.info("Extraindo dados da invoice (caso você possua tesseract instalado)")
    extra_data_file = ic.export_to_excel(invoices_files)
    if extra_data_file is not None:
        invoices_files.append(extra_data_file)

    logger.info("Gerando arquivo zip com as invoices baixadas")
    zip_path = ic.zip_invoices(invoices_files)
    logger.info(f"Arquivo zip gerado com sucesso!\n{zip_path}")

    logger.info("Removendo arquivos temporários")
    for file in invoices_files:
        os.remove(file)

    logger.info("Desafio finalizado!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py 2,4 -> lista de invoices separados por vírgula")
        print("Uso: python script.py i -> 'i' modo interativo")
        sys.exit(1)
    main_invoice(sys.argv[1])