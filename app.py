import streamlit as st
import pandas as pd

# ======================
# CONFIGURATION DE LA PAGE
# ======================
st.set_page_config(
    page_title="Permanence",
    page_icon="🛒",
    layout="wide"
)

# ======================
# LOGO + TITRE
# ======================
st.image("logo.png", width=150)
st.title("🛒 Permanence — Vos besoins essentiels livrés sans stress")

st.write("""
Bienvenue sur **Permanence**, votre application de commande et livraison 
de produits **alimentaires** 🍞 et **pharmaceutiques** 💊.
""")

# ======================
# CHARGEMENT DES DONNÉES
# ======================
@st.cache_data
def load_data():
    aliments = pd.read_csv("data/produits_alimentaires.csv")
    pharma = pd.read_csv("data/produits_pharma.csv")
    return aliments, pharma

aliments, pharma = load_data()

# ======================
# BARRE DE NAVIGATION
# ======================
section = st.sidebar.radio("🗂 Choisissez un secteur :", ["Alimentaire", "Pharmaceutique"])

if section == "Alimentaire":
    st.header("🥐 Produits Alimentaires")
    search = st.text_input("🔍 Rechercher un produit alimentaire :")
    df = aliments[aliments["nom"].str.contains(search, case=False)] if search else aliments

    # Affichage du catalogue
    st.dataframe(df[["nom", "prix", "categorie"]].reset_index(drop=True))

    # Sélection et commande
    selected = st.selectbox("🛒 Choisissez un produit à commander :", df["nom"])
    quantite = st.number_input("Quantité", min_value=1, max_value=50, value=1)
    if st.button("✅ Ajouter au panier"):
        st.success(f"{quantite} × {selected} ajouté(s) au panier !")

elif section == "Pharmaceutique":
    st.header("💊 Produits Pharmaceutiques")
    search = st.text_input("🔍 Rechercher un médicament :")
    df = pharma[pharma["nom"].str.contains(search, case=False)] if search else pharma

    st.dataframe(df[["nom", "prix", "forme"]].reset_index(drop=True))
    selected = st.selectbox("🛒 Choisissez un médicament à commander :", df["nom"])
    quantite = st.number_input("Quantité", min_value=1, max_value=10, value=1)
    ordonnance = st.file_uploader("📷 Joindre une ordonnance (optionnel)", type=["jpg", "png", "pdf"])

    if st.button("✅ Commander"):
        if ordonnance:
            st.success(f"{quantite} × {selected} commandé(s) avec ordonnance jointe.")
        else:
            st.success(f"{quantite} × {selected} commandé(s) sans ordonnance.")

# ======================
# PANIER / LIVRAISON
# ======================
st.sidebar.markdown("---")
st.sidebar.subheader("🚚 Livraison")
st.sidebar.text_input("Adresse de livraison")
st.sidebar.selectbox("Mode de livraison", ["Standard (1-2h)", "Express (30 min)"])
st.sidebar.button("Confirmer la commande")

# ======================
# PIED DE PAGE
# ======================
st.markdown("---")
st.caption("© 2025 Permanence — Simplifiez vos achats essentiels.")
