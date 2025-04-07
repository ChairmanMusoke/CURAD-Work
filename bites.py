import streamlit as st
import pandas as pd
import base64
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Devine Bites", layout="wide")
# Custom Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: #f8f9fa;
        }
        .title-text {
            color: #e63946;
            font-size: 60px;
            text-align: center;
            font-weight: bold;
        }
        .subtitle-text {
            color: #457b9d;
            text-align: center;
            font-size: 40px;
        }
        .menu-item {
            background-color: red;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .menu-img {
            border-radius: 10px;
        }
        .order-btn {
            background-color: #e63946;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Sample menu data
menu_data = [
    {"name": "Margherita Pizza", "price": 10, "image": "photo.jpg", "category": "Main Course"},
    {"name": "Cheeseburger", "price": 8, "image": "photo.jpg", "category": "Main Course"},
    {"name": "Chocolate Cake", "price": 5, "image": "photo.jpg", "category": "Dessert"},
    {"name": "Lemonade", "price": 3, "image": "photo.jpg", "category": "Beverage"}
]
menu_df = pd.DataFrame(menu_data)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Menu", "Blog", "Order Now"])

# Home Page
if page == "Home":
    st.markdown("<div class='title-text'>Welcome to Devine Bites! 🍽️</div>", unsafe_allow_html=True)
    st.image("photo.jpg", use_column_width=True)
    st.markdown("<div class='subtitle-text'>Where every meal feels like home.</div>", unsafe_allow_html=True)

# Menu Page
elif page == "Menu":
    st.markdown("<div class='title-text'>Our Menu 📜</div>", unsafe_allow_html=True)
    category = st.selectbox("Filter by category:", ["All"] + list(menu_df["category"].unique()))
    
    filtered_menu = menu_df if category == "All" else menu_df[menu_df["category"] == category]
    
    for index, row in filtered_menu.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row["image"], width=150, caption=row["name"], use_column_width=True)
            with col2:
                st.markdown(f"<div class='menu-item'><h3>{row['name']}</h3><p>Price: ${row['price']}</p></div>", unsafe_allow_html=True)
                if st.button(f"Order {row['name']}", key=index, help="Click to order this item"):
                    st.session_state["order"] = row["name"]
                    st.experimental_rerun()

# Blog Page
elif page == "Blog":
    st.markdown("<div class='title-text'>Devine Bites Blog 📝</div>", unsafe_allow_html=True)
    st.write("Stay updated with our latest news, dishes, and events.")
    st.write("(Blog posts will go here...)")

# Order Now Page
elif page == "Order Now":
    st.markdown("<div class='title-text'>Place Your Order 🛒</div>", unsafe_allow_html=True)
    if "order" in st.session_state:
        st.write(f"You selected: **{st.session_state['order']}**")
    name = st.text_input("Your Name")
    contact = st.text_input("Your contact to recieve delivery")
    address = st.text_area("Delivery Address")
    if st.button("Submit Order", help="Click to place your order"):
        st.success("Order placed successfully! We'll contact you soon.")
