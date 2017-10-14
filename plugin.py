# -*- coding: utf-8 -*-
# A Python plugin for Domoticz to access burze.dzis.net API for weather/storm data
#
# Author: fisher
#
#
# v0.1.0 - initial version
# v0.1.1 - removed gettext based translations - it caused plugin instability
#
"""
<plugin key="domoticz-storm-report" name="domoticz-storm-report (burze.dzis.net)" author="fisher" version="0.1.0" wikilink="https://www.domoticz.com/wiki/Plugins/domoticz-storm-report.html" externallink="https://github.com/lrybak/domoticz-storm-report">
    <params>
		<!-- param field="Mode1" label="Burze.dzis.net API entrypoint" default="https://burze.dzis.net/soap.php?WSDL" width="400px" required="true"  / -->
        <param field="Mode2" label="Burze.dzis.net API key" width="400px" default="" required="true" />
		<param field="Mode3" label="Check every x minutes" width="40px" default="15" required="true" />

		<param field="Mode4" label="City to monitor" width="400px" default="" required="true" />
        <param field="Mode5" label="Monitoring radius (km)" width="40px" default="25" required="false" />
		<param field="Mode6" label="Debug" width="75px">
			<options>
				<option label="True" value="Debug"/>
				<option label="False" value="Normal" default="true" />
			</options>
		</param>
    </params>
</plugin>
"""

import Domoticz
import os
import sys
import datetime

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    # linux/mac specific code here
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/libs/suds-py3")
elif sys.platform.startswith('win32'):
    #  win specific
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\libs\suds-py3")

from suds.client import Client
from suds import WebFault

L10N = {
    'pl': {
        "Creating devices...":
            "Tworzenie urządzeń...",

        "Frost alert":
            "Ostrzeżenie o mrozie",

        "Heat alert":
            "Ostrzeżenie o upale",

        "Wind alert":
            "Ostrzeżenie o wietrze",

        "Rain/snowfall alert":
            "Ostrzeżenie o deszczu/śniegu",

        "Storm alert":
            "Ostrzeżenie przed burzą",

        "Cyclone alert":
            "Ostrzeżenie przed trąbą pow.",

        "Lightning alert":
            "Ostrzeżenie o wyładowaniach",

        "Lightnings":
            "Wyładowania",

        "Nearest lightning":
            "Najbliższe wyładowanie",

        "Period of data":
            "Okres czasu",

        "min":
            "min",

        "Devices created.":
            "Urządzenia utworzone.",

        "Fetching data every %(time)d min.":
            "Pobieranie danych co %(time)d min.",

        "City not validated":
            "Niepoprawne miasto, popraw swoje zapytanie",

        "Looking for city: %(city)s":
            "Szukam miasta: %(city)s",

        "City [%(city)s] not found.":
            "Miasto [%(city)s] nie zostało znalezione.",

        "Please check your plugin configuration.":
            "Sprawdź konfigurację pluginu.",

        "City found: [%(city)s] cords are (%(cords_y)s, %(cords_x)s).":
            "Miasto znalezione: [%(city)s], koordynaty  (%(cords_y)s, %(cords_x)s).",

        "Fetching weather alerts for [%(city)s]":
            "Pobieram ostrzeżenia pogodowe dla miasta [%(city)s]",

        "No warning":
            "Brak ostrzeżeń",

        "Frost warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenie o mrozie (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Snow/rainfall warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenie o opadach deszczu/śniegu (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Storm warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenie o burzy  (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Cyclone warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenieo trąbie powietrznej (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Wind warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenie o wietrze (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Heat warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s":
            "Ostrzeżenie o upale (%(level)d poziom)<br>Obowiązuje od %(valid_from)s do %(valid_to)s",

        "Number of lightnings (last %(lightning_period)d min): %(lightning_qty)d<br/>\n"
        "Nearest: %(lightning_distance).2f km (%(lightning_direction)s)<br/>\n"
        "Lookup radius: %(lightning_lookup_range)d km":
            "Liczba wyładowań (ostatnie %(lightning_period)d min): %(lightning_qty)d<br/>\n"
            "Najbliższe: %(lightning_distance).2f km (%(lightning_direction)s)<br/>\n"
            "Promień pomiaru: %(lightning_lookup_range)d km",

        "No lightning registered (last %(lightning_period)d min)<br/>\n"
        "Lookup radius: %(lightning_lookup_range)d km":
            "Brak zarejestrowanych wyładowań (ostatnie %(lightning_period)d min)<br/>\n"
            "Promień pomiaru: %(lightning_lookup_range)d km",

        "North":
            "Północ",

        "North-west":
            "Północny-zachód",

        "North-east":
            "Północny-wschód",

        "South":
            "Południe",

        "South-west":
            "Południowy-zachód",

        "South-east":
            "Południowy-wschód",

        "East":
            "Wschód",

        "West":
            "Zachód",

        "Looking up for storm information near [%(city)s]":
            "Szukam informacji o burzach w okolicy miasta [%(city)s]",

        "No lightnings":
            "Brak wyładowań",

        "Fetch data complete":
            "Pobrano dane",

        "Looking up city: [%(city)s]":
            "Szukam miasta: [%(city)s]",

        "The city name [%(city)s] not found.":
            "Miasto [%(city)s] nie zostało znalezione.",

        "City found: [%(city)s]":
            "Miasto znalezione: [%(city)s]",

        "Best match: [%(city)s], however you can narrow your query to get more "
        "precise weather prediction:":
            "Najlepiej dopasowane: [%(city)s], popraw swoje zapytanie aby otrzymać "
            "bardziej szczegółowe dane pogodowe:",

        "The possible choices are: ":
            "Dostępne opcje: ",

        "The city name [%(city)s] is ambiguous, please narrow your query.":
            "Nazwa miasta [%(city)s] jest niejednoznaczna, popraw swoje zapytanie.",

        "Device=%(device_unit)d has been updated.":
            "Urządzenie device=%(device_unit)d zostało uaktualnione.",

        "No such Device=%(device_unit)d.":
            "Nie ma takiego urządzenia Device=%(device_unit)d.",

        "Distance to nearest lightning":
            "Odległość do najbliższego wyładowania",

        "None":
            "Brak",

        "Check if device=%(device_unit)d has to be updated...":
            "Sprawdzam czy urządzenie device=%(device_unit)d powinno być uaktualnione...",

        "The possible entries are: ":
            "Dostępne opcje: ",

        "Updating device=%(device_unit)d":
            "Uaktualniam urządzenie device=%(device_unit)d",
    },
    'en': { }
}

