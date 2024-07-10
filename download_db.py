import gdown

# Define the URL of the file on Google Drive
url = 'https://drive.google.com/uc?id=1HAchuckJEaT2tdYo4sThNYowup29o_vN'

# Define the path where you want to save the downloaded file
output = 'olist.sqlite'

# Download the file
gdown.download(url, output, quiet=False)
