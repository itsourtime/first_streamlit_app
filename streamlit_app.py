import streamlit
import requests
streamlit.title("My Parents New Healthy Diner")

streamlit.header("🥣 Breakfast Menu")
streamlit.text("🥗 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥑🍞 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
import pandas 
my_fruits_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruits_list = my_fruits_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits", list(my_fruits_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruits_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input("What fruit would you like to have?")
streamlit.write('The user entered ' fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice")
# streamlit.text(fruityvice_response.json())

# normalize the json response
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)
