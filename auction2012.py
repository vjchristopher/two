import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    linkedinlink = '[DoT Website](https://dot.gov.in/spectrum-management/2463)'
    auction_timetable = '[Time Table]()'
    nia = '[NIA](https://dot.gov.in/sites/default/files/18_0.pdf)'
    
    col1, mid, col2 = st.columns([2, 1, 20])
    with col1:
        st.image('dot.jpg', width=80)
    with col2:
         st.write("""## Spectrum Auction in Year 2012""")

    # Read and ffill cleaning
    df = pd.read_csv('final_results_2012.csv')
    df['Service_Area'] = df['Service_Area'].ffill()
    df['Band'] = df['Band'].ffill()
    df['Company_Name'] = df['Company_Name'].ffill()
    df['Winning_Price'] = df['Winning_Price'].ffill()
    
    spectrum_bands = ['800 MHz', '1800 MHz']
    remarks = ['❌', '✔️']
    operators = df['Company_Name'].unique().tolist()
    lsa = df['Service_Area'].unique().tolist()
    
    stats, bands, winners, freq, revenue = st.tabs(['🍎Auction Stats', '🍏Bands', '🍑Winners', '🍓Frequency', '🍇Revenue'])
    
    with stats:
        st.subheader(":rainbow[Statistics for 2012 Auction]")
        st.markdown("###### 👉 2G Auction")
        st.markdown("###### :key: Auction of 2G bands- 800 MHz and 1800 MHz")
        st.markdown("###### :gem: Quantum of Spectrum put to auction: :blue[390 MHz]")
        st.markdown("###### :battery: Quantum of Spectrum sold: :green[127.5 MHz] ")
        st.markdown("###### :bell: 33 percent spectrum was sold")
        st.markdown("###### :nazar_amulet: Auction Format - Simultaneous Multi Round Auction(SMRA)")
        st.markdown("###### :chopsticks: Six bidders participated in 2G auction")
        st.markdown("###### :jigsaw: Five bidders won spectrum")        
        st.markdown("###### :wastebasket: The 800 MHz band was not sold.")
        st.markdown("###### :stopwatch: The Auction lasted only one day - 14th November, 2012")
        st.markdown("###### :slightly_smiling_face: Auction ended in 14 clock rounds")
        
        # Load and render table
        time_table = pd.read_excel('time_table_auction_12.xlsx')
        st.markdown("##### <span style='color : DodgerBlue'><u>|AUCTION TIME_ TABLE|</u></span>", unsafe_allow_html=True)
        time_table.index += 1
        st.table(time_table)        
        
        st.write("#### ", " | ", nia, " | ")
        st.write("#### ", " | ", linkedinlink, " | ")

    with bands:
        st.markdown("#### :man-cartwheeling: The bands which were :green[sold] ; few which were :red[not sold :anguished:]")
        df_bands = pd.DataFrame()
        df_bands['Bands'] = spectrum_bands
        df_bands['Remarks'] = remarks
        df_bands.index += 1
        st.table(df_bands.T)
        
        st.markdown("#### :doughnut: The service areas for which Spectrum was bought by the TSPs")
        df_lsa = pd.DataFrame()
        df_lsa['LSAs'] = lsa
        df_lsa.index += 1
        st.dataframe(df_lsa.T)
        
    with winners:
        winner = [str(x) for x in operators]
        winner = list(set(winner))
        winner.sort()
        df_winner = pd.DataFrame()
        df_winner['Successful Bidders'] = winner
        df_winner.index += 1
        st.table(df_winner.T)
        
        st.markdown('#### Detailed list of winners in each LSAs')
        st.subheader('', divider='grey')
        
        win = df[['Service_Area', 'Band', 'Company_Name']].drop_duplicates(
            subset=['Service_Area', 'Band', 'Company_Name']
        ).reset_index(drop=True)
        win.index += 1
        st.dataframe(win)
        
        ax = px.bar(
            win, x='Service_Area', facet_col='Band', color='Band', facet_col_wrap=1, 
            hover_name='Company_Name', text='Company_Name', 
            color_continuous_scale=px.colors.sequential.Tealgrn, 
            labels={'count': 'Count of TSPs in the LSA'}
        )
        ax.update_layout(autosize=False, width=1400, height=500)
        st.plotly_chart(ax, theme=None)
        
    with freq:
        dfg = pd.read_csv('final_results_2012_grouped_processed.csv')
        dfg.index += 1
        st.dataframe(dfg, column_config={
            "Frequency, Quantum": st.column_config.Column(width="medium")
        })
        
        df_slice = pd.read_csv('Slices_2012_processed.csv')
        fig = px.treemap(
            df_slice, path=['Service_Area', 'Company_Name', 'Freq_slices'], 
            title='Spectrum slices acquired by the TSPs in 2012 Auction'
        )
        fig.update_layout(autosize=False, width=700, height=1200)
        st.plotly_chart(fig, theme="streamlit")
        
    with revenue:
        price = df[['Service_Area', 'Band', 'Company_Name', 'Winning_Price']].reset_index(drop=True)
        st.subheader('1. Consolidated cash outflow for each TSP from all LSAs')
        
        # Calculate metric structures
        gp = price.groupby(['Company_Name'])['Winning_Price'].sum().reset_index(drop=False)
        gross_total = gp['Winning_Price'].sum()
        
        # Generate chart config mapping with clean dataset metrics
        ax = px.bar(
            gp, y='Company_Name', x='Winning_Price', hover_name='Company_Name', 
            orientation='h', text_auto='0', template='seaborn',
            title='Winners of the Spectrum Auction',
            labels={
                'Company_Name': 'Winners in Auction',
                'Winning_Price': 'The payment committed by each TSP in Rs Crore at the end of Auction'
            }
        )
        ax.update_layout(autosize=False, width=800, height=600).update_traces(marker=dict(color='crimson'))
        
        # Concat Total row into DataFrame natively before UI delivery
        df2 = pd.DataFrame({'Company_Name': ['Gross Total'], 'Winning_Price': [gross_total]})
        final_table_df = pd.concat([gp, df2], ignore_index=True)
        final_table_df.index += 1
        
        # Render visual components
        st.dataframe(final_table_df)
        st.plotly_chart(ax, theme=None)

        # Breakdown Groupings
        price_grp = price.groupby(['Company_Name', 'Band', 'Service_Area'], as_index=False)[['Winning_Price']].sum()
        price_grp.index += 1
        st.subheader('2. Total cash outflow per TSP per LSA per Band')
        st.dataframe(price_grp)
        
        fig = px.treemap(
            price_grp, path=['Service_Area', 'Band', 'Company_Name', 'Winning_Price'], 
            values='Winning_Price', color='Winning_Price', hover_data=['Service_Area'], 
            color_continuous_scale='RdBu', 
            labels={
                'Winning_Price': 'Price in Rs.Crore',
                'Service_Area': 'LSA',
                'Winning_Price_sum': 'Winning Price'
            },
            title='Payment Committed in Rs Crores by each TSP per band per LSA'
        )
        fig.update_layout(autosize=False, width=1000, height=1600)
        st.plotly_chart(fig, theme="streamlit")
        
        st.divider()
        st.subheader(f'3. Consolidated Revenue to Govt from all bidders : :green[Rs.{round(price_grp.Winning_Price.sum(), 2)} Crores]')

       


