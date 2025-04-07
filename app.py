import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import base64

st.set_page_config(page_title="Dart Distance Tracker", layout="centered")
st.title("🎯 Dart Miss Distance Tracker")
st.markdown("Click twice: first for **TARGET**, then for **HIT**")

# Load dartboard image and display it
img_path = "dartboard.png"
image = Image.open(img_path)
st.image(image, caption="Dartboard")

# Convert image to URL for Streamlit canvas
def get_image_url(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return f"data:image/png;base64,{encoded}"

image_url = get_image_url(img_path)

# Create drawing canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.4)",
    stroke_width=10,
    background_image=None,
    background_image_url=image_url,
    update_streamlit=True,
    height=image.height,
    width=image.width,
    drawing_mode="point",
    key="canvas",
)

# Process click data
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if len(objects) >= 2:
        # Get last two points: target and hit
        target = objects[-2]
        hit = objects[-1]

        target_x, target_y = target["left"], target["top"]
        hit_x, hit_y = hit["left"], hit["top"]

        # Calculate distance
        distance = np.sqrt((target_x - hit_x) ** 2 + (target_y - hit_y) ** 2)
        st.success(f"Miss Distance: **{distance:.2f} pixels**")

        # Save throw to session state
        if "throws" not in st.session_state:
            st.session_state.throws = []

        if st.button("✅ Save This Throw"):
            st.session_state.throws.append({
                "target_x": target_x,
                "target_y": target_y,
                "hit_x": hit_x,
                "hit_y": hit_y,
                "miss_distance_px": distance
            })

# Show saved throw data
if "throws" in st.session_state and len(st.session_state.throws) > 0:
    df = pd.DataFrame(st.session_state.throws)
    st.subheader("📋 Throw Log")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download as CSV", csv, "dart_data.csv", "text/csv")
