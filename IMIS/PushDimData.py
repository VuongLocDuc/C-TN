import pyodbc as odbc
import pandas as pd
import numpy as np
from datetime import date
DRIVER_NAME='SQL Server'
SERVER_NAME='DESKTOP-TF6BQMV\SQLEXPRESS01'
DATABASE_NAME='SCM'
connection_string= f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    """
db=odbc.connect(connection_string)
query=db.cursor()

# dfKhoINF=pd.read_excel('D:\IMIS\Data\DSachKhoINF.xlsx')
# for i,row in dfKhoINF.iterrows():
#     mk=row[0]
#     tk=row[1]
#     cn=row[2]
#     lk=row[3]
#     lkt=row[4]
#     if pd.isna(lkt):
#         query_string = "insert into KhoINF (MaKho, TenKho,MaLoaiKho,MaCN) values (?, ?, ?,?)"
#         values = (mk, tk,lk,cn)
#     else:
#         query_string = "insert into KhoINF (MaKho, TenKho,MaLoaiKho,MaLoaiKT,MaCN) values (?, ?, ?, ?,?)"
#         values = (mk, tk,lk,lkt,cn)
#     query.execute(query_string, values)
# db.commit()

# dfDSachNH=pd.read_excel('D:\IMIS\Data\DSachNH.xlsx')
# for i,row in dfDSachNH.iterrows():
#     mnh=row[0]
#     tnh=row[1]
#     query_string = "insert into NhomNH (MaNhomNH, TenNhomNH) values (?, ?)"
#     values = (mnh,tnh)
#     query.execute(query_string, values)
# db.commit()

# dfDSachBP=pd.read_excel('D:\IMIS\Data\DSachBP.xlsx')
# for i,row in dfDSachBP.iterrows():
#     mbp=row[0]
#     ttat=row[1]
#     tfull=row[2]
#     gchu=row[3]
#     if pd.isna(gchu):
#         query_string = "insert into BoPhan (MaBP, TenBPTat,TenBPDu) values (?, ?,?)"
#         values = (mbp,ttat,tfull)
#     else:
#         query_string = "insert into BoPhan (MaBP, TenBPTat,TenBPDu,GhiChu) values (?, ?,?,?)"
#         values = (mbp,ttat,tfull,gchu)
#     query.execute(query_string, values)
# db.commit()

# dfDSachLoaiVT=pd.read_excel('D:\IMIS\Data\DSachLoaiVT.xlsx')
# for i,row in dfDSachLoaiVT.iterrows():
#     mlvt=row[0]
#     tlvt=row[1]
#     query_string = "insert into ChungLoaiHH (MaChungLoaiHH, TenChungLoaiHH) values (?,?)"
#     values = (mlvt,tlvt)
#     query.execute(query_string, values)
# db.commit()

# dfDSachHMDT=pd.read_excel('D:\IMIS\Data\DSachHMDT.xlsx')
# for i,row in dfDSachHMDT.iterrows():
#     mhmdt=row[0]
#     thmdt=row[1]
#     gchu=row[2]
#     mabp=row[3]
#     if pd.isna(gchu):
#         query_string = "insert into HMDT (MaHMDT, TenHMDT,MaBP) values (?,?,?)"
#         values = (mhmdt,thmdt,mabp)
#     else:
#         query_string = "insert into HMDT (MaHMDT, TenHMDT,MaBP,GhiChu) values (?,?,?,?)"
#         values = (mhmdt,thmdt,mabp,gchu)
#     query.execute(query_string, values)
# db.commit()

# dfDSachDA=pd.read_excel('D:\IMIS\Data\DSachDA.xlsx')
# for i,row in dfDSachDA.iterrows():
#     mda=row[0]
#     tda=row[1]
#     nbd=row[2]
#     nkt=row[3]
#     namns=row[4]
#     macn=row[5]
#     mahmdt=row[6]
#     query_string = "insert into DA (MaDA, TenDA,NgayBD,NgayKT,MaHMDT,MaCN,NamNS) values (?,?,?,?,?,?,?)"
#     values = (mda,tda,nbd,nkt,mahmdt,macn,namns)
#     query.execute(query_string, values)
# db.commit()

# dfDSachCN=pd.read_excel('D:\IMIS\Data\DSachCN.xlsx')
# for i,row in dfDSachCN.iterrows():
#     mcn=row[0]
#     tcn=row[1]
#     ttat=row[2]
#     ho=row[3]
#     mavung=row[4]
#     query_string = "insert into CN (MaCN, TenCN,TenVietTat,HO,MaVung) values (?,?,?,?,?)"
#     values = (mcn,tcn,ttat,ho,mavung)
#     query.execute(query_string, values)
# db.commit()

# dfDSachNV=pd.read_excel('D:\IMIS\Data\DSachNV.xlsx')
# for i,row in dfDSachNV.iterrows():
#     mnv=row[0]
#     tnv=row[1]
#     mail=row[2]
#     dc=row[3]
#     sdt=row[4]
#     nvl=row[5]
#     mbp=row[6]
#     if pd.isna(nvl) and pd.isna(sdt) and pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP) values (?,?,?,?)"
#         values = (mnv,tnv,mail,mbp)
#     elif pd.isna(nvl) and pd.isna(sdt) and not pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,DiaChi) values (?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,dc)
#     elif pd.isna(nvl) and not pd.isna(sdt) and pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,SDT) values (?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,sdt)
#     elif not pd.isna(nvl) and pd.isna(sdt) and pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,NgayVaoLam) values (?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,nvl)
#     elif pd.isna(nvl) and not pd.isna(sdt) and not pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,DiaChi,SDT) values (?,?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,dc,sdt)
#     elif not pd.isna(nvl) and pd.isna(sdt) and not pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,NgayVaoLam,DiaChi) values (?,?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,nvl,dc)
#     elif not pd.isna(nvl) and not pd.isna(sdt) and pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,NgayVaoLam,SDT) values (?,?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,nvl,sdt)
#     elif not pd.isna(nvl) and not pd.isna(sdt) and not pd.isna(dc):
#         query_string = "insert into NhanVien (MaNV,TenNV,email,MaBP,NgayVaoLam,DiaChi,SDT) values (?,?,?,?,?,?,?)"
#         values = (mnv,tnv,mail,mbp,nvl,dc,sdt)
#     query.execute(query_string, values)
# db.commit()

# dfDSachKH=pd.read_excel('D:\IMIS\Data\DSachKH_TruMaDA_NA.xlsx',sheet_name='KH')
# for i,row in dfDSachKH.iterrows():
#     mkh=row[0]
#     tkh=row[1]
#     lkh=row[2]
#     tghu=row[3]
#     nbd=row[4]
#     nkt=row[5]
#     gchu=row[6]
#     mda=row[7]
#     mcn=row[8]
#     # yyyy-mm-dd
#     if pd.isna(nbd):
#         nbd = date(1999, 1, 1)
#     if pd.isna(nkt):
#         nkt = date(1999, 1, 1)
#     if pd.isna(gchu) and pd.isna(lkh):
#         query_string = f"insert into KH (MaKH,TenKH,TGHoanUng,TgBD,TgKT,MaDA,MaCN) values ('{mkh}',N'{tkh}','{tghu}','{nbd}','{nkt}','{mda}','{mcn}')"
#     elif pd.isna(gchu) and not pd.isna(lkh):
#         query_string = f"insert into KH (MaKH,TenKH,LoaiKH,TGHoanUng,TgBD,TgKT,MaDA,MaCN) values ('{mkh}',N'{tkh}',N'{lkh}','{tghu}','{nbd}','{nkt}','{mda}','{mcn}')"
#     elif not pd.isna(gchu) and pd.isna(lkh):
#         query_string = f"insert into KH (MaKH,TenKH,GhiChu,TGHoanUng,TgBD,TgKT,MaDA,MaCN) values ('{mkh}',N'{tkh}',N'{gchu}','{tghu}','{nbd}','{nkt}','{mda}','{mcn}')"
#     elif not pd.isna(gchu) and not pd.isna(lkh):
#         query_string = f"insert into KH (MaKH,TenKH,LoaiKH,TGHoanUng,TgBD,TgKT,MaDA,MaCN,GhiChu) values ('{mkh}',N'{tkh}',N'{lkh}','{tghu}','{nbd}','{nkt}','{mda}','{mcn}',N'{gchu}')"
#     query.execute(query_string)
# db.commit()
# query.execute("select * from Kho")
# dfKho=query.fetchall()
# data =[]
# for i in dfKho:
#     i=tuple(i)
#     data.append(i)
# names = [ x[0] for x in query.description]
# dfKho = pd.DataFrame(data, columns=names)
# dfB048=pd.read_excel('D:\IMIS\Data\data.xlsx')
# dfB048=dfB048.rename(columns={'Mã kho':'MaKho'})
# dfB048=dfB048.merge(dfKho,on='MaKho',how='inner')
# for i,row in dfB048.iterrows():
#     mk=row[0]
#     mtt=row[1]
#     mda=row[2]
#     mh=row[3]
#     tonhon90=row[4]
#     tongton=row[5]
#     tg=row[6]
#     query_string = f"insert into B048 (MaTTH,MaDA,MaHang,SLTonHon90,TongTon,MaKho,ThoiGian) values ('{mtt}','{mda}','{mh}','{tonhon90}','{tongton}','{mk}','{tg}')"
#     query.execute(query_string)
# db.commit()

# dfA040=pd.read_excel('D:\IMIS\Data\A0401.xlsx')
# for i,row in dfA040.iterrows():
#     mycgh=row[0]
#     nv=row[1]
#     nyc=row[2]
#     kn=row[3]
#     dgiai=row[4]
#     hmdt=row[5]
#     ntc=row[6]
#     tt=row[7]
#     dh=row[8]
#     if pd.isna(dgiai):
#         query_string = f"insert into A040 (MaYCGH,MaTT,MaHMDT,MaDH,MaNVTao,NgayYC,NamTC,MaKhoNhap) values ('{mycgh}','{tt}','{hmdt}','{dh}','{nv}','{nyc}','{ntc}','{kn}')"
#     else:
#         query_string = f"insert into A040 (MaYCGH,MaTT,MaHMDT,MaDH,MaNVTao,NgayYC,NamTC,DienGiai,MaKhoNhap) values ('{mycgh}','{tt}','{hmdt}','{dh}','{nv}','{nyc}','{ntc}',N'{dgiai}','{kn}')"
#     query.execute(query_string)
# db.commit()

# dfA040=pd.read_excel('D:\IMIS\Data\A0401Detail.xlsx')
# for i,row in dfA040.iterrows():
#     mycgh=row[0]
#     mh=row[1]
#     slyc=row[2]
#     query_string = f"insert into A040Detail (MaYCGH,MaHang,SLYC) values ('{mycgh}','{mh}','{slyc}')"
#     query.execute(query_string)
# db.commit()

df=pd.read_excel('D:\IMIS\Data\LSGD.xlsx')
for i,row in df.iterrows():
    sct=row[0]
    mcn=row[1]
    nt=row[2]
    mh=row[3]
    sl=row[4]
    query_string = f"insert into LichSuGD (SoCT,MaHang,MaCN,NgayXK ,SLXuat ) values ('{sct}','{mh}','{mcn}','{nt}','{sl}')"
    query.execute(query_string)
db.commit()

# dfA010=pd.read_excel('D:\IMIS\Data\A0101.xlsx')
# for i,row in dfA010.iterrows():
#     mdh=row[0]
#     mnvt=row[1]
#     nd=row[2]
#     cn=row[3]
#     dgiai=row[4]
#     tt=row[5]
#     ntc=row[6]
#     mda=row[7]
#     if pd.isna(dgiai):
#         query_string = f"insert into A010 (MaDH,MaNVTao, NgayDatDH, MaTT, MaDA, NamTC, MaCN) values ('{mdh}','{mnvt}','{nd}','{tt}','{mda}','{ntc}','{cn}')"
#     else:
#         query_string = f"insert into A010 (MaDH,MaNVTao, DienGiai,NgayDatDH, MaTT, MaDA, NamTC, MaCN) values ('{mdh}','{mnvt}',N'{dgiai}','{nd}','{tt}','{mda}','{ntc}','{cn}')"
#     query.execute(query_string)
# db.commit()

# dfA010=pd.read_excel('D:\IMIS\Data\A0101Detail.xlsx')
# for i,row in dfA010.iterrows():
#     mdh=row[0]
#     mh=row[1]
#     sldd=row[2]
#     sld=row[3]
#     slcg=row[4]
#     query_string = f"insert into A010Detail (MaDH,MaHang, SLDuyet,SLDat , SLChuaGiao) values ('{mdh}','{mh}','{sld}','{sldd}','{slcg}')"
#     query.execute(query_string)
# db.commit()

# dfTinhTrangHang=pd.read_excel('D:\IMIS\Data\Tình trạng hàng.xlsx')
# for i,row in dfTinhTrangHang.iterrows():
#     mtth=row[0]
#     ttth=row[1]
#     query_string = f"insert into TinhTrangHang (MaTTH,TenTTH) values ('{mtth}',N'{ttth}')"
#     query.execute(query_string)
# db.commit()


# dfHH=pd.read_excel('D:\IMIS\Data\DSachHH.xlsx')
# for i,row in dfHH.iterrows():
#     mh=row[0]
#     th=row[1]
#     dvt=row[2]
#     nnh=row[3]
#     dg=row[4]
#     lt=row[5]
#     query_string = "insert into HangHoa (MaHang,TenHang,DVT,DonGia,MaNhomNH,LT) values (?, ?, ?,?,?,?)"
#     values = (mh,th,dvt,dg,nnh,lt)
#     query.execute(query_string, values)
# db.commit()

db.close()


