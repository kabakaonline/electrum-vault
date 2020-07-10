from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QComboBox

from .send_tab import AlertTransactionListWidget
from .util import read_QIcon
from .main_window import ElectrumWindow
from electrum.i18n import _
from ... import bitcoin
from ...transaction import PartialTxOutput
from ...util import bfh


class ElectrumARWindow(ElectrumWindow):
    def __init__(self, gui_object: 'ElectrumGui', wallet: 'Abstract_Wallet'):
        super().__init__(gui_object=gui_object, wallet=wallet)
        self.recovery_tab = self.create_recovery_tab()
        # todo add proper icon
        self.tabs.addTab(self.recovery_tab, read_QIcon("tab_send.png"), _('Recovery'))

    def create_recovery_tab(self):
        # todo finish development
        layout = QVBoxLayout()
        label = QLabel(_('Alert transaction to recovery'))
        layout.addWidget(label)

        combo_box = QComboBox()
        combo_box.addItems([
            'alert',
            'recovery',
        ])

        layout.addWidget(combo_box)

        widget = AlertTransactionListWidget(parent=self)
        widget.setLayout(layout)

        button = QPushButton('Recovery')
        button.clicked.connect(self.do_recovery)
        layout.addWidget(button)

        return widget

    def _get_recovery_output(self, tx, address):
        scriptpubkey = bfh(bitcoin.address_to_script(address))
        value = 0
        for txout in tx.outputs():
            value += txout.value
        return PartialTxOutput(scriptpubkey=scriptpubkey, value=value)

    def do_recovery(self):
        # todo add password validation
        password = None
        address = '2MtgzTDFJJcgQQF7awK8SofcBGyEuRutApw'
        atx = self.wallet.get_atx_list()
        self.wallet.set_recovery()
        self.wallet.prepare_and_sign_recovery_transaction(self, atx, address, recovery_privkey='', password='')

    def show_recovery_tab(self):
        self.tabs.setCurrentIndex(self.tabs.indexOf(self.recovery_tab))
