import numpy as np
from sklearn.ensemble import RandomForestClassifier


def accuracy(output, result):
    match = 0
    length = len(result)
    for i in range(0, length):
        if output[i] == result[i]:
            match = match+1

    return (match/(length+0.0))*100


def classifiers(trainingFeatures, output, testFeatures, testOutput):
    print("Applying Random Forrest...\n")
    # print(np.unique(output))
    # Random Forrest Classifier
    clf = RandomForestClassifier(n_estimators=50)
    clf = clf.fit(trainingFeatures, output)
    print("detect")
    result_1 = clf.predict(testFeatures)
    acc = (accuracy(testOutput, result_1))
    print("Random Forrest: %.2f " % (acc))

    return result_1, clf
