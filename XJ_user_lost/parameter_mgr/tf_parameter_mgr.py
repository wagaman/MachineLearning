import os
import sys
import tensorflow as tf

"""
Guides to use this module
1. Update dlpd.conf to add 'PARM_MGR_DIR' which is the path name where this module is located, 
   this py should be accessible(located at) to all the TF cluster hosts. 
2. Add 'PARM_MGR_DIR' into sys.path or PYTHONPATH before using this module,
   spark.executorEnv.PYTHONPATH can be used as a conf parameter in spark-submit command in spark runtime.
3. In the TF model py, add 'import tf_parameter_mgr' at the beginning and call its interfaces as tf_parameter_mgr.XXX. 
"""

#default parameter conf file name
PS_CONF="ps.conf"

#Optimizer options
Opt_GradientDescent = "GradientDescent"
Opt_Adadelta = "Adadelta"
Opt_Adagrad = "Adagrad"
Opt_AdagradDAt = "AdagradDA"
Opt_Momentum = "Momentum"
Opt_Adam = "Adam"
Opt_Ftrl = "Ftrl"
Opt_GroximalGradientDescent = "ProximalGradientDescent"
Opt_ProximalAdagrad = "ProximalAdagrad"
Opt_RMSProp = "RMSProp"

"""
Retrieve the configured base learning rate
"""
def getBaseLearningRate():
    return float(_readPropertyFromFile("base_lr", 0.01))

"""
If model defined any policy to decay learning rate, it can get the decay rate with this interface  
"""
def getLearningRateDecay():
    return float(_readPropertyFromFile("lr_decay_rate", 0.95))

"""
model can call this interface to retrieve the configured training batch_size 
"""
def getTrainBatchSize():
    return int(_readPropertyFromFile("batch_size"))

"""
model can call this interface to retrieve the configured test batch_size
"""
def getTestBatchSize():
    test_value = _readPropertyFromFile("test_batch_size")
    train_value = _readPropertyFromFile("batch_size")
    return test_value and int(test_value) or int(train_value)

"""
retrieve the training data set as a list
["/path/train_data1","/path/train_data2"]
"""
def getTrainData():
    return _readPropertyFromFile("train_data").split(",")

"""
retrieve the test data set as a list
["/path/test_data1","/path/test_data2"]
"""
def getTestData():
    return _readPropertyFromFile("test_data").split(",")

"""
retrieve the validation data set
["/path/val_data1","/path/val_data2"]
"""    
def getValData():
    return _readPropertyFromFile("val_data").split(",")

"""
Retrieve the configured max training steps
"""
def getMaxSteps():
    return int(_readPropertyFromFile("max_steps"))

"""
Retrieve the configured interval to run test phase
"""
def getTestInterval():
    value = _readPropertyFromFile("test_interval")
    return value and int(value) or 100

"""
model can call this interface to retrieve the optimizer with the configured parameters
"""
def getOptimizer(learning_rate):
    optimizer = _readPropertyFromFile("optimizer", "momentum")
    print("optimizer: " + optimizer)
    if optimizer == Opt_Momentum:
        return _getMomentumOptimizer(learning_rate)
    elif optimizer == Opt_Adadelta:
        return _getAdadeltaOptimizer(learning_rate)
    elif optimizer == Opt_Adagrad:
        return _getAdagradOptimizer(learning_rate)
    elif optimizer == Opt_AdagradDAt:
        return _getAdagradDAOptimizer(learning_rate)
    elif optimizer == Opt_Adam:
        return _getAdamOptimizer(learning_rate)
    elif optimizer == Opt_Ftrl:
        return _getFtrlOptimizer(learning_rate)
    elif optimizer == Opt_GroximalGradientDescent:
        return _getProximalGradientDescentOptimizer(learning_rate)
    elif optimizer == Opt_ProximalAdagrad:
        return _getProximalAdagradOptimizer(learning_rate)
    elif optimizer == Opt_RMSProp:
        return _getRMSPropOptimizer(learning_rate)
    else:
        return tf.train.GradientDescentOptimizer(learning_rate)

def _getMomentumOptimizer(learning_rate):
    #use_nesterov seems not support currently
    momentum = float(_readPropertyFromFile("momentum"))
    return tf.train.MomentumOptimizer(learning_rate, momentum)

def _getAdadeltaOptimizer(learning_rate):
    #opt_decay=0.95
    #epsilon=1e-08
    pMap = _readPropertiesFromFile(["opt_decay", "epsilon"])
    opt_decay = float(pMap.get("opt_decay", "0.95"))
    epsilon = float(pMap.get("epsilon", "1e-08"))
    return tf.train.AdadeltaOptimizer(learning_rate, rho=opt_decay, epsilon=epsilon)
 
def _getAdagradOptimizer(learning_rate):
    #accumulator=0.1
    accumulator=float(_readPropertyFromFile("accumulator", 0.1))
    return tf.train.AdagradOptimizer(learning_rate,initial_accumulator_value=accumulator)
 
def _getAdagradDAOptimizer(learning_rate):
    #accumulator=0.1
    #l1_regularization=0.0
    #l2_regularization=0.0
    global_step = tf.contrib.framework.get_or_create_global_step()
    pMap = _readPropertiesFromFile(["accumulator", "l1_regularization", "l2_regularization"])
    accumulator = float(pMap.get("accumulator", "0.1"))
    l1_regularization = float(pMap.get("l1_regularization", "0.0"))
    l2_regularization = float(pMap.get("l2_regularization", "0.0"))    
    return tf.train.AdagradDAOptimizer(learning_rate, global_step, initial_gradient_squared_accumulator_value=accumulator, l1_regularization_strength=l1_regularization, l2_regularization_strength=l2_regularization)

