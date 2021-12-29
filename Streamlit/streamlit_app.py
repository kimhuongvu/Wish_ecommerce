import streamlit as st
import spacy_streamlit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle, argparse 
import tensorflow as tf
import seaborn as sns

import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder,MinMaxScaler,PolynomialFeatures,OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import xgboost

PATH = 'EDA/EDA_Wish.csv'
DATA_RAW = 'EDA/Data Raw.csv'
filename = 'Model/XGBoostClassifier.save_model'

def set_home():
    home = '''
    # About Wish
    
    **Wish** is operated by ContextLogic Inc. in [San Francisco](https://en.wikipedia.org/wiki/San_Francisco), United States. 
    The platform employs browsing technologies that personalize shopping visually for each customer, rather than relying on a search bar format. 
    It allows sellers to list their products on Wish and sell directly to consumers. 
    Wish works with payment service providers to handle payments and does not stock the products themselves or manage returns.
    
    **Wish** is an American online [e-commerce](https://en.wikipedia.org/wiki/E-commerce) platform that facilitates transactions between sellers and buyers.
    Wish was founded in 2010 by [Piotr Szulczewski](https://en.wikipedia.org/wiki/Piotr_Szulczewski) (CEO) and Danny Zhang (former CTO). Wish** has become one of the most popular ecommerce platforms in the world — by selling an avalanche of cheap junky stuff, nearly all of it sourced from China. 
    Most of Wish’s customers are working-class people who can’t afford Amazon Prime and are more likely to shop at dollar stores. Today, just 20% of the company’s customers fork over $119 a year for Amazon Prime, while nearly 90% frequent Walmart.

    Some FAQ about Wish:

    - There are **over** **300 million items** available on Wish ([Indigo Digital](https://www.indigo9digital.com/blog/seven-things-you-may-not-know-about-wish-the-shopping-app-that-is-taking-on-ebay-and-amazon))
    - A **third** of Wish’s total **order volume** comes from **the US** ([Forbes](https://www.forbes.com/sites/laurendebter/2020/07/30/wish-ecommerce-shipping-rate-increase-china-brick-and-mortar-stores-partnership/#7dbea53a4d6e))
    - It is the **fourth** largest **online marketplace** in the **US** by sales volume
    - Wish was the **most downloaded** shopping app in the world in **2018** ([Forbes](https://www.forbes.com/sites/parmyolson/2019/03/13/meet-the-billionaire-who-defied-amazon-and-built-wish-the-worlds-most-downloaded-e-commerce-app/#49154bd870f5))
    - Wish **sells** about **three million items** daily
    - Wish main demographic is **young and middle class** ([Cnet](https://www.cnet.com/news/shopping-app-wish-is-building-a-retail-empire-on-2-sunglasses/))
    
    ## Problem Statement

    Increasing penetration of the internet is bolstering the smartphone using population across the world. Digital content, travel and leisure, financial services, e-tailing among others constitute a variety of e-commerce options available to the internet accessing customer base that are gaining momentum with increased internet usage.
    This shows that e-commerce is a potential market for many retailers around the world.
    By offering their customers a way to browse specific items recommended to them, and focusing more on discounted pricing than anything else, Wish is turning eCommerce conventional wisdom on its head.

    ## Solution Statement
    
    To be more specific, the solution statement is to create a machine learning model that can forecast the sale volume of the merchant in Wish e-commerce by the classification algorithm, which has 7 classes followed in order by 100, 1.000, 5.000, 10.000, 20.000, 50.000, 100.000.
    Before that, we will explore data and answer a few questions to know deeply about this dataset.
    
    **A** **BIG** **QUESTION**: What are the elements that help the new seller increase their sales?

    - What is the difference between the 'price' from 'retail price' and how is the effect of the units sold?
    - Does having ad boosts increase success?
    - Is there any correlation between units sold and ratings?
    - Does a badge contribute to the sales of a product? What is the effect of different types of badges?
    - Do increased variations lead to increased success?
    - How does shipping affect sales?
    - Which tags should merchants use?
    - Does seller location affect sales?
    - What kind of merchants is likely to gain product success?
    - Do all product contains pictures?
    - What about the details of the merchant? Does not having a profile picture reduce success? Perhaps detailed info leads to higher success?
    '''

    dataset_info = '''
    - The data comes from the Wish platform, an e-commerce site that is famous for selling items at affordable prices. This dataset contains product listings as well as products **ratings** and **sales performance.**
    - The data was scraped in the ***french localisation*** (hence some non-ascii Latin characters such as « é » and « à ») in the title column.

    '''

    columns_information = '''

    | Column name    		        | Description    	                                                            	                                                          
    |---					        |---				                                                                                                                      |
    | Title_orig       	            | contains the original title (the base title) that is displayed by default	                                                              |
    | Discount_price		        |  discount price                        			                                                                                      |  
    | Retail_price		            | retail price, or reference price in other stores/places.Used by the seller to indicate a regular value or the price before discount     |
    | Nb_cart_orders_approx         | number of units sold. Lower bound approximation by steps			                                                                      |
    | Rating	                    | mean product rating                                                   	                                                              |     
    | Product_color		            | product's main color                                           			                                                              |
    | Product_variation_size_id     | one of the available size variations for this product        				                                                              |
    | Product_variation_inventory	| inventory the seller has. Max allowed quantity is 50				                                                                      |
    | Shipping_option_price         | shipping price                                                                                                                          |
    | Merchant_title                | merchant's displayed name (show in the UI as the seller's shop name)                                                                    |                                               
    | Merchant_name                 | merchant's canonical name. A name not shown publicly. Used by the website under the hood as a canonical name. Easier to process since all lowercase without white space |
    <p><br></p>
    ---
    '''

    data_source = '''
    --- 
    ## Data source: 

    Sales of summer clothes in E-commerce Wish   
    https://www.kaggle.com/jmmvutu/summer-products-and-sales-in-ecommerce-wish

    '''

    img_intro_1 = 'https://cdn.dribbble.com/users/2701034/screenshots/8217027/media/672c4538404d09bc4cfc58d1a27e81f6.png?compress=1&resize=800x600'
    img_intro_2 = 'https://cdn.dribbble.com/users/2701034/screenshots/8807775/media/8b7effeb5fb6173bcbd17b3edcf6a4c0.png?compress=1&resize=1600x1200'
    
    col1, col2= st.columns(2)

    with col1:
        st.image(img_intro_1, use_column_width='always')
    with col2:
        st.image(img_intro_2, use_column_width='always')
    
    st.write(home, unsafe_allow_html=True)
    st.header('Data information')
    st.write(dataset_info,unsafe_allow_html=True)
    st.write(columns_information, unsafe_allow_html=True)
    st.write(data_source,unsafe_allow_html=True )

