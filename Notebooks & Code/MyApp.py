# Importer les bibliothèques nécessaires
import streamlit as st
import pickle
import numpy as np

# Charger le modèle de machine learning (généré précédement)

model=pickle.load(open('/content/drive/MyDrive/Colab Notebooks/Data Mining project/model.pkl','rb'))
scaler=pickle.load(open('/content/drive/MyDrive/Colab Notebooks/Data Mining project/scaler.pkl','rb'))
encoder_merchandise=pickle.load(open('/content/drive/MyDrive/Colab Notebooks/Data Mining project/label_encoder_merchandise.pkl','rb'))
encoder_country=pickle.load(open('/content/drive/MyDrive/Colab Notebooks/Data Mining project/label_encoder_country.pkl','rb'))


# Définir les listes comprenant les valeurs associés aux marchendise et aux pays
merchandise_options = encoder_merchandise.classes_.tolist()
country_options = encoder_country.classes_.tolist()

# Définir la fonction de prédiction
def predict(total_bids, unique_auctions, avg_time_between_bids, most_frequent_merchandise, most_frequent_country, unique_device_ratio):
    input_data = np.array([[total_bids, avg_time_between_bids, most_frequent_merchandise, most_frequent_country, unique_auctions, unique_device_ratio]])

    # Transformer la merchandise s'il existe dans la liste encoder_merchandise.classes_
    if most_frequent_merchandise in encoder_merchandise.classes_:
        input_data[:, 2] = encoder_merchandise.transform([most_frequent_merchandise])[0]
    else:
        # traiter le cas d'une exception de catégorie imprévu
        input_data[:, 2] = -1  
    # Transformer le pays s'il existe dans la liste encoder_country.classes_
    if most_frequent_country in encoder_country.classes_:
        input_data[:, 3] = encoder_country.transform([most_frequent_country])[0]
    else:
        # traiter le cas d'une exception de catégorie imprévu
        input_data[:, 3] = -1  # or any default value or special treatment for unseen labels

    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    return prediction

# Configurer l'interface utilisateur de Streamlit
st.title('Détection des Enchères Robotiques et Humaines')
st.write('Entrez les caractéristiques du bidder pour prédire s\'il s\'agit d\'un robot ou d\'un humain.')

# Entrées de l'utilisateur
total_bids = st.number_input('Total des enchères', min_value=0, value=10)
unique_auctions = st.number_input('Enchères uniques', min_value=0, value=5)
avg_time_between_bids = st.number_input('Temps moyen entre les enchères', min_value=0.0, value=5.0)
most_frequent_merchandise = st.selectbox('Marchandise la plus fréquente', merchandise_options)
most_frequent_country = st.selectbox('Pays le plus fréquent', country_options)
unique_device_ratio = st.number_input('Ratio des devices uniques', min_value=0.0, value=0.5)

# Bouton de prédiction
if st.button('Prédire'):
    result = predict(total_bids,unique_auctions, avg_time_between_bids, most_frequent_merchandise, most_frequent_country, unique_device_ratio)
    if result == 0:
        st.success('Le bidder est humain.')
    else:
        st.error('Le bidder est un robot.')