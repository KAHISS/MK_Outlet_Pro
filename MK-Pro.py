# libs of python ==========
from tkinter import ttk
from tkcalendar import DateEntry
from random import randint
# my modules ==============
from databaseConnection import DataBase, Criptography
from functions import *
from interface import Interface


class Aplication(
    Interface,
    FunctionsOfSchedule,
    FunctionsOfCustomsInformations,
    FunctionsOfProfessionalInformations,
    FunctionsOfBarCodeInformations,
    FunctionsOfStockInformations,
    FunctionsOfCashManagement,
    FunctionsOfPayment,
    FunctionsOfLogin,
    FunctionsOfInformationsStock,
    FunctionsOfConfigurations
):

    def __init__(self):
        self.lineTreeviewColor = {}
        self.lastSearch = {}
        self.dataBases = {
            'sale': DataBase('resources/Vendas.db'),
            'informations': DataBase('resources/informações.db'),
            'stock': DataBase('resources/Estoque.db'),
            'cash': DataBase('resources/Caixa.db'),
            'config': DataBase('resources/config.db'),
        }
        self.openColorPicker = True
        self.criptography = Criptography()
        super().__init__()
        self.login_window()

    def login_window(self):
        self.loginWindow = Tk()
        self.loginWindow.title('Login - MK Outlet Pro')
        width = self.loginWindow.winfo_screenwidth()
        height = self.loginWindow.winfo_screenheight()
        posx = width / 2 - 800 / 2
        posy = height / 2 - 500 / 2
        self.loginWindow.geometry('800x500+%d+%d' % (posx, posy))
        self.loginWindow.config(bg='#FFFFFF')
        self.loginWindow.iconphoto(False, PhotoImage(file='assets/logo.png'))

        # logo image ==============================
        logoImage = self.labels(self.loginWindow, '', 0.009, 0.01, width=0.48, height=0.98, photo=self.image('assets/logo.png', (350, 350))[0], position=CENTER)

        # frame of inputs =========================
        frameInputs = self.frame(self.loginWindow, 0.5, 0.005, 0.49, 0.985, border=2, radius=10)

        # name login ---------------------------
        labelLogin = self.labels(
            frameInputs, 'LOGIN', 0.253, 0.05, width=0.5, height=0.2, position=CENTER, size=50, color='#3b321a',
            font='Handmade'
        )

        # user name and password -----------------------------
        userName = self.entry(
            frameInputs, 0.1, 0.3, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Usuário'
        )
        userName.bind('<FocusIn>', lambda e: userName.configure(fg_color='#FFFFFF'))

        password = self.entry(
            frameInputs, 0.1, 0.5, 0.8, 0.12, type_entry='entryLogin', border=2, radius=10,
            place_text='Senha', show='*'
        )

        # visibility ---------------------------------
        visibilityPasswordBtn = self.button(
            frameInputs, '', 0.76, 0.52, 0.13, 0.08, photo=self.image('assets/icon_eyeClose.png', (26, 26))[0],
            type_btn='buttonPhoto', background='white', hover_cursor='white', function=lambda: self.toggle_visibility(password, visibilityPasswordBtn)
        )
        password.bind('<FocusIn>', lambda e: [password.configure(fg_color='#FFFFFF'), visibilityPasswordBtn.configure(fg_color='#FFFFFF')])
        password.bind('<Return>', lambda e: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''}))

        # line separator higher --------------------
        lineHigher = Canvas(frameInputs, background='#FFFFFF', highlightthickness=0)
        lineHigher.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.1)
        lineHigher.create_line(1, 15, 1000, 15, fill='#3b321a', width=2)

        # button of login and button of register ----------------------
        loginBtn = self.button(
            frameInputs, 'Iniciar sessão', 0.1, 0.72, 0.8, 0.1, background='#e8d499',
            border=0, color='#3b321a',
            function=lambda: self.validating_user([userName, password, visibilityPasswordBtn], self.open_software, type_password='login', parameters={'e': ''})
        )
        closeBtn = self.button(
            frameInputs, 'Fechar', 0.1, 0.85, 0.8, 0.1, background='#b59b50',
            border=0, color='#3b321a', function=lambda: self.loginWindow.destroy()
        )
        self.loginWindow.mainloop()

    # ================================== main window configure =======================================
    def main_window(self):
        # screen configure ===================================
        self.root = Toplevel()
        self.root.title('MK Outlet Pro')
        self.root.state('zoomed')
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')
        self.root.configure(background='#FFFFFF')
        self.root.iconphoto(False, PhotoImage(file='assets/logo.png'))
        self.root.wm_protocol('WM_DELETE_WINDOW', lambda: self.check_treeview_to_close(self.treeviewRegisterSale))
        # event bind ============================================
        self.root.bind_all('<Control-b>', lambda e: self.backup_dataBaes())
        self.root.bind_all('<Control-l>', lambda e: self.loading_database())

        # style notebook
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 13, "bold"), foreground=self.colorsOfLabels[1])

        # style treeviews ==================================================
        self.style_treeview = ttk.Style()
        self.style_treeview.theme_use('vista')
        self.style_treeview.configure('Treeview', rowheight=25, fieldbackground='#261c20', foreground=self.colorsOfTreeviews[2], font='Arial 13')
        self.style_treeview.map('Treeview',
                                background=[('selected', '#000000')],  # Cor de fundo da seleção
                                foreground=[('selected', 'white')]
                                )
        self.photosAndIcons = {
            'pdf': self.image('assets/icon_pdf.png', (46, 46)),
            'informações': self.image('assets/icon_informacoes.png', (46, 46)),
            'random': self.image('assets/icon_random.png', (36, 36)),
            'image': self.image('assets/icon_imagem.png', (26, 26)),
            'costumer': self.image('assets/icon_no_picture.png', (76, 76)),
            'employee': self.image('assets/icon_no_picture.png', (76, 76)),
            'product': self.image('assets/cabide.png', (76, 76)),
            'barCode': self.image('assets/icon_barCode.png', (76, 76)),
        }
        self.mainTabview = ttk.Notebook(self.root)
        self.mainTabview.place(relx=0, rely=0.01, relwidth=1, relheight=1)

        # schedule ============================================================
        self.mainScheduleFrame = self.main_frame_notebook(self.mainTabview, ' Vendas ')
        self.scheduleManagementTabview = self.notebook(self.mainScheduleFrame)
        # schedule management ---------------------------------------------------
        self.scheduleFrame = self.main_frame_notebook(self.scheduleManagementTabview, ' Gerenciamento de vendas ')
        self.frame_sales()
        # scheduling ------------------------------------------------------------
        self.registerSaleFrame = self.main_frame_notebook(self.scheduleManagementTabview, ' Ponto de venda ')
        self.frame_register_sales()

        # information ============================================================
        self.mainInformationFrame = self.main_frame_notebook(self.mainTabview, ' Cadastro & Informações ')
        self.informationsManagementTabview = self.notebook(self.mainInformationFrame)
        # costumers management ---------------------------------------------------
        self.costumersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Clientes ')
        self.frame_customers()
        # employers management ---------------------------------------------------
        self.employersFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Profissionais ')
        self.frame_employers()
        # stock informations -----------------------------------------------------
        self.stockInformationsFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Informações de estoque ')
        self.typeStockInformations = self.tabview(self.stockInformationsFrame, 0, 0, 1, 0.98, background='white', border='white')
        self.frame_stock_informations()
        # bar code management ---------------------------------------------------
        self.barCodeFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Código de barras ')
        self.frame_barCode()
        # bar code management ---------------------------------------------------
        self.userFrame = self.main_frame_notebook(self.informationsManagementTabview, ' Usuários ')
        self.frame_users()

        # stock ============================================================
        self.mainStockFrame = self.main_frame_notebook(self.mainTabview, ' Estoque ')
        self.frame_sale_inventory_control()

        # cash register ============================================================
        self.mainCashRegisterFrame = self.main_frame_notebook(self.mainTabview, ' Caixa ')
        self.cashManagementTabview = self.notebook(self.mainCashRegisterFrame)
        # cash management ---------------------------------------------------
        self.cashFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciamento de caixa ')
        self.typeCashManagement = self.tabview(self.cashFrame, 0, 0, 1, 0.98, background='white', border='white')
        # day finish
        self.typeCashManagement.add(' Gerenciamento do dia ')
        self.frame_cash_register_management_day()
        # month finish
        self.typeCashManagement.add(' Gerenciamento do mês ')
        self.frame_cash_register_management_month()
        # employee management ---------------------------------------------------
        self.employersPayFrame = self.main_frame_notebook(self.cashManagementTabview, ' Gerenciar pagamentos ')
        self.frame_pay_management()

        # configuration ============================================================
        self.configurationFrame = self.main_frame_notebook(self.mainTabview, ' Configurações ')
        self.configurationTabview = self.notebook(self.configurationFrame)
        # costumization ---------------------------------------------------
        self.costumizationFrame = self.main_frame_notebook(self.configurationTabview, ' Customização ')
        # costimizators ===============================================
        self.frameForCostumizations = self.frame(self.costumizationFrame, 0, 0.01, 0.999, 0.95)
        self.frame_costumization_buttons()
        self.frame_costumization_frames()
        self.frame_costumization_tabview()
        self.frame_costumization_treeview()
        self.frame_costumization_entrys()
        self.frame_costumization_labels()
        self.save()
        # loadings configs ---------------------------
        self.load_configs()

        # filling in lists -----------------------------------------
        self.refresh_combobox_client()
        self.refresh_combobox_professional()
        self.refresh_combobox_barCode()
        self.refresh_combobox_InformationsStock()
        self.refresh_combobox_stock()

        # keeping window ===========================================
        self.root.mainloop()

    # =================================  schedule configuration  ======================================
    def frame_sales(self):
        # frame inputs ==========================================
        self.frameInputsSchedule = self.frame(self.scheduleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom -------------
        labelCustom = self.labels(self.frameInputsSchedule, 'Cliente:', 0.02, 0.22, width=0.08)
        self.customScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.22, 0.2, 0.12, type_entry='list')

        # amount -------------
        labelAmount = self.labels(self.frameInputsSchedule, 'Q/Peças:', 0.02, 0.375, width=0.15)
        self.amountScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.375, 0.20, 0.12, type_entry='list')

        # value total -------------
        labelValueTotal = self.labels(self.frameInputsSchedule, 'Total:', 0.02, 0.535, width=0.15)
        self.valueTotalScheduleEntry = self.entry(self.frameInputsSchedule, 0.12, 0.535, 0.2, 0.12, type_entry='entry')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsSchedule, 'M/Pagamento:', 0.34, 0.22, width=0.15)
        self.methodPayScheduleEntry = self.entry(
            self.frameInputsSchedule, 0.46, 0.22, 0.177, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # professional -------------
        labelProfessional = self.labels(self.frameInputsSchedule, 'Profissional:', 0.34, 0.375, width=0.15)
        self.professionalScheduleEntry = self.entry(self.frameInputsSchedule, 0.44, 0.375, 0.199, 0.12, type_entry='list')

        # data of sale ----------
        labelMarking = self.labels(self.frameInputsSchedule, 'D/Venda:', 0.34, 0.535, width=0.12)
        self.markingScheduleEntry = self.entry(self.frameInputsSchedule, 0.44, 0.535, 0.2, 0.12, type_entry='date')

        # events bind of frame inputs ===========================
        self.markingScheduleEntry.bind('<<DateEntrySelected>>', lambda e: self.search_sale(self.treeviewOrders, entryPicker()[2]))

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSchedule, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewOrders, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewOrders = self.frame(self.scheduleFrame, 0.005, 0.45, 0.48, 0.53)
        self.frameTreeviewItens = self.frame(self.scheduleFrame, 0.49, 0.45, 0.505, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTableOrders = ('ID', 'Cliente', 'Q/peças', 'Valor total', 'Método de Pagamento', 'Profissional', 'Data de venda')
        informationOfTableItens = ('ID', 'Marca', 'Modelo', 'Peça', 'Valor', 'código', 'número do pedido')
        self.treeviewOrders = self.treeview(self.frameTreeviewOrders, informationOfTableOrders)
        self.treeviewItens = self.treeview(self.frameTreeviewItens, informationOfTableItens)
        self.lineTreeviewColor['sale'] = 0
        self.lineTreeviewColor['itens'] = 0
        # event bind treeview ==========================================
        self.treeviewOrders.bind(
            "<Double-Button-1>",
            lambda e: [
                self.insert_informations_entrys(entryPicker()[1], self.treeviewOrders),
                self.search_itens(self.treeviewItens, entryPicker()[0])
            ]
        )

        # save last search schedule ===================================
        self.lastSearch['sale'] = ''

        # buttons management ===========================================
        functions = {
            'search': lambda: self.search_sale(self.treeviewOrders, entryPicker()[0]),
            'order': lambda e: self.search_sale(self.treeviewOrders, entryPicker()[0]),
            'update': lambda: self.update_schedule(self.treeviewOrders, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_schedule(self.treeviewOrders),
            'pdf': lambda: self.create_pdf_schedule(self.treeviewOrders),
            'informations': lambda: self.message_informations_schedule(self.treeviewOrders),
        }
        self.orderBtnSchedule = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSchedule, functions, self.photosAndIcons, informationOfTableOrders, type_btns='management')

        # pick up entrys ===========================
        def entryPicker():
            entrysGet = []
            entrys = []
            for widget in self.frameInputsSchedule.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            entrysGet.append(self.orderBtnSchedule.get())
            return [entrysGet, entrys, ['', '', '', '', '', self.markingScheduleEntry.get(), self.orderBtnSchedule.get()]]

        # init search for day ===============================================
        self.search_sale(self.treeviewOrders, entryPicker()[0])

    def frame_register_sales(self):
        # frame inputs ==========================================
        self.frameInputsScheduling = self.frame(self.registerSaleFrame, 0.005, 0.01, 0.989, 0.43)

        # custom ----------
        labelCustom = self.labels(self.frameInputsScheduling, 'Cliente:', 0.014, 0.13, width=0.11)
        self.customSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.125, 0.17, 0.12, type_entry='list')

        # brand --------------
        labelBrand = self.labels(self.frameInputsScheduling, 'Marca:', 0.014, 0.30, width=0.08)
        self.brandSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.295, 0.17, 0.12, type_entry='list')

        # model --------------
        labelModel = self.labels(self.frameInputsScheduling, 'Modelo:', 0.014, 0.47, width=0.08)
        self.modelSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.465, 0.17, 0.12, type_entry='list')

        # part ----------
        labelPart = self.labels(self.frameInputsScheduling, 'Peça:', 0.014, 0.64, width=0.11)
        self.partSchedulingEntry = self.entry(self.frameInputsScheduling, 0.15, 0.635, 0.17, 0.12, type_entry='list')

        # value ----------
        labelValue = self.labels(self.frameInputsScheduling, 'Valor:', 0.35, 0.13, width=0.11)
        self.valueSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.125, 0.17, 0.12, type_entry='entry')

        # professional ---------------
        labelProfessional = self.labels(self.frameInputsScheduling, 'Profissional:', 0.35, 0.30, width=0.1)
        self.professionalSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.295, 0.17, 0.12, type_entry='list')

        # cheat ----------
        labelCheat = self.labels(self.frameInputsScheduling, 'Código:', 0.35, 0.47, width=0.13)
        self.cheatSchedulingEntry = self.entry(self.frameInputsScheduling, 0.47, 0.465, 0.17, 0.12, type_entry='list')

        # method pay -------------
        labelMethodPay = self.labels(self.frameInputsScheduling, 'M/Pagamento:', 0.35, 0.64, width=0.15)
        self.methodPaySchedulingEntry = self.entry(
            self.frameInputsScheduling, 0.47, 0.635, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # Total ----------
        self.labelTotal = self.labels(self.frameInputsScheduling, 'Total:', 0.35, 0.82, width=0.19, color='#917c3f')

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsScheduling, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewRegisterSale, False),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # event bind frameInput ==========================================
        self.cheatSchedulingEntry.bind('<Return>', lambda e: self.register_with_barCode(self.treeviewRegisterSale, entryPicker()[0], entrys=entryPicker()[1][1:5]))

        # pick up entrys =============================
        def entryPicker():
            entrysGet = [[]]
            entrys = []
            for widget in self.frameInputsScheduling.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    match widget:
                        case self.valueSchedulingEntry:
                            entrysGet[0].append(self.treating_numbers(widget.get(), 1) if widget.get() != '' else 'R$0,00')
                            entrys.append(widget)
                        case _:
                            entrysGet[0].append(widget.get().upper())
                            entrys.append(widget)
            return [entrysGet, entrys]

        # buttons management ============
        frameBtns = self.tabview(self.frameInputsScheduling, 0.675, 0.02, 0.3, 0.9)
        frameBtns.add('Agendamento')
        # add -------------
        addBtn = self.button(frameBtns.tab('Agendamento'), 'Adicionar item', 0.225, 0.08, 0.55, 0.2, function=lambda: self.register_sale(entryPicker()[0], type_function='add', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))
        # remove -------------
        removeBtn = self.button(frameBtns.tab('Agendamento'), 'Remover item', 0.225, 0.38, 0.55, 0.2, function=lambda: self.register_sale(entryPicker()[0], type_function='remove', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))
        # finish scheduling ---------
        registerBtn = self.button(frameBtns.tab('Agendamento'), 'Finalizar pedido', 0.225, 0.68, 0.55, 0.2, function=lambda: self.register_sale(entryPicker()[0], type_function='finishRegister', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))

        # events bind for buttons ===========
        self.registerSaleFrame.bind_all('<Control-plus>', lambda e: self.register_sale(entryPicker()[0], type_function='add', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))
        self.registerSaleFrame.bind_all('<Control-minus>', lambda e: self.register_sale(entryPicker()[0], type_function='remove', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))
        self.registerSaleFrame.bind_all('<Control-f>', lambda e: self.register_sale(entryPicker()[0], type_function='finishRegister', treeview=self.treeviewRegisterSale, button=deleteInformationsInputs))

        # frame treeview ==================
        self.frameTreeviewRegisterSale = self.frame(self.registerSaleFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('Cliente', 'Marca', 'Modelo', 'Peça', 'Valor', 'Profissional', 'Código', 'M/Pagamento')
        self.treeviewRegisterSale = self.treeview(self.frameTreeviewRegisterSale, informationOfTable, max_width=330)
        self.lineTreeviewColor['saleRegister'] = 0

    # =================================  informations configuration  ======================================
    def frame_customers(self):
        # frame photo ==========================================
        self.framePhotoClient = self.frame(self.costumersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelClient = self.labels(self.framePhotoClient, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['costumer'][0], position=CENTER)

        # observation --------------------
        self.observationClientEntry = self.text_box(self.costumersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsClient = self.frame(self.costumersFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsClient, 'Nome:', 0.02, 0.08, width=0.08)
        self.nameClientEntry = self.entry(self.frameInputsClient, 0.1, 0.08, 0.2, 0.12, type_entry='entry')

        # birtday -------------
        labelBirtday = self.labels(self.frameInputsClient, 'Nascimento:', 0.02, 0.22, width=0.15)
        self.birtdayClientEntry = self.entry(self.frameInputsClient, 0.14, 0.22, 0.16, 0.12, type_entry='date')

        # cpf -------------
        labelcpf = self.labels(self.frameInputsClient, 'CPF:', 0.02, 0.36, width=0.15)
        self.cpfClientEntry = self.entry(self.frameInputsClient, 0.1, 0.36, 0.20, 0.12, type_entry='entry')

        # children -------------
        labelchildren = self.labels(self.frameInputsClient, 'Filhos:', 0.02, 0.50, width=0.15)
        self.childrenClientBtn = StringVar(value='')
        yes = self.button(
            self.frameInputsClient, 'Sim', 0.11, 0.51, 0.12, 0.1, type_btn='radioButton',
            value='Sim', retur_variable=self.childrenClientBtn
        )
        no = self.button(
            self.frameInputsClient, 'Não', 0.18, 0.51, 0.12, 0.1, type_btn='radioButton',
            value='Não', retur_variable=self.childrenClientBtn
        )

        # phone -------------
        labelPhono = self.labels(self.frameInputsClient, 'Telefone:', 0.02, 0.64, width=0.15)
        self.phonoClientEntry = self.entry(self.frameInputsClient, 0.126, 0.64, 0.173, 0.12, type_entry='entry')

        # firstDate -------------
        labelFirstDate = self.labels(self.frameInputsClient, 'Cliente desde:', 0.02, 0.78, width=0.16)
        self.firstDateClientEntry = self.entry(self.frameInputsClient, 0.159, 0.78, 0.14, 0.12, type_entry='date')

        # adress -----------------
        labelAdress = self.labels(self.frameInputsClient, 'Endereço:', 0.32, 0.08, width=0.16)
        self.adressClientEntry = self.entry(self.frameInputsClient, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsClient, 'CEP:', 0.32, 0.22, width=0.16)
        self.zipCodeClientEntry = self.entry(self.frameInputsClient, 0.44, 0.22, 0.125, 0.12, type_entry='entry')

        # district -----------------
        labelDistrict = self.labels(self.frameInputsClient, 'Bairro:', 0.32, 0.36, width=0.16)
        self.districtClientEntry = self.entry(self.frameInputsClient, 0.44, 0.36, 0.2, 0.12, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsClient, 'Cidade:', 0.32, 0.50, width=0.16)
        self.cityClientEntry = self.entry(self.frameInputsClient, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # state -----------------
        labelState = self.labels(self.frameInputsClient, 'Estado:', 0.32, 0.64, width=0.16)
        self.stateClientEntry = self.entry(self.frameInputsClient, 0.44, 0.64, 0.2, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsClient, 'Foto:', 0.32, 0.78, width=0.16, color='#917c3f')
        imageBtn = self.button(
            self.frameInputsClient, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelClient, 'costumer')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsClient, '', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Clientes', photo='costumer'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        self.zipCodeClientEntry.bind('<FocusOut>', lambda e: self.request_adrees(entryPicker()[0][7], entryPicker()[1][8:11]))

        # frame treeview ==================
        self.frameTreeviewClient = self.frame(self.costumersFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'Nascimento', 'CPF', 'Filhos', 'Telefone', 'Cliente desde', 'Endereço', 'CEP', 'Bairro', 'Cidade', 'Estado')
        self.treeviewClient = self.treeview(self.frameTreeviewClient, informationOfTable)
        self.lineTreeviewColor['client'] = 0
        # event bind treeview ==========================================
        self.treeviewClient.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, type_insert='advanced', table='Clientes', photo='costumer'))

        # save last search schedule ===================================
        self.lastSearch['client'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_client(entryPicker()[0], self.treeviewClient),
            'search': lambda: self.search_client(self.treeviewClient, entryPicker()[0]),
            'order': lambda e: self.search_client(self.treeviewClient, entryPicker()[0]),
            'update': lambda: self.update_client(self.treeviewClient, entryPicker()[0], entryPicker()[1]),
            'delete': lambda: self.delete_client(self.treeviewClient),
            'pdf': lambda: self.create_pdf_client(self.treeviewClient),
            'informations': lambda: self.message_informations_clients(self.treeviewClient)
        }
        self.orderBtnClient = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsClient, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsClient.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # string var informations ======================
            entrysGet.insert(3, self.childrenClientBtn.get())
            entrys.insert(3, self.childrenClientBtn)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['costumer'][1])

            # label photo =================================
            entrys.append(self.labelClient)

            # observations informations ====================
            entrysGet.append(self.observationClientEntry.get("1.0", "end-1c"))
            entrys.append(self.observationClientEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnClient.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_client(self.treeviewClient, entryPicker()[0])

    def frame_employers(self):
        # frame photo ==========================================
        self.framePhotoEmployee = self.frame(self.employersFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelProfessional = self.labels(self.framePhotoEmployee, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['employee'][0], position=CENTER)

        # observation --------------------
        self.observationEmployeeEntry = self.text_box(self.employersFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsEmployee = self.frame(self.employersFrame, 0.14, 0.01, 0.855, 0.43)

        # name -------------
        labelName = self.labels(self.frameInputsEmployee, 'Nome:', 0.02, 0.08, width=0.08)
        self.nameEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.08, 0.2, 0.12, type_entry='entry')

        # cpf -------------
        labelcpf = self.labels(self.frameInputsEmployee, 'CPF:', 0.02, 0.22, width=0.15)
        self.cpfEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.22, 0.20, 0.12, type_entry='entry')

        # admissom -------------
        labelAdmisson = self.labels(self.frameInputsEmployee, 'Admissão:', 0.02, 0.36, width=0.15)
        self.admissonEmployeeEntry = self.entry(self.frameInputsEmployee, 0.14, 0.36, 0.16, 0.12, type_entry='date')

        # email -------------
        labelEmail = self.labels(self.frameInputsEmployee, 'E-mail:', 0.02, 0.50, width=0.15)
        self.emailEmployeeEntry = self.entry(self.frameInputsEmployee, 0.1, 0.50, 0.2, 0.12, type_entry='entry')

        # phone -------------
        labelPhone = self.labels(self.frameInputsEmployee, 'Telefone:', 0.02, 0.64, width=0.15)
        self.phonoEmployeeEntry = self.entry(self.frameInputsEmployee, 0.126, 0.64, 0.173, 0.12, type_entry='entry')

        # phone emergency -------------
        labelPhoneEmergency = self.labels(self.frameInputsEmployee, 'Emergência:', 0.02, 0.78, width=0.16)
        self.phoneEmergencyEmployeeEntry = self.entry(self.frameInputsEmployee, 0.14, 0.78, 0.159, 0.12, type_entry='entry')

        # adress -----------------
        labelAdress = self.labels(self.frameInputsEmployee, 'Endereço:', 0.32, 0.08, width=0.16)
        self.adressEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.08, 0.2, 0.12, type_entry='entry')

        # zip code -----------------
        labelZipCode = self.labels(self.frameInputsEmployee, 'CEP:', 0.32, 0.22, width=0.16)
        self.zipCodeEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.22, 0.125, 0.12, type_entry='entry')

        # district -----------------
        labelDistrict = self.labels(self.frameInputsEmployee, 'Bairro:', 0.32, 0.36, width=0.16)
        self.districtEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.36, 0.2, 0.12, type_entry='entry')

        # city -----------------
        labelCity = self.labels(self.frameInputsEmployee, 'Cidade:', 0.32, 0.50, width=0.16)
        self.cityEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # state -----------------
        labelState = self.labels(self.frameInputsEmployee, 'Estado:', 0.32, 0.64, width=0.16)
        self.stateEmployeeEntry = self.entry(self.frameInputsEmployee, 0.44, 0.64, 0.2, 0.12, type_entry='entry')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsEmployee, 'Foto:', 0.32, 0.78, width=0.16, color='#917c3f')
        imageBtn = self.button(
            self.frameInputsEmployee, 'Selecionar imagem', 0.44, 0.78, 0.2, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelProfessional, 'employee')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsEmployee, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Profissional', photo='employee'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frameInputs =========================
        self.zipCodeEmployeeEntry.bind('<FocusOut>', lambda e: self.request_adrees(entryPicker()[0][7], entryPicker()[1][8:11]))

        # frame treeview ==================
        self.frameTreeviewEmployer = self.frame(self.employersFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Nome', 'CPF', 'Admissão', 'E-mail', 'Telefone', 'Emergência', 'Endereço', 'Bairro', 'CEP', 'Cidade', 'Estado')
        self.treeviewEmployer = self.treeview(self.frameTreeviewEmployer, informationOfTable)
        self.lineTreeviewColor['employee'] = 0
        # event bind treeview ==========================================
        self.treeviewEmployer.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewEmployer, type_insert='advanced', table='Profissionais', photo='employee'))

        # save last search schedule ===================================
        self.lastSearch['employee'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_professional(entryPicker()[0], self.treeviewEmployer),
            'search': lambda: self.search_professional(self.treeviewEmployer, entryPicker()[0]),
            'order': lambda e: self.search_professional(self.treeviewEmployer, entryPicker()[0]),
            'update': lambda: self.update_professional(self.treeviewEmployer, entryPicker()[0]),
            'delete': lambda: self.delete_professional(self.treeviewEmployer),
            'pdf': lambda: self.create_pdf_professional(self.treeviewEmployer),
            'informations': lambda: self.message_informations_professional(self.treeviewEmployer)
        }
        self.orderBtnEmployer = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsEmployee, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsEmployee.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['employee'][1])

            # label photo =================================
            entrys.append(self.labelProfessional)

            # observations informations ====================
            entrysGet.append(self.observationEmployeeEntry.get("1.0", "end-1c"))
            entrys.append(self.observationEmployeeEntry)

            # order informations and ==========================
            entrysGet.append(self.orderBtnEmployer.get())
            return [entrysGet, entrys]

        # init search for day ===============================================
        self.search_professional(self.treeviewEmployer, entryPicker()[0])

    def frame_barCode(self):
        # frame photo ==========================================
        self.framePhotoBarCode = self.frame(self.barCodeFrame, 0.02, 0.01, 0.15, 0.3)

        # photo ----------
        self.labelBarCode = self.labels(self.framePhotoBarCode, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['barCode'][0], position=CENTER)

        # observation --------------------
        self.observationBarCodeEntry = self.text_box(self.barCodeFrame, 0.02, 0.32, 0.15, 0.12)

        # frame inputs ==========================================
        self.frameInputsBarCode = self.frame(self.barCodeFrame, 0.175, 0.01, 0.8, 0.43)

        # barcode -------------------
        labelBarCode = self.labels(self.frameInputsBarCode, 'Código:', 0.07, 0.40, width=0.1)
        self.barCodeEntry = self.entry(self.frameInputsBarCode, 0.20, 0.40, 0.2, 0.12, type_entry='entry')

        # button random -------------
        btnRandom = self.button(
            self.frameInputsBarCode, '', 0.422, 0.387, 0.047, 0.145, photo=self.photosAndIcons['random'][0], type_btn='buttonPhoto', background='white',
            function=lambda: [self.barCodeEntry.delete(0, END), self.barCodeEntry.insert(0, randint(100000000000, 999999999999))]
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsBarCode, 'apagar', 0.003, 0.87, 0.04, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewClient, False, type_insert='advanced', table='Código_de_barras', photo='barCode'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewBarCode = self.frame(self.barCodeFrame, 0.02, 0.45, 0.953, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Código', 'Imagem')
        self.treeviewBarCode = self.treeview(self.frameTreeviewBarCode, informationOfTable, max_width=600)
        self.lineTreeviewColor['barCode'] = 0
        # event bind treeview ==========================================
        self.treeviewBarCode.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewBarCode, type_insert='advanced', table='Código_de_barras', photo='barCode', size=(250, 200)))

        # save last search schedule ===================================
        self.lastSearch['barCode'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_barCode(entryPicker()[0], self.treeviewBarCode),
            'search': lambda: self.search_barCode(self.treeviewBarCode, entryPicker()[0]),
            'order': lambda e: self.search_barCode(self.treeviewBarCode, entryPicker()[0]),
            'update': lambda: self.update_barCode(self.treeviewBarCode, entryPicker()[0]),
            'delete': lambda: self.delete_barCode(self.treeviewBarCode),
            'pdf': lambda: self.create_pdf_barCode(self.treeviewBarCode),
            'informations': lambda: self.message_informations_barCode(self.treeviewBarCode)
        }
        self.orderBtnBarCode = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsBarCode, functions, self.photosAndIcons, informationOfTable)

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsBarCode.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # label photo =================================
            entrys.append(self.labelBarCode)

            # observations informations ====================
            entrysGet.append(self.observationBarCodeEntry.get("1.0", "end-1c"))
            entrys.append(self.observationBarCodeEntry)

            # order =============================================
            entrysGet.append(self.orderBtnBarCode.get())

            return [entrysGet, entrys]

        # init search =========================
        self.search_barCode(self.treeviewBarCode, entryPicker()[0])

    def frame_stock_informations(self):
        # Supplier ========================================
        self.typeStockInformations.add(' Fornecedor ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get(), 'supplier'], self.supplier['treeview']
            ),
            'search': lambda: self.search_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'update': lambda: self.update_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get()], typeInformations='supplier'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.supplier['treeview'], ['Fornecedor', self.supplier['entry'].get(), self.supplier['order'].get()], typeInformations='supplier', table='Fornecedor'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.supplier['treeview'], 'Fornecedores'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.supplier['treeview'], 'Fornecedores'
            )
        }
        self.supplier = self.informations_simple(self.typeStockInformations.tab(' Fornecedor '), 'Fornecedor', ('ID', 'Fornecedor'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['supplier'] = 0
        # event bind treeview ==========================================
        self.supplier['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.supplier['entry']], self.supplier['treeview']))
        # save last search schedule ===================================
        self.lastSearch['supplier'] = ''

        # Brand ========================================
        self.typeStockInformations.add(' Marca ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Marca', self.brand['entry'].get(), self.brand['order'].get(), 'brand'], self.brand['treeview']
            ),
            'search': lambda: self.search_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'update': lambda: self.update_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get()], typeInformations='brand'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.brand['treeview'], ['Marca', self.brand['entry'].get(), self.brand['order'].get()], typeInformations='brand', table='Marca'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.brand['treeview'], 'Marcas'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.brand['treeview'], 'Marcas'
            )
        }
        self.brand = self.informations_simple(self.typeStockInformations.tab(' Marca '), 'Marca', ('ID', 'Marca'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['brand'] = 0
        # event bind treeview ==========================================
        self.brand['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.brand['entry']], self.brand['treeview']))
        # save last search schedule ===================================
        self.lastSearch['brand'] = ''

        # Typr ========================================
        self.typeStockInformations.add(' Modelo ')
        functions = {
            'register': lambda: self.register_InformationsStock(['Modelo', self.model['entry'].get(), self.model['order'].get(), 'supplier'], self.model['treeview']),
            'search': lambda: self.search_InformationsStock(
                self.model['treeview'], ['Modelo', self.model['entry'].get(), self.model['order'].get()], typeInformations='model', table='Modelo'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.model['treeview'], ['Modelo', self.model['entry'].get(), self.model['order'].get()], typeInformations='model', table='Modelo'
            ),
            'update': lambda: self.update_InformationsStock(
                self.model['treeview'], ['Modelo', self.model['entry'].get()], typeInformations='model'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.model['treeview'], ['Modelo', self.model['entry'].get(), self.model['order'].get()], typeInformations='model', table='Modelo'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.model['treeview'], 'Modelo'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.supplier['treeview'], 'Modelo'
            )
        }
        self.model = self.informations_simple(self.typeStockInformations.tab(' Modelo '), 'Modelo', ('ID', 'Modelo'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['model'] = 0
        # event bind treeview ==========================================
        self.model['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.model['entry']], self.model['treeview']))
        # save last search schedule ===================================
        self.lastSearch['model'] = ''

        # measure ========================================
        self.typeStockInformations.add(' Peça ')
        functions = {
            'register': lambda: self.register_InformationsStock(
                ['Peça', self.part['entry'].get(), self.part['order'].get(), 'measure'], self.part['treeview']
            ),
            'search': lambda: self.search_InformationsStock(
                self.part['treeview'], ['Peça', self.part['entry'].get(), self.part['order'].get()], typeInformations='part', table='Peça'
            ),
            'order': lambda e: self.search_InformationsStock(
                self.part['treeview'], ['Peça', self.part['entry'].get(), self.part['order'].get()], typeInformations='part', table='Peça'
            ),
            'update': lambda: self.update_InformationsStock(
                self.part['treeview'], ['Peça', self.part['entry'].get()], typeInformations='part'
            ),
            'delete': lambda: self.delete_InformationsStock(
                self.part['treeview'], ['Peça', self.part['entry'].get(), self.part['order'].get()], typeInformations='part', table='Peça'
            ),
            'pdf': lambda: self.create_pdf_InformationsStock(
                self.part['treeview'], 'Peças'
            ),
            'informations': lambda: self.message_informations_InformationsStock(
                self.part['treeview'], 'Peças'
            )
        }
        self.part = self.informations_simple(self.typeStockInformations.tab(' Peça '), 'Peça', ('ID', 'Peça'), functions, self.photosAndIcons, self.image('assets/clear_inputs.png', (26, 26))[0])
        self.lineTreeviewColor['part'] = 0
        # event bind treeview ==========================================
        self.part['treeview'].bind("<Double-Button-1>", lambda e: self.insert_informations_entrys([self.part['entry']], self.part['treeview']))

        # save last search schedule ===================================
        self.lastSearch['part'] = ''

        # init search for day ===============================================
        self.search_init()

    def frame_users(self):
        # frame inputs =========================================
        self.frameInputsUsers = self.frame(self.userFrame, 0.195, 0.01, 0.6, 0.43)

        # user --------------------
        labelUser = self.labels(self.frameInputsUsers, 'Usuário:', 0.07, 0.25, width=0.1)
        self.userEntry = self.entry(self.frameInputsUsers, 0.20, 0.25, 0.23, 0.12, type_entry='entry')

        # password -------------------
        labelPassword = self.labels(self.frameInputsUsers, 'Senha:', 0.07, 0.45, width=0.1)
        self.passwordEntry = self.entry(self.frameInputsUsers, 0.20, 0.45, 0.23, 0.12, type_entry='entry')

        # level -------------------
        labelLevel = self.labels(self.frameInputsUsers, 'Nivel:', 0.07, 0.65, width=0.1)
        self.levelEntry = self.entry(
            self.frameInputsUsers, 0.20, 0.65, 0.23, 0.12, type_entry='list',
            value=['ADMINISTRADOR', 'USUÀRIO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsUsers, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewUsers = self.frame(self.userFrame, 0.195, 0.45, 0.6, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Usuário', 'Senha', 'Nivel')
        self.treeviewUsers = self.treeview(self.frameTreeviewUsers, informationOfTable, max_width=380)
        self.lineTreeviewColor['users'] = 0
        # event bind treeview ==========================================
        self.treeviewUsers.bind("<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewUsers))

        # save last search schedule ===================================
        self.lastSearch['users'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'search': lambda: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'order': lambda e: self.search_users(self.treeviewUsers, entryPicker()[0]),
            'update': lambda: self.password_window(self.update_users, {'treeview': self.treeviewUsers, 'informatons': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_users, {'treeview': self.treeviewUsers})
        }
        self.buttons = self.tab_of_buttons(0.49, 0.02, 0.45, 0.9, self.frameInputsUsers, functions, self.photosAndIcons, informationOfTable, treeview='no')

        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsUsers.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)
            return [entrysGet, entrys]

    # =================================  stock configuration  ======================================
    def frame_sale_inventory_control(self):
        # frame photo ==========================================
        self.framePhotoSaleInventoryControl = self.frame(self.mainStockFrame, 0.005, 0.01, 0.13, 0.3)

        # photo ----------
        self.labelSaleProduct = self.labels(self.framePhotoSaleInventoryControl, '', 0.009, 0.01, width=0.98, height=0.98, photo=self.photosAndIcons['product'][0], position=CENTER)

        # observation --------------------
        self.observationSaleinventoryControlEntry = self.text_box(self.mainStockFrame, 0.005, 0.32, 0.13, 0.12)

        # frame inputs ==========================================
        self.frameInputsSaleInventoryControl = self.frame(self.mainStockFrame, 0.14, 0.01, 0.855, 0.43)

        # supplier -------------
        labelSupplier = self.labels(self.frameInputsSaleInventoryControl, 'Fornecedor:', 0.02, 0.12, width=0.12)
        self.supplierSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.12, 0.18, 0.12, type_entry='list')

        # brand -------------
        labelBrand = self.labels(self.frameInputsSaleInventoryControl, 'Marca:', 0.02, 0.26, width=0.15)
        self.brandSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.26, 0.18, 0.12, type_entry='list')

        # model -------------
        labelModel = self.labels(self.frameInputsSaleInventoryControl, 'Modelo:', 0.02, 0.40, width=0.15)
        self.modelSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.40, 0.18, 0.12, type_entry='list')

        # part -------------
        labelPart = self.labels(self.frameInputsSaleInventoryControl, 'Peça:', 0.02, 0.54, width=0.15)
        self.partSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.54, 0.18, 0.12, type_entry='list')

        # quantity -------------
        labelQuantity = self.labels(self.frameInputsSaleInventoryControl, 'Quantidade:', 0.02, 0.68, width=0.15)
        self.QuantitySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.14, 0.68, 0.18, 0.12, type_entry='entry')

        # buy -----------------
        labelBuy = self.labels(self.frameInputsSaleInventoryControl, 'V/compra:', 0.34, 0.12, width=0.16)
        self.buySaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.12, 0.18, 0.12, type_entry='entry')

        # sale -----------------
        labelsale = self.labels(self.frameInputsSaleInventoryControl, 'V/venda:', 0.34, 0.26, width=0.16)
        self.saleInputsSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.26, 0.18, 0.12, type_entry='entry')

        # barcode -----------------
        labelBarcode = self.labels(self.frameInputsSaleInventoryControl, 'Código:', 0.34, 0.40, width=0.16)
        self.barcodeSaleInventoryControlEntry = self.entry(self.frameInputsSaleInventoryControl, 0.46, 0.40, 0.18, 0.12, type_entry='list')

        # selection image ---------
        labelPhoto = self.labels(self.frameInputsSaleInventoryControl, 'Foto:', 0.34, 0.54, width=0.16, color='#917c3f')
        imageBtn = self.button(
            self.frameInputsSaleInventoryControl, 'Selecionar imagem', 0.46, 0.54, 0.18, 0.12, photo=self.photosAndIcons['image'][0],
            function=lambda: self.pick_picture(self.labelSaleProduct, 'product')
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsSaleInventoryControl, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewStockControl, False, type_insert='advanced', table='Produtos', photo='productSale', data_base='informations'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of inputs ====================

        # frame treeview ==================
        self.frameTreeviewSaleInventoryControl = self.frame(self.mainStockFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Fornecedor', 'Marca', 'Modelo', 'Peça', 'Quantidade', 'V/Compra', 'V/Venda', 'Código')
        self.treeviewStockControl = self.treeview(self.frameTreeviewSaleInventoryControl, informationOfTable)
        self.lineTreeviewColor['product'] = 0
        # event bind treeview ==========================================
        self.treeviewStockControl.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewStockControl, type_insert='advanced', table='Produtos', photo='product', data_base='stock')
        )

        # save last search schedule ===================================
        self.lastSearch['product'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.register_stock(entryPicker()[0], self.treeviewStockControl),
            'search': lambda: self.search_stock(self.treeviewStockControl, entryPicker()[0]),
            'order': lambda e: self.search_stock(self.treeviewStockControl, entryPicker()[0]),
            'update': lambda: self.update_stock(self.treeviewStockControl, entryPicker()[0]),
            'delete': lambda: self.delete_stock(self.treeviewStockControl),
            'pdf': lambda: self.create_pdf_stock(self.treeviewStockControl),
            'informations': lambda: self.message_informations_stock(self.treeviewStockControl)
        }
        self.orderBtnSaleIventoryControl = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsSaleInventoryControl, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsSaleInventoryControl.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # directory photo =======================
            entrysGet.append(self.photosAndIcons['product'][1])

            # label photo =================================
            entrys.append(self.labelSaleProduct)

            # observations informations ====================
            entrysGet.append(self.observationSaleinventoryControlEntry.get("1.0", "end-1c"))
            entrys.append(self.observationSaleinventoryControlEntry)

            # order =============================================
            entrysGet.append(self.orderBtnSaleIventoryControl.get())
            return [entrysGet, entrys]

        # init search =================================
        self.search_stock(self.treeviewStockControl, entryPicker()[0])

    # ================================== cash register configuration ===============================

    def frame_cash_register_management_day(self):

        # frame inputs ==========================================
        self.frameInputsCashDay = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashDayEntry = self.text_box(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.005, 0.01, 0.13, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashDay, 'T/Cliente:', 0.02, 0.08, width=0.12)
        self.customDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.08, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashDay, 'T/Cartão:', 0.02, 0.22, width=0.15)
        self.cardDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.22, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashDay, 'T/Dinheiro:', 0.02, 0.36, width=0.15)
        self.moneyDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.36, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashDay, 'T/Transferência:', 0.02, 0.50, width=0.15)
        self.transferDayEntry = self.entry(self.frameInputsCashDay, 0.17, 0.50, 0.15, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashDay, 'T/Nota:', 0.02, 0.64, width=0.16)
        self.noteDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.64, 0.18, 0.12, type_entry='entry')

        # to receive -----------------
        labelToReceive = self.labels(self.frameInputsCashDay, 'A receber:', 0.02, 0.78, width=0.16)
        self.toReceivedDayEntry = self.entry(self.frameInputsCashDay, 0.14, 0.78, 0.18, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashDay, 'T/Recebido:', 0.34, 0.08, width=0.16)
        self.receivedDayEntry = self.entry(self.frameInputsCashDay, 0.45, 0.08, 0.19, 0.12, type_entry='entry')

        # date -----------------
        labelDate = self.labels(self.frameInputsCashDay, 'Data:', 0.34, 0.22, width=0.16)
        self.dateDayEntry = self.entry(self.frameInputsCashDay, 0.44, 0.22, 0.14, 0.12, type_entry='date', validity='yes')

        # status -----------------
        labelStatus = self.labels(self.frameInputsCashDay, 'Status:', 0.34, 0.36, width=0.16, color='#917c3f')
        self.statusDayEntry = self.entry(
            self.frameInputsCashDay, 0.44, 0.36, 0.2, 0.12, type_entry='list',
            value=['DIA EM ANDAMENTO', 'DIA FINALIZADO']
        )

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashDay, 'Saida:', 0.34, 0.50, width=0.16, color='#917c3f')
        self.exitDayEntry = self.entry(self.frameInputsCashDay, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashDay, 'M/Saida:', 0.34, 0.64, width=0.16, color='#917c3f')
        self.MetodyExitDayEntry = self.entry(
            self.frameInputsCashDay, 0.44, 0.64, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashDay, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDay, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashDay, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: self.password_window(self.pick_informations_for_cash, {'entrys': entryPicker()[1], 'date': self.dateDayEntry.get()}),
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashDay, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashDay, self.lineTreeviewColor['cashDay']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # frame treeview ==================
        self.frameTreeviewCashDay = self.frame(self.typeCashManagement.tab(' Gerenciamento do dia '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'T/Clientes', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'A receber', 'T/Recebido', 'Data', 'Status')
        self.treeviewCashDay = self.treeview(self.frameTreeviewCashDay, informationOfTable)
        self.lineTreeviewColor['cashDay'] = 0
        # event bind treeview ==========================================
        self.treeviewCashDay.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashDay, type_insert='advanced', table='Gerenciamento_do_dia', data_base='cash')
        )

        # save last search schedule ===================================
        self.lastSearch['cashDay'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashDay,
                    'parameters': {
                        'sqlRegister': registerCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data'
                    }
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data'
                    }
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data'
                    }
                }
            ),
            'update': lambda: self.password_window(
                self.update_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateCashManagement,
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data'
                    }
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data'
                    }
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'parameters': {
                        'tablePart1': tableWithInformationsCashManagementTreeview1,
                        'tablePart2': tableWithInformationsCashManagementTreeview2,
                        'supplementaryTable': tableWithInformationsComplementaryCashManagement,
                        'table': 'Gerenciamento_do_dia',
                        'type_cash': 'cashDay',
                        'typeDate': 'data',
                        'type_message': 'Dias'
                    }
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashDay,
                    'parameters': {
                        'type_message': 'Dias'
                    }
                }
            ),
        }
        self.orderBtnDay = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashDay, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashDay.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashDayEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashDayEntry)

            # order =============================================
            entrysGet.append(self.orderBtnDay.get())
            return [entrysGet, entrys]

        # init search =============================
        self.search_cashManagement(
            self.treeviewCashDay,
            self.searching_list('', 11, 'ID'),
            parameters={
                'type_cash': 'cashDay',
                'table': 'Gerenciamento_do_dia',
                'typeDate': 'data'
            },
            insert=False
        )

    def frame_cash_register_management_month(self):
        # frame inputs ==========================================
        self.frameInputsCashMonth = self.frame(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashMonthEntry = self.text_box(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.005, 0.01, 0.13, 0.43)

        # Custom -------------
        labelCustom = self.labels(self.frameInputsCashMonth, 'T/Clientes:', 0.02, 0.08, width=0.12)
        self.customMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.08, 0.18, 0.12, type_entry='entry')

        # card -------------
        labelCard = self.labels(self.frameInputsCashMonth, 'T/Cartão:', 0.02, 0.22, width=0.15)
        self.cardMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.22, 0.18, 0.12, type_entry='entry')

        # money -------------
        labelMoney = self.labels(self.frameInputsCashMonth, 'T/Dinheiro:', 0.02, 0.36, width=0.15)
        self.moneyMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.36, 0.18, 0.12, type_entry='entry')

        # tranfer -------------
        labelTransfer = self.labels(self.frameInputsCashMonth, 'T/Transferência:', 0.02, 0.50, width=0.15)
        self.transferMonthEntry = self.entry(self.frameInputsCashMonth, 0.17, 0.50, 0.15, 0.12, type_entry='entry')

        # note -------------
        labelNote = self.labels(self.frameInputsCashMonth, 'T/Nota:', 0.02, 0.64, width=0.16)
        self.noteMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.64, 0.18, 0.12, type_entry='entry')

        # total exit -----------------
        labelToReceive = self.labels(self.frameInputsCashMonth, 'A receber:', 0.02, 0.78, width=0.16)
        self.toReceiveMonthEntry = self.entry(self.frameInputsCashMonth, 0.14, 0.78, 0.18, 0.12, type_entry='entry')

        # received -----------------
        labelReceived = self.labels(self.frameInputsCashMonth, 'T/Recebido:', 0.34, 0.08, width=0.16)
        self.receivedMonthEntry = self.entry(self.frameInputsCashMonth, 0.45, 0.08, 0.19, 0.12, type_entry='entry')

        # month -----------------
        labelMonth = self.labels(self.frameInputsCashMonth, 'Mês:', 0.34, 0.22, width=0.16)
        self.dateMonthEntry = self.entry(self.frameInputsCashMonth, 0.44, 0.22, 0.14, 0.12, type_entry='date', validity='yes')
        self.dateMonthEntry.delete(0, END)
        self.dateMonthEntry.insert(0, datetime.today().strftime("%m/%Y"))

        # status -----------------
        labelStatus = self.labels(self.frameInputsCashMonth, 'Status:', 0.34, 0.36, width=0.16, color='#917c3f')
        self.statusMonthEntry = self.entry(
            self.frameInputsCashMonth, 0.44, 0.36, 0.2, 0.12, type_entry='list',
            value=['MÊS EM ANDAMENTO', 'MÊS FINALIZADO']
        )

        # exit -----------------
        labelExit = self.labels(self.frameInputsCashMonth, 'Saida:', 0.34, 0.50, width=0.16, color='#917c3f')
        self.exitMonthEntry = self.entry(self.frameInputsCashMonth, 0.44, 0.50, 0.2, 0.12, type_entry='entry')

        # metody exit -----------------
        labelMetodyExit = self.labels(self.frameInputsCashMonth, 'M/Saida:', 0.34, 0.64, width=0.16, color='#917c3f')
        self.metodyExitMonthEntry = self.entry(
            self.frameInputsCashMonth, 0.44, 0.64, 0.2, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashMonth, '', 0.003, 0.87, 0.04, 0.12,
            function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # cash flow -------------
        cashFlow = self.button(
            self.frameInputsCashMonth, '', 0.05, 0.87, 0.04, 0.10,
            function=lambda: self.password_window(self.pick_informations_for_cash, {'entrys': entryPicker()[1], 'date': self.dateMonthEntry.get(), 'type': 'month'}),
            photo=self.image('assets/icon_cashFlow.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashMonth, '', 0.1, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashMonth, self.lineTreeviewColor['cashMonth']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind of frame inputs ========================
        self.dateMonthEntry.bind(
            '<<DateEntrySelected>>',
            lambda e: self.dateMonthEntry.delete(0, 3)
        )
        self.dateMonthEntry.bind('<FocusOut>', lambda e: self.dateMonthEntry.delete(0, 3) if len(self.dateMonthEntry.get()) > 7 else '')

        # frame treeview ==================
        self.frameTreeviewCashMonth = self.frame(self.typeCashManagement.tab(' Gerenciamento do mês '), 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'T/Clientes', 'T/Cartão', 'T/Dinheiro', 'T/Transferência', 'T/nota', 'S/Cartão', 'S/Dinheiro', 'S/Transferência', 'S/Nota', 'A receber', 'T/Recebido', 'Mês', 'Status')
        self.treeviewCashMonth = self.treeview(self.frameTreeviewCashMonth, informationOfTable)
        self.lineTreeviewColor['cashMonth'] = 0
        # event bind treeview ==========================================
        self.treeviewCashMonth.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashMonth, type_insert='advanced', table='Gerenciamento_do_mês', data_base='cash')
        )

        # save last search schedule ===================================
        self.lastSearch['cashMonth'] = ''

        functions = {
            'register': lambda: self.password_window(
                self.register_cashManagement, {
                    'informations': entryPicker()[0],
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'sqlRegister': registerCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'search': lambda: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'order': lambda e: self.password_window(
                self.search_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'update': lambda: self.password_window(
                self.update_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'informations': entryPicker()[0],
                    'parameters': {
                        'sqlUpdate': updateCashManagement,
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'delete': lambda: self.password_window(
                self.delete_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'sqlSearch': searchCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês'
                    }
                }
            ),
            'pdf': lambda: self.password_window(
                self.create_pdf_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'tablePart1': tableWithInformationsCashManagementTreeview1,
                        'tablePart2': tableWithInformationsCashManagementTreeview2,
                        'supplementaryTable': tableWithInformationsComplementaryCashManagement,
                        'table': 'Gerenciamento_do_mês',
                        'type_cash': 'cashMonth',
                        'typeDate': 'mês',
                        'type_message': 'Meses'
                    }
                }
            ),
            'informations': lambda: self.password_window(
                self.message_informations_cashManagement, {
                    'treeview': self.treeviewCashMonth,
                    'parameters': {
                        'type_message': 'Meses'
                    }
                }
            ),
        }
        self.orderBtnMonth = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashMonth, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashMonth.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashMonthEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashMonthEntry)

            # order =============================================
            entrysGet.append(self.orderBtnMonth.get())
            return [entrysGet, entrys]

        # init search =============================
        self.search_cashManagement(
            self.treeviewCashMonth,
            self.searching_list('', 11, 'ID'),
            parameters={
                'type_cash': 'cashMonth',
                'table': 'Gerenciamento_do_mês',
                'typeDate': 'mês'
            },
            insert=False
        )

    def frame_pay_management(self):
        # frame inputs ==========================================
        self.frameInputsCashPay = self.frame(self.employersPayFrame, 0.14, 0.01, 0.855, 0.43)

        # observation --------------------
        self.observationCashPayEntry = self.text_box(self.employersPayFrame, 0.005, 0.01, 0.13, 0.43)

        # employee -------------
        labelEmployee = self.labels(self.frameInputsCashPay, 'Profissional:', 0.02, 0.22, width=0.12)
        self.employeeCashPayEntry = self.entry(
            self.frameInputsCashPay, 0.14, 0.22, 0.18, 0.12, type_entry='list',
            function=lambda e: self.pick_informations_for_payment(entryPicker()[1], professional=self.employeeCashPayEntry.get(), date=self.monthCashPayEntry.get())
        )

        # Date -------------
        labelMonth = self.labels(self.frameInputsCashPay, 'Mês/P:', 0.02, 0.36, width=0.15)
        self.monthCashPayEntry = self.entry(self.frameInputsCashPay, 0.14, 0.36, 0.14, 0.12, type_entry='date', validity='yes')
        self.monthCashPayEntry.delete(0, END)
        self.monthCashPayEntry.insert(0, datetime.today().strftime("%m/%Y"))

        # custom -------------
        labelCustom = self.labels(self.frameInputsCashPay, 'T/Clientes:', 0.02, 0.50, width=0.15)
        self.customCashPayEntry = self.entry(self.frameInputsCashPay, 0.14, 0.50, 0.18, 0.12, type_entry='entry')

        # invoicing -------------
        labelInvoicing = self.labels(self.frameInputsCashPay, 'Faturamento:', 0.02, 0.64, width=0.15)
        self.invoicingCashPayEntry = self.entry(self.frameInputsCashPay, 0.15, 0.64, 0.17, 0.12, type_entry='entry')

        # percentage -------------
        labelPercentage = self.labels(self.frameInputsCashPay, 'Porcentagem:', 0.34, 0.22, width=0.15)
        self.percentageCashPayEntry = self.entry(self.frameInputsCashPay, 0.47, 0.22, 0.17, 0.12, type_entry='entry')

        # payment -------------
        labelPayment = self.labels(self.frameInputsCashPay, 'Pagamento:', 0.34, 0.36, width=0.16)
        self.paymentCashPayEntry = self.entry(self.frameInputsCashPay, 0.47, 0.36, 0.17, 0.12, type_entry='entry')

        # method paymant -----------------
        labelMethodPayment = self.labels(self.frameInputsCashPay, 'M/Pagamento:', 0.34, 0.50, width=0.16)
        self.metohPaymentCashPayEntry = self.entry(
            self.frameInputsCashPay, 0.47, 0.50, 0.17, 0.12, type_entry='list',
            value=['DINHEIRO', 'CARTÃO', 'TRANSFERÊNCIA', 'NOTA', 'SEM PAGAMENTO']
        )

        # delete informations -------------
        deleteInformationsInputs = self.button(
            self.frameInputsCashPay, 'apagar', 0.003, 0.87, 0.05, 0.12, function=lambda: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashPayment, False, type_insert='advanced'),
            photo=self.image('assets/clear_inputs.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # clearTreeview -------------
        clear = self.button(
            self.frameInputsCashPay, '', 0.05, 0.87, 0.04, 0.11,
            function=lambda: self.delete_informations_treeview(self.treeviewCashPayment, self.lineTreeviewColor['cashPayment']),
            photo=self.image('assets/clear_treeview.png', (26, 26))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # event bind frame inputs ==========================================
        self.monthCashPayEntry.bind(
            '<<DateEntrySelected>>',
            lambda e: [
                self.monthCashPayEntry.delete(0, 3),
                self.pick_informations_for_payment(entryPicker()[1], professional=self.employeeCashPayEntry.get(), date=self.monthCashPayEntry.get())
            ]
        )
        self.monthCashPayEntry.bind(
            '<FocusOut>',
            lambda e: [
                self.monthCashPayEntry.delete(0, 3) if len(self.monthCashPayEntry.get()) > 7 else '',
                self.pick_informations_for_payment(entryPicker()[1], professional=self.employeeCashPayEntry.get(), date=self.monthCashPayEntry.get())
            ]
        )
        self.percentageCashPayEntry.bind(
            '<FocusOut>',
            lambda e: [
                self.paymentCashPayEntry.delete(0, END),
                self.paymentCashPayEntry.insert(0, self.calculing_percentage_for_payment(self.invoicingCashPayEntry.get(), self.percentageCashPayEntry.get()))
            ]
        )

        # frame treeview ==================
        self.frameTreeviewCashPay = self.frame(self.employersPayFrame, 0.005, 0.45, 0.989, 0.53)

        # Treeview -----------------------------------------------------
        informationOfTable = ('ID', 'Profissional', 'Mês de pagamento', 'T/Clientes', 'Faturamento', 'Porcentagem', 'Pagamento', 'Método de pagamento', 'Data de pagamento')
        self.treeviewCashPayment = self.treeview(self.frameTreeviewCashPay, informationOfTable)
        self.lineTreeviewColor['cashPayment'] = 0
        # event bind treeview ==========================================
        self.treeviewCashPayment.bind(
            "<Double-Button-1>", lambda e: self.insert_informations_entrys(entryPicker()[1], self.treeviewCashPayment, type_insert='advanced', table='Gerenciador_de_pagamentos', data_base='cash')
        )

        # save last search schedule ===================================
        self.lastSearch['cashPayment'] = ''

        # buttons management ============
        functions = {
            'register': lambda: self.password_window(self.register_payment, {'informationa': entryPicker()[0], 'treeviw': self.treeviewCashPayment}),
            'search': lambda: self.password_window(self.search_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'order': lambda e: self.password_window(self.search_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'update': lambda: self.password_window(self.update_payment, {'treeview': self.treeviewCashPayment, 'informations': entryPicker()[0]}),
            'delete': lambda: self.password_window(self.delete_payment, {'treeview': self.treeviewCashPayment}),
            'pdf': lambda: self.password_window(self.create_pdf_payment, {'treeview': self.treeviewCashPayment}),
            'informations': lambda: self.password_window(self.message_informations_payment, {'treeview': self.treeviewCashPayment})
        }
        self.orderBtnPay = self.tab_of_buttons(0.675, 0.02, 0.3, 0.9, self.frameInputsCashPay, functions, self.photosAndIcons, informationOfTable)

        # pick up entrys ==========================
        def entryPicker():
            entrysGet = []
            entrys = []
            # entrys of frameInputs =============================
            for widget in self.frameInputsCashPay.winfo_children():
                if isinstance(widget, CTkComboBox) or isinstance(widget, DateEntry) or isinstance(widget, CTkEntry):
                    entrysGet.append(widget.get())
                    entrys.append(widget)

            # observations informations ====================
            entrysGet.append(self.observationCashPayEntry.get("1.0", "end-1c"))
            entrys.append(self.observationCashPayEntry)

            # order =============================================
            entrysGet.append(self.orderBtnPay.get())
            return [entrysGet, entrys]

        # init search ===========================================
        self.search_payment(self.treeviewCashPayment, self.searching_list('', 7, 'ID'), insert=False)

    # ================================== cash register configuration ===============================

    def frame_costumization_buttons(self):
        # buttons -------------------------
        self.frameForButtons = self.frame(self.frameForCostumizations, 0.02, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Botões')
        # -> background
        background = self.labels(self.frameForButtons, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForButtons, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForButtons, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForButtons, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForButtons, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForButtons, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForButtons, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForButtons, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForButtons, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> hover color
        hoverColor = self.labels(self.frameForButtons, 'Cor do hover:', 0.03, 0.54, 0.5, 0.1, size=13)
        colorHvEntry = self.entry(self.frameForButtons, 0.4, 0.54, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerHv = self.button(
            self.frameForButtons, '', 0.7, 0.51, 0.15, 0.17,
            function=lambda: self.colorPicker(Btn, 'hover_color', colorHvEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'border_color', colorBdEntry, color_picker='no'))
        colorHvEntry.bind('<Return>', lambda e: self.colorPicker(Btn, 'hover_color', colorHvEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForButtons, 0.03, 0.67)

        # demonstrative button ---------------------
        Btn = self.button(self.frameForButtons, 'Texto', 0.18, 0.78, 0.6, 0.2)

    def frame_costumization_frames(self):
        # buttons -------------------------
        self.frameForFrames = self.frame(self.frameForCostumizations, 0.02, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Frames')

        # -> background
        background = self.labels(self.frameForFrames, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForFrames, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForFrames, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForFrames, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForFrames, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForFrames, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(frame, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(frame, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForFrames, 0.03, 0.35)

        # demonstrative frame ---------------------
        frame = self.frame(self.frameForFrames, 0.14, 0.475, 0.67, 0.5)

    def frame_costumization_tabview(self):
        # buttons -------------------------
        self.frameForTabview = self.frame(self.frameForCostumizations, 0.38, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Tabview')

        # -> background
        background = self.labels(self.frameForTabview, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForTabview, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTabview, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> border
        border = self.labels(self.frameForTabview, 'Cor da borda:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForTabview, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTabview, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(tabview, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'fg_color', colorBgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(tabview, 'border_color', colorBdEntry, color_picker='no'))

        # demonstrative tabview ---------------------
        tabview = self.tabview(self.frameForTabview, 0.14, 0.4, 0.67, 0.55)

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForTabview, 0.03, 0.35)

    def frame_costumization_treeview(self):
        # buttons -------------------------
        self.frameForTreeview = self.frame(self.frameForCostumizations, 0.38, 0.35, 0.2, 0.4, border_color='#d2d2d2', type_frame='labelFrame', text='Tabela')

        # -> line1
        line1 = self.labels(self.frameForTreeview, 'Cor da linha 1:', 0.03, 0.03, 0.5, 0.06, size=13)
        colorL1Entry = self.entry(self.frameForTreeview, 0.4, 0.027, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForTreeview, '', 0.7, 0.001, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag1', colorL1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> line2
        line2 = self.labels(self.frameForTreeview, 'Cor da linha 2:', 0.03, 0.15, 0.5, 0.06, size=13)
        colorL2Entry = self.entry(self.frameForTreeview, 0.4, 0.15, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForTreeview, '', 0.7, 0.12, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'tag2', colorL2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # -> text color
        textColor = self.labels(self.frameForTreeview, 'Cor de texto:', 0.03, 0.27, 0.5, 0.06, size=13)
        colorFgEntry = self.entry(self.frameForTreeview, 0.4, 0.27, 0.3, 0.08, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForTreeview, '', 0.7, 0.24, 0.15, 0.13,
            function=lambda: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorL1Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag1', colorL1Entry, color_picker='no'))
        colorL2Entry.bind('<Return>', lambda e: self.colorPicker(treeview, 'tag2', colorL2Entry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(treeview, 'text_color_treeview', colorFgEntry, color_picker='no'))

        # demonstrative treeview ---------------------
        frameTreeview = self.frame(self.frameForTreeview, 0.02, 0.4, 0.97, 0.5, border_color='#d2d2d2')
        treeview = self.treeview(frameTreeview, ['informação 1'])
        self.lineTreeviewColor['demonstrative'] = 0
        self.insert_treeview_informations(treeview, ['Linha 1', 'linha2'], 'demonstrative')

    def frame_costumization_entrys(self):
        # buttons -------------------------
        self.frameForEntrys = self.frame(self.frameForCostumizations, 0.77, 0.02, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Entradas de texto')
        # -> background
        background = self.labels(self.frameForEntrys, 'Cor de fundo:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorBgEntry = self.entry(self.frameForEntrys, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBg = self.button(
            self.frameForEntrys, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'fg_color', colorBgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        textColor = self.labels(self.frameForEntrys, 'Cor do texto:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFgEntry = self.entry(self.frameForEntrys, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg = self.button(
            self.frameForEntrys, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'text_color', colorFgEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )
        # -> text color
        borderColor = self.labels(self.frameForEntrys, 'Cor da borda:', 0.03, 0.37, 0.5, 0.1, size=13)
        colorBdEntry = self.entry(self.frameForEntrys, 0.4, 0.37, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerBd = self.button(
            self.frameForEntrys, '', 0.7, 0.34, 0.15, 0.17,
            function=lambda: self.colorPicker(entry, 'border_color', colorBdEntry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorBgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'fg_color', colorBgEntry, color_picker='no'))
        colorFgEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'text_color', colorFgEntry, color_picker='no'))
        colorBdEntry.bind('<Return>', lambda e: self.colorPicker(entry, 'border_color', colorBdEntry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForEntrys, 0.03, 0.54)

        # demonstrative button ---------------------
        entry = self.entry(self.frameForEntrys, 0.18, 0.70, 0.6, 0.2, type_entry='entry')
        entry.insert(0, 'Texto')

    def frame_costumization_labels(self):
        # buttons -------------------------
        self.frameForLabels = self.frame(self.frameForCostumizations, 0.77, 0.4, 0.2, 0.3, border_color='#d2d2d2', type_frame='labelFrame', text='Textos')

        # -> text color
        text1 = self.labels(self.frameForLabels, 'Cor de texto 1:', 0.03, 0.03, 0.5, 0.1, size=13)
        colorFg1Entry = self.entry(self.frameForLabels, 0.4, 0.027, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg1 = self.button(
            self.frameForLabels, '', 0.7, 0.001, 0.15, 0.17,
            function=lambda: self.colorPicker(text1, 'text_color', colorFg1Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        text2 = self.labels(self.frameForLabels, 'Cor de texto 2:', 0.03, 0.2, 0.5, 0.1, size=13)
        colorFg2Entry = self.entry(self.frameForLabels, 0.4, 0.2, 0.3, 0.13, type_entry='entry', border_color='#d2d2d2', font_size=12)
        colorPickerFg2 = self.button(
            self.frameForLabels, '', 0.7, 0.17, 0.15, 0.17,
            function=lambda: self.colorPicker(text2, 'text_color', colorFg2Entry),
            photo=self.image('assets/icon_colorPicker.png', (20, 20))[0], type_btn='buttonPhoto', background='white', hover_cursor='white'
        )

        # events bind ==========================
        colorFg1Entry.bind('<Return>', lambda e: self.colorPicker(text1, 'text_color', colorFg1Entry, color_picker='no'))
        colorFg2Entry.bind('<Return>', lambda e: self.colorPicker(text2, 'text_color', colorFg2Entry, color_picker='no'))

        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForLabels, 0.03, 0.35)

        # demonstrative labels ---------------------
        text1 = self.labels(self.frameForLabels, 'Texto 1', 0.33, 0.5, 0.3, 0.2)
        text2 = self.labels(self.frameForLabels, 'Texto 2', 0.33, 0.75, 0.3, 0.2, custom='optional')

    def save(self):
        # line separator higher --------------------
        lineHigher = self.line_separator(self.frameForCostumizations, 0.02, 0.8, width=0.95)

        # demonstrative labels ---------------------
        text1 = self.button(self.frameForCostumizations, 'Salvar', 0.75, 0.86, 0.2, 0.1, function=lambda: self.save_configs())


if __name__ == '__main__':
    app = Aplication()
