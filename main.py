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

            # Preenche os dados de login
            page.locator('[id="1"]').fill(dominio)
            page.locator('[id="2"]').fill(cpf)
            page.locator('[id="3"]').fill(user)
            page.locator('[id="4"]').fill(senha)

            # Login
            with page.expect_response("**/bin/ssw0422") as resposta_login:
                page.get_by_role("link", name="►").click()

            resposta = resposta_login.value

            print("STATUS DO LOGIN:", resposta.status)
            print("URL DA RESPOSTA:", resposta.url)
            print("TIPO:", resposta.headers.get("content-type"))

            print("TAMANHO DA RESPOSTA:", len(resposta.body()))

            texto_resposta = resposta.text()

            print("CONTEÚDO DA RESPOSTA:")
            print(texto_resposta[:5000])

            # Aguarda o processamento do SSW
            page.wait_for_timeout(5000)

            print("URL depois do login:", page.url)
            print("Título:", page.title())

            # Campo da opção
            campo_opcao = page.locator('[id="3"]').last
            campo_opcao.wait_for(state="visible", timeout=60000)

            # Preenche a opção 063
            campo_opcao.fill("063")

            print("Valor do campo:", campo_opcao.input_value())

            # Pressiona Enter
            campo_opcao.press("Enter")

            # Aguarda o SSW abrir/processar a opção
            page.wait_for_timeout(5000)

            print("URL após Enter:", page.url)
            print("Título após Enter:", page.title())

            # ==========================================================
            # DIAGNÓSTICO DAS PÁGINAS ABERTAS
            # ==========================================================

            print("\n========================================")
            print("PÁGINAS ABERTAS")
            print("========================================")

            print("Número de páginas:", len(contexto.pages))

            for i, pagina in enumerate(contexto.pages):

                print(f"\n--- PÁGINA {i} ---")

                print("URL:", pagina.url)
                print("Título:", pagina.title())

                print("\nINPUTS:")

                inputs = pagina.locator("input")

                print("Quantidade de inputs:", inputs.count())

                for j in range(inputs.count()):

                    elemento = inputs.nth(j)

                    try:
                        valor = elemento.input_value()
                    except:
                        valor = "NÃO FOI POSSÍVEL LER"

                    print(
                        f"INPUT {j} "
                        f"id={elemento.get_attribute('id')} "
                        f"name={elemento.get_attribute('name')} "
                        f"type={elemento.get_attribute('type')} "
                        f"value={valor}"
                    )

                print("\nTEXTO DA PÁGINA:")

                try:
                    texto = pagina.locator("body").inner_text()
                    print(texto[:5000])
                except Exception as erro:
                    print("Não foi possível ler o texto:", erro)

        finally:
            navegador.close()


if __name__ == "__main__":
    baixar_relatorio()
