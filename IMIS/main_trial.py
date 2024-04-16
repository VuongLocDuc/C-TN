import typing
from PyQt6 import QtCore,QtGui,QtWidgets,uic
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
import sys
import pyodbc as odbc
from sqlalchemy import create_engine
import pandas as pd
from tkinter import filedialog
import win32com.client as win32
import B048
import matplotlib.pyplot as plt
import seaborn as sb
#from PySide6.QtCharts import *
#from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

#Cửa sổ login
class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w,self).__init__()
        uic.loadUi('loginnew.ui',self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.reg_form)
        # Remove default frame
        # flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        # self.pos_ = self.pos()
        # self.setWindowFlags(flags)
    def login(self):
        un=self.user.text()
        pw=self.psw.text()
        db=odbc.connect(connection_string)
        query=db.cursor()
        query.execute("select * from user_list where username='"+un+"' and password='"+pw+"'")
        kt=query.fetchone()
        if kt:
            QMessageBox.information(self,"Reg output","Dang nhap thanh cong")
            widget.setCurrentIndex(2)
        else:
            QMessageBox.information(self,"Reg output","Dang nhap fail")
            #widget.setCurrentIndex(0)
    def reg_form(self):
        widget.setCurrentIndex(1)
# Cửa sổ register
class Reg_w(QMainWindow):
    def __init__(self):
        super(Reg_w,self).__init__()
        #self.showMaximized()
        uic.loadUi('register.ui',self)
        self.b1.clicked.connect(self.reg)
        
    def reg(self):
        un=self.user.text()
        pw=self.psw.text()
        db=odbc.connect(connection_string)
        query=db.cursor()
        query.execute("select * from user_list where username='"+un+"' and password='"+pw+"'")
        kt=query.fetchone()
        if kt:
            QMessageBox.information(self,"Reg output","Tai khoan da ton tai")
        else:
            query.execute("insert into user_list values ('"+un+"','"+pw+"')")
            db.commit()
            QMessageBox.information(self,"Reg output","Dang ky thanh cong")
            widget.setCurrentIndex(0)
# Cửa sổ Can Ton KD
class CanTonKD_w(QMainWindow):
    def __init__(self):
        super(CanTonKD_w,self).__init__()
        uic.loadUi('frmCanTonKD.ui',self)
# Check ton
class CheckTon_w(QMainWindow):
    def __init__(self):
        super(CheckTon_w,self).__init__()
        uic.loadUi('frmCheckTon.ui',self)
        self.btnCheck.clicked.connect(self.CheckTon)
    def CheckTon(self):
        mh=self.mh.text()
        choice=self.cb.currentText()
        db=odbc.connect(connection_string)
        query=db.cursor()
        dfCheckTon = pd.read_sql('select * from B048', db)
        dfKho = pd.read_sql('select MaKho,TenKho,TenCN,TenVung from KhoINF,CN,Vung where KhoINF.MaCN=CN.MaCN and CN.MaVung=Vung.MaVung', db)
        df=pd.merge(dfCheckTon,dfKho,on="MaKho",how='inner')
        df=df[df['MaHang']==mh]
        df = df.groupby(["TenVung", "TenCN", "MaKho"], as_index=False)["SLTonKD"].sum()
        self.tbCheckTon.setRowCount(0)
        for row_number, row_data in df.iterrows():
            self.tbCheckTon.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tbCheckTon.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
# Cửa sổ cân đối vật tư
class CDVT_w(QMainWindow):
    def __init__(self):
        super(CDVT_w,self).__init__()
        uic.loadUi('frmCanDoiVT.ui',self)
        db=odbc.connect(connection_string)
        query=db.cursor()
        dfNhuCau = pd.read_sql('select MaHang, SLYeuCau, ThangNhan from NhuCau', db)
        dfNhuCau = dfNhuCau.groupby(["ThangNhan", "MaHang"], as_index=False)["SLYeuCau"].sum()
        self.tbNhuCau.setRowCount(0)
        for row_number, row_data in dfNhuCau.iterrows():
            self.tbNhuCau.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tbNhuCau.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.btnExit.clicked.connect(self.do_exit)
        db.close()
        self.tbNhuCau.itemSelectionChanged.connect(self.frmCanTonKD)
        #self.b2.clicked.connect(self.reg_form)
    def frmCanTonKD(self):
        widget.setCurrentIndex(7)
    # def CDVT(self):
    #     widget.setCurrentIndex(1)
    #     selected_row = self.tbNhuCau.currentRow()  # Lấy chỉ số của dòng được chọn
    #     if selected_row >= 0:  # Kiểm tra xem có dòng nào được chọn không
    #         # Lấy giá trị từ các ô trong dòng được chọn
    #         cell_values = []
    #         for column_number in range(self.tbNhuCau.columnCount()):
    #             item = self.tbNhuCau.item(selected_row, column_number)
    #             if item is not None:
    #                 cell_values.append(item.text())
    #             else:
    #                 cell_values.append("")  # Nếu ô không có giá trị, thêm giá trị rỗng vào danh sách
    #         # Sử dụng giá trị từ các ô trong dòng được chọn
    #         # Ví dụ: In giá trị của các ô
    #         for value in cell_values:
    #             print(value)
    def do_exit(self):
        self.close()
        widget.setCurrentIndex(2)
