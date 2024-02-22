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


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # streamlit.text(fruityvice_response.json())
    # normalize the json response
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like to have?')
 # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()
  
#streamlit.stop()

#snowflake functions

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)


#allow the user to add a fruit to the list
streamlit.header("View our Fruit List - Add Your Favorites")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall() #fetch ALL row   

if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row_fruits = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_row_fruits)

#sqls = "INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values('" + new_fruit_choice + "')"
#streamlit.text(sqls)
#my_cur.execute(sqls)
#my_cur.execute("INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values('from streamlit')")

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT into pc_rivery_db.public.fruit_load_list (fruit_name) values('" + new_fruit + "'")
        return "Thanks for adding " + new_fruit
        
new_fruit_choice = streamlit.text_input('What fruit would you like to add to the list')
if streamlit.button('Add fruit to the load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(new_fruit_choice)
    my_cnx.close()
    streamlit.write(back_from_function)
    
