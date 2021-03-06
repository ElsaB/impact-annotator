# ggplot tools
###################################################################################

# tilt the x labels by 45 degrees on any plot
tilt_x_label_45 <- function() {
    return (theme(axis.text.x = element_text(angle = 45, hjust = 1)))
}


# set the size of the plot in jupyter notebook
notebook_plot_size <- function(width = 6, height = 3) {
    options(repr.plot.width = width, repr.plot.height = height)
}


# plot two plots side-by-side
plot_side_by_side <- function(plot1, plot2, width = 10, height = 2) {
    notebook_plot_size(width, height)

    grid.arrange(plot1, plot2, ncol = 2)
}


# plot three plots side-by-side
plot_side_by_side_3 <- function(plot1, plot2, plot3, width = 10, height = 3) {
    notebook_plot_size(width, height)

    grid.arrange(plot1, plot2, plot3, ncol = 3)
}


# sort a categorical feature over the count of the categories it contains (ie sort the associated histogram)
sort_histogram <- function(data, feature_name, reverse = FALSE) {

    if (!reverse) {
        data[, feature_name] <- factor(data[, feature_name], levels = names(rev(sort(table(data[, feature_name])))))
    }
    else {
        data[, feature_name] <- factor(data[, feature_name], levels = names(sort(table(data[, feature_name]))))
    }

    return (data)
}


# plot two histograms side-by-side to study the contingency table between two features
plot_contingency_table_as_histograms <- function(data, feature_x_name, feature_y_name, width = 10, height = 3, flip = FALSE) {
    
    data <- sort_histogram(data, feature_x_name, reverse = flip)
    data <- sort_histogram(data, feature_y_name, reverse = TRUE)

    plot1 <- ggplot(data) + geom_bar(aes_string(x = feature_x_name, fill = feature_y_name), show.legend = FALSE) +
                                                    tilt_x_label_45()
    plot2 <- ggplot(data) + geom_bar(aes_string(x = feature_x_name, fill = feature_y_name), position = "fill") +
                                                    tilt_x_label_45() + labs(y = "frequency")

    if (flip) {
        plot1 <- plot1 + coord_flip()
        plot2 <- plot2 + coord_flip() + theme(axis.title.y = element_blank(), axis.text.y = element_blank(), axis.ticks.y=element_blank())
    }

    plot_side_by_side(plot1, plot2, width, height)                             
}


# plots three histograms side-by-side showing the distribution of the features confidence_class, Variant_Type and Consequence for the given dataset
# also prints the number of unique genes in the given dataset
get_possible_correlations <- function(data) {
        print(paste("Number of different genes: ", toString(length(unique(data$Hugo_Symbol)))))
                
        data <- sort_histogram(data, "confidence_class")
        plot1 <- ggplot(data) + geom_bar(aes(confidence_class)) + tilt_x_label_45()
        
        data <- sort_histogram(data, "Variant_Type")
        plot2 <- ggplot(data) + geom_bar(aes(Variant_Type))
        
        data <- sort_histogram(data, "Consequence")
        plot3 <- ggplot(data) + geom_bar(aes(Consequence)) + tilt_x_label_45()

        plot_side_by_side_3(plot1, plot2, plot3, 10, 3)
}


# custom density plot
plot_density <- function(data, feature_name, fill_feature_name = NULL, adjust = 1, width = 10, height = 3, lines = NULL) {
        notebook_plot_size(width, height)
                                                         
        plot <- ggplot(data) + geom_density(aes_string(feature_name, fill = fill_feature_name), adjust = adjust, alpha = 0.2) +
                                                     scale_fill_manual(values = c("blue", "green", "red", "yellow"))
        
        for (value in lines)
                plot <- plot + geom_vline(aes_(xintercept = value), linetype = "dashed", color = "red")
                
        return (plot)
}


# custom histogram plot
plot_histogram <- function(data, feature_name, fill_name = NULL, width = 10, height = 3, flip = FALSE) {
    notebook_plot_size(width, height)

    if (flip)
        data <- sort_histogram(data, feature_name, reverse = TRUE)
    else
        data <- sort_histogram(data, feature_name)

    plot <- ggplot(data) + geom_bar(aes_string(feature_name, fill = fill_name))

    if (flip)
        plot <- plot + coord_flip()
    
    return (plot)
}


# plot the top maximum values of an histogram, the argument number regulates the number of values plotted
plot_histogram_top <- function(data, feature_name, number, width = 10, height = 3) {
    notebook_plot_size(width, height)
    
    data_top <- as.data.frame(rev(sort(table(data[,feature_name])))[1:number])
    colnames(data_top) <- c("feature", "count")
    return (ggplot(data_top) + geom_col(aes(feature, count)) + xlab(feature_name))
}


# custom density 2d plot
plot_density_2d <- function(data, x_name, y_name, width = 12, height = 4, to_add = NULL, points_only = FALSE) {
    notebook_plot_size(width, height)
        
    data$density <- densCols(data[,x_name], data[,y_name], colramp = colorRampPalette(rev(rainbow(10, end = 4/6))))

    plot1 <- ggplot(data) + geom_point(aes_string(x_name, y_name, color = "density"), alpha = 0.1) +
                     scale_color_identity() + to_add

    if (points_only)
        return (plot1)
    
    plot2 <- ggplot(data) + geom_hex(aes_string(x_name, y_name)) +
                     scale_fill_gradient(low = "#FFEDA0", high = "#F03B20") + theme(legend.position = "none") + to_add
    plot3 <- ggplot(data) + stat_density_2d(aes_string(x_name, y_name, fill = "..level.."), geom = "polygon") +
                     scale_fill_gradientn(colors = c("#FFEDA0", "#FEB24C", "#F03B20")) + theme(legend.position = "none") + to_add
        
    plot_side_by_side_3(plot1, plot2, plot3, width, height)
}
