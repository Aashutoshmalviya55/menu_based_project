import streamlit as st
st.set_page_config(page_title="Python Automation Toolkit", layout="wide")
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        color: #00cc66;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .sub-title {
        text-align: center;
        font-size: 24px;
        color: #00cc66;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Linux World Menu Based Project</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">👨‍💻 Name: <strong>Aashutosh Malviya</strong> | Team No. :- <strong>26</strong></div>', unsafe_allow_html=True)

st.markdown("---")

import datetime
import requests
import smtplib
import pywhatkit
from instagrapi import Client as InstaClient
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import tweepy
import os

twilio_client = TwilioClient("")
twilio_phone_number = ""
telegram_token = ""                 #paste credentials 
telegram_chat_id = ""
email_password = ""

with st.sidebar.expander(" Python Automation Tasks", expanded=True):
    sms_checked = st.checkbox(" Send SMS via Twilio")
    whatsapp_checked = st.checkbox(" Send WhatsApp Message")
    email_checked = st.checkbox(" Send Email")
    telegram_checked = st.checkbox(" Send Telegram Message")
    call_checked = st.checkbox(" Twilio Call")
    insta_checked = st.checkbox(" Instagram Auto Post")
    twitter_checked = st.checkbox(" Post on Twitter")

# python task 
if sms_checked:
    st.subheader(" Send SMS via Twilio")
    phone = st.text_input("Recipient Phone Number (e.g. +91...)")
    message = st.text_area("SMS Message")
    if st.button("Send SMS"):
        try:
            msg = twilio_client.messages.create(body=message, from_=twilio_phone_number, to=phone)
            st.success(f" SMS sent! SID: {msg.sid}")
        except Exception as e:
            st.error(f"Error: {e}")

if whatsapp_checked:
    st.subheader(" Send WhatsApp Message")
    phone = st.text_input("WhatsApp Number (+countrycode)")
    message = st.text_area("WhatsApp Message")
    image = st.file_uploader("Upload Image (Optional)", type=["jpg", "png"])
    now = datetime.datetime.now()

    if st.button("Send Text Message"):
        try:
            pywhatkit.sendwhatmsg(phone, message, now.hour, now.minute + 1)
            st.success(" Text message scheduled! Leave browser open.")
        except Exception as e:
            st.error(f" Error: {e}")

    if st.button("Send Image"):
        if image:
            with open("temp_img.jpg", "wb") as f:
                f.write(image.getbuffer())
            try:
                pywhatkit.sendwhats_image(phone, "temp_img.jpg", caption=message)
                st.success(" Image sent!")
            except Exception as e:
                st.error(f" Error: {e}")
        else:
            st.warning(" Please upload an image.")

if email_checked:
    st.subheader("📧 Send Email")
    sender = st.text_input("Sender Gmail")
    recipient = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    msg_body = st.text_area("Email Body")
    if st.button("Send Email"):
        try:
            content = f"Subject: {subject}\n\n{msg_body}"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, email_password)
            server.sendmail(sender, recipient, content)
            server.quit()
            st.success(" Email sent successfully!")
        except Exception as e:
            st.error(f" Error: {e}")

if telegram_checked:
    st.subheader("📩 Send Telegram Message")
    telegram_message = st.text_input("Enter your message")
    if st.button("Send to Telegram"):
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={telegram_message}"
            res = requests.get(url)
            if res.status_code == 200:
                st.success(" Message sent!")
            else:
                st.error(" Failed. Check token/chat ID.")
        except Exception as e:
            st.error(f" Error: {e}")

if call_checked:
    st.subheader(" Twilio Call")
    call_number = st.text_input("Phone Number to Call (e.g. +91...)")
    call_message = st.text_area("Message to Speak", "Hello! This is a Python-powered call.")
    if st.button("Make Call"):
        try:
            call = twilio_client.calls.create(
                to=call_number,
                from_=twilio_phone_number,
                twiml=f"<Response><Say>{call_message}</Say></Response>"
            )
            st.success(" Call started!")
            st.info(f"Call SID: {call.sid}")
        except Exception as e:
            st.error(f" Error: {e}")

