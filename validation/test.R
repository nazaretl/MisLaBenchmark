shhh <- suppressPackageStartupMessages
shhh(library('NoiseFiltersR'))
#library('NoiseFiltersR')

library(data.table)

# paramaters are taken from pakage recommendations, not tested 
k = 4
nfolds = 4
noiseThreshold = 0.2
N = 20 

noise <- snakemake@wildcards[['noise']]
model <- snakemake@wildcards[['model']]
dataset <- snakemake@wildcards[['dataset']]

output1 <- snakemake@output[[1]]
output = paste(dataset,'_predictions.csv', sep='')

input1 <- snakemake@input[[1]]
input2 <- snakemake@input[[2]]

n = 10000 # if df has less instances the max is read in

df = read.csv(file = input1, sep = '\t', nrows = n, header = FALSE)
noisyLabels = read.csv(file =input2, sep = '\t', nrows = n)    

X = df[,1:(ncol(df)-1)]
df = X

col=paste('X',noise,sep = '')
labels = factor(noisyLabels[,col])

df$labels = labels
# the model string looks like this 'BBNR(df, k = k)' which is evaluated with 'eval'
out = tryCatch({
        toString(eval(parse(text = model))$remIdx)}, 

            error = function(e){
                        message('Caught an error!')
                        message(e)
                return('failed!')
                               })

out = c(model,noise,out)
out = data.frame(out)
out = transpose(out)
# written to a temp file (for snakemake) and appended to a predictions file
write.table(out, file = output, append = TRUE, quote = FALSE, sep = "\t", eol = "\n", na = "NA", dec = ".", row.names = FALSE, col.names = FALSE, qmethod = c("escape", "double"))

write.csv(out, output1)
