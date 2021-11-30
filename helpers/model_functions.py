

def feature_engineering_pipeline(df,py_library,func_list):

    df_model = df

    for func in func_list:

        method_to_call = getattr(py_library, func[0])

        df_model = df_model.pipe(method_to_call,*func[1:])

        print("Feature Engineering","(",func[0],func[1],")","Complete")

    return df_model


def split_dataset(df,train_size=0.80,target="target_COV"):

    X = df[[col for col in df.columns if col != target]]

    y = df[target]

    X_train,X_test,y_train,y_test = tts(X.to_numpy(),y.to_numpy(),random_state=random_state,train_size=train_size)

    print("Split Dataset into","Train_size =",train_size,"Test_size = ",1-train_size)

    return X,y,X_train,X_test,y_train,y_test
  
def parameter_intersection(pipeline=[]):

  common_parameters = list()

  for model in pipeline:

      common_p = set(model.get_params().keys())

      common_parameters.append(common_p)

  # finds the intersection of all set of params
  return set.intersection(*common_parameters)

warnings.filterwarnings("ignore")

def get_linear_model_hp(key):

    linear_model_hp = {"G1":{'alpha':[0,0.5,1],'max_iter':[300,400,500], 'tol':[1e-7]},
                    "G2":{"cv":[3]},
                    "G3":{'alpha_1':[1e-3,1e-6,1e-9],
                            'alpha_2':[1e-3,1e-6,1e-9],
                            'lambda_1':[1e-3,1e-6,1e-9],
                            'lambda_2':[1e-3,1e-6,1e-9],
                            'n_iter':[100,300,500,700],
                            'tol':[1e-7],
                        },
                    "G4":{
                        'max_iter':[300,400,500],
                        'max_subpopulation':[1e2,1e4,1e6],
                        'n_subsamples':[None,8,16,24,32],
                        'random_state':[random_state],
                        'tol':[1e-7],
                        }
                    
                    }

    return linear_model_hp[key]


def get_ensemble_model_hp(key):

    ensemble_models_hp = {
                    "Trees":{'bootstrap':[False],
                                    'ccp_alpha':[0],
                                    'criterion':["squared_error"],
                                    'max_depth':[10,50,100,200],
                                    'max_features':[None],
                                    'max_leaf_nodes':[20,50,100,200],
                                    'max_samples':[None],
                                    'min_impurity_decrease':[0],
                                    'min_samples_leaf':[1,24,48,64],
                                    'min_samples_split':[1,24,48,64],
                                    'min_weight_fraction_leaf':[0],
                                    'n_estimators':[100,200,300],
                                    'n_jobs':[None],
                                    'oob_score':[False],
                                    'random_state':[random_state]},
                        
                    "Boosting":{'learning_rate':[0.1,0.01,0.001,0.0001],
                                    'loss':["squared_error"],
                                    'max_depth':[10,50,100,200,400,1000],
                                    'max_leaf_nodes':[None],
                                    'min_samples_leaf':[20],
                                    'n_iter_no_change':[10],
                                    'random_state':[random_state],
                                    'tol':[1e-7],
                                    'validation_fraction':[0.1]}#default
                    }

    return ensemble_models_hp[key]


def get_linear_models():

    linear_models = [
            #LinearRegression(),
            #G1
            # (Ridge(),get_linear_model_hp("G1")),
            # (Lasso(),get_linear_model_hp("G1")),
            # (ElasticNet(),get_linear_model_hp("G1")),
            # (HuberRegressor(),get_linear_model_hp("G1")),
            
            # #G2
            # (RidgeCV(cv=5),get_linear_model_hp("G2")),
            # (LassoCV(cv=5),get_linear_model_hp("G2")),
            # (ElasticNetCV(cv=5),get_linear_model_hp("G2")),
            # (LarsCV(cv=5),get_linear_model_hp("G2")),
            # (LassoLarsCV(cv=5),get_linear_model_hp("G2")),

            # #G3
            # (BayesianRidge(),get_linear_model_hp("G3")),
            (ARDRegression(),get_linear_model_hp("G3")),
            

            #G4
            (TheilSenRegressor(),get_linear_model_hp("G4")),
             
    ]

           
            #G5 - Not included
            # SGDRegressor(),
            # PassiveAggressiveRegressor(),
            
            
            # #G6
            # (Lars(),
            # LassoLarsIC(criterion="bic")

    return ("Linear",linear_models)

def get_ensemble_models():

    ensemble_models = [
                    #Tree
                    (ExtraTreesRegressor(),get_ensemble_model_hp("Trees")),
                    (RandomForestRegressor(),get_ensemble_model_hp("Trees")),
                    #Boosting
                    (HistGradientBoostingRegressor(),get_ensemble_model_hp("Boosting")),
                    (GradientBoostingRegressor(),get_ensemble_model_hp("Boosting"))


                    #Regressor - Used with other models like a wrapper
                    # BaggingRegressor(random_state=random_state),
                    # AdaBoostRegressor(random_state=random_state), 
                    
                    

                    ]

    return ("Ensemble",ensemble_models)


def get_svm_models():

    svm_models = [#G1
                  LinearSVR(),

                  #G2
                  NuSVR(),
                  SVR()
                ]

    return ("SVM",svm_models)

def get_neptune_key(username):

    with open("creds/creds.json","r") as f:

        api_token = json.load(f)["Users"][username]["neptune_key"]

    return api_token
  
 def plot_test_train(X_train,X_test,y_train,y_test):


    _ = plt.plot(range(X_train.shape[0]),y_train,label="Train")
    _ = plt.plot(range(X_train.shape[0],X_train.shape[0] +X_test.shape[0]),y_test,label="Test")
    _ = plt.title("Test Train Split")
    _ = plt.yscale("log")

    return _

def print_header(header_name): 
    print("--------"*8)
    print(header_name)
    
