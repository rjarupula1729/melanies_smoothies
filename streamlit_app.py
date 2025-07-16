# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input(' Name of Smoothie:')
st.write('Tha name on your smoothie will be: ', name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data = my_dataframe, use_container_width = True)
#st.stop()
# Convert the snowpark dataframe to a pandas dataframe so we can use LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe ,max_selections=5)

if ingredient_list:
    ingredients_string = ''

    for fruits_choosen in ingredient_list:
        ingredients_string += fruits_choosen + ' '
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/"+fruits_choosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Your Smoothie is ordered! {name_on_order}",  icon="✅")