def set_eda():
    dataset = pd.read_csv('EDA/Dataset_Wish.csv')
    data_raw = pd.read_csv(DATA_RAW)

    # Show dataframe
    data_selection = st.radio(
        "Data Selection",
        ('Raw Data', 'Cleaned Data'),
        help='Data source that will be displayed in the charts')
    if data_selection == 'Raw Data':
        with st.container():
            st.header('Descriptive Statistics\n')
            st.table(data_raw.describe())
        
    else:
        with st.container():
            st.header('Descriptive Statistics\n')
            st.table(dataset.describe())

    st.header('Data Visualization')
    height, width, margin = 450, 1500, 10

    st.subheader('Scatterplot')

    select_numerical = st.selectbox(
        'Select the Numerical Variable',
        ['discount_price', 'retail_price'])
    fig = sns.histplot(data=dataset, x="retail_price")

def load_model():
    # loaded_model = pickle.load(open(filename, 'rb'))
    loaded_model = xgboost.XGBClassifier()
    loaded_model.load_model(filename)
    return loaded_model
    
def set_predict():
    st.subheader("Wish Sales Predictor - for new seller")

    cols = st.columns((1, 1))

    retail_price = cols[0].number_input("Retail price",1.00,12256.00,1.00)
    discount_price = cols[1].number_input("Discount price",1.00,12256.00,1.00)
    
    cols = st.columns(2)
    product_variation_size_id = cols[0].selectbox("Size",["XXXS","XS","S","M","L","Xl","XXL","XXXXL","XXXXXL", 'Other'])
    origin_country = cols[1].selectbox("Country",['CN', 'CA', 'US', 'KR', 'GB', 'PL', 'CZ', 'VN', 'VE', 'TR', 'Other'])
    
    cols = st.columns(2)
    shipping_option_name = cols[0].selectbox("Shipping option name",['Livraison standard', 'Livraison Express'])
    product_color = cols[1].selectbox("Color",['White', 'Red', 'Grey', 'Yellow', 'Orange', 'Green','Brown', 'Black', 'Blue', 'Pink', 'Purple', 'Dual', 'Other'])
    
    cols = st.columns(3)
    shipping_option_price = cols[0].slider("Shipping price",0.00,80.00,0.10)
    inventory_total = cols[1].slider("Variation inventory",0,50,1)
    product_variation_inventory =cols[2].slider("Product variation inventory",0,50,1)

    # Predict button
    button = st.button('Predict !!!')
    st.markdown(
        "<hr />",
        unsafe_allow_html=True)

    if button:
        st.spinner("Generating the best for you ...")
        #### CLASSIFICATION ####
        df = pd.read_csv('EDA/Dataset_Wish.csv')

        x = df.drop('nb_cart_orders_approx',axis=1)
        y = df['nb_cart_orders_approx']

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Preprocessing
        numerical = list(x_train.select_dtypes('number').columns) 
        categorical = [col for col in x_train.columns if col not in numerical]

        cat_pipe = Pipeline([('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))])
        num_pipe = Pipeline([
                        ('poly', PolynomialFeatures(degree=1, include_bias=False)), 
                        ('scaler', MinMaxScaler())
                        ])

        # Fit column transformer to training data
        full_pipeline = ColumnTransformer(transformers=[
                                            ('cat', cat_pipe, categorical),
                                            ('num', num_pipe, numerical)],
                                            remainder='passthrough')

        X_train_transformed = full_pipeline.fit_transform(x_train)
        X_test_prepared = full_pipeline.transform(x_test)

        my_model= load_model()

        final_model = my_model.fit(X_train_transformed, y_train)
        y_pred = my_model.predict(X_test_prepared)

        test_data = {
        'discount_price': discount_price,
        'retail_price' : retail_price,
        'product_color' : product_color,
        'product_variation_size_id': product_variation_size_id,
        'product_variation_inventory': product_variation_inventory,
        'shipping_option_name': shipping_option_name,
        'shipping_option_price' : shipping_option_price,
        'inventory_total':inventory_total,
        'origin_country': origin_country}

        test_df = pd.DataFrame(data=test_data, index = ['Option'])
        test_df

        X_test_real = full_pipeline.transform(test_df)

        # Using the best_estimator to predict 
        unit_pred = my_model.predict(X_test_real)
        for i, unit in enumerate(unit_pred):
            st.success(f'The predicted cart is {round(unit, 2)}')

        with st.expander("Model Parameters"):
            st.write(f"{my_model}")

        with st.expander('Available Models'):     
            report = classification_report(y_test, y_pred)
            st.write('Report', report)

# Header page
st.set_page_config(page_title='EDA - Wish - Shopping Made Fun',
                   page_icon='https://seeklogo.com/images/W/wish-logo-64777655D1-seeklogo.com.jpg',
                   layout="wide")

# Sub header page
st.sidebar.image('Media/wish_logo.png', width=200)
st.sidebar.header('Are you a new seller in Wish?')
st.sidebar.markdown('You do not know how to optimize your performed to get more order cart? ')

# Select dashboard view from sidebar
menu = st.sidebar.selectbox('Select view', ('Home',
                                'Predict your customers cart'))
def main():
    if menu == 'Home':
        set_home()
    elif menu == 'Exploratory Data Analysis':
        set_eda()
    elif menu == 'Predict your customers cart':
        set_predict()
        # model_predict()

    

if __name__ == '__main__':
    main()    