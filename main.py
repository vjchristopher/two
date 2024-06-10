import streamlit as st
from streamlit_option_menu import option_menu
import auction2010,auction2014,auction2012,auction2013,auction2015,auction2016,auction2021,auction2022,auction2024

st.set_page_config(page_title="Auction Info")

class MultipagesApp:
    def __init__(self):
        self.apps=[]
    def add_application(self,title,function):
          self.apps.append({
              'title':title,
              'function':function
          })
          
    def run():
        with st.sidebar:
            app=option_menu(
                menu_title="Spectrum Auction",
                options=['Auction-2010','Auction-2012','Auction-2013','Auction-2014','Auction-2015','Auction-2016','Auction-2021','Auction-2022','Auction-2024'],
                icons=['1-circle','2-circle','3-circle','4-circle','5-circle','6-circle','7-circle','8-circle','9-circle'],    
                menu_icon='menu-app',
                default_index=1,
                styles={
                    'container':{'color':'white','font-size':'20px'},
                    'icon':{'color':'white','font-size':'20px'},
                    'nav-link':{'color':'white','font-size':'20px','text-align':'left','--hover-color':'black'},
                    'nav-link-selected':{'background-color':'#4a4a49'},})
      
        if app=='Auction-2010':
            auction2010.app()
        if app=='Auction-2012':
            auction2012.app()
        if app=='Auction-2013':
            auction2013.app()
        if app=='Auction-2014':
            auction2014.app()
        if app=='Auction-2015':
            auction2015.app()
        if app=='Auction-2016':
            auction2016.app()
        if app=='Auction-2021':
            auction2021.app()
        if app=='Auction-2022':
            auction2022.app()
        if app=='Auction-2024':
            auction2024.app()
    run()
