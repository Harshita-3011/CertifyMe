import streamlit as st
import pymongo
#from pymongo import MongoClient
from gridfs import GridFS
import base64
import time
from PIL import Image as PILImage
st.set_page_config(
    page_title="CertifyMe",
    page_icon="📄" # Use the document emoji as an example
    
)
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["pyth"]  # database
def about():
    with st.sidebar:
        st.title("Dashboard")
        if st.button("Login"):
            st.session_state.page = "login"
            st.experimental_rerun()
        if st.button("About Us"):
            st.session_state.page = "about"
            st.experimental_rerun()
        if st.button("Contact Us"):
            st.session_state.page = "contact"
            st.experimental_rerun()
    st.title("ABOUT US")
    st.write("Welcome to centralized repository for storing and organizing certificates accessed by both teachers and students. Here individual can enhance the efficiency, accuracy, and convenience of managing student certificates in educational institutions.Hence one can eliminate paper-based or scattered storage systems")
def contact():
    with st.sidebar:
        st.title("Dashboard")
        if st.button("Login"):
            st.session_state.page = "login"
            st.experimental_rerun()
        if st.button("About Us"):
            st.session_state.page = "about"
            st.experimental_rerun()
        if st.button("Contact Us"):
            st.session_state.page = "contact"
            st.experimental_rerun()
    st.title("CONTACT US")
    st.write("#")
    st.write("If you have any questions or need assistance, please feel free to contact our team:")
    with st.container():

        left, mid, right = st.columns(3)

        profile = {
            "image": "profile.webp",
        }
        with left:
            st.image(profile["image"], caption='XXX', use_column_width=True)
            st.write("email: xxx@gmail.com")
            st.write("phone: +1 (123) 456-7890")
        with mid:
            st.image(profile["image"], caption='YYY', use_column_width=True)
            st.write("email: yyy@gmail.com")
            st.write("phone: +1 (123) 456-7890")
        with right:
            st.image(profile["image"], caption='ZZZ', use_column_width=True)
            st.write("email: zzz@gmail.com")
            st.write("phone: +1 (123) 456-7890")

def main_page():
    st.title("Welcome to the CertifyMe")
    with st.sidebar:
        st.title("Dashboard")
        if st.button("Login", key="login_button"):
            st.session_state.page = "login"
            st.experimental_rerun()
        if st.button("About Us", key="about_button"):
            st.session_state.page = "about"
            st.experimental_rerun()
        if st.button("Contact Us", key="contact_button"):
            st.session_state.page = "contact"
            st.experimental_rerun()
    images = [
        "1.jpeg",
        "2.jpeg",
        "3.jpeg",
    ]
    image_placeholder = st.empty()
    while(True):
        for i in range(len(images)):
            image_placeholder.image(images[i], use_column_width=True, caption=f"Image {i+1}")
            time.sleep(3)

def get_user_name(email):
    student = mydb["Student"].find_one({"email": email})
    teacher = mydb["Teacher"].find_one({"email": email})
    
    if student:
        return student["name"]
    elif teacher:
        return teacher["name"]
    else:
        return "User"
def logout():
    # Reset session state variables
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.session_state.user_type = ""
    st.session_state.page = "main"
def login():
    st.title("Login Page")
    name = st.text_input("Enter Username")
    email = st.text_input("Enter UserID")
    ipass = st.text_input("Enter password", type="password")
    submit = st.button("Login")

    if submit:
        row = mydb["Student"].find_one({"email": email})
        if not row:
            row1 = mydb["Teacher"].find_one({"email": email})
            if not row1:
                st.write("Wrong Credentials! Please try again!!")
                return
            else:
                pass2 = row1["password"]
                if str(pass2) == ipass:
                    st.write("TEACHER LOGIN SUCCESSFUL")
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_type = "teacher"
                    st.session_state.page = "teacher_dashboard"
                else:
                    st.write("Wrong Credentials! Please try again!!")
        else:
            pass1 = row["password"]
            if str(pass1) == ipass:
                st.write("STUDENT LOGIN SUCCESSFUL")
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_type = "student"
                st.session_state.page = "student_dashboard"
            else:
                st.write("Wrong Credentials! Please try again!!")

