#引入yinru引入引入huanjingbianliang
Sys.setenv(HADOOP_CMD="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/bin/hadoop")
Sys.setenv(HADOOP_STREAMING="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar")
Sys.setenv(JAVA_LIBRARY_PATH="/opt/cloudera/parcels/CDH/lib/hadoop/lib/native")
Sys.setenv(HADOOP_HOME="/opt/cloudera/parcels/CDH-5.3.3-1.cdh5.3.3.p0.5")


#set the memory ()
options(java.parameters = "-Xmx5120m")
.jinit(parameters="-Xmx5120m")


# Fits a Random Forest to the Bulldozer data via Hadoop

library(rmr2)
library(randomForest)
library(rhdfs)
library(rJava)
hfds.init()

# PARAM
# A great advantage of RHadoop is that the R environment I'm defining here will be
# packaged and distributed to each mapper/reducer, so there is no need to mess with
# Hadoop configuration variables or distributed cache
frac.per.model <- 0.1
num.models <- 50

# here we manually set the schema for the input data
# printed with dput(names(training.data))
column.names <- c("MachineID", "SalePrice", "ModelID.x", "datasource", "auctioneerID", 
                  "YearMade", "MachineHoursCurrentMeter", "UsageBand", "saledate", 
                  "fiModelDesc.x", "fiBaseModel.x", "fiSecondaryDesc.x", "fiModelSeries.x", 
                  "fiModelDescriptor.x", "ProductSize", "fiProductClassDesc.x", 
                  "state", "ProductGroup.x", "ProductGroupDesc.x", "Drive_System", 
                  "Enclosure", "Forks", "Pad_Type", "Ride_Control", "Stick", "Transmission", 
                  "Turbocharged", "Blade_Extension", "Blade_Width", "Enclosure_Type", 
                  "Engine_Horsepower", "Hydraulics", "Pushblock", "Ripper", "Scarifier", 
                  "Tip_Control", "Tire_Size", "Coupler", "Coupler_System", "Grouser_Tracks", 
                  "Hydraulics_Flow", "Track_Type", "Undercarriage_Pad_Width", "Stick_Length", 
                  "Thumb", "Pattern_Changer", "Grouser_Type", "Backhoe_Mounting", 
                  "Blade_Type", "Travel_Controls", "Differential_Type", "Steering_Controls", 
                  "saledatenumeric", "ageAtSale", "saleYear", "saleMonth", "saleDay", 
                  "saleWeekday", "MedianModelPrice", "ModelCount", "ModelID.y", 
                  "fiModelDesc.y", "fiBaseModel.y", "fiSecondaryDesc.y", "fiModelSeries.y", 
                  "fiModelDescriptor.y", "fiProductClassDesc.y", "ProductGroup.y", 
                  "ProductGroupDesc.y", "MfgYear", "fiManufacturerID", "fiManufacturerDesc", 
                  "PrimarySizeBasis", "PrimaryLower", "PrimaryUpper")

# here we pick the actual variables to use for building the model
# note that randomForest doesn't like missing data, so we'll just
# nix some of those variables
# TODO
model.formula <- SalePrice ~ datasource + auctioneerID + YearMade + saledatenumeric + ProductSize +
                               ProductGroupDesc.x + Enclosure + Hydraulics + ageAtSale + saleYear +
                               saleMonth + saleDay + saleWeekday + MedianModelPrice + ModelCount +
                               MfgYear
# target <- "SalePrice"
# predictors <- c("datasource", )

# here's a helper function to parse the input text data into a data frame
parse.raw <- function(raw) {
  read.table(textConnection(raw),
             header=FALSE,
             sep=",",
             quote="\"",
             row.names=NULL,
             col.names=column.names,
             fill=TRUE,
             na.strings=c("NA"),
             colClasses=c(MachineID="NULL",
                          SalePrice="numeric",
                          YearMade="numeric",
                          MachineHoursCurrentMeter="numeric",
                          ageAtSale="numeric",
                          saleYear="numeric",
                          ModelCount="numeric",
                          MfgYear="numeric",
                          ModelID.x="factor",
                          ModelID.y="factor",
                          fiManufacturerID="factor",
                          datasource="factor",
                          auctioneerID="factor",
                          saledatenumeric="numeric",
                          saleDay="factor",
                          Stick_Length="numeric"))
}

# MAP function
poisson.subsample <- function(k, v) {
  # parse data chunk into data frame
  # raw is basically a chunk of a csv file
  raw <- paste(v, sep="\n")
  # convert to data.frame using read.table() in parse.raw()
  input <- parse.raw(raw)
  
  # this function is used to generate a sample from the current block of data
  generate.sample <- function(i) {
    # generate N Poisson variables
    draws <- rpois(n=nrow(input), lambda=frac.per.model)
    # compute the index vector for the corresponding rows,
    # weighted by the number of Poisson draws
    indices <- rep((1:nrow(input))[draws > 0], draws[draws > 0])
    # emit the rows; RHadoop takes care of replicating the key appropriately
    # and rbinding the data frames from different mappers together for the
    # reducer
    keyval(rep(i, length(indices)), input[indices, ])
  }
  
  # here is where we generate the actual sampled data
  raw.output <- lapply(1:num.models, generate.sample)
  
  # and now we must reshape it into something RHadoop expects
  output.keys <- do.call(c, lapply(raw.output, function(x) {x$key}))
  output.vals <- do.call(rbind, lapply(raw.output, function(x) {x$val}))
  keyval(output.keys, output.vals)
}

# REDUCE function
fit.trees <- function(k, v) {
  # rmr rbinds the emited values, so v is a dataframe
  # note that do.trace=T is used to produce output to stderr to keep
  # the reduce task from timing out
  rf <- randomForest(formula=model.formula, data=v, na.action=na.roughfix, ntree=10, do.trace=TRUE)
  # rf is a list so wrap it in another list to ensure that only
  # one object gets emitted. this is because keyval is vectorized
  keyval(k, list(forest=rf))
}

hdfs.ls('./')
# put the file training.csv to hfds
hdfs.put('./rf_rhadoop_demo/training.csv','/user/yimr/Rhadoop/test/training.csv')
hdfs.ls('/user/yimr/Rhadoop/test/')

#make the directory of hdfs output
hdfs.mkdir('/user/yimr/Rhadoop/output')
# new the dir,the mapreduce error:Output directory hdfs://cdh2:8020/user/yimr/Rhadoop/output already exists
hdfs.delete('/user/yimr/Rhadoop/output')

# input = '/user/yimr/Rhadoop/test/training.csv'

mapreduce(input="/user/yimr/Rhadoop/test/training.csv",
               input.format="text",
               map=poisson.subsample,
               reduce=fit.trees,
               output="/user/yimr/Rhadoop/output")

raw.forests <- from.dfs("/user/yimr/Rhadoop/output")[["val"]]
forest <- do.call(combine, raw.forests)

