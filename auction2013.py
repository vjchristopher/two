import streamlit as st
import pandas as pd
import plotly_express as px

def app():
    linkedinlink = '[DoT Website](https://dot.gov.in/spectrum-management/2463)'
    auction_timetable='[Time Table](https://dot.gov.in/sites/default/files/Revised%20Auction%20table_0.pdf)'
    nia='[NIA](https://dot.gov.in/sites/default/files/30-1-13.pdf)'
    col1, mid, col2 = st.columns([2,1,20])
    with col1:
      st.image('dot.jpg', width=80)
    with col2:
       st.write("""## Spectrum Auction In Year 2013""")
    
    df=pd.read_csv('final_results_2013.csv')
    df['Service_Area']=df['Service_Area'].fillna(method='ffill')
    df['Band']=df['Band'].fillna(method='ffill')
    df['Company_Name']=df['Company_Name'].fillna(method='ffill')
    df['Winning_Price']=df['Winning_Price'].fillna(method='ffill')
    spectrum_bands=['800 MHz','900 MHz','1800 MHz']
    remarks=['✔️','❌','❌']
    operators=df['Company_Name'].unique().tolist()
    lsa=df['Service_Area'].unique().tolist()
    
    stats,bands,winners,freq,revenue=st.tabs(['🍎Auction Stats','🍏Bands','🍑Winners','🍓Frequency','🍇Revenue'])
    with stats:
        st.subheader(":rainbow[Statistics for 2013 Auction]")
        st.markdown("###### 👉 2G Auction")
        st.markdown("###### :key: Auction of 2G bands- 800 MHz, 900 MHz and 1800 MHz")
        st.markdown("###### :gem: Quantum of Spectrum put to auction: :blue[195 MHz]")
        st.markdown("###### :battery: Quantum of Spectrum sold: :green[30 MHz] ")
        st.markdown("###### :bell: 15 percent spectrum was sold")
        st.markdown("###### :nazar_amulet: Auction Format - Simultaneous Multi Round Auction(SMRA)")
        st.markdown("###### :chopsticks: Only one bidders participated-SSTL")
        st.markdown("###### :jigsaw: One bidder won spectrum in 800 MHz")        
        st.markdown("###### :wastebasket: The 900 MHz and 1800 MHz band were not sold.")
        st.markdown("###### :stopwatch: The Auction lasted only one day - 11th March, 2013")        
        st.markdown("###### :slightly_frowning_face: Auction ended in 3 clock rounds")
        #st.write( """#### """," | ",auction_timetable," | ")
        
        #Bring in the data
        time_table = pd.read_excel('time_table_auction_13.xlsx')
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
         #plot        
        # ax=px.line(win,x='Service_Area',y='Company_Name',facet_col='Band',color='Band',facet_col_wrap=1,
        #           text='Company_Name',labels={'Company_Name':'Name of TSP'})
        ax=px.bar(win,x='Service_Area',facet_col='Band',color='Band',facet_col_wrap=1,hover_name='Company_Name',
                  text='Company_Name',color_continuous_scale=px.colors.sequential.Tealgrn,labels={'count':'Count of TSPs in each LSA'})

        ax.update_layout(
            autosize=False,
            width=1400,
            height=700,
        )#.update_traces(marker=dict(color='red'))
       
        st.plotly_chart(ax,  theme='streamlit')
    with freq:
        #st.dataframe(df[['Band','Service_Area','Company_Name','Uplink_Start','Uplink_Stop']])
        #do a groupby to agregate the frequencies
        # dfg=df.groupby(['Service_Area','Band','Company_Name'],as_index=False)[['Uplink_Start','Uplink_Stop']].agg({'Uplink_Start':'min','Uplink_Stop':'max'})
        # dfg['quantum']=dfg['Uplink_Stop']-dfg['Uplink_Start']        
        # dfg.index+=1
        dfg=pd.read_csv('final_results_2013_grouped_processed.csv')
        
        dfg.index+=1
        st.dataframe(dfg, column_config={
        "Frequency, Quantum": st.column_config.Column(
            width="large"
        )
        })
        df_slice=pd.read_csv('Slices_2013_processed.csv')
        fig = px.treemap(df_slice, path=['Service_Area','Company_Name','Freq_slices'], title='Spectrum slices acquired by the TSPs in 2013 Auction',
                 )
        fig.update_layout(
        autosize=False,
        width=700,
        height=1200)
        st.plotly_chart(fig, theme="streamlit")

    with revenue:
        #drop duplicates for display.
       
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
        # st.subheader(f'3. Consolidated Revenue to Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(),2)} Crores]')
    
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
        #st.write('',divider='grey')
        st.divider()
        st.subheader(f'3. Consolidated Revenue to Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(),2)} Crores]')


