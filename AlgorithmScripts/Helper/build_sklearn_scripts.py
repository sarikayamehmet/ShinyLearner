import os, sys, shutil
import itertools as it

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algClass, paramDict):
    scriptDir = "../{}/tsv/sklearn/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))
#    return None

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()

        if algClass != None:
            template = template.replace("{algorithmClass}", algClass)

        algInstantiation = replaceTokens(globals()[shortAlgName], paramDict, shortAlgName)
        template = template.replace("{algorithmInstantiation}", algInstantiation)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

def replaceTokens(instantiation, paramDict, shortAlgName):
    for key, value in paramDict.items():
        if "{" + key + "}" not in instantiation:
            print("A key of {} was not found in the algorithm template for {}.".format(key, shortAlgName))
            sys.exit(1)
        instantiation = instantiation.replace("{" + key + "}", str(value))

    return instantiation

def createScripts(algorithmType, templateFilePath, shortAlgName, algClass, paramDict):
    createScript(algorithmType, templateFilePath, shortAlgName, "default", algClass, parseDefaultParams(paramDict))

#    for paramComboDict in parseNonDefaultParamCombos(paramDict):
#        paramName = buildParamName(paramComboDict)
#        createScript(algorithmType, templateFilePath, shortAlgName, paramName, algClass, paramComboDict)

def parseDefaultParams(paramDict):
    defaultParamDict = {}

    for key, value in paramDict.items():
        defaultParamDict[key] = value[0]

    return defaultParamDict

def parseNonDefaultParamCombos(paramDict):
    parameterNames = sorted(paramDict.keys())
    return [dict(zip(parameterNames, prod)) for prod in it.product(*(paramDict[varName] for varName in parameterNames))]

def buildParamName(paramDict):
    return "_".join([str(paramDict[key]).replace("()", "") for key in sorted(paramDict.keys())])

#############################################################
# Meta options
#############################################################

baseEstimatorOptions = ["DecisionTreeClassifier()", "KNeighborsClassifier()", "LinearDiscriminantAnalysis()", "LogisticRegression()", "MLPClassifier()", "SGDClassifier()", "SVC()"]
numEstimatorOptions = [50, 100, 1000]
boostAlgorithmOptions = ["SAMME.R", "SAMME"]
bootstrapOptions = [True, False]
oobScoreOptions = [False, True]
treeCriterionOptions = ["gini", "entropy"]
splitterOptions = ["best", "random"]
classWeightOptions = [None, "balanced"]
lossOptions = ['deviance', 'exponential']
neighborOptions = [1, 5, 10, 20]
weightOptions = ["uniform", "distance"]
pOptions = [1, 2]
cOptions = [1.0, 0.01, 0.1, 10.0]

#############################################################
# Classifiers
#############################################################

adaboost = "clf = AdaBoostClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, learning_rate=1.0, algorithm='{algorithm}', random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "adaboost", None, {"base_estimator": baseEstimatorOptions, "n_estimators": numEstimatorOptions, "algorithm": boostAlgorithmOptions})

bagging = "clf = BaggingClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, max_samples=1.0, max_features=1.0, bootstrap={bootstrap}, bootstrap_features=False, oob_score={oob_score}, warm_start=False, n_jobs=1, random_state=R_SEED, verbose=0)"
createScripts("Classification", "sklearn_c_template", "bagging", None, {"base_estimator": baseEstimatorOptions, "n_estimators": numEstimatorOptions, "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions})

decision_tree = "clf = DecisionTreeClassifier(criterion='{criterion}', splitter='{splitter}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, class_weight={class_weight}, presort=False, random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "decision_tree", None, {"criterion": treeCriterionOptions, "splitter": splitterOptions, "max_depth": [None], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_features": [None], "max_leaf_nodes": [None], "min_impurity_split": [1e-07], "class_weight": classWeightOptions})

extra_trees = "clf = ExtraTreesClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, bootstrap={bootstrap}, oob_score={oob_score}, class_weight={class_weight}, n_jobs=1, random_state=R_SEED, verbose=0, warm_start=False)"
createScripts("Classification", "sklearn_c_template", "extra_trees", None, {"n_estimators": numEstimatorOptions, "criterion": treeCriterionOptions, "max_depth": [None], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_features": [None], "max_leaf_nodes": [None], "min_impurity_split": [1e-07], "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions, "class_weight": classWeightOptions})

gradient_boosting = "clf = GradientBoostingClassifier(loss='{loss}', learning_rate=0.1, n_estimators={n_estimators}, subsample=1.0, criterion='{criterion}', min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_depth={max_depth}, min_impurity_split={min_impurity_split}, init=None, max_features={max_features}, verbose=0, max_leaf_nodes={max_leaf_nodes}, warm_start=False, presort='auto', random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "gradient_boosting", None, {"loss": lossOptions, "n_estimators": numEstimatorOptions, "criterion": ['friedman_mse'], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_depth": [3], "min_impurity_split": [1e-07], "max_features": [None], "max_leaf_nodes": [None]})

knn = "clf = KNeighborsClassifier(n_neighbors={n_neighbors}, weights='{weights}', algorithm='auto', leaf_size=30, p={p}, metric='minkowski', metric_params=None, n_jobs=1)"
createScripts("Classification", "sklearn_c_template", "knn", None, {"n_neighbors": neighborOptions, "weights": weightOptions, "p": pOptions})

