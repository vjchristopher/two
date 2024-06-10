import streamlit as st
import pandas as pd

def app():
    linkedinlink = '[DoT Website](https://dot.gov.in/spectrum-management/2463)'
    auction_timetable='[Auction Time Table](https://dot.gov.in/sites/default/files/Revised%20Auction%20table_0.pdf)'
    nia='[NIA](https://dot.gov.in/sites/default/files/3G%20%26%20BWA%20Auctions_Notice%20Inviting%20Applications_0.pdf)'
    col1, mid, col2 = st.columns([2,1,20])
    with col1:
        st.image('dot.jpg', width=80)
    with col2:
        st.write("""## 3G & BWA Spectrum Auction in 2010 """)

    #chnage 2 column names
    col_names=['Service_Area','Band','Winning_Price','Company_Name','Uplink_Start','Uplink_Stop','Downlink_Start','Downlink_Stop']
    df=pd.read_csv('final_results_2010.csv')

    df['Service_Area']=df['Service_Area'].fillna(method='ffill')
    df['Band']=df['Band'].fillna(method='ffill')
    df['Winning_Price']=df['Winning_Price'].fillna(method='ffill')
    spectrum_bands=['2100 MHz','2300 MHz']
    remarks=['✔️','✔️']
    operators=df['Company_Name'].unique().tolist()
    lsa=df['Service_Area'].unique().tolist()
    
    stats,bands,winners,freq,revenue=st.tabs(['🍎Auction Stats','🍏Bands','🍑Winners','🍓Frequency','🍇Revenue'])
    with stats:
        #st.balloons()
        st.subheader(":rainbow[Statistics for 2010 Auction]")
        st.markdown("###### 👉 3G and BWA Auction")
        st.markdown("###### :key: Auction of 3G band,2100 MHz and BWA band, 2300 MHz")
        st.markdown("###### :bell: 100 percent spectrum was sold")
        st.markdown("###### :nazar_amulet: Auction Format - Simultaneous Multi Round Auction(SMRA)")
        st.markdown("###### :chopsticks: Nine bidders participated in 3G auction")
        st.markdown("###### :jigsaw: Eleven bidders particpated in BWA auction")
        st.markdown("###### :stopwatch: 3G Auction lasted 34 days from  9th April to 19th May, 2010)")
        st.markdown("###### :timer_clock: BWA Auction lasted 16 days from 24th May to 11th June, 2010)")
        st.markdown("###### :slightly_smiling_face: Auction ended in total 183/117 clock rounds for 3G/BWA")
        st.write( """#### """," | ",auction_timetable," | ")
        st.write( """#### """," | ", nia," | ")
        st.write( """#### """," | ", linkedinlink," | ")
    with bands:
        #dataframe for dispalying the LSA names where spectrum was sold
        st.markdown("#### :man-cartwheeling: The auctioned bands which were :green[sold] ; which were :red[not sold :anguished:]")
        df_bands=pd.DataFrame()
        #st.write(type(bands))
        df_bands['Bands']=spectrum_bands
        df_bands['Remarks']=remarks
        df_bands.index+=1
        st.table(df_bands.T)
        
               
        # st.markdown('1) Six bands were offered in the :red[2016] auction:  \n\n  :violet[700 MHz,800 MHz, 900 MHz, 1800 MHz,2100 MHz,\
        #             2300 MHz and 2500 MHz](:red[700 band] not sold in any LSA)\n\n \
        #              \n 2) Spectrum got auctioned in the following service areas: ')
        st.markdown("#### :doughnut: The service areas for which Spectrum was bought by the TSPs")
        df_lsa=pd.DataFrame()
        df_lsa['LSAs']=lsa
        df_lsa.index+=1
        st.dataframe(df_lsa.T)
    with winners:
        winner=[str(x) for x in operators]
        winner = list(set(winner)) # to make it unique
        winner.sort()
        df_winner=pd.DataFrame()
        df_winner['Successful Bidders']=winner
        df_winner.index+=1
        st.table(df_winner.T)
        #st.markdown('#### The Winners of 3G/BWA auction are: \n\n {}'.format(" ,".join([str(x) for x in operators])))
        st.markdown('#### Detailed list of winners in each LSAs')
        st.subheader('',divider='grey')
        #drop duplicates
        win=df[['Service_Area','Band','Company_Name']]\
            .drop_duplicates(subset=['Service_Area','Band','Company_Name']).reset_index(drop=True)
        win.index += 1
        st.dataframe(win)

    with freq:
        #st.dataframe(df[['Band','Service_Area','Company_Name','Start_Freq','Stop_Freq']])
        # dfg=df.groupby(['Service_Area','Band','Company_Name'],as_index=False)[['Uplink_Start','Uplink_Stop']].agg({'Uplink_Start':'min','Uplink_Stop':'max'})
        # dfg['quantum']=dfg['Uplink_Stop']-dfg['Uplink_Start']       
        dfg=pd.read_csv('final_results_2010_grouped_processed.csv')
        dfg.index+=1
        st.dataframe(dfg, column_config={
        "Frequency-Quantum": st.column_config.Column(
            width="medium"
        )
    })

    with revenue:
        #drop duplicates for display.
       
        price=df[['Service_Area','Band','Company_Name','Winning_Price']].reset_index(drop=True)
       
        price_grp=price.groupby(['Company_Name','Band','Service_Area'],as_index=False)[['Winning_Price']].sum()
        price_grp.index+=1
        st.subheader('1. Total cash outflow per TSP per LSA per Band')
        st.dataframe(price_grp)
        
        st.subheader('2. Consolidated cash outflow for each TSP from all LSAs')
        gp=price.groupby(['Company_Name'])['Winning_Price'].sum().reset_index(drop=False)
        gp.index+=1
        st.dataframe(gp)
        st.write('',divider='grey')
        st.subheader(f'3. Consolidated Revenue to Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(),2)} Crores]')
   