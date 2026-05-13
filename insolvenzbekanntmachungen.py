import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import sys
import datetime

url = "https://neu.insolvenzbekanntmachungen.de/ap/suche.jsf" # also works with https://www.restrukturierungsbekanntmachung.de/res-ap/suche.jsf
company_full_name ="FULL_COMPANY_NAME" # must be the full name, with which you can also find the company here: https://www.handelsregister.de/rp_web/normalesuche/welcome.xhtml
found_message = "INSOLVENZBEKANNTMACHUNG GEFUNDEN!"
not_found_message = "Keine Insolvenzbekanntmachung gefunden."

# variables for error and found
use_windows_notifier = True # using windows notifier on error or when found
add_info_to_file = True # creates a file on error or when found
info_file_path = "C:\\Users\\YOUR_USER\\Desktop\\Insolvenzbekanntmachung.txt" # your file path to see any important information, creates a new file or writes in the existing file a new line.


def get_frm_suche_inputs(soup):
    """
    Pull **every** control belonging to the JSF form named `frm_suche`
    (inputs, selects, textareas, checkboxes/radios).  
    The return contains all expected form input fields.

    Parameters
    ----------
    soup : bs4.BeautifulSoup
        Parsed HTML of the search page.

    Returns
    -------
    dict
        `{field_name: field_value}` for all relevant controls.
    """

    # form identifier itself
    result = {"frm_suche": ""}

    # locate the form – name or id is usually `frm_suche`
    form = soup.find("form", {"name": "frm_suche"}) or \
           soup.find("form", {"id": "frm_suche"})
    if not form:
        # no form -> nothing else to do
        return result

    # iterate over all possible controls
    for tag in form.find_all(["input", "select", "textarea"]):
        name = tag.get("name")
        if not name or not name.startswith("frm_suche"):
            # we only care about frm_suche.* fields
            continue

        if tag.name == "select":
            # single‑select: pick the first <option selected>
            if tag.has_attr("multiple"):
                values = [opt.get("value", opt.text)
                          for opt in tag.find_all("option") if opt.has_attr("selected")]
                result[name] = ",".join(values) if values else ""
            else:
                opt = tag.find("option", selected=True)
                if opt:
                    result[name] = opt.get("value", opt.text)
                else:
                    # no explicit selection – fall back to first option
                    opt = tag.find("option")
                    result[name] = opt.get("value", opt.text) if opt else ""

        elif tag.name == "textarea":
            result[name] = tag.text or ""

        else:  # <input>
            input_type = tag.get("type", "").lower()
            if input_type in {"radio", "checkbox"}:
                if tag.has_attr("checked"):
                    result[name] = tag.get("value", "on")
                # otherwise skip unchecked boxes
            else:
                result[name] = tag.get("value", "")

    return result

def check_insolvenzbekanntmachungen():
    session = requests.Session()
    get_resp = session.get(url)
    try:
        get_resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        if add_info_to_file == True:
            update_or_create_file(err)
        if use_windows_notifier == True:
            windows_notifier(err)

    soup = BeautifulSoup(get_resp.text, 'html.parser')

    # get everything for the payload, so it is as expected by the server
    frm_inputs = get_frm_suche_inputs(soup)

    # one more frm_input than needed, but no problem:
    # frm_suche:lsom_gericht:lsom ='-- Alle Insolvenzgerichte --'

    # keeping the jsf information as well
    hidden_inputs = {inp['name']: inp.get('value', '')
                    for inp in soup.find_all('input', type='hidden')}

    # build the payload
    payload = hidden_inputs.copy()
    payload.update(frm_inputs)

    # add own search-terms
    payload['frm_suche:litx_firmaNachName:text'] = company_full_name

    # post by simulating the "Search"-click
    post_resp = session.post(url, data=payload)
    post_resp.raise_for_status()

    # parse result
    result_soup = BeautifulSoup(post_resp.text, 'html.parser')
    no_hits_span = result_soup.find('span', id='otx_keineTreffer')

    if no_hits_span and 'Keine Treffer' in no_hits_span.text:
        print(not_found_message, company_full_name)
        update_or_create_file(not_found_message)
    else:
        print(found_message, company_full_name)
        if add_info_to_file == True:
            update_or_create_file(found_message)
        if use_windows_notifier == True:
            windows_notifier(found_message)

    print ("End")

def windows_notifier(message):
    """
    Makes a Windows notification with the `message` as title and the `company_full_name` as description.

    Parameters
    ----------
    message : str
        Custom message to be shown
    """
    toaster = ToastNotifier()
    toaster.show_toast(message, 
                    company_full_name,
                    icon_path=None,
                    duration=10)
    
def update_or_create_file(message, path = info_file_path):
    """
    Creates a file on the info_file_path if not exists and adds a new line with the message and the company_full_name

    Parameters
    ----------
    message : str
        String to add to the file.
    path : str, optional
        Path to the file location. Defaults to `info_file_path`
    """
    file = open(info_file_path, "a")
    # makes a new line + timestamp + the message + the company name
    file.write("\n" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + 
               message + " " + company_full_name)
    file.close

if __name__ == "__main__":
    try:
        check_insolvenzbekanntmachungen()
    except Exception as err:
        if add_info_to_file == True:
            update_or_create_file(err)
        if use_windows_notifier == True:
            windows_notifier(err)
        # make an error for the windows task scheduler
        sys.exit(1)
