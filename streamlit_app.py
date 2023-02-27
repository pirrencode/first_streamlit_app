import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Setting normalizer
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Get Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        # # Setting normalizer
        # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        # # Running normalizer
        # streamlit.dataframe(fruityvice_normalized)
        streamlit.write('The user entered ', fruit_choice)

except URLError as e:
    streamlit.error()

# Don't run anything before we troubleshoot
# streamlit.stop()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("insert into fruit_load_list values ('from _streamlit');")
# my_data_rows = my_cur.fetchall()

#streamlit.header("Generate recipe!")

streamlit.text('Hit generate when you feel no more fruits are needed for recipe')

streamlit.button('Generate recipe!')
#recipe_name = streamlit.text('Avocado & strawberry smoothie')
streamlit.text('Recipe Avocado & Strawberry smoothie is generated 🥑🥭')

streamlit.header("🥑Avocado & 🥭Strawberry smoothie")

streamlit.header("Ingridients")

#receipe = streamlit.text_input('Hint: Hit generate when you feel no more fruits are needed for recipe')
streamlit.text('')
streamlit.text('½ 🥑avocado, stoned, peeled and cut into chunks')
streamlit.text('150g 🥭strawberry, halved')
streamlit.text('4 tbsp low-fat natural yogurt')
streamlit.text('200ml semi-skimmed milk')
streamlit.text('lemon or lime juice, to taste')
streamlit.text('honey, to taste')

streamlit.header("Method")

streamlit.text('STEP 1')
streamlit.text('Put all the ingredients in a blender and whizz until smooth. If the consistency is too thick, add a little water.')
streamlit.text('STEP 2..')

streamlit.text('Recipe source: BBC goodfood')

streamlit.header("View our Fruit List - Add your Favorites!")

#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

#adding button to load fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.header("The fruit load contains:")

# streamlit.dataframe(my_data_rows)

#Adding second entry box
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
    my_cnx.close()

# streamlit.write('Thanks for adding ', add_my_fruit)