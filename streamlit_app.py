# Import python packages

import requests
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:")



cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

name_on_order = st.text_input("Name on Smothie: ")
st.write("The name on your Smothie will be: ", name_on_order)

ingridients_list  = st.multiselect(
    "Choose up to 5 ingridients:"
    , my_dataframe
    , max_selections =5
    
)

if ingridients_list:

    ingredients_string = ''

    for fruit_chosen in ingridients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search valuer for', fruit_chosen, ' is ', search_on, '.' )
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)


    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string +  """','""" +  name_on_order + """')"""
    
    st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!' , icon="✅")


