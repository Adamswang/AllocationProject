import os
import PyQt5

from AllocationMainWin_v2 import Ui_AllocationWizard
from AllocaitonDialog_v2 import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pandas as pd
#import numpy as np
import datetime


class MyForm2(QMainWindow, Ui_AllocationWizard):
    mySignal = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(MyForm2, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('/opt/anaconda3/envs/iPhone_Allocation/iPhone_v2/scales_v2.ico'))
        self.pushButton.setIcon(QIcon('/opt/anaconda3/envs/iPhone_Allocation/iPhone_v2/wrench.png'))
        self.toolButton.clicked.connect(self.selectsupply)
        self.toolButton_2.clicked.connect(self.selectdemand)
        self.toolButton_3.clicked.connect(self.selectoutput)
        self.pushButton.clicked.connect(self.opendialog)
        self.pushButton_3.clicked.connect(self.add_line)
        self.pushButton_4.clicked.connect(self.deletetablevalue)
        self.pushButton_5.clicked.connect(self.dtprocess)
        self.Childform = Childform()
        self.mySignal.connect(self.Childform.getpath_s)

    def opendialog(self):
        self.Childform.show()
        xlsx_s = self.lineEdit.text()
        xlsx_d = self.lineEdit_2.text()
        self.mySignal.emit(xlsx_s, xlsx_d)

    def selectsupply(self):
        supply_filename = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                                    options=QtWidgets.QFileDialog.DontUseNativeDialog)[
                                  0])
        self.lineEdit.setText(supply_filename)
        xlsx_s = self.lineEdit.text()
        print(xlsx_s)
        return xlsx_s

    def selectdemand(self):
        demand_filename = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                                                                    options=QtWidgets.QFileDialog.DontUseNativeDialog)[
                                  0])
        self.lineEdit_2.setText(demand_filename)
        xlsx_d = self.lineEdit_2.text()
        print(xlsx_d)
        return xlsx_d

    def selectoutput(self):
        output_filename = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder',
                                                                         options=QtWidgets.QFileDialog.DontUseNativeDialog))
        xlsx_o = self.lineEdit_3.setText(output_filename)
        return xlsx_o

    def add_line(self):
        row = self.tableWidget_2.rowCount()
        self.tableWidget_2.setRowCount(row + 1)
        btn = QPushButton('Add Ratio->>%' + str(row + 1))
        btn.setStyleSheet('''background-color:NavajoWhite;
                             font-size: 12pt;                                                      
                        ''')

        #h = QHBoxLayout()
        #h.addWidget(btn)
        #w = QWidget()
        #w.setLayout(h)
        #self.tableWidget_2.setCellWidget(row, 1, w)
        #btn.clicked.connect(lambda: self.showdialog())

    def deletetablevalue(self):
        row = self.tableWidget_2.currentRow()
        self.tableWidget_2.removeRow(row)

    def gettablevalue(self):
        row_get = self.tableWidget_2.rowCount()
        col_get = self.tableWidget_2.columnCount()

        ratiolist = []
        for row in range(row_get):
            for col in range(col_get):
                itemratio = self.tableWidget_2.item(row, 0)
                rratio = self.tableWidget_2.item(row, 1)
                item = [itemratio.text(), rratio.text()]
                ratiolist.append(item)
        ratiodic = dict(ratiolist)
        print(ratiodic)
        return ratiodic

    def dtprocess(self):

            nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
            xlsx_s = self.lineEdit.text()
            xlsx_d = self.lineEdit_2.text()
            xlsx_o = self.lineEdit_3.text() + str('/Output_') + nowtime + str('.xlsx')
            ratiodic = self.gettablevalue()

            df_d = pd.read_excel(xlsx_d, index_col=0)
            df_s = pd.read_excel(xlsx_s, index_col=0)
            df_consol = pd.merge(df_d, df_s, on='MPN')
            df_consol = df_consol.fillna(0)
            df_consol2 = df_consol.groupby(['Model'], as_index=False)
            d_f_output = pd.DataFrame()
            for df_consol2_split in df_consol2:
                df_consol_split_main = pd.DataFrame(df_consol2_split[1]).reset_index(drop=True)
                df_consol_split_main = df_consol_split_main.groupby(['MPN', 'Supply CW+1', 'ODQ'], as_index=False)
                d_output = pd.DataFrame()
                m = df_consol2_split[0]
                ratio_ini = str(ratiodic.get(m)).split(',')
                ratio_ini = list(map(float, ratio_ini))
                print(ratio_ini)

                for d_c_main_split in df_consol_split_main:
                    od = d_c_main_split[0][2]
                    s = d_c_main_split[0][1]
                    d = d_c_main_split[1]['Demand'].values.tolist()
                    d_c_split_main = pd.DataFrame(d_c_main_split[1]).reset_index(drop=True)

                    if s > sum(d):
                        F_allo = self.suffisupply(s, d, ratio_ini, od)

                    elif s == 0:
                        #F_allo = (np.random.randint(0, 1, len(ratio_ini))).tolist()
                        F_allo = [0 for i in range(len(ratio_ini))]
                    else:
                        F_allo = self.tightsupply(s, d, ratio_ini, od)

                    F_allo = pd.DataFrame(F_allo, columns={'allo'})
                    d_combine = pd.concat([d_c_split_main, F_allo], axis=1)
                    d_combine = pd.DataFrame(d_combine)
                    d_output = d_output.append(d_combine, ignore_index=True)
                d_f_output = d_f_output.append(d_output, ignore_index=True)
            print(d_f_output)
            d_f_output.to_excel(xlsx_o)
            self.statusBar().showMessage('Process Done!', 10000)


    def infoerror(self):
        reply = QMessageBox.information(self,
                                        "文件选择or填写的Ratio不匹配",
                                        "请查看文件是否选择，或Ratio添加个数与文件一致",
                                        QMessageBox.Ok)

    # 分货function
    # scenario 1: n/a供货
    def nullsupply(self, supply, demand, ratio, ODQ):
        F_allo = []
        for i in range(len(ratio)):
            F_allo.append(0)

    # scenario 2: 充足供货
    def suffisupply(self, supply, demand, ratio, ODQ):
        # define list
        ind = []
        for i in range(len(ratio)):
            ind.append(0)

        allo = []
        for i in range(len(ratio)):
            allo.append(0)

        F_allo = []
        for i in range(len(ratio)):
            F_allo.append(0)

        adj_s = []
        for i in range(len(ratio)):
            adj_s.append(0)

        allo = demand
        F_allo = allo

        return F_allo

    # scenario 3: 紧缺供货
    def tightsupply(self, supply, demand, ratio_ini, ODQ):
        # define list
        ratio = ratio_ini[:]
        #ind = (np.random.randint(0, 1, len(ratio))).tolist()
        #allo = (np.random.randint(0, 1, len(ratio))).tolist()
        #F_allo = (np.random.randint(0, 1, len(ratio))).tolist()
        #adj_s = (np.random.randint(0, 1, len(ratio))).tolist()

        ind = [0 for i in range(len(ratio))]
        allo = [0 for i in range(len(ratio))]
        F_allo = [0 for i in range(len(ratio))]
        adj_s = [0 for i in range(len(ratio))]


        # calculation
        supply_ini = supply

        j = 0
        while sum(F_allo) < supply_ini:
            j = j + 1
            supply = supply - sum(allo)
            demand = list(map(lambda x, y: x - y, demand, allo))

            for l in range(len(demand)):
                if demand[l] != 0:
                    ratio[l] = ratio[l]
                else:
                    ratio[l] = 0

            for i in range(len(ratio)):
                ind[i] = ratio[i] / sum(ratio)

            # max_ind = ind.index(max(ind))
            ind_position = [i for i, e in enumerate(ind) if e > 0]
            ind_count = sum(list(map(lambda x: x > 0, ind)))
            for i in range(len(ratio)):
                adj_s[i] = int((supply * ind[i]) / ODQ) * ODQ

            if supply > ind_count * ODQ:
                for i in range(len(ratio)):
                    allo[i] = min(adj_s[i], demand[i])
            else:
                #allo = (np.random.randint(0, 1, len(ratio))).tolist()
                allo = [0 for i in range(len(ratio))]
                for k in ind_position:
                    allo[k] = ODQ
                    if sum(allo) == supply:
                        break
            for i in range(len(ratio)):
                F_allo[i] = F_allo[i] + allo[i]
        return F_allo

    def filecheck(self):
        xlsx_s = self.lineEdit.text()
        xlsx_d = self.lineEdit_2.text()
        df_d = pd.read_excel(xlsx_d, index_col=0)
        df_s = pd.read_excel(xlsx_s, index_col=0)
        df_consol = pd.merge(df_d, df_s, on='MPN')
        df_consol = df_consol.fillna(0)
        print(df_consol)

    #def sendEditcontent(self):
     #   xlsx_s = self.lineEdit()
      #  xlsx_d = self.lineEdit_2()
       # self.mySignal.emit(xlsx_s, xlsx_d)


