import os
import sys
import pyodbc as odbc
import pandas as pd
from IMISNhanVien import *
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from PyQt5.QtCore import QObject,pyqtSlot
from AdminWindow import AdminWindow
from datetime import datetime
import pytz
# from main_login import MainWindow
from Function import AppFunction,MplCanvas,MplCanvasVung1,MplCanvasVung2,MplCanvasVung3,MplCanvasHMDT,MplCanvasNhomHang,MplCanvasTyLe
settings = QSettings()
## MAIN WINDOW CLASS
########################################################################
class NhanVienWindow(QMainWindow):
    def __init__(self, maNV, tenNV, boPhan):
        QMainWindow.__init__(self)
        self.ui = Ui_NhanVienWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(850,600)
        # self.setWindowState(Qt.WindowMaximized)
        # self.setWindowState(self.windowState()^Qt.WindowFullScreen)
        self.ui.maNV.setText(maNV)
        self.ui.tenNV.setText(tenNV)
        self.ui.boPhan.setText(boPhan)
        self.ui.tenTKDoiMK.setText(maNV)
        dynamic_link = "https://fpt.vn/vi"  # Replace with your dynamic link
        content = "IMIS - Là hệ thống phân tích dữ liệu hàng tồn kho giúp tối ưu hóa hàng tồn kho. Hệ thống được xây dựng bởi FPT Telecom"
        # full_content = f"{content} <a href='{dynamic_link}'>{dynamic_link}</a>"
        full_content = f"{content} <a href='{dynamic_link}' style='color: white;'>{dynamic_link}</a>"
        self.ui.label_3.setText(full_content)
        self.ui.label_3.setOpenExternalLinks(True)

        title = "DASHBOARD THEO DÕI TỒN KHO"
        link = "https://app.powerbi.com/Redirect?action=OpenReport&appId=2bc7de0e-fde8-40c1-a422-5817f2a9805f&reportObjectId=4f479c08-ec0b-455a-a337-73be34f4833c&ctid=f01e930a-b52e-42b1-b70f-a8882b5d043b&reportPage=ReportSection564803f656d32d99a027&pbi_source=appShareLink&portalSessionId=f647174b-7de7-421f-a297-1f0354e1e2fc"

        self.ui.dashboard.setText(title)
        self.ui.dashboard.setOpenExternalLinks(True)
        self.ui.dashboard.setTextFormat(Qt.RichText)
        self.ui.dashboard.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.ui.dashboard.setText(f'<a href="{link}">{title}</a>')
        self.ui.mainPages.setCurrentIndex(0)
        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        #loadJsonStyle(self, self.ui)
        loadJsonStyle(self, self.ui, jsonFiles = {
            "JsonStyle/style1.json"
        })
        ########################################################################
        ########################################################################
        self.show()
        # set header fit to content
        header = self.ui.phanTichABC.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header1 = self.ui.safetyStock.horizontalHeader()
        header1.setSectionResizeMode(QHeaderView.ResizeToContents)
        header2 = self.ui.tbCheckTon.horizontalHeader()
        header2.setSectionResizeMode(QHeaderView.ResizeToContents)
        header3 = self.ui.dhTb.horizontalHeader()
        header3.setSectionResizeMode(QHeaderView.ResizeToContents)
        header4 = self.ui.ycghTb.horizontalHeader()
        header4.setSectionResizeMode(QHeaderView.ResizeToContents)

        # CLOSE CENTER MENU WIDGET SIZE
        # self.ui.settingsBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.helpBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.infoBtn.clicked.connect(lambda: self.ui.centerMenuContainer.expandMenu())
        self.ui.closeCenterMenuBtn.clicked.connect(lambda: self.ui.centerMenuContainer.collapseMenu())
        # EXPAND RIGHT MENU WIDGET SIZE
        self.ui.moreMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        self.ui.profileMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.expandMenu())
        # CLOSE RIGHT MENU WIDGET SIZE
        self.ui.closeRightMenuBtn.clicked.connect(lambda: self.ui.rightMenuContainer.collapseMenu())
        # # CLOSE RIGHT MENU WIDGET SIZE
        self.ui.closeNotificationBtn.clicked.connect(lambda: self.ui.popupNotificationContainer.collapseMenu())
        self.ui.bcKhoBtn.clicked.connect(lambda: AppFunction.BCKho(self))
        self.ui.bcHHBtn.clicked.connect(lambda: AppFunction.BCHH(self))
        #################################################################
        # run main function to create database and table
        # Change theme
        # if self.ui.darkBlue.clicked():
        #     settings.setValue("THEME", "Dark-Blue")
        # elif self.ui.darkNight.clicked():
        #     settings.setValue("THEME", "Dark-Night")
        # elif self.ui.lightBlue.clicked():
        #     settings.setValue("THEME", "Light-Blue")
        # elif self.ui.lightOrange.clicked():
        #     settings.setValue("THEME", "Light-Orange")
        # QAppSettings.updateAppSettings(self)
        # Bảng kho
        AppFunction.displayKho(self)
        # self.ui.loaiKhoCb.currentIndexChanged.connect(lambda: AppFunction.combobox_intertwine(self))
        self.ui.tbKho.clicked.connect(lambda: AppFunction.NapKho(self))
        self.ui.filterBtn.clicked.connect(lambda: AppFunction.FilterKho(self))
        self.ui.hoanTacBtn.clicked.connect(lambda: AppFunction.displayKho(self))
        self.ui.themKhoBtn.clicked.connect(lambda: AppFunction.addKho(self))
        self.ui.suaKhoBtn.clicked.connect(lambda: AppFunction.SuaKho(self))
        self.ui.xoaKhoBtn.clicked.connect(lambda: AppFunction.XoaKho(self))
        # Bảng check tồn kho
        AppFunction.DisplayB048(self)
        self.ui.tkdRadioBtn.setChecked(True)  # Set the default selection
        self.ui.tkdRadioBtn.clicked.connect(lambda: AppFunction.DisplayB048(self))
        self.ui.dhRadioBtn.clicked.connect(lambda: AppFunction.DisplayA010(self))
        self.ui.ycghRadioBtn.clicked.connect(lambda: AppFunction.DisplayA040(self))
        self.ui.checkTonFilterBtn.clicked.connect(lambda: AppFunction.FilterB048(self))
        # self.ui.checkTonXuatExcelBtn.clicked.connect(lambda: AppFunction.XuatExcelB048(self))
        self.ui.checkTonXuatBCBtn.clicked.connect(lambda: AppFunction.XuatReportB048(self))
        self.ui.hoanTacB048Btn.clicked.connect(lambda: AppFunction.DisplayB048(self))
        
        #Bảng tài khoản
        # AppFunction.displayTK(self)
        # self.ui.tbTaiKhoan.clicked.connect(lambda: AppFunction.NapTK(self))
        # self.ui.filterTKBtn.clicked.connect(lambda: AppFunction.FilterTK(self))
        # self.ui.hoanTacTKBtn.clicked.connect(lambda: AppFunction.displayTK(self))
        # self.ui.themTKBtn.clicked.connect(lambda: AppFunction.ThemTK(self))
        # self.ui.suaTKBtn.clicked.connect(lambda: AppFunction.SuaTK(self))
        # self.ui.xoaTKBtn.clicked.connect(lambda: AppFunction.XoaTK(self))
        #Bảng nhân viên
        AppFunction.displayNV(self)
        self.ui.tbNhanVien.clicked.connect(lambda: AppFunction.NapNV(self))
        self.ui.filterNVBtn.clicked.connect(lambda: AppFunction.FilterNV(self))
        self.ui.hoanTacNVBTn.clicked.connect(lambda: AppFunction.displayNV(self))
        self.ui.themNVBtn.clicked.connect(lambda: AppFunction.ThemNV(self))
        self.ui.suaNVBtn.clicked.connect(lambda: AppFunction.SuaNV(self))
        self.ui.xoaNVBtn.clicked.connect(lambda: AppFunction.XoaNV(self))
        #Bảng hàng hóa
        AppFunction.displayHH(self)
        self.ui.tbHangHoa.clicked.connect(lambda: AppFunction.NapHH(self))
        self.ui.filterHHBtn.clicked.connect(lambda: AppFunction.FilterHH(self))
        self.ui.hoanTacHHBtn.clicked.connect(lambda: AppFunction.displayHH(self))
        self.ui.themHHBtn.clicked.connect(lambda: AppFunction.ThemHH(self))
        self.ui.suaHHBtn.clicked.connect(lambda: AppFunction.SuaHH(self))
        self.ui.xoaHHBtn.clicked.connect(lambda: AppFunction.XoaHH(self))
        # Bảng CDVT
        # AppFunction.DisplayDH(self)
        # self.ui.canDoiVT.clicked.connect(lambda: AppFunction.DisplayDH(self))
        # self.ui.cdvtBtn.clicked.connect(lambda: AppFunction.CDVT(self))
        # self.ui.xuatExcelCDVT.clicked.connect(lambda: AppFunction.ExportBCCDVT(self))
        # self.ui.deleteBtn.clicked.connect(lambda: AppFunction.Delete(self))
        # self.ui.filterCDVT.clicked.connect(lambda: AppFunction.FilterCDVT(self))
        # Change password
        self.ui.doiMKBtn.clicked.connect(lambda: AppFunction.ChangePW(self))
        # Chức năng chính thức
        self.ui.phanTichBtn.clicked.connect(lambda: AppFunction.ABCAnalysis(self))
        # self.ui.tquan.clicked.connect(lambda: AppFunction.TQ(self))
        self.ui.backABC.clicked.connect(lambda: self.ui.mainPages.setCurrentIndex(11))
        # self.ui.back.clicked.connect(lambda: self.ui.mainPages.setCurrentIndex(13))
        self.ui.back.clicked.connect(lambda: AppFunction.Back(self))
        self.ui.tinhSS.clicked.connect(lambda: AppFunction.SS(self))
        self.ui.tinhEOQ.clicked.connect(lambda: AppFunction.EOQ(self))
        self.ui.xuateoq.clicked.connect(lambda: AppFunction.DatHangBC(self))
        # self.ui.rop.clicked.connect(lambda: AppFunction.ROP(self))
        AppFunction.TQ(self)
        AppFunction.ROP(self)
        self.ui.bcSS.clicked.connect(lambda: AppFunction.BCSS(self))
        self.ui.bcABC.clicked.connect(lambda: AppFunction.BCABC(self))
        # Cập nhật nhu cầu
        # AppFunction.displayNhuCau(self)
        # self.ui.nhuCauFilter.clicked.connect(lambda: AppFunction.FilterNhuCau(self))
        # self.ui.importNhuCauBtn.clicked.connect(lambda: AppFunction.capNhatNhuCau(self))
        # self.ui.exportBCNhuCauBtn.clicked.connect(lambda: AppFunction.BCNhuCau(self))
        # Cảnh báo tồn kho
        # AppFunction.Alert(self)
        # self.ui.canhBaoFilterBtn.clicked.connect(lambda: AppFunction.FilterCanhBao(self))
        # self.ui.hoanTacCbBtn.clicked.connect(lambda: AppFunction.HoanTacCanhBao(self))
        # self.ui.canhBaoXuatBCBtn.clicked.connect(lambda: AppFunction.BCCanhBao(self))
        # Dashboard
        # self.tonTheoVung=MplCanvas()
        # self.ui.tonTheoVung.addWidget(self.tonTheoVung)
        # self.tonVung1=MplCanvasVung1()
        # self.ui.tonVung1.addWidget(self.tonVung1)
        # self.tonVung2=MplCanvasVung2()
        # self.ui.tonVung2.addWidget(self.tonVung2)
        # self.tonVung3=MplCanvasVung3()
        # self.ui.tonVung3.addWidget(self.tonVung3)
        # self.tonTheoHMDT=MplCanvasHMDT()
        # self.ui.tonTheoHMDT.addWidget(self.tonTheoHMDT)
        # self.tonTheoNhomHang=MplCanvasNhomHang()
        # self.ui.tonTheoNhomHang.addWidget(self.tonTheoNhomHang)
        # self.tyLeTon=MplCanvasTyLe()
        # self.ui.tyLeTon.addWidget(self.tyLeTon)
        # Cập nhật dữ liệu
        # self.ui.b048.clicked.connect(lambda: AppFunction.capNhatB048(self))
        # self.ui.a010.clicked.connect(lambda: AppFunction.CapNhatDataO(self))
        # # self.ui.a040.clicked.connect(lambda: AppFunction.capNhatA040(self))
        # self.ui.cleardata.clicked.connect(lambda: AppFunction.DeleteData(self))
        # Logout
        self.ui.dangXuatBtn.clicked.connect(lambda: AppFunction.Logout(self))
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app,theme='light_orange.xml')
    window = NhanVienWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  