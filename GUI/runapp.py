import BankbookGUI # test bankbook ui
from LoginGUI import LoginGUI
if __name__ == "__main__" : 
    app = LoginGUI()
    # app = BankbookGUI.BankbookGUI() #test bankbook ui
    app.run()