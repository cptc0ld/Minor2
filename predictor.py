import FeatureExtractor as fe
import imaplib
import email
import EmailFetcher as ef

INBOX_DIRECTORY = "email/new"  # Path where Inbox emails are saved
Num_MAIL = 2  # Number of mails to save on disk
MAILBOX = '"[Gmail]/All Mail"'


def saveToFolder(num, data, directory):
    f = open('%s/%s.eml' % (directory, -num), 'wb')
    f.write(data)
    f.close()


def saveEmails(imap):
    status, data = imap.select(MAILBOX)

    if status == 'OK':
        status, data = imap.search(None, "ALL")
        emailIds = data[0].split()

        for i in range(-1, -Num_MAIL, -1):
            rv, mail = imap.fetch(emailIds[i], "(RFC822)")
            if rv != 'OK':
                print("ERROR getting message", -i)
                return
            # fe.parseEmail(mail[0][1])
            saveToFolder(i, mail[0][1], INBOX_DIRECTORY)
    else:
        print("Unable to access ", MAILBOX)


def login(username, password):
    #username = raw_input("Enter emailid : ")
    #password = raw_input("Enter password : ")
    imap = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        imap.login(username, password)
    except imaplib.IMAP4.error:
        print("LOGIN FAILED... ")

    # status, mailboxes = imap.list()
    #print(status, mailboxes)
    saveEmails(imap)
    imap.logout()


def extractFeatures():
    emails = fe.read_from_disk(INBOX_DIRECTORY, 2)
    inboxEmails = []
    # seprate sent and inbox emails
    for email in emails:
        email = fe.parseEmail(email)
        inboxEmails.append(email)
    inboxEmailFeatures = []
    output = []

    # find numerical features
    for email in inboxEmails:
        features = {}
        features["sender_frequency"] = fe.senderFrequency(
            email["From"], inboxEmails)
        features["is_automated_mail"] = fe.words_present(
            email["emailText"], fe.negative_words)
        if(email["Subject"]):
            features["is_interrogative_text"] = fe.words_present(
                email["emailText"] + email["Subject"], fe.interrogative_words)
        else:
            features["is_interrogative_text"] = fe.words_present(
                email["emailText"], fe.interrogative_words)
        features["Cc"] = email["Cc"]
        # features["reply"] = replied(email["Message-ID"],sentEmails)
        featureslist = fe.dictList(features)
        inboxEmailFeatures.append(featureslist)
        # print("Mail Text: ", email['emailText'])
        return inboxEmailFeatures, email['emailText']


def predict(clss):
    input_feature, msg = extractFeatures()
    print(input_feature)
    if(clss.predict(input_feature)):
        print("Reply")
        return 1, msg
    else:
        print("Dont Reply")
    return 0, "no-reply"
