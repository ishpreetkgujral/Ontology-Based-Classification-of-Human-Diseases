# -*- coding: utf-8 -*-
"""Demov2 Ontology Based Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LbN5wAeIlmU6cAbkpfzx4fOCFb-ncnxB
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import csv,nltk
# nltk.download()
!python -m nltk.downloader all
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import  pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from operator import itemgetter, attrgetter

from sklearn.feature_extraction.text import CountVectorizer
from numpy import array
import string
from numpy import array
import random
from math import floor
from collections import OrderedDict
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

def dataset_creation():
    disease_symptom_dict = defaultdict(list)
    with open('Final_Dataset.csv','r',encoding='utf-8') as csvFile:
      reader=csv.reader(csvFile)
      data=list(reader)
    csvFile.close()
    keywords=[]
    # print(len(data))
    for i in range(1,len(data)):
      # print(i,'Entity:'+data[i][0])
      data[i][0].replace('\xa0',' ')
      # print('Keywords:'+data[i][1])
      # print('Additional Keywords:'+data[i][2])
      for j in range(0,len(data[i][1])):
        data[i][1][j].replace('\xa0',' ')
      keywords=data[i][1].split(',')
      # print(keywords)
      disease_symptom_dict[str(data[i][0]).strip()].append(keywords)
    # print(len(disease_symptom_dict))
    x = []
    y = []
    for i in disease_symptom_dict:
        y.append(i)
        x.append(disease_symptom_dict[i][0])
    temp = []
    for i in x:
        for j in i:
            temp.append(j)

    from collections import OrderedDict
    temp = list(OrderedDict((x, True) for x in temp).keys())
    for i in range(len(y)):
      for j in range(150):
          y.append(y[i])
          x.append(random.sample(x[i],floor(len(x[i])/3)))
    x_ = []
    for i in x:
      x_.append(' '.join(i))
    return x_,y

# data_x,data_y=dataset_creation()
# data_x

class cleaning_nlp_processes:

    def __init__(self,description):
        self.description=description

    def same_frequency_words_priority(self,word_list):
        final_list=[]
        parts_of_speech = self.parts_of_speech()
        for i in range(0,len(word_list)):
            words = self.lemmatization(parts_of_speech, [word_list[i][0]])
            if len(words)==0 or word_list[i][0]==words[0]:
                # print(words,word_list[i],"Flag=1")
                final_list.append((word_list[i][0],word_list[i][1],1))
            else:
                # print(words,word_list[i]," Flag=0")
                final_list.append((word_list[i][0],word_list[i][1],0))
        return final_list


    def priority_provide(self, stop_words_remove,freq_dict):
        final_priority_list=[]
        print(freq_dict)
        import operator
        sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1),reverse=True)
        import collections
        sorted_dict = dict(collections.OrderedDict(sorted_x))
        sorted_list = [(k, v) for k, v in sorted_dict.items()]
        print(sorted_list)
        splice_index=[]
        for i in range(1,len(sorted_list)):
            if sorted_list[i-1][1]==sorted_list[i][1]:
                continue
            else:
                splice_index.append(i)
        print(splice_index)
        if len(splice_index)==0:
            final_priority_list=self.same_frequency_words_priority(sorted_list)

        elif len(splice_index)==1:
            list_1=(sorted_list[:splice_index[0]])
            list_2=(sorted_list[splice_index[0]:])
            final_priority_list = self.same_frequency_words_priority(list_1)
            final_priority_list += self.same_frequency_words_priority(list_2)

        else:
            list_1=(sorted_list[:splice_index[0]])
            final_priority_list=self.same_frequency_words_priority(list_1)

            for i in range(1,len(splice_index)):
                list_i=(sorted_list[splice_index[i-1]:splice_index[i]])
                final_priority_list+=self.same_frequency_words_priority(list_i)
            list_end=(sorted_list[splice_index[len(splice_index)-1]:])
            final_priority_list += self.same_frequency_words_priority(list_end)

        print(final_priority_list)
        sorted_x = sorted(freq_dict.items(), key=operator.itemgetter(1), reverse=True)
        return final_priority_list

    def keywords_formation(self):
        word_arr = self.tokenizing([self.description])
        stopwords_remove = self.stop_words_removal(word_arr)
        # print(stopwords_remove)
        count = self.freq(stopwords_remove)
        final_prority_array=self.priority_provide(stopwords_remove,count)
        # print(final_prority_array)
        return final_prority_array

    def tokenizing(self, parameters):
        # Tokenising..............................................
        data = '';
        for i in parameters:
            data += i + ' '
        data = data.strip()
        # print(data)
        data = data.split(' ')
        # print(data)
        sentence = ''
        for i in data:
            sentence += i+' '
        sentence=sentence.strip()
        word_arr = word_tokenize(sentence.lower())
        #  Here lower case is done to remove more stopwords, but some information is lost
        # print( word_arr)
        return word_arr

    def stop_words_removal(self, word_arr):
        # Stopwords and Punctuations.........................................
        stop_words = stopwords.words('english')
        # Stop Words are present of different languages, for papers of different languages.
        # Cleaning words(removing stopwords and punctuations
        # print(stop_words)
        punctuations = list(string.punctuation)
        # print(string.punctuation)
        stop_words += punctuations
        # print(len(stop_words))
        file_data = []
        with open('stopwords', 'r') as f:
            for line in f:
                for word in line.split():
                    file_data.append(word)
        stop_words += file_data
        stop_words = set(stop_words)
        stop_words = list(stop_words)
        new_word_arr = []
        for i in word_arr:
            new_word_arr.append(i.lower())
        clean_words = [w for w in new_word_arr if not w in stop_words]
        # print(len(stop_words))
        # print("After cleaning the stopwords, no of words:", len(clean_words))
        # print(clean_words)
        return clean_words

    def freq(self, words):
        dict = {
        }
        for i in words:
            dict[i] = words.count(i)
        # print("Dictionary after stopwords removal(no lemmatization)")
        # print(dict)
        return dict

    def lemmatization(self, part_of_speech, clean_words):
        lemmatized = []
        lemmatizer = WordNetLemmatizer()
        # print pos[2][0]
        # print clean_words[1]
        for i in range(0, len(part_of_speech)):
            for j in range(0, len(clean_words)):
                if part_of_speech[i][0].lower() == clean_words[j]:
                    # print part_of_speech[i][0], clean_words[j], part_of_speech[i][1]
                    lemmatized.append(
                        (lemmatizer.lemmatize(clean_words[j], pos=self.pos_to_wordnet(part_of_speech[i][1]))).lower())
                    break
                else:
                    continue
        # print("After Lemmatization No. of Words:", len(list(set(lemmatized))))
        # print(lemmatized)
        return list(set(lemmatized))

    def parts_of_speech(self):
        parts_of_speech = pos_tag(word_tokenize(self.description))  # +' '+self.synonym+ ' ' + self.name))
        # print(parts_of_speech)
        return parts_of_speech

    def pos_to_wordnet(self, pos_tag):
        if pos_tag.startswith('J'):
            return wordnet.ADJ
        elif pos_tag.startswith('N'):
            return wordnet.NOUN
        elif pos_tag.startswith('V'):
            return wordnet.VERB
        # elif pos_tag.startswith('M'):
        #     return wordnet.MODAL
        # elif pos_tag.startswith('R'):
        #     return wordnet.ADVERB
        else:
            return wordnet.NOUN

    def stemming(self, cleaning_words):
        '''
        The process of stemmimng is very dumb. Not always give reslutant output. The information passed through it might result in bad output.
        Stemming is the process of finding the root word of the given word.
        Prefer Lemmatization over it.
        '''
        ps = PorterStemmer()
        # stem_words = ['play', 'playing', 'played', 'player', "happy", 'happier']
        stemmed_words = [ps.stem(w) for w in cleaning_words]
        # print(len(stemmed_words))
        # print(stemmed_words)
        return stemmed_words

import csv
with open('Final_Dataset.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        additional_keywords = list(reader)
csvFile.close()
    
temp=cleaning_nlp_processes(additional_keywords[4][2]+additional_keywords[4][3])
temp.keywords_formation()

class keywords_from_ontology:
    def __init__(self,properties):
        # self.defintion=definition
        # self.synonym=synonym
        # self.entity_name=entity_name
        self.properties=properties

    def keywords_creation(self):
        tokens=self.tokenizing(self.properties)
        clean_words=self.stop_words_removal(tokens)
        return clean_words

    def stop_words_removal(self, word_arr):
        # Stopwords and Punctuations.........................................
        stop_words = stopwords.words('english')
        # Stop Words are present of different languages, for papers of different languages.
        # Cleaning words(removing stopwords and punctuations
        # print(stop_words)
        
        punctuations = list(string.punctuation)
        # print(string.punctuation)
        stop_words += punctuations
        # print(len(stop_words))
        file_data = []
        with open('stopwords', 'r') as f:
            for line in f:
                for word in line.split():
                    file_data.append(word)
        stop_words += file_data
        stop_words = set(stop_words)
        stop_words = list(stop_words)
        new_word_arr = []
        for i in word_arr:
            new_word_arr.append(i.lower())
        clean_words = [w for w in new_word_arr if not w in stop_words]
        # print(len(stop_words))
        # print("After cleaning the stopwords, no of words:", len(clean_words))
        # print(clean_words)
        return clean_words

    def tokenizing(self, parameters):
        # Tokenising..............................................
        data = '';
        for i in parameters:
            data += i + ' '
        data = data.strip()
        # print(data)
        data = data.split(' ')
        # print(data)
        sentence = ''
        for i in data:
            sentence += i+' '
        sentence=sentence.strip()
        word_arr = word_tokenize(sentence.lower())
        #  Here lower case is done to remove more stopwords, but some information is lost
        # print( word_arr)
        return word_arr

class Node:
    def __init__(self,entity,keywords):
        self.entity=entity
        # self.children=children
        self.keywords=keywords
        # self.deprecated=deprecated

def ontology_creation():
    with open('DOID_Ontology - Sheet1.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        data = list(reader)
    csvFile.close()
    # for i in range(0,len(data[0])):
    #   print(i,data[0][i])
    # print(additional_keywords[0])
    temp_object_for_keywords = keywords_from_ontology('')
    nodes=[]
    for k in range(1,len(data)):
      parent_keywords=[]
      child_keywords=[]
      temp_object_for_keywords = keywords_from_ontology([str(data[k][0]), str(data[k][3]),
                                                               str(data[k][4]),str(data[k][5]),
                                                               str(data[k][6]), str(data[k][7]),
                                                               str(data[k][7]),str(data[k][9]), 
                                                               str(data[k][10]),str(data[k][13]),
                                                               str(data[k][14]),str(data[k][24]),
                                                               str(data[k][25]),str(data[k][54]),
                                                               str(data[k][55]),str(data[k][58])])      
      for i in range(1,len(data)):
        if data[i][0]==data[k][2]:
          temp_object_for_keywords_parent = keywords_from_ontology([str(data[i][0]), str(data[i][3]),
                                                               str(data[i][4]),str(data[i][5]),
                                                               str(data[i][6]), str(data[i][7]),
                                                               str(data[i][8]),str(data[i][9]), 
                                                               str(data[i][10]),str(data[i][13]),
                                                               str(data[i][14]),str(data[i][24]),
                                                               str(data[i][25]),str(data[i][54]),
                                                               str(data[i][55]),str(data[i][58])])
          parent_keywords=list(set(temp_object_for_keywords_parent.keywords_creation()))
          break
        else:
          continue

      child_keywords=list(set(temp_object_for_keywords.keywords_creation()))
      obj=Node(str(data[k][0]),list(set(child_keywords+parent_keywords)))
      nodes.append(obj)
    
    return nodes

def ontology_mathing(tree,keywords):
    # print('Keywords formed from given x data:',keywords)
    # print()
    nodes_to_search=[]
    found_nodes = []
    priority_1 = []
    priority_2 = []
    priority_3 = []

    for i in range(0, len(keywords)):
        if keywords[i][1] != 1:
            priority_1.append(keywords[i][0])
        else:
            if keywords[i][2] == 1:
                priority_2.append(keywords[i][0])
            else:
                priority_3.append(keywords[i][0])

    # nodes_to_search.append(tree[0])
    # nodes_to_search.append(tree[76])
    # i=0
    # flag=0
    # while i in range(0,len(nodes_to_search)):
    #     if i==0:
    #         node=nodes_to_search.index(tree[0])
    #         print('Entity whose children are Currently Under Search:',tree[node].entity)
    #         flag=0
    #     else:
    #         node = tree.index(nodes_to_search[i])
    #         print('Entity whose children are Currently Under Search:', tree[node].entity)
    #         flag=1
    #     for j in range(0,len(tree[node].children)):
    #         print('Child under Consideration:',tree[node].children[j])
    #         for k in range(i,len(tree)):
    #             if tree[k].entity==tree[node].children[j]:
    #                 print('Found Entity in Tree:', tree[k].entity)
    #                 if flag==0:
    #                     for l in range(0,len(keywords)):
    #                         if keywords[l][0] in tree[k].keywords:
    #                             found_nodes.append((k,tree[k].entity,keywords[l][0]))
    #                             nodes_to_search.append(tree[k])
    #                             print('Keyword ',keywords[l][0],' Found in Node:',tree[k].entity)
    #                             break
    #                         else:
    #                             continue
    #                 else:
    #                     nodes_to_search.append(tree[k])
    #                     for l in range(0,len(keywords)):
    #                         if keywords[l][0] in tree[k].keywords:
    #                             found_nodes.append((k,tree[k].entity,keywords[l][0]))
    #                             print('Keyword ',keywords[l][0],' Found in Node:',tree[k].entity)
    #                             break
    #                         else:
    #                             continue
    #             else:
    #                 continue
    #     i=i+1
        # print(nodes_to_search)
    priority_1_count = 0
    priority_2_count = 0
    priority_3_count = 0

    for i in range(0,len(tree)):
        priority_1_count = 0
        priority_2_count = 0
        priority_3_count = 0
        for j in range(0,len(priority_1)):
                if priority_1[j].lower() in [x.lower() for x in tree[i].keywords]:
                    priority_1_count=priority_1_count+1
                else:
                    continue
        for j in range(0, len(priority_2)):
            if priority_2[j].lower() in [x.lower() for x in tree[i].keywords]:
                priority_2_count = priority_2_count + 1
            else:
                continue

        for j in range(0, len(priority_3)):
            if priority_3[j].lower() in [x.lower() for x in tree[i].keywords]:
                priority_3_count = priority_3_count + 1
            else:
                continue

        # print("Priority_1:", priority_1_count)
        # print("Priority_2:", priority_2_count)
        # print("Priority_3:", priority_3_count)

        # if priority_1_count>=1:
        #     if priority_2_count>=1:
        #         if priority_3_count>=1:
        #             found_nodes.append((tree[i].entity))
        #         else:
        #             continue
        #     else:
        #         continue
        # else:
        #     continue
        if priority_1_count+priority_2_count+priority_3_count>=1:
            # print('Possible Node :', tree[i].entity)
            # print('Possible Node Keywords:', tree[i].keywords)
            # print('Keywords Passed:',keywords)
            found_nodes.append((tree[i].entity))
        else:
            continue

    # for i in range(0,len(found_nodes)):
    #     print('Possible Class/Node:',found_nodes[i])
    classes=[]
    for i in range(0,len(found_nodes)):
        classes.append(found_nodes[i])
    classes=list(set(classes))
    # print(classes)
    return classes

def Classification_without_Ontology(x_train, y_train,x_test,y_test):
    names=['Multinomial Naive Bayes','Bagging', 'KNN', 'SVM','Decision Tree','Random Forest','Gradient Boost','Logistic Regression']
    count_vector = CountVectorizer(max_features=400)
    training_data = count_vector.fit_transform(x_train)
    predictions=[]
    testing_data = count_vector.transform(x_test)
 
    naive_bayes = MultinomialNB()
    grad_boost=GradientBoostingClassifier()
    bagging=BaggingClassifier()
    KNN=KNeighborsClassifier(n_neighbors=2)
    SVM=LinearSVC()
    decision_tree=DecisionTreeClassifier()
    random_forest=RandomForestClassifier()
    lr=LogisticRegression()
    
    classifiers=[naive_bayes,bagging,KNN,SVM,decision_tree,random_forest,grad_boost,lr]
    for i in range(0,len(classifiers)):
      # print('Classifier in use:'+names[i])
      classifiers[i].fit(training_data, y_train)
    # print(count_vector.get_feature_names())
      predictions.append(classifiers[i].predict(testing_data))
    
    return predictions

def entire_process_without_ontology():
    data_x,data_y=dataset_creation()
    names=['Multinomial Naive Bayes','Bagging', 'KNN', 'SVM','Decision Tree','Random Forest','Gradient Boost','Logistic Regression']
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2)
    predictions_without_ontology = Classification_without_Ontology(x_train, y_train,x_test[:500],y_test[:500])
    # print(predictions_without_ontology)
    # from sklearn.metrics import classification_report
    # print((classification_report(y_test[:len(predictions_without_ontology[1])], predictions_without_ontology[1], target_names=list(set(data_y)))))
    # from sklearn.metrics import precision_recall_fscore_support
    # print(precision_recall_fscore_support(y_test[:len(predictions_without_ontology[1])], predictions_without_ontology[1], target_names=list(set(data_y)), average='macro'))
    for i in range(0,len(predictions_without_ontology)):
      print('Classifier under consideration: '+ names[i])
      print('Accuracy score:',format(accuracy_score(y_test[:len(predictions_without_ontology[i])], predictions_without_ontology[i])))
      print('Precision score:',format(precision_score(y_test[:len(predictions_without_ontology[i])], predictions_without_ontology[i], average='micro')))
      print('Recall score:',format(recall_score(y_test[:len(predictions_without_ontology[i])], predictions_without_ontology[i], average='micro')))
      print('F1 score:',format(f1_score(y_test[:len(predictions_without_ontology[i])], predictions_without_ontology[i], average='micro')))

entire_process_without_ontology()

def Classification_with_Ontology(x_train, y_train,x_test,y_test):
    ontology_tree=ontology_creation()
    tree=ontology_tree
    predictions=[[],[],[],[],[],[],[]]
    c1,c2,c3=0,0,0
    all_classes = list(set(list(set(y_train))+list(set(y_test))))
    names=['Multinomial Naive Bayes','Bagging', 'KNN', 'SVM','Decision Tree','Random Forest','Logistic Regression'] #'Gradient Boost']
    keywords_for_matching=[]
    
    with open('Final_Dataset.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        additional_keywords = list(reader)
    csvFile.close()
    
    for i in range(1,len(additional_keywords)):
      obj = cleaning_nlp_processes(additional_keywords[i][2]+additional_keywords[i][3])
      additional_words = obj.keywords_formation()
      # print('Keywords From Dataset for '+additional_keywords[i][0] +' are:')
      # print(additional_words)
      keywords_for_matching.append((additional_keywords[i][0],additional_words))

    count_vector_entire_data_set = CountVectorizer(max_features=400)
    training_data_entire_data_set = count_vector_entire_data_set.fit_transform(x_train)

    naive_bayes_entire_data_set = MultinomialNB()
    # grad_boost_entire_data_set=GradientBoostingClassifier()
    bagging_entire_data_set=BaggingClassifier()
    KNN_entire_data_set=KNeighborsClassifier(n_neighbors=2)
    SVM_entire_data_set=LinearSVC()
    decision_tree_entire_data_set=DecisionTreeClassifier()
    random_forest_entire_data_set=RandomForestClassifier()
    lr_entire_dataset=LogisticRegression()
    
    classifiers_entire_data_set=[naive_bayes_entire_data_set,bagging_entire_data_set,KNN_entire_data_set,SVM_entire_data_set,decision_tree_entire_data_set,
                                 random_forest_entire_data_set,lr_entire_dataset]#,grad_boost_entire_data_set]
    
    naive_bayes = MultinomialNB()
    # grad_boost=GradientBoostingClassifier()
    bagging=BaggingClassifier()
    KNN=KNeighborsClassifier(n_neighbors=2)
    SVM=LinearSVC()
    decision_tree=DecisionTreeClassifier()
    random_forest=RandomForestClassifier()
    lr=LogisticRegression()
    classifiers=[naive_bayes,bagging,KNN,SVM,decision_tree,random_forest,lr]#,grad_boost]
    
    for i in range(0,len(classifiers_entire_data_set)):
      # print('Classifier in use:'+names[i])
      classifiers_entire_data_set[i].fit(training_data_entire_data_set, y_train)
    # print(count_vector.get_feature_names())
    
    for z in range(0,len(x_test)):
      # print('Disease Under Consideration:',y_test[z])
      obj = cleaning_nlp_processes(x_test[z])
      words = obj.keywords_formation()
      # print('Initially Keywords from symtoms:')
      # print(words)
      for q in range(0,len(keywords_for_matching)):
        # print(y_test[z],keywords_for_matching[q][0],y_test[z].strip()==keywords_for_matching[q][0].strip())
        if y_test[z].strip()==keywords_for_matching[q][0].strip():
          words=words+keywords_for_matching[q][1]
          break
        else:
          continue
      # print('Adding additional Keywords From Dataset are:')
      # print(words)
      # flag=1
      # for i in range(0,len(tree)):
      #   if tree[i].entity[len(tree[i].entity)-1]=="'":
      #     # print(tree[i].entity[0:len(tree[i].entity)-2].strip(),data_y[no])
      #     if set(word_tokenize(y_test[z])).issubset(word_tokenize(tree[i].entity[0:len(tree[i].entity)-2])):
      #       print('Ontology Node:',tree[i].entity[0:len(tree[i].entity)-2])
      #       print('Keywords of ontology Node:',tree[i].keywords)
      #       flag=0
      #       break
      #     else:
      #       continue
      #   else:      
      #     # print(tree[i].entity,data_y[no])
      #     if set(word_tokenize(y_test[z])).issubset(word_tokenize(tree[i].entity)):
      #       print('Ontology Node:',tree[i].entity)
      #       print('Keywords of ontology Node:',tree[i].keywords)
      #       flag=0
      #       break
      #     else:
      #       continue
      common_classes=[]
      # if flag==1:
        # print('Disease doesn"t occur in ontology')
        # pass
      possible_classes=ontology_mathing(ontology_tree,words)
      # print('Possibilities After Ontology Matching:',possible_classes)
      for i in range(0,len(all_classes)):
          dataset_elements=[x.lower() for x in list(set(word_tokenize(all_classes[i])))]
          for j in range(0,len(possible_classes)):
            ontology_node=[x.lower() for x in list(set(word_tokenize(possible_classes[j])))]
            if set(dataset_elements).issubset(set(ontology_node)):
              common_classes.append(all_classes[i])
            else:
              continue      
      common_classes=list(set(common_classes))
      # print('Final Possibilites After Ontology Dataset Intersections:',common_classes)
      # print('Number of possible Classes after intersection:',len(common_classes))
      # print('Does Actual Class exsist in Possible Classes after intersection:', y_test[z] in common_classes)
      if len(common_classes)==0:
        c1=c1+1
        # print('No Entry Found in Dataset and Ontology, Using Normal Classification.........')
        # print('Comparing Predictions...............')
        # print('Actual Value:',y_test[z])
        testing_data = count_vector_entire_data_set.transform([x_test[z]])[0]
        for h in range(0,len(classifiers_entire_data_set)):
          prediction= classifiers_entire_data_set[h].predict(testing_data)[0] 
          predictions[h].append(prediction)
          # print('Comparing Predictions...............')
          # print('Classifier in use: ',names[h])
          # print('Actual value: ',y_test[z])
          # print('Predicted Value:',prediction)  
      else:
        c2=c2+1
        # print('Using Ontology Matching............')
        indexes_to_use = []
        for j in range(0, len(y_train)):
          if y_train[j] in common_classes:
            indexes_to_use.append(j)
          else:
            continue
        new_x=[x_train[x] for x in indexes_to_use]
        new_y=[y_train[x] for x in indexes_to_use]

        count_vector = CountVectorizer(max_features=400)
        training_data = count_vector.fit_transform(new_x)
        testing_data = count_vector.transform([x_test[z]])[0]
        
        for h in range(0,len(classifiers)):
          classifiers[h].fit(training_data,new_y)
          prediction= classifiers[h].predict(testing_data)[0] 
          predictions[h].append(prediction)
          # print('Comparing Predictions...............')
          # print('Classifier in use: ',names[h])
          # print('Actual Value:',y_test[z])
          # print('Predicted Value:',prediction)
        # if set(word_tokenize(y_test[z])).issubset(set(word_tokenize(prediction))):
          # c3=c3+1
      # print(c1,c2,c3)
      print(((z+1)/len(x_test))*100,'% Completed')
      # print()
    return predictions

def entire_process_with_ontology():
    names=['Multinomial Naive Bayes','Bagging', 'KNN', 'SVM','Decision Tree','Random Forest','Logistic Regression']#'Gradient Boost']
    data_x,data_y=dataset_creation()
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2,random_state=0)
    predictions_with_ontology = Classification_with_Ontology(x_train,y_train,x_test[:500] ,y_test[:500])
    print(predictions_with_ontology)

    for i in range(0,len(predictions_with_ontology)):
      print('Classifier under consideration:'+ names[i])
      print('Accuracy score:',format(accuracy_score(y_test[:len(predictions_with_ontology[i])], predictions_with_ontology[i])))
      print('Precision score:',format(precision_score(y_test[:len(predictions_with_ontology[i])], predictions_with_ontology[i], average='micro')))
      print('Recall score:',format(recall_score(y_test[:len(predictions_with_ontology[i])], predictions_with_ontology[i], average='micro')))
      print('F1 score:',format(f1_score(y_test[:len(predictions_with_ontology[i])], predictions_with_ontology[i], average='micro')))

entire_process_with_ontology()

# Following Code is for Testing Purpose only.......................................................

def data_analysis():
    total_count=0
    c=0
    print('Analysing Common Diseases in Dataset and Ontology.................')
    data_x,data_y=dataset_creation()
    ontology_tree = ontology_creation()
    for i in list(set(data_y)):
      print('Disease From Dataset:',i)
      dataset_elements=[x.lower() for x in list(set(word_tokenize(i)))]
      for j in range(0,len(ontology_tree)):
            ontology_node=[x.lower() for x in list(set(word_tokenize(ontology_tree[j].entity)))]
            if set(dataset_elements).issubset(set(ontology_node)):
                c=c+1
                # print('Disease Name Ontology from ontology:', ontology_tree[j].entity)
                # indices = [l for l, x in enumerate(data_y) if x == str(ontology_tree[i].entity)]
                # print('Indices in Dataset for :',i, ' are:', indices)
                # obj = cleaning_nlp_processes(data_x[random.choice(indices)])
                # words = obj.keywords_formation()
                # print('Keywords From Dataset are:')
                # print(words)
                # obj = cleaning_nlp_processes(data_x[random.choice(indices)])
                # words = obj.keywords_formation()
                # print('Keywords From Dataset are:')
                # print(words)
                # obj = cleaning_nlp_processes(data_x[random.choice(indices)])
                # words = obj.keywords_formation()
                # print('Keywords From Dataset are:')
                # print(words)
                # obj = cleaning_nlp_processes(data_x[random.choice(indices)])
                # words = obj.keywords_formation()
                # print('Keywords From Dataset are:')
                # print(words)
                # print('Ontology Information:')
                # print('Keywords From Ontology Node:')
                # print(ontology_tree[j].keywords)
                # print('Children of Ontology Node:',ontology_tree[i].children)
            else:
                continue
      print('Number of Nodes Match for this disease are:',c)
      if c!=0:
        total_count=total_count+1
      else:
        print("This Disease can't matched in the ontology:",i)
      c=0
    print(total_count)

# data_analysis()

data_x,data_y=dataset_creation()
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2,random_state=0)

ontology_tree=ontology_creation()
    tree=ontology_tree

x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.2,random_state=0)
all_classes=list(set(data_y))
# print((all_classes).sort())
# print(all_classes)
# index=all_classes.index('Thrombophlebitis')
# print(index)
# indices = [l for l, x in enumerate(y_test) if x == str(all_classes[])]
indices=[]
temp_indices=[]
for i in range(0,len(all_classes)):
  temp_indices=[]
  for j in range(0,len(y_test)):
    if all_classes[i]==y_test[j]:
      temp_indices.append(j)
    else:
      continue
  for j in range(0,1):
    indices.append(random.choice(temp_indices))

# print(len(set(indices)))
# y_test[140]
x_test=[x_test[i] for i in indices]
y_test=[y_test[i] for i in indices]
y_test

predictions_without_ontology = Classification_without_Ontology(x_train, y_train,x_test,y_test)
    print('Accuracy score: ')
    print('Without Ontology:',format(accuracy_score(y_test, predictions_without_ontology)))

c=0
for i in range(0,len(y_test)):
  if predictions_without_ontology[i]!=y_test[i]:
    c=c+1
    print(i,y_test[i])
  else:
    continue
print(c)



predictions_with_ontology=predictions
    print('Accuracy score: ')
    print('With Ontology:',format(accuracy_score(y_test[:len(predictions_with_ontology)], predictions_with_ontology)))

c=0
for i in range(0,len(y_test)):
  if predictions_with_ontology[i]!=y_test[i]:
    c=c+1
    print(i,y_test[i])
  else:
    continue
print(c)