#!/bin/zsh

description="This shell script installs the chromedriver version that matches the installed Google Chrome version.\nNote that it depends on NodeJS and npm and may not work well every time."

chrome_version=$(mdls -name kMDItemVersion /Applications/Google\ Chrome.app | awk '{print $3}' | tr -d '"')
chrome_major_version=$(echo $chrome_version | cut -d '.' -f 1)
echo "Current Google Chrome Version: $chrome_version"
echo "Chrome Major Version: $chrome_major_version"

sudo npm -g install chromedriver@$chrome_major_version
installation=$(npm list -g chromedriver | grep chromedriver | awk -F '@' '{print $2}')
echo "ChromeDriver Installed: $installation"
