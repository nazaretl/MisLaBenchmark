print(gc(reset = TRUE))
options(java.parameters = "-Xmx100000m")
shhh <- suppressPackageStartupMessages
shhh(library('NoiseFiltersR'))
#library('NoiseFiltersR')

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
        li = list()
        #sink("/dev/null")
       # out = 'failed' 
        out = eval(parse(text = string))$remIdx
                      
    
#out = tryCatch({
#            eval(parse(text = string))$remIdx}, 
#                       
#                error = function(e){
#                            message('Caught an error!')
#                            message(e)
#                    return(paste('failed!',e,sep = ' '))
#                                   })
                   
                   
    
     #   message(out)
               
          #  b  = Sys.time()
           # c = as.numeric(difftime(b, a), units = "secs")
           
       #     res = list(getCM(y, noisyLabels,out))
          #  li = append(li,c(out$remIdx))
          
    return (out)
}
#runRFilters<- function(string, df) {
#    x = invisible(runRFilters0(string, df))
#                  return (x)
#}