import streamlit as st
import pandas as pd
import re
import pickle
from utils import * 


def get_drugs_list(drugs):
    print(drugs)
    if type(drugs) == str:
        return re.sub(r'[{}"\']', '', drugs)
    return "-"

def get_diseases_list(diseases):
    if type(diseases) == str:
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
    if type(row["Age"]) == str and type(row["Age_Range"]) == str:
        age = row["Age"] + " / " + row["Age_Range"]
    elif type(row["Age"]) == str:
        age = row["Age"]
    elif type(row["Age_Range"]) == str:
        age = row["Age_Range"]
    else:
        age = " - "
    if type(row["Gender"]) == str: 
        gender = row["Gender"]
    else:
        gender = " - "
    tab1, tab2, tab3 = st.tabs(["Info", "Transcription", "Definitions"])
    with tab1:
        st.markdown("**Speciality:** " + speciality)
        st.markdown("**Age**: " + age)
        st.markdown("**Gender**: " + gender)
        st.markdown("**Drugs:** " + get_drugs_list(drugs))
        st.markdown("**Diseases:** " + get_diseases_list(diseases))

    with tab2:
        for t in transcription.splitlines():
            st.text(t)
    
    with tab3:
        doencas = get_diseases_list(diseases).split(",")
        doencas = [d.strip().lower() for d in doencas]
        for d in set(doencas):
            dfselect = diseasesDF[diseasesDF["Name"] == d]
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

tab1, tab2 = st.tabs(["Search","All Transcriptions"])

with tab1:
    st.write("A search engine designed to find and retrieve medical transcriptions from mtsamples.com.\n")

    search = st.text_input("Search medical transcriptions")
    col1, col2 = st.columns([2,1])
    with col2:
        with st.expander("Filter"):
            top_k = st.slider("Number of results", 1, 10, 5)

    if search:
        results = retrieve_documents([search], vect,doc_matrix, top_k)
        if results != []:
            st.markdown("*Show first " + str(top_k) +  " results.*")
        else:
            st.markdown("*There's no result for this search. Please try again with more information.*")
        for r in results:
            row = df.iloc[r["Document"]]
            st.button(row["Sample Name"] + " - " +row["Speciality"], on_click=result, args=[row])
            
with tab2:
    col1, col2, col3 = st.columns([1,1,1])

    with col1:
        speciality = st.selectbox("Speciality",df.Speciality.unique(), index = None )
    with col2:
        gender = st.selectbox("Gender",("Male", "Female"), index = None)
    with col3:    
        age = st.selectbox("Age Range",("Child", "Adult"), index = None)    

    if speciality or gender or age :
        results2 = df[
            (df.Speciality == speciality if speciality else True) &
            (df.Gender == gender if gender else True) &
            (df.Age_Range == age if age else True)
        ]
        st.write("Transcriptions")
        results_index = []
        for row in results2.iterrows():
            results_index.append(row[0])
        
        for row in results_index:
            row = df.iloc[row]
            st.button(row["Sample Name"] + " - " +row["Speciality"], on_click=result, args=[row])