if insta_checked:
    st.subheader("📸 Instagram Auto Post")
    username = st.text_input("Instagram Username")
    password = st.text_input("Instagram Password", type="password")
    caption = st.text_area("Post Caption", "Automated post from Python!")
    photo_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if st.button("Post to Instagram"):
        if username and password and photo_file:
            with open("uploaded_image.jpg", "wb") as f:
                f.write(photo_file.read())
            try:
                cl = InstaClient()
                cl.login(username, password)
                cl.photo_upload("uploaded_image.jpg", caption)
                st.success(" Photo posted successfully!")
            except Exception as e:
                st.error(f" Error: {e}")
        else:
            st.warning(" Please fill all fields and upload an image.")

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)
if twitter_checked:
    st.subheader("Post to Twitter")
    tweet_text = st.text_area(" Enter Tweet (Max 280 characters)", max_chars=280)
    image = st.file_uploader(" Upload Image (Optional)", type=["jpg", "jpeg", "png"])

    if st.button("Post Tweet"):
        if not tweet_text.strip():
            st.warning(" Please enter some text for your tweet.")
        else:
            try:
                media_id = None
                if image:
                    with open("temp_image.jpg", "wb") as f:
                        f.write(image.getbuffer())
                    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
                    api = tweepy.API(auth)
                    media = api.media_upload("temp_image.jpg")
                    media_id = media.media_id
                if media_id:
                    response = client.create_tweet(text=tweet_text, media_ids=[media_id])
                else:
                    response = client.create_tweet(text=tweet_text)

                tweet_id = response.data["id"]
                tweet_url = f"https://twitter.com/user/status/{tweet_id}"
                st.success(" Tweet posted successfully!")
                st.markdown(f"[ View Tweet]({tweet_url})")

                # Optional: delete the temporary image file
                if os.path.exists("temp_image.jpg"):
                    os.remove("temp_image.jpg")

            except Exception as e:
                st.error(f" Error posting tweet: {e}")


#linux Taks

import paramiko
with st.sidebar.expander(" Linux Automation Task", expanded=False):
    run_linux = st.checkbox("Enable Linux SSH Task Panel")

if run_linux:
    st.subheader(" Connect to Linux via SSH")

    ssh_user = st.text_input("Enter Linux Username")
    ssh_ip = st.text_input("Enter Linux IP Address")
    ssh_password = st.text_input("Enter Password", type="password")

    options = [
        "Run `date`",
        "Run `cal`",
        "Run `ls`",
        "Run `ifconfig`",
        "Create Folder",
        "Create File",
        "Navigate into Folder",
        "Go to Home Directory",
        "Run `whoami`",
        "cat"
    ]
    selected_cmd = st.selectbox("Choose a command to run", options)

    if st.button("Execute"):
        if ssh_user and ssh_ip and ssh_password:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=ssh_ip, username=ssh_user, password=ssh_password)

                # Determine command
                if selected_cmd == "Run `date`":
                    command = "date"
                elif selected_cmd == "Run `cal`":
                    command = "cal"
                elif selected_cmd == "Run `ls`":
                    command = "ls"
                elif selected_cmd == "Run `ifconfig`":
                    command = "ifconfig"
                elif selected_cmd == "Create Folder":
                    folder = st.text_input("Enter folder name", key="folder")
                    if folder:
                        command = f"mkdir {folder}"
                    else:
                        st.warning("Enter a folder name.")
                        client.close()
                        st.stop()
                elif selected_cmd == "Create File":
                    filename = st.text_input("Enter file name", key="file")
                    if filename:
                        command = f"touch {filename}"
                    else:
                        st.warning("Enter a file name.")
                        client.close()
                        st.stop()
                elif selected_cmd == "Navigate into Folder":
                    folder = st.text_input("Enter folder name to navigate", key="nav")
                    if folder:
                        command = f"cd {folder} && ls"
                    else:
                        st.warning("Enter a folder name.")
                        client.close()
                        st.stop()
                elif selected_cmd == "Go to Home Directory":
                    command = "cd ~ && ls"
                elif selected_cmd == "Run `whoami`":
                    command = "whoami"

                elif selected_cmd == "cat":
                    command = "cat"
                    filename = st.text_input("Enter file name", key="cat")
                    if filename:
                        command = f"cat {filename}"
                    else:
                        st.warning("Enter a file name.")
                        client.close()
                        st.stop()


                else:
                    command = "echo Invalid"

                # Execute command
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()

                if output:
                    st.code(output)
                if error:
                    st.error(error)

                client.close()

            except Exception as e:
                st.error(f" SSH Error: {e}")
        else:
            st.warning("Please fill all SSH credentials.")

#Docker task
import paramiko

with st.sidebar.expander(" Docker Automation Task", expanded=False):
    enable_docker = st.checkbox("Enable Docker Control Panel")