def teacher_dashboard():
    st.title("Teacher Dashboard")
    user_name=get_user_name(st.session_state.user_email)
    st.write(f"**Welcome, {user_name}!**")

    with st.sidebar:
        st.title("Dashboard")
        if st.button("View Files"):
            st.session_state.page = "teacher_view"
        if st.button("Create Collection"):
            st.session_state.page = "create_collection"
        if st.button("Upload"):
            st.session_state.page = "t_upload"
        if st.button("View Student's Files"):
            st.session_state.page = "stud_view"
        if st.button("View Folder"):
            st.session_state.page = "stu_view"
        if st.button("Logout"):  # Add a logout button
            logout()

def student_dashboard():
    st.title("Student Dashboard")
    user_name=get_user_name(st.session_state.user_email)
    st.write(f"**Welcome, {user_name}!**")

    with st.sidebar:
        st.title("Dashboard")
        if st.button("Upload"):
            st.session_state.page = "s_upload"
        if st.button("View Files"):
            st.session_state.page = "view"
        if st.button("Logout"):  # Add a logout button
            logout()
        
def view(email):
    fs = GridFS(mydb, collection=email)
    st.title("Files List")

    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']  # List of valid extensions

    # Fetch all files' metadata from .files collection
    files_metadata = fs.find({}, limit=0)  # Pass the limit parameter directly

    for file_meta in files_metadata:
        metadata = file_meta.metadata
        file_name = file_meta.name
        
        # Check if the file extension is valid
        if any(file_name.lower().endswith(ext) for ext in valid_extensions):
            st.write("File Name:", file_name)
           
            # Display options for both opening and downloading the file
            file_content = fs.get(file_meta._id).read()
            b64_file = base64.b64encode(file_content).decode('utf-8')

            if file_name.lower().endswith('.pdf'):
                st.markdown(
                    f'<a href="data:application/pdf;base64,{b64_file}" target="_blank">Open PDF</a>',
                    unsafe_allow_html=True
                )
            elif any(file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                file_extension = file_name.split('.')[-1].lower()
                st.markdown(
                    f'<a href="data:image/{file_extension};base64,{b64_file}" target="_blank">Open {file_extension.upper()}</a>',
                    unsafe_allow_html=True
                )
            
            # Add a download link
            st.markdown(
                f'<a href="data:application/octet-stream;base64,{b64_file}" download="{file_name}">Download {file_name}</a>',
                unsafe_allow_html=True
            )
            
            st.write("---")

def s_upload(email):
    collect = mydb["dropdown"]
    documents = collect.find()

    contents_list = ["Select"]

    for document in documents:
        name = document.get("name")  # Get the value of the "name" field
        contents_list.append(name)

    print(contents_list)
    fs = GridFS(mydb, collection=email)
    st.title("File Upload")

    # Input fields
    cont = st.selectbox("Select", contents_list, index=0)
    title = st.text_input("Enter title of the file")
    description = st.text_area("Enter description of the file")
    uploaded_file = st.file_uploader("Upload a File", type=["pdf","jpeg","jpg","png"])
    fs1 = GridFS(mydb, collection=cont)
    if uploaded_file and title and description:
        # Save the file to GridFS with title and description
        file_id = fs.put(uploaded_file, filename=uploaded_file.name)
        file_id1 = fs1.put(uploaded_file, filename=uploaded_file.name)
        user_collection = mydb[email]
        user_collect=mydb[cont]
        user_collection.insert_one({
            "_id": file_id,
            "title": title,
            "description": description
        })
        user_collect.insert_one({
            "_id": file_id1,
            "title": title,
            "description": description
        })
        st.write(f"File '{uploaded_file.name}' uploaded successfully!")
        #st.write(f"File ID in GridFS: {file_id}")
        st.write(f"Title: {title}")
        st.write(f"Description: {description}")

def t_upload(email):
    f = GridFS(mydb, collection=email)
    st.title("File Upload")

    # Input fields
    title = st.text_input("Enter title of the file")
    description = st.text_area("Enter description of the file")

    # File uploader
    uploaded_file = st.file_uploader("Upload a File", type=["pdf","jpeg","jpg","png"])

    if uploaded_file and title and description:
        # Save the file to GridFS with title and description
        file_id = f.put(uploaded_file, filename=uploaded_file.name)
        user_collection = mydb[email]
        user_collection.insert_one({
            "_id": file_id,
            "title": title,
            "description": description
        })

        st.write(f"File '{uploaded_file.name}' uploaded successfully!")
        #st.write(f"File ID in GridFS: {file_id}")
        st.write(f"Title: {title}")
        st.write(f"Description: {description}")

def create():
    st.title("Create Folder")
    c_name=st.text_input("Enter Folder Name",key="collection_name_input")
    create_button=st.button("Create")
    if create_button and c_name:
        c=mydb["dropdown"]
        c.insert_one({
            "name": c_name
            })
        st.write("Folder Created Successfully!!")

def stu_view():
    st.title("Open Folder")
    collect = mydb["dropdown"]
    documents = collect.find()

    contents_list = ["Select"]

    for document in documents:
        name = document.get("name")  # Get the value of the "name" field
        contents_list.append(name)
    cont = st.selectbox("Select", contents_list, index=0)
    fs3 = GridFS(mydb, collection=cont)
    st.title("Files List")
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']  # List of valid extensions

    # Fetch all files' metadata from .files collection
    files_metadata = fs3.find({}, limit=0)  # Pass the limit parameter directly

    for file_meta in files_metadata:
        metadata = file_meta.metadata
        file_name = file_meta.name

        # Check if the file extension is valid
        if any(file_name.lower().endswith(ext) for ext in valid_extensions):
            st.write("File Name:", file_name)

            # Display options for both opening and downloading the file
            file_content = fs3.get(file_meta._id).read()
            b64_file = base64.b64encode(file_content).decode('utf-8')

            if file_name.lower().endswith('.pdf'):
                st.markdown(
                    f'<a href="data:application/pdf;base64,{b64_file}" target="_blank">Open PDF</a>',
                    unsafe_allow_html=True
                )
            elif any(file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                file_extension = file_name.split('.')[-1].lower()
                st.markdown(
                    f'<a href="data:image/{file_extension};base64,{b64_file}" target="_blank">Open {file_extension.upper()}</a>',
                    unsafe_allow_html=True
                )

            # Add a download link
            st.markdown(
                f'<a href="data:application/octet-stream;base64,{b64_file}" download="{file_name}">Download {file_name}</a>',
                unsafe_allow_html=True
            )

            st.write("---")

def stud_view():
    usn = st.text_input("Enter The USN")
    cb = st.button("Find")

    if cb and usn:
        fs4 = GridFS(mydb, collection=usn)
        st.title("Files List")

        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']  # List of valid extensions

        # Fetch all files' metadata from .files collection
        files_metadata = fs4.find({}, limit=0)  # Pass the limit parameter directly

        for file_meta in files_metadata:
            metadata = file_meta.metadata
            file_name = file_meta.name

            # Check if the file extension is valid
            if any(file_name.lower().endswith(ext) for ext in valid_extensions):
                st.write("File Name:", file_name)

                # Display options for both opening and downloading the file
                file_content = fs4.get(file_meta._id).read()
                b64_file = base64.b64encode(file_content).decode('utf-8')

                if file_name.lower().endswith('.pdf'):
                    st.markdown(
                        f'<a href="data:application/pdf;base64,{b64_file}" target="_blank">Open PDF</a>',
                        unsafe_allow_html=True
                    )
                elif any(file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                    file_extension = file_name.split('.')[-1].lower()
                    st.markdown(
                        f'<a href="data:image/{file_extension};base64,{b64_file}" target="_blank">Open {file_extension.upper()}</a>',
                        unsafe_allow_html=True
                    )

                # Add a download link
                st.markdown(
                    f'<a href="data:application/octet-stream;base64,{b64_file}" download="{file_name}">Download {file_name}</a>',
                    unsafe_allow_html=True
                )

                st.write("---")

def main():
    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        if st.session_state.user_type == "teacher":
            teacher_dashboard()
            if st.session_state.page == "teacher_view":
                view(st.session_state.user_email)
            elif st.session_state.page == "create_collection":
                create()
            elif st.session_state.page == "t_upload":
                t_upload(st.session_state.user_email)
            elif st.session_state.page == "stud_view":
                stud_view()
            elif st.session_state.page == "stu_view":
                stu_view()

        elif st.session_state.user_type == "student":
            student_dashboard()
            if st.session_state.page == "s_upload":
                s_upload(st.session_state.user_email)
            elif st.session_state.page == "view":
                view(st.session_state.user_email)
            
            
    else:
        if "page" not in st.session_state:
            st.session_state.page = "main"

        if st.session_state.page == "main":
            main_page()
        elif st.session_state.page == "login":
            login()
        elif st.session_state.page == "about":
            about()
        elif st.session_state.page == "contact":
            contact()
if __name__ == "__main__":
    main()
