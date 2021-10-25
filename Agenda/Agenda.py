from PyQt5 import uic, QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
import sqlite3



#Insert
def cadastrarContato():
    campoNome = agenda.NameCustomer.text()
    campoEmail = agenda.EmailCustomer.text()
    campoTelefone = agenda.TelephoneCustomer.text()

    #Verification (Name,Email,Telephone and Radio Buttons)
    campoNome = campoNome.strip()
    campoEmail = campoEmail.strip()
    campoTelefone = campoTelefone.strip()

    if agenda.HomeTell.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.CellPhone.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado"

    #if any or All text camp is null
    if not campoNome or not campoEmail or not campoTelefone or tipoTelefone == "Não informado":
        print("Informe todos os campos")

    else:
        cursor = banco.cursor()
        comando_SQL = f"INSERT INTO contatos (nome, email, telefone, tipo_telefone ) VALUES (%s, %s, %s, %s)"
        dados = (str(campoNome),str(campoEmail),str(campoTelefone), tipoTelefone)

        cursor.execute(comando_SQL, dados)
        banco.commit()
        print("Cadastrado com sucesso")

#Create
def consultarContatos():

    listarContatos.show()

    campoId = agenda.IDCustomer.text()
    campoNome = agenda.NameCustomer.text()
    campoEmail = agenda.EmailCustomer.text()
    campoTelefone = agenda.TelephoneCustomer.text()

    #Verification (ID, Name,Email,Telephone and Radio Buttons)
    campoId = campoId.strip()
    campoNome = campoNome.strip()
    campoEmail = campoEmail.strip()
    campoTelefone = campoTelefone.strip()

    if agenda.HomeTell.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.CellPhone.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado"

    #Dynamic Query (SELECT)
    comando_SQL = "SELECT * FROM contatos "

    if campoId != "":
        comando_SQL =  comando_SQL + f"WHERE id = '{campoId}' "

    if campoNome != "" and not campoId:
        comando_SQL = comando_SQL + f"WHERE nome LIKE '%{campoNome}%' "
    elif campoNome != "":
        comando_SQL = comando_SQL + f"AND nome LIKE '%{campoNome}%' "

    if campoEmail != '' and not campoNome and not campoId:
        comando_SQL = comando_SQL + f"WHERE email = '{campoEmail}' "
    elif campoEmail != "":
        comando_SQL = comando_SQL + f"AND email = '{campoEmail}' "

    if campoTelefone != "" and not campoNome and not campoId and not campoEmail:
        comando_SQL = comando_SQL + f"WHERE telefone = '{campoTelefone}' "
    elif campoTelefone != "":
        comando_SQL = comando_SQL + f"AND telefone = '{campoTelefone}' "

    if tipoTelefone != "Não informado" and not campoNome and not campoId and not campoEmail and not campoTelefone :
        comando_SQL = comando_SQL + f"WHERE tipo_telefone = '{tipoTelefone}'"
    elif tipoTelefone != "Não informado":
        comando_SQL = comando_SQL + f"AND tipo_telefone = '{tipoTelefone}'"

    cursor = banco.cursor()
    cursor.execute(comando_SQL)
    contatosLidos = cursor.fetchall()

    if not contatosLidos:
        print("Não há informações com essas especificações")

    else:
        listarContatos.tableContatos.setRowCount(len(contatosLidos))
        listarContatos.tableContatos.setColumnCount(5)

        for i in range(0, len(contatosLidos)):
            for f in range(0, 5):
                listarContatos.tableContatos.setItem(i, f, QtWidgets.QTableWidgetItem(str(contatosLidos[i][f])))

        print("Exibido com sucesso")

#Exclude by Id
def excluirContatoBotao():

    campoId = agenda.IDCustomer.text()
    campoId = campoId.strip()

    if not campoId:
        print("Preencha o campo Id")
    else:
        cursor = banco.cursor()
        comando_SQL = f"DELETE FROM contatos where id='{campoId}'"
        cursor.execute(comando_SQL)
        banco.commit()
        print("Excluido com sucesso")

