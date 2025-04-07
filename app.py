import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

# Load dartboard image
img_path = "dartboard.png"
if not os.path.exists(img_path):
    st.error("Dartboard image not found. Please upload 'dartboard.png' to the same folder.")
else:
    st.image(img_path, caption="Click to mark TARGET and HIT")

    # Streamlit canvas
    click_data = st.data_editor(pd.DataFrame(columns=["Label", "X", "Y"]), num_rows="dynamic", key="click_log")

    st.markdown("👆 Add two rows: one for target, one for hit.")

    if len(click_data) == 2:
        # Extract points
        point1 = click_data.iloc[0]
        point2 = click_data.iloc[1]

        if point1["Label"].lower() == "target":
            target = (point1["X"], point1["Y"])
            hit = (point2["X"], point2["Y"])
        else:
            target = (point2["X"], point2["Y"])
            hit = (point1["X"], point1["Y"])

        # Calculate distance
        distance = np.sqrt((target[0] - hit[0])**2 + (target[1] - hit[1])**2)

        st.success(f"🎯 Miss Distance: **{distance:.2f} pixels**")

        # Store the throw
        if "throws" not in st.session_state:
            st.session_state.throws = []

        if st.button("Save Throw"):
            st.session_state.throws.append({
                "target_x": target[0],
                "target_y": target[1],
                "hit_x": hit[0],
                "hit_y": hit[1],
                "miss_distance_px": distance
            })

    # Show all throws
    if "throws" in st.session_state and len(st.session_state.throws) > 0:
        df = pd.DataFrame(st.session_state.throws)
        st.subheader("📊 Throw Log")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", csv, "dart_data.csv", "text/csv")
