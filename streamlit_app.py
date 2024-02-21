import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header("🥣 Breakfast Menu")
streamlit.text("🥗 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥑🍞 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruits_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruits_list = my_fruits_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits", list(my_fruits_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruits_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like to have?', 'Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# normalize the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


#allow the user to add a fruit to the list
new_fruit_choice = streamlit.text_input('What fruit would you like to add to the list', 'jackfruit')
streamlit.write('Thanks for adding ', new_fruit_choice)
#sqls = "INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values (" + new_fruit_choice ))
sqls = "INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values('" + new_fruit_choice + "')"
streamlit.text(sqls)
my_cur.execute(sqls)

my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
my_data_row_fruits = my_cur.fetchall() #fetch ALL row
streamlit.header("The fruit list contains")
streamlit.dataframe(my_data_row_fruits)

my_cur.execute("INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values('from streamlit')")