def _(key):
    try:
        return L10N[Settings["Language"]][key]
    except KeyError:
        return key

class BasePlugin:
    enabled = True
    def __init__(self):
        # Constants
        self.FROST_UNIT = 1
        self.HEAT_UNIT = 2
        self.WIND_UNIT = 3
        self.FALL_UNIT = 4
        self.STORM_UNIT = 5
        self.CYCLONE_UNIT = 6
        self.LIGHTNING_UNIT=7
        self.LIGHTNING_QTY_UNIT=8
        self.LIGHTNING_DISTANCE_UNIT=9
        self.LIGHTNING_DIRECTION_UNIT=10
        self.LIGHTNING_PERIOD_UNIT=11

        self.lastDataFetch = datetime.datetime.now()
        self.inProgress = False
        self.cityInPoland = False

        return

    def onStart(self):
        self.api_wsdl = "https://burze.dzis.net/soap.php?WSDL"
        self.api_key = Parameters["Mode2"]
        self.api_check_every = int(Parameters["Mode3"])
        self.api_city_to_lokup = Parameters["Mode4"]
        self.api_radius = int(Parameters["Mode5"])
        self.city_validated = False
        self.city_to_lookup = ''
        self.debug = False
        self.authentication_failed = False

        if Parameters["Mode6"] == "Debug":
            Domoticz.Debugging(1)
            DumpConfigToLog()
            self.debug = True

        self.client = Client(url=self.api_wsdl)

        Domoticz.Debug("onStart called")

        self.city_validated = self.checkCity(self.api_city_to_lokup)

        if self.city_validated:
            self.cityInPoland = self.cityInCountry(self.api_city_to_lokup, "PL")

        if (len(Devices) == 0 and self.city_validated):
            Domoticz.Debug(_("Creating devices..."))
            device_used = 1
            # Alert services are available only in Poland
            if self.cityInPoland:
                Domoticz.Device(Name=_("Frost alert"), Unit=self.FROST_UNIT, TypeName="Alert", Used=device_used).Create()
                Domoticz.Device(Name=_("Heat alert"), Unit=self.HEAT_UNIT, TypeName="Alert", Used=device_used).Create()
                Domoticz.Device(Name=_("Wind alert"), Unit=self.WIND_UNIT, TypeName="Alert", Used=device_used).Create()
                Domoticz.Device(Name=_("Rain/snowfall alert"), Unit=self.FALL_UNIT, TypeName="Alert", Used=device_used).Create()
                Domoticz.Device(Name=_("Storm alert"), Unit=self.STORM_UNIT, TypeName="Alert", Used=device_used).Create()
                Domoticz.Device(Name=_("Cyclone alert"), Unit=self.CYCLONE_UNIT, TypeName="Alert", Used=device_used).Create()

            Domoticz.Device(Name=_("Lightning alert"), Unit=self.LIGHTNING_UNIT, TypeName="Text", Used=device_used).Create()
            Domoticz.Device(Name=_("Lightnings"), Unit=self.LIGHTNING_QTY_UNIT,
                            TypeName="Custom", Used=device_used).Create()
            Domoticz.Device(Name=_("Nearest lightning"), Unit=self.LIGHTNING_DISTANCE_UNIT,
                            TypeName="Custom", Used=device_used, Options={"Custom": "1;km"}).Create()
            Domoticz.Device(Name=_("Nearest lightning"), Unit=self.LIGHTNING_DIRECTION_UNIT,
                            TypeName="Text", Used=device_used).Create()
            Domoticz.Device(Name=_("Period of data"), Unit=self.LIGHTNING_PERIOD_UNIT, TypeName="Custom",
                            Used=device_used, Options={"Custom": "1;" + _("min")}).Create()
            Domoticz.Debug(_("Devices created."))

        # Domoticz.Connect()
        Domoticz.Debug(_("Fetching data every %(time)d min.") % {'time': self.api_check_every})
        Domoticz.Heartbeat(20)
        self.onHeartbeat(fetch=True)

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self, fetch=False):
        Domoticz.Debug("onHeartbeat called")

        self.client = Client(url=self.api_wsdl)

        if self.authentication_failed:
            return True

        # check if another thread is not running
        # and time between last fetch has elapsed
        if fetch == False:
            if self.inProgress or ((datetime.datetime.now() - self.lastDataFetch).total_seconds() < self.api_check_every * 60):
                return

        self.inProgress = True

        if not self.city_validated:
            Domoticz.Debug(_("City not validated"))
            return

        Domoticz.Log(_("Looking for city: %(city)s") % {'city': self.city_to_lookup})
        # client = Client(url = self.api_wsdl)
        # city = client.service.miejscowosc(self.city_to_lookup, self.api_key)
        city = self.cityLookup(self.city_to_lookup)
        x = city.x
        y = city.y

        if (x==0.0 and y==0.0):
            Domoticz.Log(_("City [%(city)s] not found.") % {'city': self.city_to_lookup})
            Domoticz.Log(_("Please check your plugin configuration."))
        else:
            Domoticz.Log(_("City found: [%(city)s] cords are (%(cords_y)s, %(cords_x)s).")
                         % {'city': self.city_to_lookup, 'cords_y': y, 'cords_x': x})

        # Weather alerts (covering country of Poland only)
        Domoticz.Log(_("Fetching weather alerts for [%(city)s]") % {'city': self.city_to_lookup})
        weather_alerts = self.client.service.ostrzezenia_pogodowe(y, x, self.api_key)
        LEVEL_MAPPING = {0: 1, 1: 2, 2: 3, 3: 4}

        # Freeze alert
        frost_level = weather_alerts['mroz']
        frost_from = weather_alerts['mroz_od_dnia']
        frost_to = weather_alerts['mroz_do_dnia']
        if frost_level == 0:
            frost_alert = _("No warning")
        else:
            frost_alert = _("Frost alert")
            frost_alert = _("Frost warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                          % {'level': frost_level, 'valid_from': frost_from, 'valid_to': frost_to}
        UpdateDevice(Unit=self.FROST_UNIT, nValue=LEVEL_MAPPING[frost_level], sValue=frost_alert)

        # Rainfall/Snowfall alert
        fall_level = weather_alerts['opad']
        fall_from = weather_alerts['opad_od_dnia']
        fall_to = weather_alerts['opad_do_dnia']
        if fall_level == 0:
            rainfall_alert = _("No warning")
        elif fall_level in (1, 2, 3):
            rainfall_alert = _("Snow/rainfall warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                             % {'level': fall_level, 'valid_from': fall_from, 'valid_to': fall_to}
        UpdateDevice(Unit=self.FALL_UNIT, nValue=LEVEL_MAPPING[fall_level], sValue=rainfall_alert)

        # Storm alert
        storm_level = weather_alerts['burza']
        storm_from = weather_alerts['burza_od_dnia']
        storm_to = weather_alerts['burza_do_dnia']
        if storm_level == 0:
            storm_alert = _("No warning")
        elif storm_level in (1, 2, 3):
            storm_alert = _("Storm warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                          % {'level': storm_level, 'valid_from': storm_from, 'valid_to': storm_to}
        UpdateDevice(Unit=self.STORM_UNIT, nValue=LEVEL_MAPPING[storm_level], sValue=storm_alert)

        # Cyclone alert
        cyclone_level = weather_alerts['traba']
        cyclone_from = weather_alerts['traba_od_dnia']
        cyclone_to = weather_alerts['traba_od_dnia']
        if cyclone_level == 0:
            storm_alert = _("No warning")
        elif cyclone_level in (1, 2, 3):
            storm_alert = _("Cyclone warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                          % {'level': cyclone_level, 'valid_from': cyclone_from, 'valid_to': cyclone_to}
        UpdateDevice(Unit=self.CYCLONE_UNIT, nValue=LEVEL_MAPPING[cyclone_level], sValue=storm_alert)

        # Wind alert
        wind_level = weather_alerts['wiatr']
        wind_from = weather_alerts['wiatr_od_dnia']
        wind_to = weather_alerts['wiatr_do_dnia']
        if wind_level == 0:
            wind_alert = _("No warning")
        elif wind_level in (1, 2, 3):
            wind_alert = _("Wind warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                         % {'level': wind_level, 'valid_from': wind_from, 'valid_to': wind_to}
        # Devices[self.WIND_UNIT].Update(nValue=LEVEL_MAPPING[wind_level], sValue=wind_alert)
        UpdateDevice(Unit=self.WIND_UNIT, nValue=LEVEL_MAPPING[wind_level], sValue=wind_alert)

        # Heat alert
        heat_level = weather_alerts['upal']
        heat_from = weather_alerts['upal_od_dnia']
        heat_to = weather_alerts['upal_do_dnia']
        if heat_level == 0:
            heat_alert = _("No warning")
        elif heat_level in (1, 2, 3):
            heat_alert = _("Heat warning (%(level)d degree)<br>Valid from %(valid_from)s to %(valid_to)s") \
                         % {'level': heat_level, 'valid_from': heat_from, 'valid_to': heat_to}
        UpdateDevice(Unit=self.HEAT_UNIT, nValue=LEVEL_MAPPING[heat_level], sValue=heat_alert)

        LIGHTNING_ALERT = _("""Number of lightnings (last %(lightning_period)d min): %(lightning_qty)d<br/>
        Nearest: %(lightning_distance).2f km (%(lightning_direction)s)<br/>
        Lookup radius: %(lightning_lookup_range)d km""")
        LIGHTNING_NO_ALERT = _("""No lightning registered (last %(lightning_period)d min)<br/>
        Lookup radius: %(lightning_lookup_range)d km""")

        CARDINAL_DIRECTION_MAPPING = {
            'N':    _("North"),
            'NW':   _("North-west"),
            'NE':   _("North-east"),
            'S':    _("South"),
            'SW':   _("South-west"),
            'SE':   _("South-east"),
            'E':    _("East"),
            'W':    _("West")
        }

        # Storm details
        Domoticz.Debug(_("Looking up for storm information near [%(city)s]") % {'city': self.city_to_lookup})
        storm_alert = self.client.service.szukaj_burzy(y, x, self.api_radius, self.api_key)

        lightning_qty = storm_alert['liczba']
        lightning_distance = storm_alert['odleglosc']
        lightning_direction = storm_alert['kierunek'] if storm_alert['kierunek'] else ""
        lightning_period = storm_alert['okres']

        if lightning_qty > 0:
            UpdateDevice(self.LIGHTNING_UNIT, 1, LIGHTNING_ALERT %
                         {'lightning_qty': lightning_qty, 'lightning_lookup_range': self.api_radius,
                          'lightning_distance': lightning_distance, 'lightning_direction': lightning_direction,
                          'lightning_period': lightning_period})
            UpdateDevice(self.LIGHTNING_QTY_UNIT, lightning_qty, str(lightning_qty))
            Devices[self.LIGHTNING_DISTANCE_UNIT].Update(nValue=0, sValue=str(lightning_distance).replace('.', ','))
            UpdateDevice(self.LIGHTNING_DIRECTION_UNIT, 1, "%s (%s)" % (CARDINAL_DIRECTION_MAPPING[lightning_direction], lightning_direction))
            Devices[self.LIGHTNING_PERIOD_UNIT].Update(nValue=lightning_period, sValue=str(lightning_period))
        else:
            UpdateDevice(self.LIGHTNING_UNIT, 1, LIGHTNING_NO_ALERT %
                         {'lightning_lookup_range': self.api_radius, 'lightning_period': lightning_period})
            UpdateDevice(self.LIGHTNING_DIRECTION_UNIT, 1, _("No lightnings"))
            UpdateDevice(self.LIGHTNING_QTY_UNIT, lightning_qty, str(lightning_qty))
            Devices[self.LIGHTNING_DISTANCE_UNIT].Update(nValue=0, sValue=str(0))
            Devices[self.LIGHTNING_PERIOD_UNIT].Update(nValue=lightning_period, sValue=str(lightning_period))

        self.lastDataFetch = datetime.datetime.now()
        self.inProgress = False
        Domoticz.Log(_("Fetch data complete"))

    def cityInCountry(self, city, country="PL"):
        """Check if city is in Poland"""

        try:
            city_list = eval(
                self.client.service.miejscowosci_lista(city, country, self.api_key)
            )
        except WebFault as e:
            Domoticz.Error(e.fault.faultstring)
            return False

        search_query = city_list[0]
        search_res = city_list[1]

        if len(search_res) >= 1:
            if search_query.lower().strip() == search_res[0].lower().strip():
                return True
        else:
            return False

    def cityLookup(self, city):
        """Lookup WS against user-entered city"""

        try:
            return self.client.service.miejscowosc(city, self.api_key)
        except WebFault as e:
            Domoticz.Error(e.fault.faultstring)
            self.authentication_failed = True
            return False

    def checkCity(self, city):
        """Query WS against user-entered city"""

        try:
            city_list = eval(
                self.client.service.miejscowosci_lista(city, "", self.api_key)
            )
        except WebFault as e:
            Domoticz.Error(e.fault.faultstring)
            self.authentication_failed = True
            return False
        search_query = city_list[0]
        search_res = city_list[1]

        Domoticz.Debug(_("Looking up city: [%(city)s]") % {'city': search_query})

        if len(search_res) == 0:
            Domoticz.Error(_("The city name [%(city)s] not found.") % {'city': city})
            return False
        elif len(search_res) == 1:
            Domoticz.Debug(_("City found: [%(city)s]") % {'city': search_res[0]})
            self.city_to_lookup = search_res[0]
            return True
        if len(search_res) > 1:
            if search_query.lower().strip() == search_res[0].lower().strip():
                Domoticz.Log(_("Best match: [%(city)s], however you can narrow your query to get more precise weather prediction:")
                            % {'city': search_res[0]})
                Domoticz.Log(_("The possible choices are: "))
                for item in search_res:
                    Domoticz.Log("[%s]" % item)
                self.city_to_lookup = search_res[0]
                return True
            else:
                Domoticz.Error(_("The city name [%(city)s] is ambiguous, please narrow your query.") % {'city': city})
                Domoticz.Error(_("The possible choices are: "))
                for item in search_res:
                    Domoticz.Error("[%s]" %item)
                return False
        return False

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Status, Description):
    global _plugin
    _plugin.onConnect(Status, Description)

def onMessage(Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect():
    global _plugin
    _plugin.onDisconnect()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def UpdateDevice(Unit, nValue, sValue):
    # Domoticz.Debug(_("Check if device=%(device_unit)d has to be updated...") % {'device_unit': Unit})
    # if not (Devices[Unit].sValue == sValue and Devices[Unit].nValue == nValue):

    try:
        Devices[Unit].Update(nValue=nValue, sValue=sValue)
        Domoticz.Debug(_("Device=%(device_unit)d has been updated.") % {'device_unit': Unit})
    except KeyError:
        Domoticz.Debug(_("No such Device=%(device_unit)d.") % {'device_unit': Unit})