from playwright.sync_api import sync_playwright
import time
from pathlib import Path
import os

pasta_projeto = Path(__file__).resolve().parent
arquivo_csv = pasta_projeto / "relatorio.csv"

dominio = os.getenv("SSW_DOMINIO")
cpf = os.getenv("SSW_CPF")
user = os.getenv("SSW_USUARIO")
senha = os.getenv("SSW_SENHA")


def baixar_relatorio():
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=True)

        try:
            contexto = navegador.new_context()
            page = contexto.new_page()

            page.goto(
                "https://sistema.ssw.inf.br",
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.locator('[id="1"]').fill(dominio)
            page.locator('[id="2"]').fill(cpf)
            page.locator('[id="3"]').fill(user)
            page.locator('[id="4"]').fill(senha)

            # Login
            page.get_by_role("link", name="►").click()

            # Espera o AJAX do login
            page.wait_for_timeout(5000)

            print("URL depois do login:", page.url)
            print("Título:", page.title())

            # ESC - teste que fizemos
            page.keyboard.press("Escape")

            page.wait_for_timeout(1000)

            # Campo da opção
            campo_opcao = page.locator('[id="3"]').last
            campo_opcao.wait_for(state="visible", timeout=60000)

            # TESTE: preencher 063 sem clicar antes
            campo_opcao.fill("063")

            print("Valor do campo:", campo_opcao.input_value())

            # TESTE: pressionar Enter
            campo_opcao.press("Enter")

            # Espera o SSW processar o Enter
            page.wait_for_timeout(3000)

            print("URL após Enter:", page.url)
            print("Título após Enter:", page.title())

            # Verifica quantas páginas existem
            print("Número de páginas:", len(contexto.pages))

            for i, pagina in enumerate(contexto.pages):
                print(f"Página {i}:", pagina.url)

            # Verifica os inputs que ficaram na página
            inputs = page.locator("input")
            print("Quantidade de inputs:", inputs.count())

            for i in range(inputs.count()):
                elemento = inputs.nth(i)

                print(
                    f"INPUT {i} "
                    f"id={elemento.get_attribute('id')} "
                    f"name={elemento.get_attribute('name')} "
                    f"type={elemento.get_attribute('type')} "
                    f"value={elemento.input_value()}"
                )

        finally:
            navegador.close()


if __name__ == "__main__":
    baixar_relatorio()
