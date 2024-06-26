import streamlit as st
import pandas as pd
import plotly_express as px
def app():
    linkedinlink = '[DoT Website](https://dot.gov.in/spectrum-management/2463)'
    auction_timetable='[Time Table](https://dot.gov.in/sites/default/files/Revised%20Auction%20table_0.pdf)'
    nia='[NIA](https://dot.gov.in/sites/default/files/NIA_Version_Dated_15_06_2022.pdf)'
    col1, mid, col2 = st.columns([2,1,20])
    with col1:
        st.image('dot.jpg', width=80)
    with col2:
         st.write("""## Spectrum Auction In Year 2022""")

    df=pd.read_csv('final_results_2022.csv')
    df['Service_Area']=df['Service_Area'].fillna(method='ffill')
    df['Band']=df['Band'].fillna(method='ffill')
    df['Company_Name']=df['Company_Name'].fillna(method='ffill')
    df['Winning_Price']=df['Winning_Price'].fillna(method='ffill')
    spectrum_bands=['600 MHz','700 MHz','800 MHz','900 MHz','1800 MHz','2100 MHz','2300 MHz','2500 MHz','3300 MHz','26 GHz']
    remarks=['❌','✔️','✔️','✔️','✔️','✔️','❌','✔️','✔️','✔️']
    operators=df['Company_Name'].unique().tolist()
    lsa=df['Service_Area'].unique().tolist()
    lsa.sort()
    
    stats,bands,winners,freq,revenue=st.tabs(['🍎Auction Stats','🍏Bands','🍑Winners','🍓Frequency','🍇Revenue'])
    
    with stats:
        st.subheader(":rainbow[Statistics for 2022 Auction]")        
        st.markdown("###### 👉 2G/3G/4G/5G Auction")
        st.markdown("###### :key: Auction of multi bands-600,700,800,900,1800,2100,2300,2500,3300,26000 MHz")
        st.markdown("###### :gem: Quantum of Spectrum put to auction: :blue[72097.85 MHz]")
        st.markdown("###### :battery: Quantum of Spectrum sold: :green[51236.2 MHz] ")
        st.markdown("###### :bell: 71 percent spectrum was sold")
        st.markdown("###### :nazar_amulet: Auction Format - Simultaneous Multi Round Auction(SMRA)")
        st.markdown("###### :chopsticks: Four bidders participated in the auction")
        st.markdown("###### :jigsaw: All four bidders won spectrum")
        st.markdown("###### :candy: Adani Networks bought spectrum only in 26 GHz")     
        st.markdown("###### :beer: Spectrum in 600 MHz,3300 MHz and 26 GHz offered first time.")   
        st.markdown("###### :wastebasket: Spectrum in 600 MHz and 2300 MHz band were not sold.")
        st.markdown("###### :stopwatch: Auction lasted only 7 days from 26th July 2022 to 1st August, 2022")
        st.markdown("###### :slightly_smiling_face: Auction ended in 40 clock rounds")
         #st.write( """#### """," | ",auction_timetable," | ")
        
        #Bring in the data
        time_table = pd.read_excel('time_table_auction_22.xlsx')
        st.markdown("##### <span style='color : DodgerBlue'><u>|AUCTION TIME_ TABLE|</u></span>",unsafe_allow_html=True)
        time_table.index+=1
        st.table(time_table)  
       
        st.write( """#### """," | ", nia," | ")
        st.write( """#### """," | ", linkedinlink," | ")
   
    with bands:
        #dataframe for dispalying the LSA names where spectrum was sold
        st.markdown("#### :man-cartwheeling: The bands which were :green[sold] ; few which were :red[not sold :anguished:]")
        df_bands=pd.DataFrame()
        #st.write(type(bands))
        df_bands['Bands']=spectrum_bands
        df_bands['Remarks']=remarks
        df_bands.index+=1
        st.table(df_bands.T)
        
        # st.markdown('1) Ten bands were offered in the :red[2022] auction:  \n\n  :violet[600 MHz,700 MHz,800 MHz, 900 MHz, 1800 MHz,2100 MHz,\
        #             2300 MHz, 2500 MHz ans 26 GHz](:red[600 band and 2300 band] not sold in any LSA)\n\n \
        #              \n 2) Spectrum got auctioned in the following service areas:')
        #dataframe for dispalying the LSA names where spectrum was sold
        st.markdown("#### :doughnut: The service areas for which Spectrum was bought by the TSPs")
        df_lsa=pd.DataFrame()
        df_lsa['LSAs']=lsa
        df_lsa.index+=1
        st.table(df_lsa.T)
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
         #plot       
        # ax=px.bar(win,x='Service_Area',y='Company_Name',facet_col='Band',color='Band',facet_col_wrap=1,
        #           text='Company_Name',color_continuous_scale=px.colors.sequential.solar,labels={'Company_Name':'Name of TSP'})
        ax=px.bar(win,x='Service_Area',facet_col='Band',color='Band',facet_col_wrap=1,hover_name='Company_Name',
                  text='Company_Name',color_continuous_scale=px.colors.sequential.solar,labels={'count':'Count of TSPs in each LSA'})

        ax.update_layout(
            autosize=False,
            width=1400,
            height=2000,
        )#.update_traces(marker=dict(color='red'))
       
        st.plotly_chart(ax,  theme=None)
    with freq:
        #st.dataframe(df[['Band','Service_Area','Company_Name','Uplink_Start','Uplink_Stop']])
        #do a groupby to agregate the frequencies
        # dfg=df.groupby(['Service_Area','Band','Company_Name'],as_index=False)[['Uplink_Start','Uplink_Stop']].agg({'Uplink_Start':'min','Uplink_Stop':'max'})
        # dfg['quantum']=dfg['Uplink_Stop']-dfg['Uplink_Start']
        dfg=pd.read_csv('final_results_2022_grouped_processed.csv')
        
        dfg.index+=1
        st.dataframe(dfg, column_config={
        "Frequency, Quantum": st.column_config.Column(
            width="large"
        )
        })
        df_slice=pd.read_csv('Slices_2022_processed.csv')
        fig = px.treemap(df_slice, path=['Service_Area','Company_Name','Freq_slices'], title='Spectrum slices acquired by the TSPs in 2022 Auction',
                 )
        fig.update_layout(
        autosize=False,
        width=800,
        height=1200)
        st.plotly_chart(fig, theme="streamlit")


    with revenue:
        #drop dupplicates for display
       
        price=df[['Service_Area','Band','Company_Name','Winning_Price']].reset_index(drop=True)        
      
        # price_grp=price.groupby(['Company_Name','Band','Service_Area'],as_index=False)[['Winning_Price']].sum()
        # price_grp.index+=1
        # st.subheader('1. Total cash outflow per TSP per LSA per Band')
        # st.dataframe(price_grp)
        
        # st.subheader('2. Consolidated cash outflow for each TSP from all LSAs')
        # gp=price.groupby(['Company_Name'])['Winning_Price'].sum().reset_index()
        # gp.index+=1
        # st.dataframe(gp)
        # st.write('',divider='grey')
        # st.subheader(f'3. Consolidated Revenue for Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(),2)} Crores]')

        st.subheader('1. Consolidated cash outflow for each TSP from all LSAs')
        gp=price.groupby(['Company_Name'])['Winning_Price'].sum().reset_index(drop=False)
        gp.index+=1
        #gp.loc[len(gp.index)]=['Total',100000]
        my_table=st.dataframe(gp)
        gross_total=gp['Winning_Price'].sum()
        df2=pd.DataFrame({'Company_Name':['Gross Total'],'Winning_Price':[gross_total]})
        my_table.add_rows(df2)
        ax=px.bar(gp,y='Company_Name', x='Winning_Price',hover_name='Company_Name', orientation='h',text_auto='0',template='seaborn',
         title='Winners of the Spectrum Auction',
         labels={'Company_Name':'Winners in Auction','Winning_Price':'The payment committed by each TSP in Rs Crore at the end of Auction ' } )
        ax.update_layout(
        autosize=False,
        width=800,
        height=600,
        ).update_traces(marker=dict(color='crimson'))

        st.plotly_chart(ax, theme=None)

       
        price_grp=price.groupby(['Company_Name','Band','Service_Area'],as_index=False)[['Winning_Price']].sum()
        price_grp.Winning_Price=round(price_grp.Winning_Price,2)
        price_grp.index+=1
        st.subheader('2. Total cash outflow per TSP per LSA per Band')
        st.dataframe(price_grp)
        fig = px.treemap(price_grp, path=['Service_Area','Band','Company_Name','Winning_Price'],values='Winning_Price',color='Winning_Price', 
                 hover_data=['Service_Area'], color_continuous_scale='RdBu', labels={'Winning_Price':'Price in Rs.Crore',
                 'Service_Area':'LSA','Winning_Price_sum':'Winning Price'},
                 title='Payment Committed in Rs Crores by each TSP per band per LSA',
                 )
        fig.update_layout(
            autosize=False,
            width=1000,
            height=1600)
        
        st.plotly_chart(fig, theme="streamlit")
        

        #Display the total
        st.write('',divider='grey')
        st.subheader(f'3. Consolidated Revenue to Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(),2)} Crores]')