#Exclude
def excluirContatoTopo():

   linhaContato = listarContatos.tableContatos.currentRow()
   listarContatos.tableContatos.removeRow(linhaContato)

   cursor = banco.cursor()
   comando_SQL = "SELECT id FROM contatos"
   cursor.execute(comando_SQL)
   contatos_lidos = cursor.fetchall()

   if not contatos_lidos:
        print("Não há contatos inseridos")
   else:
        valorId = contatos_lidos[linhaContato][0]
        cursor.execute(f"DELETE FROM contatos WHERE id='{str(valorId)}'")
        banco.commit()

#Change
def alterarContato():
    listarContatos.show()

    campoId = agenda.IDCustomer.text()
    campoNome = agenda.NameCustomer.text()
    campoEmail = agenda.EmailCustomer.text()
    campoTelefone = agenda.TelephoneCustomer.text()

    # Verification (ID, Name,Email,Telephone and Radio Buttons)
    campoId = campoId.strip()
    campoNome = campoNome.strip()
    campoEmail = campoEmail.strip()
    campoTelefone = campoTelefone.strip()

    if agenda.HomeTell.isChecked():
        tipoTelefone = "Residencial"
    elif agenda.CellPhone.isChecked():
        tipoTelefone = "Celular"
    else:
        tipoTelefone = "Não informado"

    if not campoId:
        print("Digite o campo ID")
    elif not campoNome and not campoEmail and not campoTelefone and tipoTelefone=="Não informado":
        print("Não há alterações para serem feitas")

    else:
        # Dynamic Query (DELETE)
        comando_SQL = "UPDATE contatos "

        if campoNome != "":
            comando_SQL = comando_SQL + f"SET nome = '{campoNome}' "

        if campoEmail != '' and not campoNome:
            comando_SQL = comando_SQL + f"SET email = '{campoEmail}' "
        elif campoEmail != "":
            comando_SQL = comando_SQL + f", email = '{campoEmail}' "

        if campoTelefone != "" and not campoNome and not campoEmail:
            comando_SQL = comando_SQL + f"SET telefone = '{campoTelefone}' "
        elif campoTelefone != "":
            comando_SQL = comando_SQL + f", telefone = '{campoTelefone}' "

        if tipoTelefone != "Não informado" and not campoNome and not campoEmail and not campoTelefone:
            comando_SQL = comando_SQL + f"SET tipo_telefone = '{tipoTelefone}'"
        elif tipoTelefone != "Não informado":
            comando_SQL = comando_SQL + f", tipo_telefone = '{tipoTelefone}'"

        comando_SQL = comando_SQL + f" WHERE id = {campoId}"

        #Verification - ID
        cursor = banco.cursor()
        comando_SQL2 = f"SELECT id FROM contatos WHERE id='{campoId}'"
        cursor.execute(comando_SQL2)
        contatos_lidos = cursor.fetchall()

        if not contatos_lidos:
            print("Não há um contato com o id informado")
        else:
            cursor = banco.cursor()
            cursor.execute(comando_SQL)
            print("Contato atualizado com sucesso")

#Get PDF
def gerarPDF():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas("lista_contatos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Lista de Contatos")

    pdf.setFont("Times-Bold", 15)
    pdf.drawString(10, 750, "ID")
    pdf.drawString(50, 750, "NOME")
    pdf.drawString(210, 750, "EMAIL")
    pdf.drawString(390, 750, "TELEFONE")
    pdf.drawString(490, 750, "TIPO")

    pdf.setFont("Times-Bold", 10)
    for i in range(0, len(contatos_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(contatos_lidos[i][0]))
        pdf.drawString(50, 750 - y, str(contatos_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(contatos_lidos[i][2]))
        pdf.drawString(390, 750 - y, str(contatos_lidos[i][3]))
        pdf.drawString(490, 750 - y, str(contatos_lidos[i][4]))

    pdf.save()
    print("PDF gerado com sucesso")

app=QtWidgets.QApplication([])

#For load All Ui's
agenda=uic.loadUi("agendaFront.ui")
listarContatos=uic.loadUi("ListFront.ui")


#Methods for buttons
agenda.ChangeButton.clicked.connect(alterarContato)
agenda.RegisterButton.clicked.connect(cadastrarContato)
agenda.QueryButton.clicked.connect(consultarContatos)
agenda.ExcludeButton.clicked.connect(excluirContatoBotao)
listarContatos.btnExcluir.clicked.connect(excluirContatoTopo)
listarContatos.btnGerarPDF.clicked.connect(gerarPDF)

#MySQL conection
banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda"
)

agenda.show()
app.exec()