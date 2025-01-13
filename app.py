import streamlit as st
import pandas as pd
import re
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def retrieve_documents(query, vect, doc_matrix, top_k=5, threshold=0.12):
    # Vetor da query
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


def get_drugs_list(drugs):
    if drugs != "set()":
        return re.sub(r'[{}"\']', '', drugs)
    return "-"

def get_diseases_list(diseases):
    if diseases != "set()":
        return re.sub(r'[{}"\']', '', diseases)
    return "-"

def moreinfo(definition):
    st.write(definition)

@st.dialog("Sample Transcription", width ="large")
def result(row):
    transcription = row["Transcription"]
    drugs = row["Drugs"]
    speciality = row["Speciality"]
    diseases = row["Diseases"]

    tab1, tab2, tab3 = st.tabs(["Info", "Transcription", "Definitions"])
    with tab1:
        st.markdown("**Speciality:** " + speciality)
        st.markdown("**Age**: -")
        st.markdown("**Gender**: -")
        st.markdown("**Drugs:** " + get_drugs_list(drugs))
        st.markdown("**Diseases:** " + get_diseases_list(diseases))
        # for disease in get_diseases_list(diseases).split(", "):
        #     st.markdown("- " + disease)
       

    with tab2:
        for t in transcription.splitlines():
            st.text(t)
    
    with tab3:
        doencas = get_diseases_list(diseases).split(",")
        for d in doencas:
            dfselect = diseasesDF[diseasesDF["Name"] == d.strip().lower()]
            if dfselect.size > 0:
                if type(dfselect.Definition.values[0]) == str:
                    st.markdown("**" + d.strip().lower() + "**: *" + dfselect.Definition.values[0] + "*")  

diseasesDF=pd.read_csv('D-DoMiner_miner-diseaseDOID.tsv',sep='\t')
diseasesDF["Name"] = diseasesDF["Name"].apply(lambda x: x.lower())

df = pd.read_csv("sample_struct.csv")

with open("vectorizer.pkl", 'rb') as f:
    vect = pickle.load(f)
with open("doc_matrix.pkl", 'rb') as f:
    doc_matrix = pickle.load(f)


st.image("mtsamples.png")

st.write("A search engine designed to find and retrieve medical transcriptions from mtsamples.com.\n")


search = st.text_input("Search medical transcriptions")
col1, col2 = st.columns([2,1])
with col2:
    with st.expander("Filter"):
        top_k = st.slider("Number of results", 1, 10, 5)

if search:
    st.markdown("*Show first " + str(top_k) +  " results.*")
    results = retrieve_documents([search], vect,doc_matrix, top_k)
    for r in results:
        row = df.iloc[r["Document"]]

        st.button(str(row["ID"]) + " - " +row["Speciality"], on_click=result, args=[row])
        
    # row = df[df.Speciality == search].head(10)
    # for index, r in row.iterrows():
    #     st.button(str(r["ID"]) + " - " +r["Speciality"], on_click=result, args=[r])
    

        
