import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LoginGUI import LoginGUI

if __name__ == "__main__" : 
    app = LoginGUI()
    app.run()