if enable_docker:
    st.header(" Remote Docker Control via SSH")

    #SSH Inputs
    docker_host = st.text_input(" Host (IP Address)", "")
    docker_user = st.text_input(" SSH Username", "root")
    docker_pass = st.text_input(" SSH Password", type="password")

    #Docker Command Options
    docker_command = st.selectbox("🛠️ Choose Docker Operation", [
        "Show Running Containers (docker ps)",
        "Show All Images (docker images)",
        "Pull Docker Image",
        "Run Container",
        "Stop Container",
        "Remove Container",
        "Remove Image",
        "Build Image from Dockerfile",
        "Create Volume",
        "Show Volumes",
        "Run Custom Command",
        "show container IP"
    ])


    def ssh_execute_docker(command):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=docker_host, username=docker_user, password=docker_pass)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            ssh.close()
            return output, error
        except Exception as e:
            return "", f"SSH Error: {e}"

    if docker_command == "Pull Docker Image":
        image = st.text_input("Enter image name (e.g. ubuntu:latest)")
        if st.button("Pull Image"):
            out, err = ssh_execute_docker(f"docker pull {image}")
            st.code(out or err)

    elif docker_command == "Run Container":
        image = st.text_input("Image Name", "ubuntu")
        cname = st.text_input("Container Name", "mycontainer")
        if st.button("Run Container"):
            out, err = ssh_execute_docker(f"docker run -dit --name {cname} {image}")
            st.code(out or err)

    elif docker_command == "Stop Container":
        cid = st.text_input("Container ID/")
        if st.button("Stop"):
            out, err = ssh_execute_docker(f"docker stop {cid}")
            st.code(out or err)

    elif docker_command == "Remove Container":
        cid = st.text_input(" Container ID/Name")
        if st.button("Remove Container"):
            out, err = ssh_execute_docker(f"docker rm {cid}")
            st.code(out or err)

    elif docker_command == "Remove Image":
        img = st.text_input("Enter Image ID/Name")
        if st.button("Remove Image"):
            out, err = ssh_execute_docker(f"docker rmi {img}")
            st.code(out or err)

    elif docker_command == "Build Image from Dockerfile":
        path = st.text_input("Path to Dockerfile directory", "/root/project/")
        tag = st.text_input("Tag Name (e.g. myimage:1.0)", "myimage:latest")
        if st.button("Build"):
            out, err = ssh_execute_docker(f"docker build -t {tag} {path}")
            st.code(out or err)

    elif docker_command == "Create Volume":
        vol = st.text_input("Enter Volume Name", "myvolume")
        if st.button("Create Volume"):
            out, err = ssh_execute_docker(f"docker volume create {vol}")
            st.code(out or err)

    elif docker_command == "Show Running Containers (docker ps)":
        if st.button("Show Running Containers"):
            out, err = ssh_execute_docker("docker ps")
            st.code(out or err)

    elif docker_command == "Show All Images (docker images)":
        if st.button("Show Images"):
            out, err = ssh_execute_docker("docker images")
            st.code(out or err)

    elif docker_command == "Show Volumes":
        if st.button("List Volumes"):
            out, err = ssh_execute_docker("docker volume ls")
            st.code(out or err)


    elif docker_command == "Run Custom Command":
        custom_cmd = st.text_input("Enter Docker command", "docker stats")
        if st.button("Run Command"):
            out, err = ssh_execute_docker(custom_cmd)
            st.code(out or err)

            
    elif docker_command == "show container IP":
     cname = st.text_input("Enter Container Name", "mycontainer")
     if st.button("Show IP"):
       
        cmd = f"docker inspect --format='{{{{.NetworkSettings.IPAddress}}}}' {cname}"
        out, err = ssh_execute_docker(cmd)

        ip = out.strip() if out else None

        if ip:
            st.success(f"📡 Container IP Address: {ip}")
        else:
            st.error(err or "Could not retrieve IP address.")

# launch ec2 based on finger count
import cv2
import mediapipe as mp
import boto3
import numpy as np

with st.sidebar.expander(" launch ec2 based on finger count", expanded=False):
    run_ec2 = st.checkbox("Enable EC2 Finger Launcher")