# Cửa số B048
class B048_w(QMainWindow):
    def __init__(self):
        super(B048_w,self).__init__()
        uic.loadUi('B048.ui',self)
        self.btnb048.clicked.connect(self.update_B048)
        self.btnb048_refresh.clicked.connect(self.refresh)
    def update_B048(self):
        to_date=self.todate.text()
        df = B048.handle_api(todate=to_date)
        db=odbc.connect(connection_string)
        query=db.cursor()
        dfKhoINF=pd.read_sql('select MaKho, TenKho from KhoINF',db)
        dfKhoINF = dfKhoINF.rename(columns={"TenKho": "Kho"})
        df=pd.merge(df,dfKhoINF,on='Kho', how="inner")
        df.drop(columns=['Kho'],inplace=True)
        dfTTH=pd.read_sql('select MaTTH, TenTT from TinhTrangHang',db)
        dfTTH=dfTTH.rename(columns={'TenTT':'Tình trạng hàng nhập'})
        df=pd.merge(df,dfTTH,on='Tình trạng hàng nhập',how='inner')
        df.drop(columns=['Tình trạng hàng nhập'])
        try:
            for i,row in df.iterrows():
                mda=row[0]
                mkh=row[1]
                mh=row[2]
                slkd=row[3]
                tt=row[4]
                tonhon90=row[5]
                mk=row[6]
                mtth=row[7]
                if pd.isna(mda) and pd.isna(mkh):
                    query_string = f"insert into B048 (MaTTH,MaHang,SLTonHon90,SLTonKD,TongTon,MaKho) values ('{mtth}','{mh}','{tonhon90}','{slkd}','{tt}','{mk}')"
                elif pd.isna(mda) and not pd.isna(mkh):
                    query_string = f"insert into B048 (MaTTH,MaHang,SLTonHon90,SLTonKD,TongTon,MaKho,MaKH) values ('{mtth}','{mh}','{tonhon90}','{slkd}','{tt}','{mk}','{mkh}')"                
                elif not pd.isna(mda) and pd.isna(mkh):
                    query_string = f"insert into B048 (MaTTH,MaHang,SLTonHon90,SLTonKD,TongTon,MaKho,MaDA) values ('{mtth}','{mh}','{tonhon90}','{slkd}','{tt}','{mk}','{mda}')"
                elif not pd.isna(mda) and not pd.isna(mkh):
                    query_string = f"insert into B048 (MaTTH,MaHang,SLTonHon90,SLTonKD,TongTon,MaKho,MaDA,MaKH) values ('{mtth}','{mh}','{tonhon90}','{slkd}','{tt}','{mk}','{mda}','{mkh}')"                
                query.execute(query_string)
            db.commit()
            msg=QtWidgets.QMessageBox()
            msg.setInformativeText('update success')
            msg.exec()
        except:
                msg=QtWidgets.QMessageBox()
                msg.setInformativeText('update fail')
                msg.exec()
    def refresh(self):
        db=odbc.connect(connection_string)
        query=db.cursor()
        result=query.execute("select MaTTH,MaDA,MaKH,MaKho,MaHang,SLTonHon90,SLTonKD,TongTon from B048")
        self.tableB048.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableB048.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableB048.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))
        db.close()
# Cửa sổ A010
class A010_w(QMainWindow):
    def __init__(self):
        super(A010_w,self).__init__()
        uic.loadUi('A010.ui',self)

