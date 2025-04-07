import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import os

st.title("🎯 Dart Miss Distance Tracker")

# Load and display the dartboard image
img_path = "dartboard.png"
image = Image.open(img_path)
st.image(image, caption="Click twice: first for TARGET, then for HIT")

# Create canvas to click on the image
canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.3)",  # Red click dot
    stroke_width=5,
    background_image=image,
    update_streamlit=True,
    height=image.height,
    width=image.width,
    drawing_mode="point",
    key="canvas",
)

# Store and process points
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if len(objects) >= 2:
        # Get the last two points
        target_obj = objects[-2]
        hit_obj = objects[-1]

        target_x, target_y = target_obj["left"], target_obj["top"]
        hit_x, hit_y = hit_obj["left"], hit_obj["top"]

        # Calculate distance
        distance = np.sqrt((target_x - hit_x) ** 2 + (target_y - hit_y) ** 2)
        st.success(f"Miss distance: **{distance:.2f} pixels**")

        # Save throw
        if "throws" not in st.session_state:
            st.session_state["throws"] = []

        if st.button("✅ Save This Throw"):
            st.session_state["throws"].append({
                "target_x": target_x,
                "target_y": target_y,
                "hit_x": hit_x,
                "hit_y": hit_y,
                "miss_distance_px": distance
            })

# Show saved data
if "throws" in st.session_state and len(st.session_state["throws"]) > 0:
    df = pd.DataFrame(st.session_state["throws"])
    st.subheader("📋 Throw Log")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "dart_data.csv", "text/csv")
