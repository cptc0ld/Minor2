import FeatureExtractor as fe
import EmailFetcher as ef
import predictor as pr
import reply.test as ts

def main():
    print("\nFetching Emails...\n")
    # gui.interfaceFetchEmails()
    username = "mrcool.cool9@gmail.com"
    password = "dheerajPant@02"
    # ef.login(username, password)

    print("Extracting Features...\n")
    clss = fe.extractFeatures()

    pr.login(username, password)
    status, msg = pr.predict(clss)
    print(msg)
    if(status):
        ts.pred_ans(msg)
main()
