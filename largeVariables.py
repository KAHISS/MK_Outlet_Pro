# sql comands general==========================================
searchAll = 'SELECT * FROM {}'
searchAllForSale = 'SELECT ID, fornecedor, marca, tipo, quantidade, medida, valor_de_compra, valor_de_venda, validade, cliente, método_de_pagamento, {}, modificação FROM {}'
deleteInformation = 'DELETE FROM {} WHERE ID = {}'

# style of tables general ===============================================
styleTableInformationsTreeview = [
    ('BACKGROUND', (0, 1), (-1, 1), '#e8d499'),
    ('BACKGROUND', (0, 2), (-1, -1), '#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, -1), '#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#e8d499'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#e8d499')
]
styleTableInformationsComplementary = [
    ('BACKGROUND', (0, 1), (-1, 1), '#b59b50'),
    ('BACKGROUND', (0, 2), (-1, -1), '#ffffff'),
    ('TEXTCOLOR', (0, 1), (-1, 1), '#000000'),
    ('FONTSIZE', (0, 1), (-1, 1), 12),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('BOX', (0, 1), (-1, -1), 0.25, '#b59b50'),
    ('INNERGRID', (0, 1), (-1, -1), 0.25, '#b59b50')]

# sql comands for scheduling ===================================
registerSale = (
    'INSERT INTO Pedidos (cliente, quantidade_de_peças, valor_total, método_de_pagamento, profissional, data_de_venda)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'
)

registerItens = (
    'INSERT INTO Itens (marca, modelo, peça, valor, código, número_do_pedido)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'
)

searchSale = '''SELECT * 
                  FROM Pedidos
                  WHERE {} LIKE "%{}%"
                  and quantidade_de_peças LIKE "%{}%"
                  and valor_total LIKE "%{}%"
                  and método_de_pagamento LIKE "%{}%"
                  and profissional LIKE "%{}%"
                  and data_de_venda LIKE "%{}%" ORDER BY {} ASC'''

updateSale = '''UPDATE Pedidos
                      SET cliente = "{}",
                          valor_total = "{}",
                          método_de_pagamento = "{}",
                          profissional = "{}"
                      WHERE ID = {}'''

# tables for schedule informations =================================
tableWithInformationsScheduleTreeview = [['', '', '', '', '', '', ''], ['ID', 'Cliente', 'Q/Peças', 'V/Total', 'M/Pagamento', 'Professional', 'Data de Venda']]
tableWithInformationsComplementarySchedule = [['', '', '', '', '', '', ''], ['Total de clientes', 'T/Cartão', 'T/Dinheiro', 'T/Tranferência', 'T/Nota', 'T/Não pago', 'T/Recebido']]

# sql comands for clients informations ==============================
registerClient = (
    'INSERT INTO Clientes (nome, nascimento, CPF, filhos, telefone, cliente_desde, endereço, CEP, bairro, cidade, estado, foto, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchClient = '''SELECT * 
                  FROM Clientes
                  WHERE {} LIKE "%{}%"
                  and nascimento LIKE "%{}%"
                  and CPF LIKE "%{}%"
                  and filhos LIKE "%{}%"
                  and telefone LIKE "%{}%"
                  and cliente_desde LIKE "%{}%"
                  and endereço LIKE "%{}%"
                  and CEP LIKE "%{}%"
                  and bairro LIKE "%{}%"
                  and cidade LIKE "%{}%"
                  and estado LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''
updateClient = '''UPDATE Clientes
                      SET nome = "{}",
                          nascimento = "{}",
                          CPF = "{}",
                          filhos = "{}",
                          telefone = "{}",
                          cliente_desde = "{}",
                          endereço = "{}",
                          CEP = "{}",
                          bairro = "{}",
                          cidade = "{}",
                          estado = "{}",
                          foto = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsClientTreeview1 = [['', '', '', '', ''], ['    ID    ', '    Nome    ', '    Nascimento    ', '    CPF    ', ' Filhos ', 'Telefone']]
tableWithInformationsClientTreeview2 = [['', '', '', '', ''], ['C/Desde ', ' Endereço ', ' CEP ', ' Bairro ', ' Cidade ', ' Estado ']]
tableWithInformationsComplementaryClient = [['', '', '', ''], ['Total de clientes', 'T/Pais', 'T/Sem filhos', 'T/Moradores', 'T/Visitantes']]

# sql comands for profissional informations ==============================
registerProfessional = (
    'INSERT INTO Profissionais (nome, CPF, admissão, e_mail, telefone, emergência, endereço, CEP, bairro, cidade, estado, foto, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchProfessional = '''SELECT * 
                  FROM Profissionais
                  WHERE {} LIKE "%{}%"
                  and CPF LIKE "%{}%"
                  and admissão LIKE "%{}%"
                  and e_mail LIKE "%{}%"
                  and telefone LIKE "%{}%"
                  and emergência LIKE "%{}%"
                  and endereço LIKE "%{}%"
                  and CEP LIKE "%{}%"
                  and bairro LIKE "%{}%"
                  and cidade LIKE "%{}%"
                  and estado LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''
updateProfessional = '''UPDATE Profissionais
                      SET nome = "{}",
                          CPF = "{}",
                          admissão = "{}",
                          e_mail = "{}",
                          telefone = "{}",
                          emergência = "{}",
                          endereço = "{}",
                          CEP = "{}",
                          bairro = "{}",
                          cidade = "{}",
                          estado = "{}",
                          foto = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsProfesiionalTreeview1 = [['', '', '', '', ''], ['    ID    ', '    Nome    ', '    CPF    ', '    Admissão    ', ' E-mail ', 'Telefone']]
tableWithInformationsProfesiionalTreeview2 = [['', '', '', '', ''], [' Emergência ', ' Endereço ', ' CEP ', ' Bairro ', ' Cidade ', ' Estado ']]
tableWithInformationsComplementaryProfesiional = [[''], ['Total de profissionais']]

# sql comands for services informations ==============================
registerServices = (
    'INSERT INTO Serviços (serviço, valor)'
    'VALUES ("{}", "{}")'
)
searchServices = '''SELECT * 
                  FROM Serviços
                  WHERE {} LIKE "%{}%"
                  and valor LIKE "%{}%" ORDER BY {} ASC'''

updateService = '''UPDATE Serviços
                      SET serviço = "{}",
                          valor = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsServiceTreeview = [['', '', ''], ['    ID    ', '    Serviço    ', 'Valor']]
tableWithInformationsComplementaryService = [[''], ['Total de Serviços']]

# sql comands for services informations ==============================
registerBarCode = (
    'INSERT INTO Código_de_barras (código, foto, observação)'
    'VALUES ("{}", "{}", "{}")'
)
searchBarCode = '''SELECT * 
                  FROM Código_de_barras
                  WHERE código LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateBarCode = '''UPDATE Código_de_barras
                      SET observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsBarCodeTreeview = [['', ''], ['    ID    ',  '  Código  ']]
tableWithInformationsComplementaryBarCode = [[''], ['Total de códigos']]

# sql comands for services informations ==============================
registerInformationsOfStock = (
    'INSERT INTO {} ({})'
    'VALUES ("{}")'
)
searchInformationsOfStock = '''SELECT * 
                  FROM {}
                  WHERE {} LIKE "%{}%" ORDER BY {} ASC'''

updateInformationsOfStock = '''UPDATE {}
                      SET {} = "{}"
                      WHERE ID = {}'''

# sql comands for sale stock ==============================
registerSaleStock = (
    'INSERT INTO Produtos (fornecedor, marca, modelo, peça, quantidade, valor_de_compra, valor_de_venda, código, foto, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchSaleStock = '''SELECT *
                  FROM Produtos
                  WHERE fornecedor LIKE "%{}%"
                  and marca LIKE "%{}%"
                  and modelo LIKE "%{}%"
                  and peça LIKE "%{}%"
                  and quantidade LIKE "%{}%"
                  and valor_de_compra LIKE "%{}%"
                  and valor_de_venda LIKE "%{}%"
                  and código LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateSaleStock = '''UPDATE Produtos
                      SET fornecedor = "{}",
                          marca = "{}",
                          modelo = "{}",
                          peça = "{}",
                          quantidade = "{}",
                          valor_de_compra = "{}",
                          valor_de_venda = "{}",
                          código = "{}",
                          foto = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsSaleStockTreeview = [['', '', '', '', '', '', '', ''], ['ID', 'Fornecedor', 'Marca', 'Modelo', 'Peça', 'Quantidade', 'V/compra', 'V/Venda', 'Código']]
tableWithInformationsComplementarySaleStock = [['', '', '', ''], ['T/Produtos', 'MAV/Compra', 'MEV/Compra', 'MAV/Venda', 'MEV/Venda']]
# message informations usage stock ===============================
messageSaleStock = ('Total de produtos = {}\n'
                    'Maior valor de compra = {}\n'
                    'Maior valor de compra  = {}\n'
                    'Maior valor de venda = {}\n'
                    'Maior valor de venda  = {}\n')

# sql comands for cash ==============================
registerCashManagement = (
    'INSERT INTO {} (t_clientes, t_cartão, t_dinheiro, t_transferência, t_nota, s_cartão, s_dinheiro, s_transferência, s_nota, a_receber, t_recebido, {}, status, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchCashManagement = '''SELECT *
                  FROM {}
                  WHERE t_clientes LIKE "%{}%"
                  and t_cartão LIKE "%{}%"
                  and t_dinheiro LIKE "%{}%"
                  and t_transferência LIKE "%{}%"
                  and t_nota LIKE "%{}%"
                  and {} LIKE "%{}%"
                  and a_receber LIKE "%{}%"
                  and t_recebido LIKE "%{}%"
                  and {} LIKE "%{}%"
                  and status LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateCashManagement = '''UPDATE {}
                      SET t_clientes = "{}",
                          t_cartão = "{}",
                          t_dinheiro = "{}",
                          t_transferência = "{}",
                          t_nota = "{}",
                          {} = "{}",
                          a_receber = "{}",
                          t_recebido = "{}",
                          {} = "{}",
                          status = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsCashManagementTreeview1 = [['', '', '', '', '', '', ''], ['ID', 'T/Clientes', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/Nota', 'S/Cartão']]
tableWithInformationsCashManagementTreeview2 = [['', '', '', '', '', '', ''], ['S/Dinheiro', 'S/Transferência', 'S/Nota', 'A receber', 'T/Recebido', 'Status']]
tableWithInformationsComplementaryCashManagement = [['', '', ''], ['T/Clientes', 'T/Recebido', 'T/Saída']]
# message informations cash day ===============================
messageCashManagement = ('{}= {}\n'
                         'Total de clientes = {}\n'
                         'Total recebido = {}\n'
                         'Total de saida = {}')

# sql comands for payments ==============================
registerCashPayment = (
    'INSERT INTO Gerenciador_de_pagamentos (profissional, mês_de_pagamento, t_clientes, faturamento, porcentagem, pagamento, método_de_pagamento, data_de_pagamento, observação)'
    'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
)
searchCashPayment = '''SELECT *
                  FROM Gerenciador_de_pagamentos
                  WHERE profissional LIKE "%{}%"
                  and mês_de_pagamento LIKE "%{}%"
                  and t_clientes LIKE "%{}%"
                  and faturamento LIKE "%{}%"
                  and porcentagem LIKE "%{}%"
                  and pagamento LIKE "%{}%"
                  and método_de_pagamento LIKE "%{}%"
                  and observação LIKE "%{}%" ORDER BY {} ASC'''

updateCashPayment = '''UPDATE Gerenciador_de_pagamentos
                      SET profissional = "{}",
                          mês_de_pagamento = "{}",
                          t_clientes = "{}",
                          faturamento = "{}",
                          porcentagem = "{}",
                          pagamento = "{}",
                          método_de_pagamento = "{}",
                          observação = "{}"
                      WHERE ID = {}'''

# tables for client informations =================================
tableWithInformationsCashPaymentTreeview1 = [['', '', '', '', ''], ['ID', 'Profissional', 'M/Pagamento', 'T/Clientes', 'Faturamento']]
tableWithInformationsCashPaymentTreeview2 = [['', '', '', ''], ['%', 'Pagamento', 'Mt/Pagamento', 'D/Pagamento']]
tableWithInformationsComplementaryCashPayment = [['', '', ''], ['Pagamentos', 'T/Clientes', 'T/Faturamento']]
# message informations cash day ===============================
messageCashPayment = ('Profissionais = {}\n'
                      'Total de clientes = {}\n'
                      'Total de Faturamento  = {}')

# sql comands for users ==============================
registerUsers = (
    'INSERT INTO Usuários (nome, senha, nivel)'
    'VALUES ("{}", "{}", "{}")'
)
searchUsers = '''SELECT *
                  FROM Usuários
                  WHERE nome LIKE "%{}%"
                  and nivel LIKE "%{}%"'''
updateUsers = '''UPDATE Usuários
                      SET nome = "{}",
                          senha = "{}",
                          nivel = "{}"
                      WHERE ID = {}'''