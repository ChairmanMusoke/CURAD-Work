import streamlit as st
import pandas as pd
from PIL import Image

# Sample menu data (you can replace this with a database later)
menu_data = [
    {"name": "Margherita Pizza", "price": 10, "image": "photo.jpg", "category": "Main Course"},
    {"name": "Cheeseburger", "price": 8, "image": "photo.jpg", "category": "Main Course"},
    {"name": "Chocolate Cake", "price": 5, "image": "photo.jpg", "category": "Dessert"},
    {"name": "Lemonade", "price": 3, "image": "photo.jpg", "category": "Beverage"}
]
menu_df = pd.DataFrame(menu_data)

# Page Configuration
st.set_page_config(page_title="Devine Bites", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Menu", "Blog", "Order Now"])

# Home Page
if page == "Home":
    st.title("Welcome to Devine Bites! 🍽️")
    st.image("photo.jpg", use_column_width=True)
    st.write("Where every meal feels like home.")

# Menu Page
elif page == "Menu":
    st.title("Our Menu 📜")
    category = st.selectbox("Filter by category:", ["All"] + list(menu_df["category"].unique()))
    
    filtered_menu = menu_df if category == "All" else menu_df[menu_df["category"] == category]
    
    for index, row in filtered_menu.iterrows():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(row["image"], width=100)
        with col2:
            st.subheader(row["name"])
            st.write(f"Price: ${row['price']}")
            if st.button(f"Order {row['name']}", key=index):
                st.session_state["order"] = row["name"]
                st.experimental_rerun()

# Blog Page
elif page == "Blog":
    st.title("Devine Bites Blog 📝")
    st.write("Stay updated with our latest news, dishes, and events.")
    st.write("(Blog posts will go here...)")

# Order Now Page
elif page == "Order Now":
    st.title("Place Your Order 🛒")
    if "order" in st.session_state:
        st.write(f"You selected: **{st.session_state['order']}**")
    name = st.text_input("Your Name")
    address = st.text_area("Delivery Address")
    if st.button("Submit Order"):
        st.success("Order placed successfully! We'll contact you soon.")
