import FeatureExtractor as fe
import EmailFetcher as ef
import gui
import predictor as pr


def main():
    print("\nFetching Emails...\n")
    # gui.interfaceFetchEmails()
    username = "mrcool.cool9@gmail.com"
    password = "****"
    #ef.login(username, password)
    print("Extracting Features...\n")
    clss = fe.extractFeatures()

    pr.login(username, password)
    pr.predict(clss)


main()
