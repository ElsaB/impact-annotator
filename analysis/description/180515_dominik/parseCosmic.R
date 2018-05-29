parseCosmic <- function(impact.ann.df) {

	ss <- mapply(strsplit, impact.ann.df$cosmic70, ';OCCURENCE=')
	for (si in 1:length(ss)) {
	cosmicCount <- 0
    	if (ss[[si]][[1]]!='.') {
        	# if found is cosmic
        	cosmicStr <- ss[[si]][[2]]
        #print(cosmicStr)
        	cosNumbers <- strsplit( cosmicStr, ',' )
        #print(cosNumbers)
	        cosInts <- mapply(strsplit, cosNumbers, '\\(')

    	    for (ci in 1:length(cosInts)) {
        	    cosInt <- as.integer(cosInts[[ci]][[1]])
            	cosmicCount <- cosmicCount + cosInt
        	}	
        		
    	}
	impact.ann.df$cosmicCount[si]  <- cosmicCount   

	}
	return(impact.ann.df)     
}