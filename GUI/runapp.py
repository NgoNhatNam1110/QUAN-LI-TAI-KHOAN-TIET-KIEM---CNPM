<<<<<<< HEAD
from LoginGUI import LoginGUI

if __name__ == "__main__" : 
    app = LoginGUI()
=======
import BankbookGUI # test bankbook ui
from LoginGUI import LoginGUI
if __name__ == "__main__" : 
    app = LoginGUI()
    # app = BankbookGUI.BankbookGUI() #test bankbook ui
>>>>>>> ddd67fe (implemented basic login functionality & created actual sqlite database via dbBrowser)
    app.run()