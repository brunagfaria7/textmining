from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer,word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

nltk.download('stopwords')


# Lista de stopwords personalizada (exclui pronomes pessoais relevantes)
def get_custom_stopwords():
    stop_words = set(stopwords.words('english'))
    # Remover pronomes pessoais das stopwords
    pronouns_to_keep = {"he", "she", "him", "her", "his", "hers", "they", "them", "their", "theirs"}
    custom_stop_words = stop_words - pronouns_to_keep
    return custom_stop_words

# Remoção da pontuação e das stopwords de cada transcrição
def filter_text(c):
    custom_stop_words = get_custom_stopwords()
    tokenizer = RegexpTokenizer(r"[\w']+")
    word_tokens = tokenizer.tokenize(c)  # Tokenizar e remover pontuação
    tokens = wordpunct_tokenize(" ".join(word_tokens))
    # Filtrar stopwords, mas manter os pronomes relevantes
    filtered_sentence = [w for w in tokens if w.lower() not in custom_stop_words]
    return filtered_sentence


def retrieve_documents(query, vect, doc_matrix, top_k=5, threshold=0.12):
    # Vetor da query
    query = [" ".join(filter_text(query[0]))]
    query_vector = vect.transform(query)

    # Similaridade por cosseno
    similarity_scores = cosine_similarity(doc_matrix, query_vector).flatten()

    # Índices dos documentos relevantes
    idx_relevant_docs = similarity_scores.argsort()[::-1][:top_k]

    # Filtrar por limiar
    results = []
    for i in idx_relevant_docs:
        if similarity_scores[i] > threshold:
            results.append(
                {
                    "Document": i,
                    "Score": similarity_scores[i],
                }
            )
    return results