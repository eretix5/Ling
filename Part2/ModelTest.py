from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import CountVectorizer
from pyspark.ml.feature import IDF
from pyspark.ml.feature import Word2Vec


spark = SparkSession \
    .builder \
    .appName("SimpleApplication") \
    .getOrCreate()


input_file = spark.sparkContext.textFile('zapas.txt')

print(input_file.collect())

prepared = input_file.map(lambda x: ([x]))
df = prepared.toDF()
prepared_df = df.selectExpr('_1 as text')


tokenizer = Tokenizer(inputCol='text', outputCol='words')
words = tokenizer.transform(prepared_df)


stop_words = StopWordsRemover.loadDefaultStopWords('russian')
remover = StopWordsRemover(inputCol='words', outputCol='filtered', stopWords=stop_words)
filtered = remover.transform(words)


print(stop_words)


filtered.show()


words.select('words').show(truncate=False, vertical=True)


filtered.select('filtered').show(truncate=False, vertical=True)


vectorizer = CountVectorizer(inputCol='filtered', outputCol='raw_features').fit(filtered)
featurized_data = vectorizer.transform(filtered)
featurized_data.cache()
vocabulary = vectorizer.vocabulary


featurized_data.show()


featurized_data.select('raw_features').show(truncate=False, vertical=True)


idf = IDF(inputCol='raw_features', outputCol='features')
idf_model = idf.fit(featurized_data)
rescaled_data = idf_model.transform(featurized_data)


rescaled_data.show()


rescaled_data.select('features').show(truncate=False, vertical=True)


word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol='words', outputCol='result')
model = word2Vec.fit(words)
w2v_df = model.transform(words)
w2v_df.show()

print(vocabulary)
print(type(vocabulary))

persons_and_sights = ["Бочаров", "Григоров", "Писемская", "Савченко", "Мержоева", "Быкадорова", "Иванов", "Бахин",
                      "Русаев", "Лихачев", "Николаев", "Черепахин", "Губин",
                      "Казанский кафедральный собор",
                      "Волгоградская областная филармония", "Авангард", "библиотека им. М. Горького",
                      "Площадь Павших Борцов", "Памятник Саше Филиппову", "Музей истории Кировского района",
                      "Памятник чекистам", "Армянская церковь Святого Георгия", "Музей истории Кировского района",
                      "Трамвай-памятник", "Воинский эшелон", "герградта", "Памятник Дзержинскому",
                      "Здание Царицынской пожарной команды", "Дом Павлова", "Челябинский колхозник",
                      "Памятник Гоголю", "БК-13", "Бейт Давид", "Фонтан Бармалей"]


for word in persons_and_sights:
    word = word.lower()
    if word in vocabulary:
        synonyms = model.findSynonymsArray(word, 10)
        print('Синонимы для  "{}": {}'.format(word, synonyms))

spark.stop()