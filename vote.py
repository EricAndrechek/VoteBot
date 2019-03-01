import requests, re, json, time, random, os
requests.packages.urllib3.disable_warnings()

base_url = "https://poll.fm/"
redirect = ""

useragents = []
current_useragent = ""

proxies = []
current_proxy = {"http": ""}
current_proxy_num = -1

def get_all_useragents():
    f = open("useragent.txt", "r")
    for line in f:
        useragents.append(line.rstrip('\n').rstrip('\r'))
    f.close()


def choose_useragent():
    k = random.randint(0, len(useragents) - 1)
    current_useragent = useragents[k]


def get_all_proxies():
    f = open("proxy.txt", "r")
    for line in f:
        proxies.append(line.rstrip('\n').rstrip('\r'))
    f.close()


def choose_proxy():
    k = random.randint(0, len(proxies) - 1)
    current_num = k
    current_proxy["http"] = proxies[k]


def vote_once(form, value):
    c = requests.Session()
    #Chooses useragent randomly
    choose_useragent()
    redirect = {
        "Referer":
        base_url + str(form) + "/",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent":
        current_useragent,
        "Upgrade-Insecure-Requests":
        "1",
        "Accept-Encoding":
        "gzip, deflate, sdch",
        "Accept-Language":
        "en-US,en;q=0.8"
    }

    # Chooses proxy randomly
    choose_proxy()
    try:
        init = c.get(base_url + str(form) + "/", headers=redirect, verify=False, proxies=current_proxy)
    except:
        print("error with proxy")
        #proxies.remove(current_proxy_num)
        return None

    data = re.search("data-vote=\"(.*?)\"", init.text).group(1).replace('&quot;', '"')
    data = json.loads(data)
    # Search for the hidden form value
    pz = re.search("type='hidden' name='pz' value='(.*?)'", init.text).group(1)
    # Build the GET url to vote
    request = "https://poll.fm/vote.php?va=" + str(data['at']) + "&pt=0&r=0&p=" + str(form) + "&a=" + str(value) + "%2C&o=&t=" + str(data['t']) + "&token=" + str(data['n']) + "&pz=" + str(pz)
    try:
        send = c.get(request, headers=redirect, verify=False, proxies=current_proxy)
    except:
        print("error with proxy")
        return None

    return ("revoted" in send.url)


def vote(form, value, times, wait_min=None, wait_max=None):
    global redirect
    # For each voting attempt
    i = 1
    print("Rigging the election for Xander...")
    while i < times + 1:
        if (i % 75 == 0) and i != 0:
            print('Taking a short nap to make sure we don\'t get shut down. I\'ll wake back up in 5 minutes.')
            time.sleep(300)
        b = vote_once(form, value)
        # If successful, print that out, else try waiting for 60 seconds (rate limiting)
        if not b:
            if wait_min and wait_max:
                seconds = random.randint(wait_min, wait_max)
            else:
                seconds = 5
            print("Voted " + str(i) + " times")
            time.sleep(seconds)
        else:
            print("Locked to prevent IP blockage. Sleeping for 90 seconds.")
            i -= 1
            time.sleep(90)
        i += 1


# Initialize these to the specific form and how often you want to vote
poll_id = 10249426
answer_id = 47133209
number_of_votes = 15576
wait_min = None
wait_max = None

get_all_proxies()
get_all_useragents()
vote(poll_id, answer_id, number_of_votes, wait_min, wait_max)
