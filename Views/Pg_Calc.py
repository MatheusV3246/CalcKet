import streamlit as st
import pandas as pd

class Calc():
    def __init__(self):

        st.title("Calculadora de Margem de Lucro")
        st.markdown("Use esta ferramenta para calcular margens de lucro, preços sugeridos e mais.")

        # Campos de entrada
        produto = st.text_input("Produto:")
        custo_fixo = st.number_input("Custo Fixo (R$)", min_value=0.0, step=0.01)
        custo_var = st.number_input("Custo Variável (R$)", min_value=0.0, step=0.01)
        imposto_fixo = st.number_input("Imposto Fixo (R$)", min_value=0.0, step=0.01)
        imposto_var = st.number_input("Imposto Variável (R$)", min_value=0.0, step=0.01)
        qtd = st.number_input("Quantidade", min_value=1, step=1)
        frete = st.number_input("Frete (R$)", min_value=0.0, step=0.01)
        mg_lucro = st.number_input("Margem Lucro (%)", min_value=0.0, step=0.1) / 100  # Convertendo para decimal
        extra = st.number_input("Extra (R$)", min_value=0.0, step=0.01)

        # Botão de cálculo
        if st.button("Calcular"):
            try:
                # Calcular custo total por unidade e preço de venda sugerido
                despesa = (
                    (qtd * (custo_var + imposto_var)) +
                    (1 / qtd) * (custo_fixo + imposto_fixo + frete) +
                    extra
                )
                custo_un = (
                    (custo_var + imposto_var) +
                    (1 / qtd) * (custo_fixo + imposto_fixo + frete)
                )
                lucro_un = mg_lucro * custo_un
                preco_venda = custo_un + lucro_un
                receita = preco_venda * qtd
                lucro = receita - despesa

                # Criar DataFrame com os resultados
                dados = pd.DataFrame({
                    "Produto": [produto],
                    "Preço Sugerido": [preco_venda],
                    "Lucro Unitário": [lucro_un],
                    "Custo Unitário": [custo_un],
                    "Custo Fixo": [custo_fixo],
                    "Custo Variável": [custo_var],
                    "Imposto Fixo": [imposto_fixo],
                    "Imposto Variável": [imposto_var],
                    "Quantidade": [qtd],
                    "Frete": [frete],
                    "Margem de Lucro (%)": [mg_lucro * 100],
                    "Extra": [extra],
                    "Receita": [receita],
                    "Despesa": [despesa],
                    "Lucro Total": [lucro]
                })

                # Salvar os dados em Excel
                dados.to_excel("Dados.xlsx", index=False)

                # Exibir resultados
                st.success("Cálculo realizado com sucesso!")
                st.subheader(f"Produto: {produto}")
                st.write(f"**Preço Sugerido:** R$ {preco_venda:.2f}")
                st.write(f"**Lucro Unitário:** R$ {lucro_un:.2f}")
                st.write(f"**Lucro Total:** R$ {lucro:.2f}")
                st.write(f"**Receita:** R$ {receita:.2f}")
                st.write(f"**Despesa Total:** R$ {despesa:.2f}")

                # Mostrar tabela de resultados
                st.dataframe(dados)

                # Botão para download do arquivo Excel
                with open("Dados.xlsx", "rb") as file:
                    st.download_button(
                        label="Baixar Resultados em Excel",
                        data=file,
                        file_name="Dados.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
