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
            page.goto("https://sistema.ssw.inf.br",
                      wait_until="domcontentloaded",
                      timeout=60000)

            page.locator('[id="1"]').fill(dominio)
            page.locator('[id="2"]').fill(cpf)
            page.locator('[id="3"]').fill(user)
            page.locator('[id="4"]').fill(senha)


            botao_login = page.get_by_role("link", name="►")

            print("HTML do botão login:")
            print(botao_login.evaluate("(el) => el.outerHTML"))
            
            botao_login.click()
            
            page.wait_for_timeout(3000)
            
            print("URL depois do login:", page.url)
            print("Título:", page.title())

            campo_opcao = page.locator('[id="3"]').last
            campo_opcao.wait_for(state="visible", timeout=60000)
            
            campo_opcao.click()
            campo_opcao.fill("063")
            
            print("Valor do campo:", campo_opcao.input_value())
            
            # Força o evento onchange usado pelo SSW
            campo_opcao.dispatch_event("change")

            print("Existe doOption?:", page.evaluate(
            "() => typeof doOption"))

            print("Valor f3:", page.locator('[name="f3"]').input_value())
            
            page.wait_for_timeout(5000)
            
            print("Depois do change:", page.url)
            print("Número de páginas:", len(contexto.pages))
            
            for i, pagina in enumerate(contexto.pages):
                print(f"Página {i}: {pagina.url}")
            
            op063 = page
          
            inputs = page.locator("input")
            
            print("Quantidade de inputs:", inputs.count())
            
            for i in range(inputs.count()):
                elemento = inputs.nth(i)
            
                print(
                    "INPUT",
                    i,
                    "id=", elemento.get_attribute("id"),
                    "name=", elemento.get_attribute("name"),
                    "type=", elemento.get_attribute("type"),
                    "value=", elemento.get_attribute("value")
                )
            
            # with page.expect_popup() as popup_info:
            #     page.keyboard.press("Enter")

            # op063 = popup_info.value
            # op063.wait_for_load_state('domcontentloaded')

            # op063.locator('[id="5"]').fill('0001')
            # op063.locator('[id="6"]').fill("2359")
            # op063.locator('[id="7"]').fill("s")

            # with op063.expect_download() as download_info:
            #     op063.get_by_role("link", name="►").click()

            # download = download_info.value
            # download.save_as(str(arquivo_csv))

            page.close()
            contexto.close()

            errorpanel = page.locator("#errorpanel")

            print("Errorpanel existe:", errorpanel.count())

            if errorpanel.count() > 0:
                print("Conteúdo do errorpanel:", errorpanel.inner_text())
            
            return str(arquivo_csv)

        finally:
            navegador.close()

if __name__ == "__main__":
    baixar_relatorio()
