import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import Treeview


Alto=350
Ancho=550
tipoCambio=[]
url=requests.get('https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx')

class MonedaCambio:

    def __init__(self,window):
        self.wind=window
        self.wind.title("Reto 1 : Exchange - SBS")
        self.wind.geometry(str(Ancho)+'x'+str(Alto))
        self.wind.configure(bg='#49A')
      
        btnExportar=Button(text='Exportar csv',command=self.exportar)
        btnExportar.grid(row=2,column=1, pady=6)
        btnMostrar=Button(text='Tipo de cambio',command=self.SBSscrapping)
        btnMostrar.grid(row=2,column=0,pady=5)
        self.trvCambioMoneda=Treeview(height=8,columns=('#1','#2'))
        self.trvCambioMoneda.grid(row=0,column=0,columnspan=3,padx=10,pady=5)
        self.trvCambioMoneda.heading('#0',text='Moneda',anchor=CENTER)
        self.trvCambioMoneda.heading('#1',text='Compra',anchor=CENTER)
        self.trvCambioMoneda.heading('#2',text='Venta',anchor=CENTER)

    def exportar(self):
        strTipoCambioExport=""
        for dictMoneda in tipoCambio:
            for clave,valor in dictMoneda.items():
                strTipoCambioExport+=valor
                if clave!='venta':
                    strTipoCambioExport+=','
                else:
                    strTipoCambioExport+='\n'
        fw=open('tipoMoneda.csv','w')
        fw.write(strTipoCambioExport)
        fw.close()

    def SBSscrapping(self):
        if(url.status_code==200):
            html=BeautifulSoup(url.text,'html.parser')
            tabla=html.find_all('table',{'id':'ctl00_cphContent_rgTipoCambio_ctl00'})
            for i in range(7):
                fila=html.find('tr',{'id':'ctl00_cphContent_rgTipoCambio_ctl00__'+str(i)})
                moneda=fila.find('td',{'class':'APLI_fila3'})
                valores=fila.find_all('td',{'class':'APLI_fila2'})
                dictMoneda={
                    'divisa':moneda.get_text(),
                    'compra':valores[0].get_text(),
                    'venta':valores[1].get_text(),
                }
                tipoCambio.append(dictMoneda)
                self.trvCambioMoneda.insert('',END,text=moneda.get_text(),values=[valores[0].get_text(),valores[1].get_text()])
                
        else:
            print("error  "+str(url.status_code))

if __name__=="__main__":
    window=Tk()
    app=MonedaCambio(window)
    window.mainloop()