class Childform(QDialog, Ui_Dialog):
    childSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Childform, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.closeit)
        self.pushButton_5.clicked.connect(self.showpath_s)

    def getpath_s(self, s, d):
        self.xlsx_s = s
        self.xlsx_d = d
        return self.xlsx_s, self.xlsx_s

    def showpath_s(self):
        #try:
            self.textEdit.append('Supply file path:...' + self.xlsx_s)
            self.textEdit.append('Demand file path:...' + self.xlsx_d)
            self.textEdit.append('                                                  ')
            self.textEdit.append('<<======== Supply file format checking =========>>')
            try:
                df_s = pd.read_excel(self.xlsx_s, index_col=0)
                df_s2 = pd.DataFrame(df_s.to_records())
                if df_s2.columns[1] == 'MPN':
                    self.textEdit.append("MPN column checking ------->" + "<font color=\"#00FF00\">[PASS]</font>")
                else:
                    self.textEdit.append("MPN column checking ------->" + "<font color=\"#FF0000\">[FALSE]</font>")

                if df_s2.columns[4] == 'Supply CW+1':
                    self.textEdit.append("Supply CW+1 column checking ------>" + "<font color=\"#00FF00\">[PASS]</font>")
                    self.textEdit.append("Supply file总行数" + str(len(df_s2)))
                    self.textEdit.append("Supply total " + str(df_s2['Supply CW+1'].sum()))
                else:
                    self.textEdit.append("Supply CW+1 column checking ------>" +
                                         "<font color=\"#FF0000\">[FALSE]</font>")
               #for i in range(0, len(df_s2)):
                #   print(df_s2.iloc[i][4])
            except (NameError, TypeError, KeyError, ValueError):
                print('Please select correct supply file...')

            self.textEdit.append('                                                  ')
            self.textEdit.append('<<======= Demand file format checking =========>>')

            try:
                df_d = pd.read_excel(self.xlsx_d, index_col=0)
                df_d2 = pd.DataFrame(df_d.to_records())
                if df_d2.columns[2] == 'Sold to Name':
                    self.textEdit.append("Sold to Name column checking ------->" +
                                         "<font color=\"#00FF00\">[PASS]</font>")
                else:
                    self.textEdit.append("Sold to Name column checking ------->"
                                         + "<font color=\"#FF0000\">[FALSE]</font>")

                if df_d2.columns[3] == 'Model':
                    self.textEdit.append("Model column checking ------->" + "<font color=\"#00FF00\">[PASS]</font>")
                else:
                    self.textEdit.append("Model Name column checking ------->"
                                         + "<font color=\"#FF0000\">[FALSE]</font>")

                if df_d2.columns[4] == 'MPN':
                    self.textEdit.append("MPN column checking ------->" + "<font color=\"#00FF00\">[PASS]</font>")
                else:
                    self.textEdit.append("MPN Name column checking ------->" + "<font color=\"#FF0000\">[FALSE]</font>")

                if df_d2.columns[5] == 'ODQ':
                    self.textEdit.append("ODQ column checking ------->" + "<font color=\"#00FF00\">[PASS]</font>")
                else:
                    self.textEdit.append("ODQ Name column checking ------->" + "<font color=\"#FF0000\">[FALSE]</font>")

                if df_d2.columns[6] == 'Demand':
                    self.textEdit.append("Demand column checking ------->" + "<font color=\"#00FF00\">[PASS]</font>")
                    self.textEdit.append("Demand file总行数" + str(len(df_d2)))
                    self.textEdit.append("Demand total " + str(df_d2['Demand'].sum()))
                    self.textEdit.append("Details:")
                    #self.df_p = pd.pivot_table(self.df_d, values='Demand', index=['Sold to Name', 'Model'], aggfunc=np.sum)
                    #for i in range(0, len(self.df_p)):
                    #    self.textEdit.append(str(self.df_p.to_records()[i]).replace(',', ' '))
                else:
                    self.textEdit.append("Demand Name column checking ------->"
                                         + "<font color=\"#FF0000\">[FALSE]</font>")

            except (NameError, TypeError, KeyError, ValueError):
                self.textEdit.append('Please select correct Demand file...')

            try:

                df_s = pd.read_excel(self.xlsx_s, index_col=0)
                df_d = pd.read_excel(self.xlsx_d, index_col=0)
                df_consol = pd.merge(df_d, df_s, on='MPN')
                df_consol['d_int'] = df_consol.apply(lambda x: abs(x['Demand'] % x['ODQ']), axis=1)
                odq_d_int = df_consol['d_int'].sum()

                if odq_d_int == 0:
                    self.textEdit.append('                                                  ')
                    self.textEdit.append('<<=========== ODQ整除checking =============>>')
                    self.textEdit.append("Demand➗ODQ是否为整数 ------->" + "<font color=\"#00FF00\">[PASS]</font>")

                else:
                    self.textEdit.append("Demand➗ODQ是否为整数 ------->" + "<font color=\"#FF0000\">[FALSE]</font>")

                df_consol['s_int'] = df_consol.apply(lambda x: abs(x['Supply CW+1'] % x['ODQ']), axis=1)
                odq_s_int = df_consol['s_int'].sum()
                if odq_s_int == 0:
                    self.textEdit.append("Supply➗ODQ是否为整数 ------->" + "<font color=\"#00FF00\">[PASS]</font>")

                else:
                    self.textEdit.append("Supply➗ODQ是否为整数 ------->" + "<font color=\"#FF0000\">[FALSE]</font>")

            except (NameError, TypeError, KeyError, ValueError):
                self.textEdit.append('                                                  ')
                self.textEdit.append('ODQ calculation error...')
        #except:
         #   self.textEdit.append('Please select Supply and demand file...')

    def closeit(self):
        self.textEdit.clear()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/opt/anaconda3/envs/iPhone_Allocation/iPhone_v2/scales_v2.ico'))
    win = MyForm2()
    childwin = Childform()
    win.show()
    sys.exit(app.exec_())
