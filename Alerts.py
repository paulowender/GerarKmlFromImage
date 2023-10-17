from tkinter import Tk, messagebox


def showInfo(title, message):
    root = Tk()
    root.withdraw()

    # Mostra uma caixa de diálogo de mensagem
    messagebox.showinfo(title, message)

    root.destroy()


def showError(title, message):
    root = Tk()
    root.withdraw()

    # Mostra uma caixa de diálogo de mensagem
    messagebox.showerror(title, message)

    root.destroy()


def showWarning(title, message):
    root = Tk()
    root.withdraw()

    # Mostra uma caixa de diálogo de mensagem
    messagebox.showwarning(title, message)

    root.destroy()


def confirmAction(title, message):
    root = Tk()
    root.withdraw()

    # Mostra uma caixa de diálogo de mensagem
    result = messagebox.askyesno(title, message)
    root.destroy()
    return result


def showConfirm(title, message):
    return confirmAction(title, message)
