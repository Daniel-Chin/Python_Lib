mywords = None
feature_length = None

def spread():
    f = open("spam_train.txt","r")
    f_validation = open("validation.txt","w")
    f_train = open("train.txt","w")
    n = 0
    while n < 1000:
        line = f.readline()
        f_validation.write(line)
        n +=1
    f_validation.close()
    while n>=1000:
        line = f.readline()
        n +=1
        if n == 1108 or n == 4185 or n == 4683:
            continue
        if len(line) == 0:
            break
        f_train.write(line)
    f_train.close()
    f.close()

def lst_of_samples(data):
    f = open(data,"r")
    lst_of_examples = []
    while True:
        line = f.readline().rstrip('\n')
        if len(line) == 0:
            break
        lst_of_examples.append(line.split(' '))
    f.close()
    return lst_of_examples

def words(data,X):
    lst0 = lst_of_samples(data)
    myset = set()
    for i in lst0:
        myset.update(i)
    lst1 = list(myset)
    dic={}
    for i in lst1:
        dic[i]=0
    lst_feature = []
    for email in lst0:
        for word in email:
            dic[word] += 1
    for word, times in dic.items():
        if times >= X:
            lst_feature.append(word)
    lst_feature.remove('1')
    lst_feature.remove('0')
    return lst_feature
 
"""...........................................................................................................................""" 
def feature_vector(email):
    lst_vector=[]
    email.split(' ')
    for i in mywords:
        if i in email:
            lst_vector.append(1)
        else:
            lst_vector.append(0)
    return lst_vector

def feature_data(lst):
    lst_vector=[]
    for i in mywords:
        if i in lst:
            lst_vector.append(1)
        else:
            lst_vector.append(0)
    return lst_vector


def perceptron_train(data):
    lst_samples_vector= []
    for i in lst_of_samples(data):
        if '1' in i:
            a = feature_data(i)
            a.append(1)
            lst_samples_vector.append(a)    
        else:
            a = feature_data(i)
            a.append(-1)
            lst_samples_vector.append(a)
    w = []
    n = 0
    while n < feature_length:
        w.append(0)
        n += 1
    k = 0
    iteration = 0
    while True:
        iteration +=1
        print(iteration)
        mark = 0
        for i in lst_samples_vector:
            tem = 0
            for j in range(feature_length):
                tem += w[j]*i[j]
            a = i[feature_length]*tem
            if a > 0:
                w = w
            else:
                for j in range(feature_length):
                    w[j] = int(w[j]) + int(i[feature_length])*int(i[j])
                    mark += 1
        if mark == 0:
            break
        else:
            k += mark
            continue
    return w,k,iteration
    print(w,k,iteration)

def perceptron_error(w,data_test):
    marker = 0
    lst_samples_vector= []
    for i in lst_of_samples(data_test):
        if '1' in i:
            a = feature_data(i)
            a.append(1)
            lst_samples_vector.append(a)
        else:
            a = feature_data(i)
            a.append(-1)
            lst_samples_vector.append(a)

    for i in lst_samples_vector:
        tem = 0
        for j in range(feature_length):
            tem += w[j]*i[j]
        a = i[feature_length]*tem
        if a > 0:
            marker =marker
        else:
            marker += 1
    error = marker/len(lst_samples_vector)
    return error

def main():
	global mywords, feature_length
	spread()
	X = int(input('please input the number determine the feature of data'))
	training_data = input('please input the training data')
	validation_data = input('please input the validation data')
	mywords = words(training_data,X)
	feature_length = len(mywords)
	print(feature_length)
	training_result = perceptron_train(training_data)
	w = training_result[0]
	k = training_result[1]
	iter = training_result[2]
	print('the total update number is',k)
	print('the total iteration is',iter)
	training_error = perceptron_error(w,training_data)
	print('the perceptron error of training data is',training_error)
	validation_error = perceptron_error(w,validation_data)
	print('the perceptron error of validation data is', validation_error)

main()
