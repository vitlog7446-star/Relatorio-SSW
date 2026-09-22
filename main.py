from playwright.sync_api import sync_playwright
import time
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent
arquivo_csv = pasta_projeto / "relatorio.csv"

dominio = 'vit'
cpf = '05155209005'
user = 'edusilva'
senha = '1008'

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


            with page.expect_navigation():
                page.get_by_role("link", name="►").click()

            page.wait_for_load_state("networkidle")

            campo_opcao = page.locator('[id="3"]').last
            campo_opcao.wait_for(state="visible")
            
            campo_opcao.click()
            campo_opcao.fill("063")

            with page.expect_popup() as popup_info:
                page.keyboard.press("Enter")

            op063 = popup_info.value
            op063.wait_for_load_state('domcontentloaded')

            op063.locator('[id="5"]').fill('0001')
            op063.locator('[id="6"]').fill("2359")
            op063.locator('[id="7"]').fill("s")

            with op063.expect_download() as download_info:
                op063.get_by_role("link", name="►").click()

            download = download_info.value
            download.save_as(str(arquivo_csv))

            op063.close()
            page.close()
            contexto.close()

            return str(arquivo_csv)

        finally:
            navegador.close()

if __name__ == "__main__":
    baixar_relatorio()