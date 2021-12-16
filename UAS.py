import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
import numpy as np

df = pd.read_csv("produksi_minyak_mentah.csv")
f=open("kode_negara_lengkap.json")
data=json.load(f)

st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Data Produksi Minyak Mentah")

st.sidebar.title("Pengaturan")
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
st.set_option('deprecation.showPyplotGlobalUse', False)
list_negara = list()
for i in data:
    list_negara.append(i["name"])
negara = st.sidebar.selectbox("Pilih negara", list_negara)

list_tahun = list()
for i in range(1971,2016):
    list_tahun.append(i)
tahun = st.sidebar.selectbox("Pilih tahun", list_tahun)

n_tampil = st.sidebar.number_input("Jumlah negara yang ditampilkan", min_value=1, max_value=100, value=10)

total_pertahun = list()
name = negara
df = df.loc[(df["kode_negara"]!="WLD")&(df["kode_negara"]!="OEU")&(df["kode_negara"]!="EU28")&(df["kode_negara"]!="G20")&(df["kode_negara"]!="OECD")]
for i in data:
    if i["name"]==name:
        kode = i["alpha-3"]
        name = i["name"]
df1 = df.loc[df["kode_negara"]==kode]
df1.plot(kind="line",x="tahun",y="produksi", title="Jumlah Produksi Minyak Mentah Negara "+name)
st.pyplot()

sorted_value = df.sort_values(["produksi"], ascending=[0])

data_tahun = sorted_value.loc[sorted_value["tahun"]==tahun]
jumlah_negara = int(n_tampil)
df2=data_tahun[0:jumlah_negara]
df2.plot(kind="bar",x="kode_negara",y="produksi", title="Top "+str(jumlah_negara)+" Jumlah Produksi Minyak Mentah Terbesar pada Tahun "+str(tahun))
st.pyplot()

data_value=sorted_value.groupby("kode_negara")["produksi"].sum()
df3=data_value.nlargest(jumlah_negara)
df3.plot(kind="bar",x="kode_negara",y="produksi", title="Top "+str(jumlah_negara)+" Jumlah Produksi Minyak Mentah Terbesar Kumulatif")
st.pyplot()

for i in data_tahun["kode_negara"]:
    kode_negara = i
    break                
for i in data:
    if i["alpha-3"]==kode_negara:
        nama = i["name"]  
        region = i["region"] 
        sub_region = i["sub-region"]

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah Terbesar pada Tahun "+str(tahun)):
    data_terbesar_tahun = data_tahun.loc[data_tahun["kode_negara"] == kode_negara]
    jumlah_produksi_tahun = float(data_terbesar_tahun["produksi"])
    st.markdown("Negara      : "+nama)
    st.markdown("Kode Negara : "+kode_negara)
    st.markdown("Region      : "+region)
    st.markdown("Sub Region  : "+sub_region)
    st.markdown("Dengan jumlah produksi "+ str(jumlah_produksi_tahun)+ " pada Tahun "+str(tahun))
    st.markdown("")

kode_negara="SAU"
for i in data:
    if i["alpha-3"]==kode_negara:
        nama = i["name"]  
        region = i["region"] 
        sub_region = i["sub-region"]

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah Terbesar pada Kumulatif Tahun"):
    data_terbesar = data_value[0]
    st.markdown("Negara      : "+nama)
    st.markdown("Kode Negara : "+kode_negara)
    st.markdown("Region      : "+region)
    st.markdown("Sub Region  : "+sub_region)
    st.markdown("Dengan jumlah produksi "+ str(data_terbesar)+ " pada Kumulatif Tahun")
    st.markdown("")

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah Terkecil pada Tahun "+str(tahun)):
    data_terkecil = df.loc[df["produksi"]>0]
    data_terkecil = data_terkecil.sort_values(["produksi"], ascending=[1])
    data_terkecil = data_terkecil.loc[data_terkecil["tahun"]==tahun]
    for i in data_terkecil["kode_negara"]:
        kode_negara = i
        break                
    for i in data:
        if i["alpha-3"]==kode_negara:
            nama = i["name"]  
            region = i["region"] 
            sub_region = i["sub-region"]
    data_terkecil_tahun = data_terkecil.loc[data_terkecil["kode_negara"] == kode_negara]
    jumlah_terkecil_tahun = float(data_terkecil_tahun["produksi"])
    st.markdown("Jumlah Produksi Minyak Mentah Terkecil pada Tahun "+str(tahun)+" adalah : ")
    st.markdown("Negara      : "+nama)
    st.markdown("Kode Negara : "+kode_negara)
    st.markdown("Region      : "+region)
    st.markdown("Sub Region  : "+sub_region)
    st.markdown("Dengan jumlah produksi "+ str(jumlah_terkecil_tahun)+ " pada Tahun "+str(tahun))
    st.markdown("")

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah Terkecil pada Kumulatif Tahun"):
    data_terkecil_kumulatif = df.loc[df["produksi"]>0]
    data_terkecil_kumulatif = data_terkecil_kumulatif.groupby("kode_negara")["produksi"].sum().sort_values(ascending=True)
    kode_negara="SEN"
    for i in data:
        if i["alpha-3"]==kode_negara:
            nama = i["name"]  
            region = i["region"] 
            sub_region = i["sub-region"]
    data_terkecil_kumulatif = data_terkecil_kumulatif[0]
    st.markdown("Negara      : "+nama)
    st.markdown("Kode Negara : "+kode_negara)
    st.markdown("Region      : "+region)
    st.markdown("Sub Region  : "+sub_region)
    st.markdown("Dengan jumlah produksi "+ str(data_terkecil_kumulatif)+ " pada Kumulatif Tahun")
    st.markdown("")

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah 0.0 pada Tahun "+str(tahun)):
    df0=df.loc[df["produksi"]==0].sort_values(["kode_negara"], ascending=[1])
    df0_tahun=df0.loc[df0["tahun"]==tahun]
    for i in df0_tahun["kode_negara"]:
        kode_negara = i
        for j in data:
            if j["alpha-3"]==kode_negara:
                nama = j["name"]  
                region = j["region"] 
                sub_region = j["sub-region"]
        data_df0_tahun = df0_tahun.loc[df0_tahun["kode_negara"] == kode_negara]
        jumlah_df0 = float(data_df0_tahun["produksi"])
        st.markdown("Negara      : "+nama)
        st.markdown("Kode Negara : "+kode_negara)
        st.markdown("Region      : "+region)
        st.markdown("Sub Region  : "+sub_region)
        st.markdown("Dengan jumlah produksi "+ str(jumlah_df0)+ " pada Tahun "+str(tahun))
        st.markdown("")

with st.expander("Negara dengan Jumlah Produksi Minyak Mentah 0.0 pada Kumulatif Tahun"):
    dic_df0 = dict()
    for i in df0["kode_negara"] :
        dic_df0[i]=0
    for a,b in dic_df0.items():
        kode_negara = a
        for i in data:
            if i["alpha-3"]==kode_negara:
                nama = i["name"]  
                region = i["region"] 
                sub_region = i["sub-region"]
        st.markdown("Negara      : "+nama)
        st.markdown("Kode Negara : "+kode_negara)
        st.markdown("Region      : "+region)
        st.markdown("Sub Region  : "+sub_region)
        st.markdown("Dengan jumlah produksi 0.0 pada Kumulatif Tahun")
        st.markdown("")
f.close()