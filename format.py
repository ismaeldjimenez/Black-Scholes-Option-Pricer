# import streamlit as st

# def format():
#   # Custom CSS to inject into Streamlit
#   st.markdown("""
#   <style>
#   /* Adjust the size and alignment of the CALL and PUT value containers */
#   .metric-container {
#       display: flex;
#       justify-content: center;
#       align-items: center;
#       padding: 8px; /* Adjust the padding to control height */
#       width: auto; /* Auto width for responsiveness, or set a fixed width if necessary */
#       margin: 0 auto; /* Center the container */
#   }

#   /* Custom classes for CALL and PUT values */
#   .metric-call {
#       background-color: #90ee90; /* Light green background */
#       color: black; /* Black font color */
#       margin-right: 10px; /* Spacing between CALL and PUT */
#       border-radius: 10px; /* Rounded corners */
#   }

#   .metric-put {
#       background-color: #ff817f; /* Light red background */
#       color: black; /* Black font color */
#       border-radius: 10px; /* Rounded corners */
#   }

#   /* Style for the value text */
#   .metric-value {
#       font-size: 1.5rem; /* Adjust font size */
#       font-weight: bold;
#       margin: 0; /* Remove default margins */
#   }

#   /* Style for the label text */
#   .metric-label {
#       font-size: 1.0rem; /* Adjust font size */
#       margin-bottom: 4px; /* Spacing between label and value */
#   }

#   </style>
#   """, unsafe_allow_html=True)