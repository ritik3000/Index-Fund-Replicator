import streamlit as st

import pandas as pd
import numpy as np
from datetime import date

# from sklearn import datasets

# from sklearn.ensemble import RandomForestClassifier

#Year_List=[2,3,4,5,6,7,8,9,10]


st.write("""

# Market Cap. Index fund

""")



st.sidebar.header('User Input Values')



def user_input_features():

    #Int_Rate = st.sidebar.slider('Interest Rate in %', 6.0, 42.0, 10.0)

    	##st.sidebar.add_rows

    Principal = int(st.sidebar.text_input('Please input Portfolio amount in numerics',0))

    	##st.sidebar.add_rows

    #No_Of_Years = st.sidebar.selectbox('Select No Of Years',Year_List, 2)



    data =  Principal
            
    #features = pd.DataFrame(data, index=[0])
    return data



data = user_input_features()





st.subheader('User Entered portfolio value is')

st.write(data)


def weighed_portfolio(x):

    url='https://www.moneycontrol.com/stocks/marketinfo/marketcap/nse/index.html'
    #x=int(input('enter the amount in numerics'))
    
    
    
    
    dfs = pd.read_html(url)
    print(dfs[0])
    top_stocks=dfs[0]
    top_stocks['Company Name']=top_stocks['Company Name'].apply(lambda x:x[0:x.find('Add')-1])
    top_stocks=top_stocks[0:30]
    total_market_cap=top_stocks['Market Cap(Rs. cr)'].sum()
    top_stocks['contribution']=top_stocks['Market Cap(Rs. cr)']/total_market_cap
    
    
    
    
    df=top_stocks
    df.sort_values(['Market Cap(Rs. cr)'],ascending=False,inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    
    
    
    balance=0
    units_to_buy=[0]*30
    for i in range(0,30):
        purchase_power=x*df.loc[i,'contribution']
        if(purchase_power//df.loc[i,'Last Price']>=1):
            units_buy=purchase_power//df.loc[i,'Last Price']
            units_to_buy[i]=units_buy
            balance+=(purchase_power-(df.loc[i,'Last Price']*units_buy))
        else:
            balance+=purchase_power
            
    #print(purchase_power)     
    df['units_to_buy']=units_to_buy 
    #df.to_excel('output_3.xlsx',index=False)
            
    
    flag=0
    while(flag!=30):
        flag=0
        
        for i in range(0,30):
            if(balance>=df.loc[i,'Last Price']):
                balance-=df.loc[i,'Last Price']
                units_to_buy[i]+=1
            else:
                flag+=1
                
    
    df['units_to_buy']=units_to_buy   
        
    df=df[['Company Name','units_to_buy','Last Price']]
    #st.dataframe(df.style.highlight_max(axis=0))
    #print("---------------------------")
    #print(balance)
    #print("---------------------------")
    
    #df.to_excel('output_2.xlsx',index=False)
    df=df.rename(columns={'Last Price':'last_price'})
    df['units_to_buy']=df['units_to_buy'].astype(int)
    balance=round(balance, 2)
    #df['Last Price']= df['Last Price'].round(2)
    df.last_price=df.last_price.round(2)
    return df,balance




df_1,balance=weighed_portfolio(data)

st.subheader('The amount that cannot be allocated is')
st.write(balance)

today = date.today()
d1 = today.strftime("%d/%m/%Y")

st.subheader('The portfolio as on {date} should be'.format(date=d1))
#df_1.last_price=(np.floor(df_1.last_price*100)/100).map('{:,.2f}'.format)
#pd.options.display.float_format = '{:,.2f}'.format
df_1=df_1.rename(columns={'last_price':'Last Price','units_to_buy':'No. of Shares to be purchased'})
df_1.index=df_1.index+1

st.table(df_1.style.set_precision(2))
