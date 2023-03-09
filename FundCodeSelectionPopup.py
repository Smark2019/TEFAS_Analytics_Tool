from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QHBoxLayout


class FundCodeSelectionPopup(QDialog):
    def __init__(self, fund_codes):
        super().__init__()
        self.fund_codes = fund_codes
        self.selected_fund_codes = []
        self.setWindowTitle('Select Fund Codes')
        self.setFixedSize(300, 400)

        # create layout for main widget
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # create search box
        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.textChanged.connect(lambda: self.filter_fund_codes(fund_codes_list, search_box.text()))
        search_layout.addWidget(search_box)
        main_layout.addLayout(search_layout)

        # create list widget for fund codes
        fund_codes_list = QListWidget()
        for fund_code in fund_codes:
            item = QListWidgetItem(fund_code)
            fund_codes_list.addItem(item)
        fund_codes_list.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(fund_codes_list)

        # create button to confirm selection
        select_button = QPushButton('Select')
        select_button.clicked.connect(lambda: self.select_fund_codes(fund_codes_list))
        main_layout.addWidget(select_button)

    def select_fund_codes(self, fund_codes_list):
        selected_items = fund_codes_list.selectedItems()
        self.selected_fund_codes = [item.text() for item in selected_items]
        self.accept()

    def filter_fund_codes(self, fund_codes_list, search_text):
        for i in range(fund_codes_list.count()):
            item = fund_codes_list.item(i)
            if search_text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)


if __name__ == '__main__':
    app = QApplication([])
    fund_codes = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZ']
    popup = FundCodeSelectionPopup(fund_codes)
    if popup.exec_() == QDialog.Accepted:
        print('Selected Fund Codes:', popup.selected_fund_codes)

