import os
import plotly.io as pio

# Set Chrome path for Windows (most common location)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

# If that doesn't work, try this path
# chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"

# Set the path for Kaleido
os.environ["KALEIDO_CHROME_PATH"] = chrome_path

print(f"✅ Chrome path set to: {chrome_path}")

# Test if it works
fig = px.scatter(x=[1,2,3], y=[1,2,3])
fig.write_image("test.png")
print("✅ Test successful! PNG saved as test.png")