# FreshDesk Q Monitor
A sound is played if the response contains valid tickets<br>
(The idea is to auto-scan the monitored Qs every 60s for new/unassigned tickets in the specified groups)

# Base URL
FD Prod:	https://aquasecurity.freshdesk.com<br>
FD Dev:		https://aquasecuritysandbox.freshdesk.com

# api_key
FD / Upper Right Icon / Profile Settings / View API Key

# Groups 
FD Prod
```[bash]
"APAC": 16000086007,
"APAC - Tier 2": 16000088977,
"APAC - Tier 3": 16000088978,
"Architects": 16000086708,
"Cloud": 16000086102,
"Customer Success": 16000089339,
"EMEA": 16000085997,
"EMEA - Tier 2": 16000088975,
"EMEA - Tier 3": 16000088976,
"ESE": 16000087280,
"Managers": 16000086063,
"Marketplace": 16000083024,
"NA": 16000085996,
"POC": 16000086229,
"Support": 16000074458,
"Warranty": 16000088209
```

# To run the script
```[bash]
sudo dnf install python3-pip  # Ensure pip is installed
pip3 install requests
pip3 install kivy

python3 main.py
```

Ensure the file AztecSkullWhistle.wav is in the same folder as the script and the FD API Key is set in the script


# To build an APK:
```[bash]
podman run -it -v $HOME/.buildozer:/home/user/.buildozer -v $(pwd):/home/user/hostcwd --entrypoint bash docker.io/mulan04/buildozer:latest
buildozer android debug
```

# To trigger the workflow:
```[bash]
git tag -a v0.1 -m "Release version 0.1"
git push --tags
```
or in the WebUI
- `https://github.com/mulan04/<repo>/releases/new`
- enter a new Tag name
- click on "Create new tag: \<new Tag\> on publish"
- click on "Publish Release"