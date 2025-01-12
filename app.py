import streamlit as st
import pandas as pd
import re

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
    diseases = row["Diseases"]

    tab1, tab2, tab3 = st.tabs(["Info", "Transcription", "Definitions"])
    with tab1:
        st.markdown("**Age**: -")
        st.markdown("**Gender**: -")
        st.markdown("**Drugs:** " + get_drugs_list(drugs))
        st.markdown("**Diseases:** " + get_diseases_list(diseases))
       

    with tab2:
        for t in transcription.splitlines():
            st.text(t)
    
    with tab3:
        doencas = get_diseases_list(diseases).split(",")
        for d in doencas:
            dfselect = diseasesDF[diseasesDF["Name"] == d.lower()]
            if dfselect.size > 0:
                st.markdown("**" + d + "**: *" + dfselect.Definition.values[0] + "*")  

diseasesDF=pd.read_csv('D-DoMiner_miner-diseaseDOID.tsv',sep='\t')
diseasesDF["Name"] = diseasesDF["Name"].apply(lambda x: x.lower())

df = pd.read_csv("sample_struct.csv")

search = st.text_input("Search medical transcriptions")
if search:
    st.markdown("*Show first 10 results.*")
    row = df[df.Speciality == search].head(10)
    for index, r in row.iterrows():
        st.button(str(r["ID"]) + " - " +r["Speciality"], on_click=result, args=[r])
    

        
