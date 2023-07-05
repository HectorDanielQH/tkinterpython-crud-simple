import tkinter

from tkinter import ttk
import sqlite3

class Producto:
    db_name='testdb'
    def __init__(self,window):
        self.wind = window
        self.wind.title('APLICACION CON SQLite')
        #contenedor
        Frame=tkinter.LabelFrame(self.wind,text="Agregar nuevo producto")
        Frame.grid(row=0,column=0,columnspan=3, pady=20)

        #name
        tkinter.Label(Frame, text="Nombre").grid(row=1,column=0)
        #input
        self.nombre=tkinter.Entry(Frame)
        self.nombre.focus()
        self.nombre.grid(row=1,column=1)

        #input precio
        tkinter.Label(Frame, text="Precio").grid(row=2,column=0)
        #input
        self.precio=tkinter.Entry(Frame)
        self.precio.grid(row=2,column=1)

        #boton agregar producto

        boton=tkinter.Button(Frame, command=self.add_producto , text='Agregar').grid(row=3,columnspan=2,sticky='we')

        #SALIDA DE MENSAJES
        self.Mensaje=tkinter.Label(text='',fg='red')
        self.Mensaje.grid(row=3, column=0, columnspan=2, sticky='we')

        #treeview
        self.tree=ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor='center')
        self.tree.heading('#1', text='Precio', anchor='center')

        #BOTONES
        tkinter.Button(text='BORRAR',command=self.borrar_productos).grid(row=5,column=0,sticky='we')
        tkinter.Button(text='EDITAR', command=self.editar_productos).grid(row=5,column=1,sticky='we')

        #OBTENER FILAS
        self.obtener_Productos()

        #

    def ejectuar_consulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    def borrar_productos(self):
        self.Mensaje['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.Mensaje['text']='Selecciona algo'
            return
        name=self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM producto where nombre = ?'
        self.ejectuar_consulta(query, (name,))
        self.obtener_Productos()

    def editar_productos(self):
        self.Mensaje['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.Mensaje['text']='Selecciona algo'
            return
        name=self.tree.item(self.tree.selection())['text']
        precio_anterior=self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = tkinter.Toplevel()
        self.edit_wind.title = 'Editar producto'

        #anterior dato
        tkinter.Label(self.edit_wind, text='anterior nombre: ').grid(row=0,column=1)
        tkinter.Entry(self.edit_wind, textvariable=tkinter.StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)
        #actual datos
        tkinter.Label(self.edit_wind, text='nombre actual: ').grid(row=1,column=1)
        nuen=tkinter.Entry(self.edit_wind)
        nuen.grid(row=1, column=2)

        #anterior dato
        tkinter.Label(self.edit_wind, text='anterior precio: ').grid(row=2,column=1)
        tkinter.Entry(self.edit_wind, textvariable=tkinter.StringVar(self.edit_wind, value=precio_anterior), state='readonly').grid(row=2, column=2)
        #actual datos
        tkinter.Label(self.edit_wind, text='precio actual: ').grid(row=3,column=1)
        nuep=tkinter.Entry(self.edit_wind)
        nuep.grid(row=3, column=2)
        tkinter.Button(self.edit_wind,text='editar',command=lambda:self.actualizar_productos(nuen.get(),name,nuep.get(),precio_anterior)).grid(row=4,column=2,sticky='w')

    def actualizar_productos(self,nuen,antn,nuep,antp):
        query= 'UPDATE PRODUCTO SET nombre=?,precio=? where nombre=? and precio=?'
        parametros=(nuen,nuep,antn,antp)
        self.ejectuar_consulta(query,parametros)
        self.edit_wind.destroy()
        self.Mensaje['text']='El producto {} fue actualizado'.format(antn)
        self.obtener_Productos()


    def obtener_Productos(self):
        datos=self.tree.get_children()
        for dato in datos:
            self.tree.delete(dato)
        #datos consultar    
        query='select * from producto order by id desc'
        db_filas=self.ejectuar_consulta(query)

        for filas in db_filas:
            self.tree.insert('',0,text=filas[1],values=filas[2])

    def validar(self):
        return len(self.nombre.get()) !=0 and len(self.precio.get()) !=0
    def add_producto(self):
        if(self.validar()):
            query = 'INSERT INTO producto VALUES(NULL,?,?)'
            parametros=(self.nombre.get(), self.precio.get())
            self.ejectuar_consulta(query,parametros)
            self.Mensaje['text']='El producto {} se agrego con exito'.format(self.nombre.get())
            self.nombre.delete(0, tkinter.END)
            self.precio.delete(0, tkinter.END)
        else:
            self.Mensaje['text']='Agrega valores validos'
        self.obtener_Productos()

if __name__ == '__main__':
    window = tkinter.Tk()
    aplicacion=Producto(window)
    window.mainloop()
