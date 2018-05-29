toPyr <- function(nctds) {
    nctds.pyr <- nctds
    nctds.pyr[nctds=='A'] <- 'T'
    nctds.pyr[nctds=='T'] <- 'A'
    nctds.pyr[nctds=='G'] <- 'C'
    nctds.pyr[nctds=='C'] <- 'G'
    as.character(nctds.pyr)
}


plotSignature <-function(subs.df, mut.order, main='') {
	subs.df$bb <- substr(subs.df$triplets,1,1)
	subs.df$ba <- substr(subs.df$triplets,3,3)
	subs.df$isPyr <- subs.df$Reference_Allele %in% c('C', 'T')
	subs.df$candi <- ''
	subs.df$candi <- paste0(subs.df$bb,'[', subs.df$Reference_Allele,'>',subs.df$Tumor_Seq_Allele2,']', subs.df$ba )
	subs.df$candi[!subs.df$isPyr] <- paste0(toPyr(subs.df$ba[!subs.df$isPyr]),
                                        '[', toPyr(subs.df$Reference_Allele[!subs.df$isPyr]),'>',
                                        toPyr(subs.df$Tumor_Seq_Allele2[!subs.df$isPyr]),']', 
                                        toPyr(subs.df$bb[!subs.df$isPyr]))
                                        
    b <- table(subs.df$candi)
    b <- b[ as.character(mut.order)]		
    b[is.na(b)] <- 0	
    barplot(b, col=c(rep('royalblue',16), rep('black',16), rep('red', 16), rep('grey', 16), rep('green2', 16), rep('hotpink',16)),
    main=paste(nrow(subs.df$muts),'substitutions', main), las=2, border=NA, cex.axis=0.5, cex.names=0.4)
	return(b)
}