def _getAdamOptimizer(learning_rate):
    #beta1=0.9
    #beta2=0.999
    #epsilon=1e-08
    pMap = _readPropertiesFromFile(["beta1", "beta2", "epsilon"])
    beta1 = float(pMap.get("beta1", "0.9"))
    beta2 = float(pMap.get("beta2", "0.999"))
    epsilon = float(pMap.get("epsilon", "1e-08"))    
    return tf.train.AdamOptimizer(learning_rate, beta1=beta1, beta2=beta2, epsilon=epsilon)

def _getFtrlOptimizer(learning_rate):
    #lr_power=-0.5
    #accumulator=0.1
    #l1_regularization=0.0
    #l2_regularization=0.0
    pMap = _readPropertiesFromFile(["lr_power", "accumulator", "l1_regularization", "l2_regularization"])
    lr_power = float(pMap.get("lr_power", "-0.5"))
    accumulator = float(pMap.get("accumulator", "0.1"))
    l1_regularization = float(pMap.get("l1_regularization", "0.0"))
    l2_regularization = float(pMap.get("l2_regularization", "0.0"))       
    return tf.train.FtrlOptimizer(learning_rate, learning_rate_power=lr_power, initial_accumulator_value=accumulator, l1_regularization_strength=l1_regularization, l2_regularization_strength=l2_regularization)

def _getProximalGradientDescentOptimizer(learning_rate):
    #l1_regularization=0.0
    #l2_regularization=0.0
    pMap = _readPropertiesFromFile(["l1_regularization", "l2_regularization"])
    l1_regularization = float(pMap.get("l1_regularization", "0.0"))
    l2_regularization = float(pMap.get("l2_regularization", "0.0"))   
    return tf.train.ProximalGradientDescentOptimizer(learning_rate, l1_regularization_strength=l1_regularization, l2_regularization_strength=l2_regularization)

def _getProximalAdagradOptimizer(learning_rate):
    #accumulator=0.1
    #l1_regularization=0.0
    #l2_regularization=0.0
    pMap = _readPropertiesFromFile(["accumulator", "l1_regularization", "l2_regularization"])
    accumulator = float(pMap.get("accumulator", "0.1"))
    l1_regularization = float(pMap.get("l1_regularization", "0.0"))
    l2_regularization = float(pMap.get("l2_regularization", "0.0"))  
    return tf.train.ProximalAdagradOptimizer(learning_rate, initial_accumulator_value=accumulator, l1_regularization_strength=l1_regularization, l2_regularization_strength=l2_regularization)

def _getRMSPropOptimizer(learning_rate):
    #opt_decay=0.9
    #momentum=0.0
    #epsilon=1e-10
    pMap = _readPropertiesFromFile(["opt_decay", "momentum", "epsilon"])
    opt_decay = float(pMap.get("opt_decay", "0.1"))
    momentum = float(pMap.get("momentum", "0.0"))
    epsilon = float(pMap.get("epsilon", "1e-10"))  
    return tf.train.RMSPropOptimizer(learning_rate, decay=opt_decay, momentum=momentum, epsilon=epsilon)

def _readPropertyFromFile(key, default=None):
    
    """
    Here we assume that the parameters conf file located at the same directory as the model py itself
    The caller here should be the model py file name, we will first check if there is same name as model py conf file exists,
    if it does exists, we will load parameters from that file
    if it does not exists, we will load parameters from ps.conf located in the same directory
    """
    caller = sys.argv[0]
    fileName = sys.path[0] + "/" + caller.split(".")[0] + ".conf"
    if not os.path.exists(fileName):
        fileName = sys.path[0] + "/" + PS_CONF
    print("Read conf file %s" % fileName)
    
    separator = "="
    with open(fileName) as psFile:
        for line in psFile:
            if line.strip().startswith("#"):
                continue
            if separator in line:
                name, value = line.split(separator, 1)
                if name.strip() == key :
                    p_name = name.strip()
                    p_value = value.strip().replace("\"", "")
                    print("read %s = %s" %(p_name,p_value))
                    return p_value
    return default

def _readPropertiesFromFile(keys):
    map = {}
    caller = sys.argv[0]
    fileName = sys.path[0] + "/" + caller.split(".")[0] + ".conf"
    if not os.path.exists(fileName):
        fileName = sys.path[0] + "/" + PS_CONF
    
    separator = "="
    with open(fileName) as psFile:
        for line in psFile:
            if line.strip().startswith("#"):
                continue
            if separator in line:
                name, value = line.split(separator, 1)
                if name.strip() in keys :
                    p_name = name.strip()
                    p_value = value.strip().replace("\"", "")
                    print("read %s = %s" %(p_name,p_value))
                    map[p_name] = p_value
    return map

def _readBoolPropertyFroomFile(key, default=None):
    p_value = _readPropertyFromFile(key, default)
    if p_value is not None:
        if p_value.capitalize() == "True":
            return True 
        else:
            return False
    else:
        return default

"""
def readFloatPropertisFromFile(propertyMap):
    keys = propertyMap.keys()
"""

