import streamlit
import pandas as pd
import snowflake.connector

streamlit.title("My parents New Healthy Diner")

streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, spinach and Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include
my_fruit_list = my_fruit_list.set_index('Fruit')
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]
# Display the table on the page.
streamlit.dataframe(fruit_to_show)

import requests
streamlit.header("Fruityvice Fruit Advice!")

#Taking fruit choice from user
fruit_choice = streamlit.text_input("What fruit would you like information about?", 'kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

#Using pandas to convert json to a table like format (dataframe)
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

#Output dataframe to screen
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains : ")
streamlit.text(my_data_row)
