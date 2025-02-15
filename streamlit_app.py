import streamlit as st

# st.title("🎈 My new app")
# st.write(
#     "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
# )
import streamlit as st
import requests
import img2pdf
from io import BytesIO

def get_image_urls(copy_no):
    """Generate and return image URLs based on the copy number."""
    base_url = "https://bteexam.com/Upload_Copy/"
    prefix = copy_no[:4]
    if prefix[0] == '9':
        prefix = '4' + prefix[1:4] + "_B"
    url_path = f"{base_url}{prefix}/{copy_no}/{copy_no}"

    img_urls = []
    for i in range(1, 36):
        img_url = f"{url_path}{i:02d}.jpg"
        
        # Check if the image exists before adding to the list
        response = requests.head(img_url)
        if response.status_code == 200:
            img_urls.append(img_url)
        else:
            break  # Stop if an image is missing (copy number might be incorrect)
    
    return img_urls

def create_pdf_from_images(img_urls):
    """Download images and generate a PDF."""
    pdf_bytes = BytesIO()
    
    img_data_list = []
    for img_url in img_urls:
        response = requests.get(img_url)
        if response.status_code == 200:
            img_data_list.append(response.content)
    
    # Convert images to a PDF
    pdf_bytes.write(img2pdf.convert(img_data_list))
    pdf_bytes.seek(0)
    
    return pdf_bytes

# Streamlit UI
st.title("Exam Copy Viewer")

# User input for copy number
copy_no = st.text_input("Enter Copy Number")

if st.button("Click to View Copy"):
    if copy_no.strip().isdigit() and len(copy_no) >= 8:  # Validate copy number
        img_urls = get_image_urls(copy_no)

        if img_urls:
            st.subheader("Scanned Copy Images:")
            for img_url in img_urls:
                st.image(img_url, use_container_width=True)

            # Generate PDF and provide a download button
            pdf_file = create_pdf_from_images(img_urls)
            st.download_button(
                label="📄 Save as PDF",
                data=pdf_file,
                file_name=f"{copy_no}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No images found. The copy number might be incorrect.")
    else:
        st.warning("Invalid Copy Number. Please enter a valid 8-digit (or more) number.")
