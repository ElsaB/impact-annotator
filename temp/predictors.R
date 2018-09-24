
#install.packages("class")
library("class")

#install.packages("e1071")
library("e1071")

#install.packages("C50")
library("C50")

#install.packages("RWeka")
library("RWeka")

#install.packages("neuralnet")
library("neuralnet")


remove_features <- function(data, features_name) {
	return (data[, ! colnames(data) %in% features_name])
}

transform_categorical_features_to_factor <- function(data, features_name) {
	for (feature in features_name)
		data[, feature] <- factor(data[, feature])

	return (data)
}

transform_categorical_features_to_integer <- function(data, features_name) {
	for (feature in features_name)
		data[, feature] <- as.integer(factor(data[, feature]))

	return (data)
}

# min-max normalization
min_max_normalize <- function(data, features_name) {
	data[, features_name] <- lapply(data[, features_name], function(x) ((x - min(x)) / (max(x) - min(x))))

	return (data)
}

shuffle_rows <- function(data) {
	return (data[sample(nrow(data)),])
}

split_train_test <- function(data, label_name) {

	split_value <- nrow(data) * 3 / 4

	data_train <- data[1 : split_value,]
	data_test  <- data[(split_value + 1) : nrow(data),]

	data_train_label <- data_train[, label_name]
	data_test_label  <- data_test[, label_name]

	data_train <- remove_features(data_train, label_name)
	data_test <- remove_features(data_test, label_name)

	return (list(data_train, data_test, data_train_label, data_test_label))
}

get_result_table <- function(data_test_label, data_test_pred) {
	return (table(data_test_label, data_test_pred))
}

get_accuracy <- function(data_test_label, data_test_pred) {

	result_table <- get_result_table(data_test_label, data_test_pred)

	return (sprintf("%.2f%%", 100 * (result_table[1] + result_table[4]) / length(data_test_label)))
}

model_knn <- function(data_train, data_test, data_train_label, k) {
	return (knn(train = data_train, test = data_test, cl = data_train_label, k = k))
}