lda = "clf = LinearDiscriminantAnalysis(solver='{solver}', shrinkage=None, priors=None, n_components=None, store_covariance=False, tol={tol})"
createScripts("Classification", "sklearn_c_template", "lda", None, {"solver": ["svd", "lsqr", "eigen"], "tol": [0.0001]})

logistic_regression = "clf = LogisticRegression(penalty='{penalty}', dual={dual}, tol={tol}, C={C}, fit_intercept=True, intercept_scaling=1, class_weight={class_weight}, solver='{solver}', max_iter={max_iter}, multi_class='{multi_class}', verbose=0, warm_start=False, n_jobs=1, random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "logistic_regression", None, {"penalty": ['l2', "l1"], "dual": [False, True], "tol": [0.0001], "C": cOptions, "class_weight": classWeightOptions, "solver": ['liblinear', 'newton-cg', 'lbfgs', 'sag'], "max_iter": [100], "multi_class": ['ovr']})

multilayer_perceptron = "clf = MLPClassifier(hidden_layer_sizes={hidden_layer_sizes}, activation='{activation}', solver='{solver}', alpha={alpha}, batch_size='auto', learning_rate='{learning_rate}', learning_rate_init=0.001, power_t=0.5, max_iter={max_iter}, shuffle=True, tol={tol}, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping={early_stopping}, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "multilayer_perceptron", None, {"hidden_layer_sizes": [(100, ), (200, ), (500, )], "activation": ['relu', 'identity', 'logistic', 'tanh'], "solver": ['adam', 'lbfgs', 'sgd'], "alpha": [0.0001], "learning_rate": ['constant', 'invscaling', 'adaptive'], "max_iter": [200], "tol": [0.0001], "early_stopping": [False, True]})

random_forest = "clf = RandomForestClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features='auto', max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, bootstrap={bootstrap}, oob_score={oob_score}, n_jobs=1, verbose=0, warm_start=False, class_weight={class_weight}, random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "random_forest", None, {"n_estimators": numEstimatorOptions, "criterion": treeCriterionOptions, "max_depth": [None], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_leaf_nodes": [None], "min_impurity_split": [1e-07], "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions, "class_weight": classWeightOptions})

sgd = "clf = SGDClassifier(loss='modified_huber', penalty='{penalty}', alpha={alpha}, l1_ratio=0.15, fit_intercept=True, n_iter={n_iter}, shuffle=True, verbose=0, epsilon={epsilon}, n_jobs=1, learning_rate='{learning_rate}', eta0=0.0, power_t=0.5, class_weight={class_weight}, warm_start=False, average=False, random_state=R_SEED)"
#loss='modified_huber' is required for probabilistic predictions
createScripts("Classification", "sklearn_c_template", "sgd", None, {"penalty": ['l2', 'l1', 'elasticnet'], "alpha": [0.0001], "n_iter": [5, 10, 20], "epsilon": [0.1], "learning_rate": ['optimal', 'constant', 'invscaling'], "class_weight": classWeightOptions})

svm = "clf = SVC(C={C}, kernel='{kernel}', degree=3, gamma='auto', coef0=0.0, shrinking={shrinking}, tol={tol}, cache_size=200, class_weight={class_weight}, verbose=False, max_iter=-1, decision_function_shape='ovr', probability=True, random_state=R_SEED)"
createScripts("Classification", "sklearn_c_template", "svm", None, {"C": cOptions, "kernel": ['rbf', 'linear', 'poly', 'sigmoid'], "shrinking": [True, False], "tol": [0.001], "class_weight": classWeightOptions})

## Failed tests: gaussian_naivebayes gaussian_process qda

#############################################################
# Feature selectors
#############################################################

anova = "F, score = f_classif(train_X, train_y)"
createScripts("FeatureSelection", "sklearn_f_template", "anova", "score", {})

mutual_info = "score = 1 - mutual_info_classif(train_X, train_y, n_neighbors={n_neighbors})"
createScripts("FeatureSelection", "sklearn_f_template", "mutual_info", "score", {"n_neighbors": [3]})

random_forest_rfe = "selector = RFE(RandomForestClassifier(n_estimators=50, random_state=R_SEED), n_features_to_select=1, step={step})"
createScripts("FeatureSelection", "sklearn_f_template", "random_forest_rfe", "rfe", {"step": [0.1]})

random_logistic_regression = "scorer = RandomizedLogisticRegression(C={C}, scaling={scaling}, sample_fraction={sample_fraction}, n_resampling={n_resampling}, selection_threshold={selection_threshold}, tol={tol}, fit_intercept=True, verbose=False, normalize=True, random_state=R_SEED)"
createScripts("FeatureSelection", "sklearn_f_template", "random_logistic_regression", "coef", {"C": [1], "scaling": [0.5], "sample_fraction": [0.75], "n_resampling": [200], "selection_threshold": [0.25], "tol": [0.001]})

svm_rfe = "selector = RFE(SVC(random_state=R_SEED, kernel='linear'), n_features_to_select=1, step={step})"
createScripts("FeatureSelection", "sklearn_f_template", "svm_rfe", "rfe", {"step": [0.1]})

## Failed tests: random_lasso