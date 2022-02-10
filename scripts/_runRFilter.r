



### PRISM functions
cld <- function(i,data,classColumn){
  classes <- unique(data[,classColumn])
  probs <- sapply(classes,function(cl){
    thisClass <- data[,classColumn]==cl
    sapply(setdiff(1:ncol(data),classColumn),function(att){
      if(is.factor(data[,att]) | is.logical(data[,att])){
        sum(data[thisClass,att]==data[i,att])/sum(thisClass)
      }
      else{
        m <- mean(data[thisClass,att])
        d <- stats::sd(data[thisClass,att])
        stats::dnorm(data[i,att], mean = m, sd = d)
      }
    })
  })
  probsPerClass <- apply(probs,2,prod)
  classIdx <- which(classes==data[i,classColumn])
  probsPerClass[classIdx]-max(probsPerClass[-classIdx])
}


dn <- function(i,data,classColumn){
  class <- as.character(data[i,classColumn])
  form <- as.formula(paste(names(data)[classColumn],"~.",sep=""))
  nn <- kknn::kknn(formula = form,
    train = data[-i,],
    test = data[i,],
    k = 17,
    kernel = "rectangular")$CL
  dns <- sapply(1:17,function(i){
    sum(nn[1:i]!=class)/i
  })
  mean(dns)
}

dcp <- function(i,data,classColumn){
  form <- as.formula(paste(names(data)[classColumn],"~.",sep=""))
  tree <- RWeka::J48(form,data)
  probs <- predict(tree,data[i,],type="probability")
  probs[1,colnames(probs)==data[i,classColumn]]
}

ds <- function(i,data,classColumn){
  equalities <- apply(data,1,function(x){
    all(x==data[i,])
  })
  sum(equalities)-1
}



shhh <- suppressPackageStartupMessages
#shhh(library('NoiseFiltersR'))
library('NoiseFiltersR')

shhh(library('caret'))

runRFilters<- function(string, df) {
        
        X = df[,1:(ncol(df)-1)]
      #  X = Filter(function(x)(length(unique(x))>1), X)
        noisyLabels = factor(df[,ncol(df)])
      
        df = X
        df$labels = noisyLabels
        k = 4
        nfolds = 4
        noiseThreshold = 0.2
        N = 20 
        #sink("/dev/null")
       # out = 'failed' 
        
    
out = eval(parse(text = string))$remIdx
               
                   
                   
    
     #   message(out)
               
          #  b  = Sys.time()
           # c = as.numeric(difftime(b, a), units = "secs")
           
       #     res = list(getCM(y, noisyLabels,out))
          #  li = append(li,c(out$remIdx))
          
    return (out)
}

df = read.csv(file = 'test/test.csv', sep = '\t',nrows = 10)
X = df[,1:(ncol(df)-1)]
#  X = Filter(function(x)(length(unique(x))>1), X)
noisyLabels = factor(df[,ncol(df)])

df = X
df$labels = noisyLabels
x = df
classColumn=ncol(x)
#i = x[1:1,]
#cld(i,x,classColumn)>=0

#print(head(df,4))



cld <- function(i,data,classColumn){
  classes <- unique(data[,classColumn])
    print(classes)
  probs <- sapply(classes,function(cl)
                  {
    thisClass <- data[,classColumn]==cl
    sapply(setdiff(1:ncol(data),classColumn),function(att){
      if(is.factor(data[,att]) | is.logical(data[,att])){
        sum(data[thisClass,att]==data[i,att])/sum(thisClass)
      }
      else{
          
        m <- mean(data[thisClass,att])
        s = sd(data[thisClass,att])
        #s = NA
        if (is.na(s)){
              d ='1'
        }else{
            d=s}
          bb = d
          print(bb)
        stats::dnorm(data[i,att], mean = m, sd =bb)
      }
    })
  })
    
  probsPerClass <- apply(probs,2,prod)
  classIdx <- which(classes==data[i,classColumn])
  probsPerClass[classIdx]-max(probsPerClass[-classIdx])
}

for (i in 1:1){
    print(i)
    print(cld(i,x,classColumn))
                   }

#sapply(1:nrow(x),function(i){
 #   if(dn(i,x,classColumn)>0.8){
 #     return(TRUE)
 #   }
#    if(cld(i,x,classColumn)>=0){
#      return(FALSE)
#    }
#    if(dcp(i,x,classColumn)>=0.5){
#      return(FALSE)
#    }
#    if(ds(i,x,classColumn)==0){
#      return(TRUE)
#    }
#    return(FALSE)
#  })

#str(df)
#runRFilters("PRISM(df)", df)
#classColumn = nrows(df)
#cld(i, x, classColumn)