from mailsendsmtp import send_mail
from browse import login, browse_search, browse_download_pdf, browse_download_csv
from parse_csv import parse_csv
import browse
import mailsendsmtp
import sys
import os

user_name = 'Rohit Koganti'
user_mail = 'koganti.rohit@gmail.com'
password = 'jfkolhusmgoqxgas'
#receiver_mail = ['koganti.rohit@gmail.com', 'pstohvpi@gmail.com', 'ajaygadevpioffice@gmail.com', 'ashok.dewan@nic.in', \
#    'secygen.rs@sansad.nic.in', 'kota.gandhi@gmail.com', 'njoshivpioffice@gmail.com', \
#    'pawandilshad@gmail.com', 'pscell-vps@nic.in', 'ps-vps@nic.in', 'rajyasabhamediaunit@gmail.com', \
#    'secyvp@sansad.nic.in', 'ivsr12@gmail.com', 'sureshaps14@gmail.com', 'apsvikrant@gmail.com', 'vpsecretariat@gmail.com', \
#     'myellaps@yahoo.com', 'satyam1957.hyd@gmail.com']
receiver_mail = ['koganti.rohit@gmail.com']

url = 'https://samvad.media/'
samvad_id = 'mahar.singh@nic.in'
samvad_pw = 'vpsec2021!'
download_dir = os.getcwd() + '/'

def main():
    global receiver_mail

    if len(sys.argv) > 1:
        print("Argument: Receiver mail is ", sys.argv[1])
        receiver_mail = [str(sys.argv[1])]

    browser = login(url, samvad_id, samvad_pw, download_dir)
    if browser:
        browser, online_articles = browse_search(browser)
        if online_articles:
            browser, pdf_file = browse_download_pdf(browser, download_dir)
            if pdf_file:
                csv_file = browse_download_csv(browser, download_dir)
                if csv_file:
                    headlines = parse_csv(csv_file)
                    if headlines:
                        err = send_mail(user_name, user_mail, password, receiver_mail, pdf_file, headlines)
                        if not err:
                            print('Send: Mail sent successfully!')
                        else:
                            print('Send: Mailing failed, reverting with error message: ', err)
                    else:
                        print('Parse: Failed to parse csv file correctly. Looping back.')
                else:
                    print('Download: Failed to download csv. Looping back.')
            else:
                print('Download: Failed to download pdf. Looping back.')
        else:
            print('Search: No online articles found. Looping back.')
    else:
        print('Login: Failed to log-in into Samvad. Looping back.')


if __name__ == "__main__":
    main()
