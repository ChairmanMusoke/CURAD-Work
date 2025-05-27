import streamlit as st
import pandas as pd
import time
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
    {"name": "Meat Katogo", "price": 5000, "image": "Katogo meat.jpg", "category": "Main Course"},
    {"name": "Katogo Beans", "price": 4000, "image": "Katogobeans.jpg", "category": "Main Course"},
    {"name": "Katogo Gnuts", "price": 4000, "image": "katogognutss.jpeg", "category": "Main Course"},
    {"name": "Katogo Liver", "price": 5000, "image": "katogoliv.jpg", "category": "Main Course"},
    {"name": "Katogo Offals", "price": 5000, "image": "katogooffals.jpeg", "category": "Main Course"}
]
menu_df = pd.DataFrame(menu_data)

# Store Orders
if "orders" not in st.session_state:
    st.session_state["orders"] = []

if "submitted_orders" not in st.session_state:
    st.session_state["submitted_orders"] = []

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Menu", "Order Now", "Admin Panel"])


# Home Page with Automatic Slideshow
if page == "Home":
    st.markdown("<div class='title-text'>Welcome to Devine Bites! 🍽️</div>", unsafe_allow_html=True)

    images = ["Cover.jpg", "Katogo meat.jpg", "Katogobeans.jpg", "katogoliv.jpg"]
    img_container = st.empty()  # Placeholder for images

    if "image_index" not in st.session_state:
        st.session_state.image_index = 0  # Initialize index

    # Auto-slideshow by updating the session state
    st.session_state.image_index = (st.session_state.image_index + 1) % len(images)
    img_container.image(images[st.session_state.image_index], use_container_width=True)

    # Refresh every 3 seconds
    time.sleep(3)
    st.rerun()  


# Menu Page
elif page == "Menu":
    st.markdown("<div class='title-text'>Our Menu 📜</div>", unsafe_allow_html=True)
    category = st.selectbox("Filter by category:", ["All"] + list(menu_df["category"].unique()))
    
    filtered_menu = menu_df if category == "All" else menu_df[menu_df["category"] == category]
    
    for index, row in filtered_menu.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row["image"], width=150, caption=row["name"], use_container_width=True)
            with col2:
                st.markdown(f"<div class='menu-item'><h3>{row['name']}</h3><p>Price: UGX{row['price']}</p></div>", unsafe_allow_html=True)
                if st.button(f"Order {row['name']}", key=index):
                    st.session_state["orders"].append(row["name"])
                    st.success(f"{row['name']} added to cart!")

# Order Now Page with Order Summary
elif page == "Order Now":
    st.markdown("<div class='title-text'>Place Your Order 🛒</div>", unsafe_allow_html=True)
    
    if not st.session_state["orders"]:
        st.warning("No items in cart. Please add items from the menu.")
    else:
        st.write("### Your Order:")
        for order in st.session_state["orders"]:
            st.write(f"- {order}")
    
    name = st.text_input("Your Name")
    contact = st.text_input("Your contact for delivery")
    address = st.text_area("Delivery Address")
    
    if st.button("Submit Order"):
        if name and contact and address and st.session_state["orders"]:
            order_details = {
                "name": name,
                "contact": contact,
                "address": address,
                "items": st.session_state["orders"]
            }
            st.session_state["submitted_orders"].append(order_details)  # Store order permanently
            st.session_state["orders"] = []  # Clear the cart
            st.success("Order placed successfully! We'll contact you soon.")
        else:
            st.error("Please fill in all details before submitting.")


# Admin Panel
elif page == "Admin Panel":
    st.markdown("<div class='title-text'>Admin Panel 🛒</div>", unsafe_allow_html=True)
    
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "admin123":
        st.success("Access Granted")
        st.write("### Orders Received")

        # Ensure submitted orders are stored
        if "submitted_orders" not in st.session_state:
            st.session_state["submitted_orders"] = []

        if st.session_state["submitted_orders"]:
            for idx, order in enumerate(st.session_state["submitted_orders"]):
                with st.container():
                    st.write(f"### Order {idx+1}")
                    st.write(f"👤 **Name:** {order['name']}")
                    st.write(f"📞 **Contact:** {order['contact']}")
                    st.write(f"📍 **Address:** {order['address']}")
                    st.write("🛒 **Items Ordered:**")
                    for item in order["items"]:
                        st.write(f"- {item}")
                    st.write("---")  # Separator
        else:
            st.write("No orders yet.")
    else:
        st.error("Incorrect Password")