if run_ec2:
    st.header(" EC2 Launcher Based on Finger Count")
    st.markdown("**Show your fingers to the webcam to launch that many EC2 instances.**")

    mp_hands = mp.solutions.hands
    FINGER_TIPS = [4, 8, 12, 16, 20]

    if st.button(" Capture from Webcam and Launch EC2"):
        cap = cv2.VideoCapture(0)
        ret, photo = cap.read()
        cap.release()

        if not ret:
            st.error(" Failed to access webcam.")
        else:
            _, buffer = cv2.imencode('.jpg', photo)
            st.image(buffer.tobytes(), channels="BGR", caption="Captured Image")
            with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7) as hands:
                image_rgb = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    landmarks = hand_landmarks.landmark

                    fingers = []
                
                    if landmarks[FINGER_TIPS[0]].x < landmarks[FINGER_TIPS[0] - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                   
                    for tip in FINGER_TIPS[1:]:
                        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

                    finger_count = sum(fingers)
                    st.success(f" Fingers Detected: {finger_count}")

                    if finger_count > 0:
                        try:
                            ec2 = boto3.resource("ec2", region_name="ap-south-1")
                            instances = ec2.create_instances(
                                ImageId="",   #ami id
                                InstanceType="t2.micro",
                                MinCount=1,
                                MaxCount=finger_count
                            )
                            for i, instance in enumerate(instances, 1):
                                st.info(f" Instance {i} launched with ID: {instance.id}")
                        except Exception as e:
                            st.error(f" Error launching EC2: {e}")
                    else:
                        st.warning("No fingers detected. No instance launched.")
                else:
                    st.error(" No hand detected.")

# launch ec2
import boto3
ec2_launch = boto3.resource("ec2")
with st.sidebar.expander(" EC2 Automation Task", expanded=False):
    st.subheader(" Launch EC2 Instance")
    st.markdown("Click the button below to launch a **t2.micro** EC2 instance on AWS.")

    if st.button("Launch EC2 Instance"):
        try:
            response = ec2_launch.create_instances(
                InstanceType="t2.micro",
                ImageId="22", #ami id AWS
                MinCount=1,
                MaxCount=1
            )
            instance_id = response[0].id
            st.success(f" EC2 Instance Launched! ID: `{instance_id}`")
        except Exception as e:
            st.error(f" Failed to launch EC2 instance: {e}")

# launch ec2 wiht API gateway
with st.sidebar.expander("Launch EC2 thorough API Gateway", expanded=True):
    st.markdown("Click below to launch an EC2 instance.")

    if st.button(" Click to Launch EC2 Instance"):
        js = f"22"        #paste API gateway link 
        st.markdown(f"<script>{js}</script>", unsafe_allow_html=True)

# S3 Bucket Notification
from botocore.exceptions import NoCredentialsError

with st.sidebar.expander(" S3 Bucket Notification", expanded=False):
    show_s3_upload = st.checkbox(" Show S3 Upload UI")


if show_s3_upload:
    st.subheader(" Upload File to S3 Bucket")
    st.markdown("Select a file and upload it directly to your AWS S3 bucket.")

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "jpg", "png", "pdf", "zip", "jpeg"])

    if uploaded_file:
        try:
            s3 = boto3.client("s3")
            bucket_name = "22"  #paste s3 bucket name
            s3.upload_fileobj(uploaded_file, bucket_name, uploaded_file.name)
            st.success(f" `{uploaded_file.name}` uploaded successfully to `{bucket_name}`.")
        except NoCredentialsError:
            st.error(" AWS credentials not found.")
        except Exception as e:
            st.error(f" Upload failed: {e}")


#jenkins ci/cd project
with st.sidebar.expander("Jenkins CI/CD Project", expanded=False):
    show_project = st.checkbox("Click to see full project")
if show_project:
    st.link_button(
        "Open Jenkins CI/CD Project",
        "22"  #your github url 
 
    )

#kubernetes project live website
with st.sidebar.expander("Kubernetes Project ", expanded=False):
    show_project = st.checkbox(" Click to see full project")
if show_project:
    st.link_button(
        "Open Kubernetes Project",
        "22" #your github url
    )


# portfolio section
with st.sidebar.expander("porfolio section", expanded=False):
    run_portfolio = st.checkbox("lauch protfoliio ")

