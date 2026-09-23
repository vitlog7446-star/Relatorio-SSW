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

            # ==========================================================
            # LOGIN
            # ==========================================================

            page.locator('[id="1"]').fill(dominio)
            page.locator('[id="2"]').fill(cpf)
            page.locator('[id="3"]').fill(user)
            page.locator('[id="4"]').fill(senha)

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

            # Aguarda o processamento do login
            page.wait_for_timeout(5000)

            print("URL depois do login:", page.url)
            print("Título:", page.title())

            # ==========================================================
            # OPÇÃO 063
            # ==========================================================

            campo_opcao = page.locator('[id="3"]').last
            campo_opcao.wait_for(state="visible", timeout=60000)

            campo_opcao.fill("063")

            print("Valor do campo:", campo_opcao.input_value())

            campo_opcao.press("Enter")

            # Aguarda a abertura da tela 063
            page.wait_for_timeout(5000)

            print("URL após Enter:", page.url)
            print("Título após Enter:", page.title())

            # ==========================================================
            # DIAGNÓSTICO DAS PÁGINAS
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

            # ==========================================================
            # PRÓXIMO TESTE
            # CLICAR NO ► DA PÁGINA 1
            # ==========================================================

            if len(contexto.pages) > 1:

                pagina_063 = contexto.pages[1]

                print("\n========================================")
                print("TESTANDO BOTÃO ► DA PÁGINA 1")
                print("========================================")

                print("URL da página 063:", pagina_063.url)

                # Localiza os links da página
                links = pagina_063.locator("a")

                print("Quantidade de links:", links.count())

                for i in range(links.count()):

                    link = links.nth(i)

                    try:
                        texto = link.inner_text().strip()
                    except:
                        texto = ""

                    print(
                        f"LINK {i} "
                        f"id={link.get_attribute('id')} "
                        f"texto={texto} "
                        f"onclick={link.get_attribute('onclick')}"
                    )

                # Localiza o botão pelo texto ►
                botao = pagina_063.get_by_role("link", name="►")

                print("Quantidade de botões ►:", botao.count())

                if botao.count() > 0:

                    print("Botão ► encontrado.")

                    # Tenta observar a requisição feita pelo SSW
                    with pagina_063.expect_response(
                        "**/bin/**",
                        timeout=30000
                    ) as resposta_063:

                        botao.click()

                    resposta_botao = resposta_063.value

                    print("\nRESPOSTA DO BOTÃO ►")
                    print("STATUS:", resposta_botao.status)
                    print("URL:", resposta_botao.url)
                    print(
                        "TIPO:",
                        resposta_botao.headers.get("content-type")
                    )

                    print(
                        "TAMANHO:",
                        len(resposta_botao.body())
                    )

                    print("CONTEÚDO:")
                    print(resposta_botao.text()[:5000])

                else:

                    print("ERRO: botão ► não encontrado.")

                # Aguarda o processamento
                pagina_063.wait_for_timeout(5000)

                print("\n========================================")
                print("ESTADO DA PÁGINA 063 APÓS CLICAR")
                print("========================================")

                print("URL:", pagina_063.url)
                print("Título:", pagina_063.title())

                print("TEXTO:")
                print(
                    pagina_063.locator("body").inner_text()[:5000]
                )

            else:

                print("\nERRO: a página 063 não foi aberta.")

        finally:
            navegador.close()


if __name__ == "__main__":
    baixar_relatorio()