# Cửa sổ Nhu cầu vật tư
class NCVT_w(QMainWindow):
    def __init__(self):
        super(NCVT_w,self).__init__()
        uic.loadUi('frmnhapnhucau.ui',self)
        self.btnUploadNhuCau.clicked.connect(self.upload_ncvt)
    def upload_ncvt(self):
        file_path = filedialog.askopenfilename()
        dfNhuCau = pd.read_excel(file_path)
        db=odbc.connect(connection_string)
        query=db.cursor()
        dfNhuCau.drop(columns=['Vùng','Tên HMDT','Tên hàng','Đơn vị tính','Slg được duyệt'],inplace=True)
        dfNV=pd.read_sql('select MaNV, email from NhanVien',db)
        dfCN=pd.read_sql('select MaCN, TenCN from CN',db)
        dfDA=pd.read_sql('select MaDA, TenDA,MaCN from DA',db)
        dfNhuCau=pd.merge(dfNhuCau, dfNV, left_on='Người yêu cầu', right_on='email', how='inner')
        dfNhuCau.drop(columns=['email','Người yêu cầu'],inplace=True)
        dfNhuCau.rename(columns={'MaNV':'MaNVYeuCau'},inplace=True)
        dfNhuCau=pd.merge(dfNhuCau, dfNV, left_on='Nhân sự P.KH tổng hợp', right_on='email', how='inner')
        dfNhuCau=pd.merge(dfNhuCau, dfCN, left_on='Tên chi nhánh', right_on='TenCN', how='inner')
        dfNhuCau=pd.merge(dfNhuCau, dfDA, left_on=['Tên dự án','MaCN'], right_on=['TenDA','MaCN'], how='inner')
        dfNhuCau.drop(columns=['email','Nhân sự P.KH tổng hợp','Tên chi nhánh','TenCN','Tên dự án','TenDA'],inplace=True)
        dfNhuCau.rename(columns={'MaNV':'MaNVTongHop'},inplace=True)
        for i,row in dfNhuCau.iterrows():
            mycgh=row[0]
            ndd=row[1]
            gchu=row[2]
            ntc=row[3]
            mh=row[4]
            slyc=row[5]
            thang=row[6]
            nvyc=row[7]
            nvth=row[8]
            cn=row[9]
            da=row[10]
            query_string = "insert into NhuCau (MaYCGH, MaNVYeuCau,NgayDuocDuyet,MaCN,MaDA,GhiChu,NamTC,MaHang,SLYeuCau,MaNVTongHop,ThangNhan) values (?,?,?,?,?,?,?,?,?,?,?)"
            values = (mycgh,nvyc,ndd,cn,da,gchu,ntc,mh,slyc,nvth,thang)
            query.execute(query_string, values)
        db.commit()

# Cửa sổ dashboard
class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(200, 200, 600, 400)

    def DB1(self):
        # Tạo các thành phần của dashboard ở đây
        db=odbc.connect(connection_string)
        query=db.cursor()
        df=pd.read_sql('select * from B048',db)
        sb.scatterplot(data=df,x=df['SLTonHon90'],y=df['TongTon'])
        plt.show()
# Cửa sổ main
class Main_w(QMainWindow):
    def __init__(self):
        super(Main_w,self).__init__()
        uic.loadUi('loginsc.ui',self)
        self.actionExit.triggered.connect(self.do_exit)
        self.actionCDVT.triggered.connect(self.do_cdvt)
        self.actionB048.triggered.connect(self.do_B048)
        self.actionA010.triggered.connect(self.do_A010)
        self.actionncvt.triggered.connect(self.do_ncvt)
        self.actionDB1.triggered.connect(self.show_dashboard)
        self.actionCheckTon.triggered.connect(self.do_check)
    def do_exit(self):
        sys.exit()
    def do_cdvt(self):
        widget.setCurrentIndex(3)
    def do_B048(self):
        widget.setCurrentIndex(4)
    def do_A010(self):
        widget.setCurrentIndex(5)
    def do_ncvt(self):
        widget.setCurrentIndex(6)
    def show_dashboard(self):
        # Tạo một cửa sổ mới để hiển thị dashboard
        dashboard_window = DashboardWindow()
        dashboard_window.DB1()
        dashboard_window.show()
    def do_check(self):
        widget.setCurrentIndex(8)

# Xử lý
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
DRIVER_NAME='SQL Server'
SERVER_NAME='W010273988'
DATABASE_NAME='SCM'
connection_string= f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    """
Login_f=Login_w()
Reg_f=Reg_w()
Main_f=Main_w()
CDVT_f=CDVT_w()
B048_f=B048_w()
A010_f=A010_w()
NCVT_f=NCVT_w()
CanTonKD_f=CanTonKD_w()
CheckTon_f=CheckTon_w()

widget.addWidget(Login_f) # 0
widget.addWidget(Reg_f)
widget.addWidget(Main_f)
widget.addWidget(CDVT_f)
widget.addWidget(B048_f)
widget.addWidget(A010_f)
widget.addWidget(NCVT_f)
widget.addWidget(CanTonKD_f)
widget.addWidget(CheckTon_f)
widget.setCurrentIndex(0)
# widget.setFixedHeight(500)
# widget.setFixedWidth(400)
widget.show()
app.exec()