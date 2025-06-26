import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie! 🎈")
st.write(
  """
  Choose your fruits here
  """
)

# Create Snowflake connection once
cnx = st.connection("snowflake")
session = cnx.session

# Get user input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get fruit options from database
my_dataframe = session.table('SMOOTHIES.PUBLIC.FRUIT_OPTIONS').select(col('FRUIT_NAME'))

# Let user select ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

# Create order when ingredients are selected
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    
    # Use parameterized query to prevent SQL injection
    my_insert_stmt = """
    INSERT INTO smoothies.public.orders(ingredients, NAME_ON_ORDER)
    VALUES (?, ?)
    """
    
    # Show the query (for debugging)
    st.write(f"Query will insert: '{ingredients_string}' for '{name_on_order}'")
    
    # Submit order button
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        # Execute with parameters to prevent SQL injection
        session.sql(my_insert_stmt).bind_params([ingredients_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
