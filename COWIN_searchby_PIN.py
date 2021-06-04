# Code to get vaccine availability: Bharath Konda

numdays = 6   # Number of days to check Vaccine Availability
Dose = 1    # Availability of which Dose to check
Age = 55  # Age of the individual to check vaccine availability, (minimum age for checking)

# Pincodes to check, give pin code number in square brackets with , between each one
pincodes = [580000,580001]

# Importing required Packages
import datetime, pyttsx3, requests, time
from fake_useragent import UserAgent


# Vaccine availability announcement
def announce(announcement):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 100)
    engine.say(announcement)
    engine.runAndWait()


# Code function to check the availability
def vaccine_availability(pin):
    temp_user_agent = UserAgent()
    browser_header = {'User-Agent': temp_user_agent.random}
    if Dose == 1:
        dose_to_check = 'available_capacity_dose1'
    else:
        dose_to_check = 'available_capacity_dose2'
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    for VAC_DATE in date_str:
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin, VAC_DATE)
        response = requests.get(url, headers=browser_header)
        if response.ok:
            resp_json = response.json()
            if resp_json["sessions"]:
                print("Availability on: {}".format(VAC_DATE))
                for session in resp_json["sessions"]:
                    if session[dose_to_check] == 0:
                        pass
                    else:
                        if session['min_age_limit'] <= Age:
                            print(f'{session["name"]} open for min AGE--> {session["min_age_limit"]}  {session["vaccine"]} '
                                  f'Number of slots availble--> {session[dose_to_check]} ')
                            announce(session["vaccine"] + ' Dose ' + str(Dose) + ' is available at ' + session[
                                "name"] + 'in location ' + str(pin))
            else:
                print("Slots not opened on {}".format(VAC_DATE))


while True:

    for location in pincodes:
        print(f'Below is the availability of the pincode -> {str(location)} for Dose {str(Dose)}')
        vaccine_availability(location)
    now = datetime.datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f'Above availability check is performed at {current_time}')

    time.sleep(300)


