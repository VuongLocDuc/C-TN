########################################################################
## SPINN DESIGN CODE
# YOUTUBE: (SPINN TV) https://www.youtube.com/spinnTv
# WEBSITE: spinncode.com
########################################################################

########################################################################
## IMPORTS
########################################################################
import os
import sys
import time
########################################################################
# IMPORT GUI FILE
from login import *
# IMPORT Custom widgets
from Custom_Widgets import *
# from Function import AppFunction

import pyodbc as odbc
########################################################################

########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    MAX_FAILED_ATTEMPTS = 3
    LOCKOUT_DURATION = 60  # 1 hour in seconds
    def __init__(self,parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(600,500)
        self.consecutive_failed_attempts=0
        self.last_failed_attempt=0
        # self.vo
        #loadJsonStyle(self, self.ui)
        loadJsonStyle(self, self.ui, jsonFiles = {
            "JsonStyle/style2.json"
        })
        ########################################################################
        ########################################################################
        self.show()
        self.ui.loginBtn.clicked.connect(lambda: self.OpenAdminWindow())
    def OpenAdminWindow(self):
        from AdminWindow import AdminWindow
        from NVWindow import NhanVienWindow
        un = self.ui.username.text()
        pw = self.ui.password.text()
        # conn=AppFunction.create_connection(self)
        # c=conn.cursor()
        DRIVER_NAME='SQL Server'
        SERVER_NAME='DESKTOP-TF6BQMV\SQLEXPRESS01'
        DATABASE_NAME='SCM'
        connection_string= f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
        """
        conn=odbc.connect(connection_string)
        c=conn.cursor()
        # Check if the user is currently locked out
        c.execute("SELECT * FROM TK WHERE TenTK ='"+un+"' and MK='"+pw+"'")
        kt = c.fetchone()
        if self.consecutive_failed_attempts >= self.MAX_FAILED_ATTEMPTS and not self.lockout_duration_expired(self.last_failed_attempt):
            remaining_time = self.LOCKOUT_DURATION - (time.time() - self.last_failed_attempt)
            # QMessageBox.information(self, "Thông báo", f"Bạn không thể đăng nhập trong {int(remaining_time)} giây. Vui lòng thử lại sau.")
            remaining_minutes = int(remaining_time // 60)
            remaining_seconds = int(remaining_time % 60)
            QMessageBox.information(self, "Thông báo", f"Bạn không thể đăng nhập trong {remaining_minutes} phút {remaining_seconds} giây. Vui lòng thử lại sau.")
            return
        if kt:
            
            if kt[2]==1:
                QMessageBox.information(self,"Thông báo","Đăng nhập thành công")
                c.execute("select MaNV,TenNV,TenBPTat from NhanVien,BoPhan where NhanVien.MaBP=BoPhan.MaBP and MaNV='"+un+"'")
                result = c.fetchone()
                if result:
                    maNV=result[0]
                    tenNV=result[1]
                    boPhan=result[2]
                    self.second_window = AdminWindow(maNV, tenNV, boPhan)  # Pass the data to the second window
                    self.hide()
                    self.second_window.show()
            elif kt[2]==0:
                # self.reset_consecutive_failed_attempts(un)
                QMessageBox.information(self,"Thông báo","Đăng nhập thành công")
                c.execute("select MaNV,TenNV,TenBPTat from NhanVien,BoPhan where NhanVien.MaBP=BoPhan.MaBP and MaNV='"+un+"'")
                result = c.fetchone()
                if result:
                    maNV=result[0]
                    tenNV=result[1]
                    boPhan=result[2]
                    self.nv_window = NhanVienWindow(maNV, tenNV, boPhan)  # Pass the data to the second window
                    self.hide()
                    self.nv_window.show()
        else:
            # self.increment_consecutive_failed_attempts(un)
            self.consecutive_failed_attempts+=1
            self.last_failed_attempt = time.time()
            QMessageBox.information(self,"Thông báo","Đăng nhập thất bại")
    # def increment_consecutive_failed_attempts(self,username):
    #     conn=AppFunction.create_connection(self)
    #     c=conn.cursor()
    #     c.execute("SELECT consecutive_failed_attempts FROM TK WHERE TenTK = ?", (username))
    #     a=c.fetchone()
    #     if a:
    #         current_attempts = a[0]
    #     new_attempts = current_attempts + 1
    #         # Update the existing row
    #     c.execute("UPDATE TK SET consecutive_failed_attempts = ?, last_failed_attempt = ? WHERE TenTK = ?", (new_attempts, time.time(), username))
    #     c.commit()
    # def reset_consecutive_failed_attempts(self,username):
    #     conn=AppFunction.create_connection(self)
    #     c=conn.cursor()
    #     c.execute("UPDATE TK SET consecutive_failed_attempts = 0, last_failed_attempt = 0 WHERE TenTK = ?", (username))
    #     c.commit()
    def lockout_duration_expired(self,last_failed_attempt):
        return time.time() - last_failed_attempt >= self.LOCKOUT_DURATION

## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app,theme='light_blue.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  

