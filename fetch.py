import imaplib
import email

user = 'mrcool.cool9@gmail.com'
password = 'dheerajPant@02'
imap_url = 'imap.gmail.com'


def auth(user, password, imap_url):
    print(user, password, imap_url)
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(user, password)
    return con


con = auth(user, password, imap_url)
con.select('INBOX')

result, data = con.fetch(b'10', '(RFC822)')
raw = email.message_from_bytes(data[0][1])
print(raw)
