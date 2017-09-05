# domoticz-storm-report
A Python plugin for Domoticz to access burze.dzis.net API for weather/storm data

## Dependencies
Plugin is using suds SOAP Python library. suds library are already embeded as git submodule

## Installation
1. Make sure your Domoticz instance supports Domoticz Plugin System - see more https://www.domoticz.com/wiki/Using_Python_plugins
2. Register at https://burze.dzis.net/ and ask author for API key https://burze.dzis.net/?page=kontakt
3. Get plugin data into DOMOTICZ/plugins directory (remember to fetch it recursivelly to get all the dependencies)
cd YOUR_DOMOTICZ_PATH/plugins
git clone --recursive https://github.com/lrybak/domoticz-storm-report
4. Restart Domoticz
5. Go to Setup > Hardware and create new Hardware with type: domoticz-storm-report
5.1 Enter name (it's up to you), API key and city you would like to monitor. You can check city availability at https://burze.dzis.net/?page=wyszukiwarka
5.2  Check every x minutes - how often plugin will check for new data. Data available through API are updated every 15 minutes so it's no need to query API more frequently
5.3 Monitoring radius (km) - range of query lookup

Plugin comunicates via Domoticz logs. Check logs for feedback about city availability, corectness of api key and so on. After first API lookup plugin will create all the devices
You can add more city to lookup - create another plugin (hardware) instance

## Troubleshooting
In case of issues, mostly plugin not visible on plugin list, check logs if plugin system is working correctly.
See Domoticz wiki for resolution of most typical installation issues http://www.domoticz.com/wiki/Linux#Problems_locating_Python

## Contribute
Feel free to test and report issues or other improvements.
Plugin uses gettext for translation, currently english and polish are available.
If you want to add another language, use included messages.pot template and prepare translation