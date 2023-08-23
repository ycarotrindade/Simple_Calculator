#importação de bibliotecas
from tkinter import *
import ttkbootstrap as ttb
from PIL import Image,ImageTk
from ttkbootstrap.dialogs.dialogs import Messagebox
from math import sqrt

def _scroll(direcao):
    if direcao=='Right':
        texto.configure(state='normal')
        texto.xview_scroll(1,'units')
        texto.configure(state='disabled')
    else:
        texto.configure(state='normal')
        texto.xview_scroll(-1,'units')
        texto.configure(state='disabled')

def _on_key_pressed(event):
    if event.keysym in '1234567890':
        adicionar_num(event.char)
    elif event.keysym in ['asterisk','minus','slash','plus','period']:
        match event.keysym:
            case 'plus':
                adicionar_sinal('+')
            case 'minus':
                adicionar_sinal('-')
            case 'asterisk':
                adicionar_sinal('x')
            case 'slash':
                adicionar_sinal('/')
            case 'period':
                adicionar_sinal('.')
    elif event.keysym=='equal':
        resultado()
    elif event.keysym=='BackSpace':
        apagar_ultimo()
    elif event.keysym=='Escape':
        root.destroy()
    elif event.keysym in ['Left','Right']:
        _scroll(event.keysym)
    else:
        print(event.keysym)
#criação da janela
root=ttb.Window(themename='darkly')
root.geometry('400x450')
root.resizable(False,False)
root.title('Calculadora')
root.bind('<Key>',func=_on_key_pressed)
#variáveis globais
display=''
podePonto=True

estilo=ttb.Style()
estilo.configure('TButton',background='black',justify='center',width=7)



def adicionar_num(valor:int):
    global display
    texto.configure(state='normal')
    display+=str(valor)
    texto.delete('1.0',END)
    texto.insert('1.0',display)
    texto.see(END)
    texto.configure(state='disabled')

def adicionar_sinal(sinal:str):
    global display,podePonto
    ultimo=display[-1] if len(display)>0 else ''
    if sinal in '+-':
        if sinal=='-' and len(display)==0:
            texto.configure(state='normal')
            display+=sinal
            texto.delete('1.0',END)
            texto.insert('1.0',display)
            texto.see(END)
            texto.configure(state='disabled')
        elif sinal=='+' and ultimo not in '+-/x.':
            texto.configure(state='normal')
            display+=sinal
            texto.delete('1.0',END)
            texto.insert('1.0',display)
            texto.see(END)
            texto.configure(state='disabled')
            podePonto=True
        elif sinal=='-' and ultimo not in '+-.':
            texto.configure(state='normal')
            display+=sinal
            texto.delete('1.0',END)
            texto.insert('1.0',display)
            texto.see(END)
            texto.configure(state='disabled')
            podePonto=True
    elif sinal in '/x' and ultimo not in '+-/x.':
        texto.configure(state='normal')
        display+=sinal
        texto.delete('1.0',END)
        texto.insert('1.0',display)
        texto.see(END)
        texto.configure(state='disabled')
        podePonto=True
    elif sinal=='.' and ultimo in '1234567890' and ultimo!='' and ultimo not in '+-/x.' and podePonto:
        texto.configure(state='normal')
        display+='.'
        texto.delete('1.0',END)
        texto.insert('1.0',display)
        texto.see(END)
        texto.configure(state='disabled')  
        podePonto=False

def resultado():
    global display
    display=display.replace('x','*')
    try:
        display=str(eval(display))
    except SyntaxError:
        Messagebox.ok(title='Erro de Sintaxe',message='Por favor, insira uma expressão válida')
    else:
        try:
            texto.configure(state='normal')
            texto.delete('1.0',END)
            texto.insert('1.0',display)
            texto.see(END)
            texto.configure(state='disabled')
        except OverflowError:
            Messagebox.ok(title='Muito grande',message='Resultado muito grande')
            apagar_tudo()

def apagar_ultimo():
    global display
    display=display[:-1]
    texto.configure(state='normal')
    texto.delete('1.0',END)
    texto.insert('1.0',display)
    texto.see(END)
    texto.configure(state='disabled')

def apagar_tudo():
    global display
    display=''
    texto.configure(state='normal')
    texto.delete('1.0',END)
    texto.see(END)
    texto.configure(state='disabled')

def calc_raiz():
    global display
    try:
        display=float(display)
    except ValueError:
        Messagebox.ok(message='Por favor, calcule um valor válido',title='Erro de Valor')
    else:
        display='{:.5f}'.format(sqrt(display))
        texto.configure(state='normal')
        texto.delete('1.0',END)
        texto.insert('1.0',display)
        texto.see(END)
        texto.configure(state='disabled')

def calc_potencia():
    global display
    try:
        display=float(display)
    except ValueError:
        Messagebox.ok(message='Por favor, calcule um valor válido',title='Erro de Valor')
    else:
        try:
            display='{:.5f}'.format(display**2)
            texto.configure(state='normal')
            texto.delete('1.0',END)
            texto.insert('1.0',display)
            texto.see(END)
            texto.configure(state='disabled')
        except OverflowError:
            Messagebox.ok(title='Muito Grande',message='Resultado muito grande')
            apagar_tudo()


#criação do display
texto=ttb.Text(root,width=100,height=1,state='disabled',font=('Regular',40),wrap=NONE)
texto.pack()

#criaçã dos botões
frame_botoes=ttb.Frame(root,width=400,height=309)

ttb.Button(frame_botoes,text='x²',style='TButton',command=calc_potencia).grid(column=0,row=0,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='C',style='TButton',command=apagar_tudo).grid(column=1,row=0,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='<--',style='TButton',command=apagar_ultimo).grid(column=2,row=0,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='/',style='TButton',command=lambda:adicionar_sinal('/')).grid(column=3,row=0,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='7',style='TButton',command=lambda:adicionar_num(7)).grid(column=0,row=1,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='8',style='TButton',command=lambda:adicionar_num(8)).grid(column=1,row=1,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='9',style='TButton',command=lambda:adicionar_num(9)).grid(column=2,row=1,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='X',style='TButton',command=lambda:adicionar_sinal('x')).grid(column=3,row=1,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='4',style='TButton',command=lambda:adicionar_num(4)).grid(column=0,row=2,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='5',style='TButton',command=lambda:adicionar_num(5)).grid(column=1,row=2,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='6',style='TButton',command=lambda:adicionar_num(6)).grid(column=2,row=2,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='-',style='TButton',command=lambda:adicionar_sinal('-')).grid(column=3,row=2,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='1',style='TButton',command=lambda:adicionar_num(1)).grid(column=0,row=3,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='2',style='TButton',command=lambda:adicionar_num(2)).grid(column=1,row=3,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='3',style='TButton',command=lambda:adicionar_num(3)).grid(column=2,row=3,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='+',style='TButton',command=lambda:adicionar_sinal('+')).grid(column=3,row=3,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='√x',style='TButton',command=calc_raiz).grid(column=0,row=4,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='0',style='TButton',command=lambda:adicionar_num(0)).grid(column=1,row=4,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='.',style='TButton',command=lambda:adicionar_sinal('.')).grid(column=2,row=4,pady=6,padx=5,ipadx=10,ipady=10)
ttb.Button(frame_botoes,text='=',style='TButton',command=resultado).grid(column=3,row=4,pady=6,padx=5,ipadx=10,ipady=10)

frame_botoes.pack(pady=30)

root.mainloop()