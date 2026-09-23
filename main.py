from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import re


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

            # ==========================================================
            # ABRIR SSW
            # ==========================================================

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

            print("Login:", resposta.status)

            page.wait_for_timeout(3000)

            # ==========================================================
            # ABRIR OPÇÃO 063
            # ==========================================================

            campo_opcao = page.locator('[id="3"]').last

            campo_opcao.wait_for(
                state="visible",
                timeout=60000
            )

            campo_opcao.fill("063")
            campo_opcao.press("Enter")

            page.wait_for_timeout(3000)

            # ==========================================================
            # LOCALIZAR PÁGINA 063
            # ==========================================================

            if len(contexto.pages) <= 1:

                print("ERRO: tela 063 não foi aberta.")
                return

            pagina_063 = contexto.pages[1]

            print("Tela 063:", pagina_063.title())

            # ==========================================================
            # CLICAR NO BOTÃO ►
            # ==========================================================

            botao = pagina_063.get_by_role(
                "link",
                name="►"
            )

            if botao.count() == 0:

                print("ERRO: botão ► não encontrado.")
                return

            with pagina_063.expect_response(
                "**/bin/**",
                timeout=30000
            ) as resposta_063:

                botao.click()

            resposta_botao = resposta_063.value

            print("Consulta:", resposta_botao.status)

            texto_dados = resposta_botao.text()

            # ==========================================================
            # EXTRAIR REGISTROS
            # ==========================================================

            registros = re.findall(
                r"<r>(.*?)</r>",
                texto_dados,
                re.DOTALL
            )

            print(
                "Registros encontrados:",
                len(registros)
            )

            # ==========================================================
            # USUÁRIOS QUE SERÃO CONSIDERADOS
            # ==========================================================

            usuarios_definidos = [
                "edusilva",
                "mabastos",
                "matorres",
                "paulod"
            ]

            cont_expedidor = {
                usuario: 0
                for usuario in usuarios_definidos
            }

            total_volumes = 0

            # ==========================================================
            # PROCESSAR REGISTROS
            # ==========================================================

            for registro in registros:

                def pegar_campo(nome):

                    resultado = re.search(
                        rf"<{nome}>(.*?)</{nome}>",
                        registro,
                        re.DOTALL
                    )

                    if resultado:
                        return resultado.group(1)

                    return ""

                volumes = pegar_campo("f13")
                usuario = pegar_campo("f20").strip()

                if usuario in usuarios_definidos:

                    cont_expedidor[usuario] += 1

                    try:

                        volumes = volumes.replace(
                            ",",
                            "."
                        ).strip()

                        total_volumes += float(volumes)

                    except Exception as erro:

                        print(
                            f"Erro ao converter volumes: "
                            f"'{volumes}' | {erro}"
                        )

            # ==========================================================
            # MOSTRAR RESUMO
            # ==========================================================

            print()
            print("========================================")
            print("RESUMO DA EXPEDIÇÃO")
            print("========================================")

            for usuario, quantidade in cont_expedidor.items():

                print(
                    f"{usuario}: "
                    f"{quantidade} emissão(ões)"
                )

            print()
            print(
                "TOTAL DE VOLUMES:",
                int(total_volumes)
            )

        finally:

            navegador.close()


if __name__ == "__main__":
    baixar_relatorio()
