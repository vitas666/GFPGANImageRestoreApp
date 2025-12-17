import streamlit as st
from PIL import Image
import io
import os
from fixer import ImageRestorer

# We use st.cache_resource so we don't reload the heavy AI model 
@st.cache_resource
def load_ai_model():
    return ImageRestorer()

def main():
    # --- UI Config ---
    print('starting point1')
    st.set_page_config(page_title="AI Image Fixer", layout="centered")

    st.title("AI Image Restoration App")
    st.write("Upload an photo to restore face details.")
    st.markdown("""
    Upload your old or blurry photo below. 
    Supported formats: **JPEG, PNG, TIFF, WEBP**
    """)

    st.divider()
    st.subheader("1. Input Image Preview")
    # 1. File Uploader
    uploaded_file = st.file_uploader(
        "Drag and drop your image here", 
        type=["jpg", "jpeg", "png", "tiff", "tif", "webp"],
        accept_multiple_files=False
    )

    # CRITICAL FIX: Only try to open the image IF a file was actually uploaded
    if uploaded_file is not None:
        try:
            # 2. Load the image
            original_image = Image.open(uploaded_file)
            
            # Show file info
            st.subheader("1. Input Image Preview")
            # Note: uploaded_file.name works better than image.filename for stream uploads
            st.caption(f"Filename: `{uploaded_file.name}` | Size: `{original_image.size}`")
            
            # Show Original Image
            st.image(original_image, caption="Original Image", use_container_width=True)
            st.info("Image loaded successfully. Ready for AI processing.")

            # 3. Load AI Model (Lazy loading)
            with st.spinner("Starting AI Engine..."):
                fixer = load_ai_model()

            # 4. Restore Button
            if st.button("✨ Restore Image"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("### Original")
                    st.image(original_image, use_container_width=True)

                with st.spinner("Processing... (This uses your Mac's Neural Engine)"):
                    # Run the restoration
                    fix_image = fixer.restore(original_image)
                
                with col2:
                    st.write("### Restored Result")
                    st.image(fix_image, use_container_width=True)
                    
                    # Prepare Download
                    from io import BytesIO
                    buf = BytesIO()
                    fix_image.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    
                    st.download_button(
                        label="📥 Download Result",
                        data=byte_im,
                        file_name="restored_image.png",
                        mime="image/png"
                    )
                        
                st.success("Restoration Complete!")

        except Exception as e:
            st.error(f"Error processing image: {e}")

if __name__ == "__main__":
    main()