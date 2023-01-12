from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# abrir um navegador                                      
navegador = webdriver.Chrome("chromedriver.exe")
navegador.get("https://www.google.com/")

# cotação do Dólar
navegador.find_element(By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")

navegador.find_element(By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element(By.XPATH,
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value") 
print(cotacao_dolar)

# Cotação do Euro
navegador.get("https://www.google.com/")
navegador.find_element(By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element(By.XPATH,
    '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element(By.XPATH,
    '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_euro)

# Cotação do Ouro
navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element(By.XPATH, '//*[@id="comercial"]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

navegador.quit()

# lista de produtos
import pandas as pd

tabela = pd.read_excel("Produtos.xlsx")
print(tabela)

# Recalculando o preço de cada produto e atualizando a cotação

tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# atualizar o preço base reais (preço base original * cotação)
tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]

# atualizar o preço final (preço base reais * Margem)
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

# tabela["Preço de Venda"] = tabela["Preço de Venda"].map("R${:.2f}".format)

print(tabela)

#  Salvando os novos preços dos produtos
tabela.to_excel("Produtos Novo.xlsx", index=False)