if run_portfolio:

        st.markdown("<h1 style='text-align: center;'> Launch My Portfolio</h1>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align: center;">
                <a href="22" target="_blank">  # your portfolio link 
                    <button style="background-color:#8b0000; color:white; padding:10px 20px; font-size:16px; border-radius:8px; border:2px solid #ff4b4b; cursor:pointer;">
                         Open Portfolio
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
  
#javascript automation task
from streamlit.components.v1 import html

with st.sidebar.expander(" Show Javascript Subtasks"):
    send_email = st.checkbox("📧 Send Email")
    take_photo = st.checkbox("📸 Take Photo")
    get_location = st.checkbox("📍 Get Geolocation")
    send_video = st.checkbox("🎥 Send Video via Gmail")
    send_whatsapp = st.checkbox("💬 Send WhatsApp Message")
    send_photo_on_gmail = st.checkbox("📸 Send Photo on Gmail")

if send_email:
    st.subheader("📧Send Email")
    html('''
        <a href="http://127.0.0.1:5500/javascript/anyone_send.html" target="_blank">
            <button style="
                background-color: #8A2BE2;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;">
                Send Email
            </button>
        </a>
    ''', height=100)

if take_photo:
    st.subheader("📸Take Photo")
    html('''
        <a href="22" target="_blank">  #your js link url 
            <button style="
                background-color: #1E90FF;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;">
                Take Photo
            </button>
        </a>
    ''', height=100)

if get_location:
    st.subheader("📍 Get Location")
    html('''
        <a href="http://127.0.0.1:5500/javascript/current_location.html" target="_blank">
            <button style="
                background-color: #4CAF50;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;">
                GetGeolocation
            </button>
        </a>
    ''', height=100)

if send_video:
    st.subheader("🎥 Send Video via Gmail")
    html('''
        <a href="http://127.0.0.1:5500/javascript/vedio_gmail.html" target="_blank">
            <button style="
                background-color: #FF4500;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;">
                Send Video
            </button>
        </a>
    ''', height=100)

if send_whatsapp:
    st.subheader("💬 Send WhatsApp Message")
    html('''
        <a href="http://127.0.0.1:5500/javascript/whatsapp_msg.html" target="_blank"> //paste here the link
            <button style="
                background-color: #25D366;
                color: white;
                padding: 10px 24px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                cursor: pointer;">
                Send WhatsApp Message
            </button>
        </a>
    ''', height=100)
\

# prompt enggineering first project 
from openai import OpenAI

key = "22"         # your api key
gemini_model = OpenAI(
    api_key=key,
    base_url="22"  # your base url
)
def predict(share_bazar_query):
    mymsg = [
        {
            "role": "system",
            "content": (
                "You are a financial expert specialized in the stock market. "
                "You provide clear, concise, and accurate information about stock trends, technical analysis, fundamental analysis, "
                "investment strategies, risk management, and real-time stock movements. Tailor your response based on the user's prompt, "
                "and include examples or market data when needed."
            )
        },
        {"role": "user", "content": share_bazar_query}
    ]
    response = gemini_model.chat.completions.create(
        model="gemini-2.5-flash",
        messages=mymsg
    )
    return response.choices[0].message.content

with st.sidebar.expander("AI Prompt First project", expanded=True):
    run_portfolio = st.checkbox("Launch AI Stock Advisors")

if run_portfolio:
    st.title("Intelligent Stock Market Advisor")
    st.markdown("Enter your **stock market question** or request advice on strategies, analysis, or trends.")

    user_input = st.text_input("Your Question", placeholder="e.g., What are the best stocks for 2025?")
    submit = st.button("Predict")

    if submit and user_input:
        with st.spinner("Analyzing stock trends..."):
            result = predict(user_input)
            st.text_area(" Market Insight", result, height=300)

# prompt enggineering second project
import google.generativeai as genai
genai.configure(api_key="22") # your api key
gemini_model = genai.GenerativeModel("gemini-2.5-flash")
if "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = gemini_model.start_chat(history=[])

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

with st.sidebar.expander("AI Prompt Second Project", expanded=True):
    use_gemini = st.checkbox("Launch AI")
if use_gemini:
    st.subheader("Ask Questions")

    user_prompt = st.text_input("You:", placeholder="Ask something...", key="user_input")
    send_btn = st.button("Send")

    if send_btn and user_prompt.strip() != "":
        st.session_state.chat_messages.append({"role": "user", "text": user_prompt})

        with st.spinner("Gemini is thinking..."):
            try:
                response = st.session_state.gemini_chat.send_message(user_prompt)
                st.session_state.chat_messages.append({"role": "gemini", "text": response.text})
            except Exception as e:
                st.error(f"Error from Gemini: {e}")
                st.session_state.chat_messages.append({"role": "gemini", "text": " Gemini failed to respond."})

        st.session_state.user_input = ""  

    for msg in st.session_state.chat_messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["text"])
