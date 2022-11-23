import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_lasso_reg.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

lasso = data["model"]
le_location = data["le_location"]


def show_predict_page1():
    st.title("Bangalore Home Price Prediction.")

    st.write("""### The following information are needed for home price prediction""")

    location = (
        'Electronic City Phase II', 'Chikka Tirupathi', 'Uttarahalli',
       'Lingadheeranahalli', 'Kothanur', 'Whitefield', 'Old Airport Road',
       'Rajaji Nagar', 'Marathahalli', 'other', '7th Phase JP Nagar',
       'Gottigere', 'Sarjapur', 'Mysore Road', 'Bisuvanahalli',
       'Raja Rajeshwari Nagar', 'Kengeri', 'Binny Pete', 'Thanisandra',
       'Bellandur', 'Electronic City', 'Ramagondanahalli', 'Yelahanka',
       'Hebbal', 'Kasturi Nagar', 'Kanakpura Road',
       'Electronics City Phase 1', 'Kundalahalli', 'Chikkalasandra',
       'Murugeshpalya', 'Sarjapur  Road', 'HSR Layout', 'Doddathoguru',
       'KR Puram', 'Bhoganhalli', 'Lakshminarayana Pura', 'Begur Road',
       'Varthur', 'Bommanahalli', 'Gunjur', 'Devarachikkanahalli',
       'Hegde Nagar', 'Haralur Road', 'Hennur Road', 'Kothannur',
       'Kalena Agrahara', 'Kaval Byrasandra', 'ISRO Layout',
       'Garudachar Palya', 'EPIP Zone', 'Dasanapura', 'Kasavanhalli',
       'Sanjay nagar', 'Domlur', 'Sarjapura - Attibele Road',
       'Yeshwanthpur', 'Chandapura', 'Nagarbhavi', 'Devanahalli',
       'Ramamurthy Nagar', 'Malleshwaram', 'Akshaya Nagar', 'Shampura',
       'Kadugodi', 'LB Shastri Nagar', 'Hormavu', 'Vishwapriya Layout',
       'Kudlu Gate', '8th Phase JP Nagar', 'Bommasandra Industrial Area',
       'Anandapura', 'Vishveshwarya Layout', 'Kengeri Satellite Town',
       'Kannamangala', 'Hulimavu', 'Mahalakshmi Layout', 'Hosa Road',
       'Attibele', 'CV Raman Nagar', 'Kumaraswami Layout', 'Nagavara',
       'Hebbal Kempapura', 'Vijayanagar', 'Pattandur Agrahara',
       'Nagasandra', 'Kogilu', 'Panathur', 'Padmanabhanagar',
       '1st Block Jayanagar', 'Kammasandra', 'Dasarahalli', 'Magadi Road',
       'Koramangala', 'Dommasandra', 'Budigere', 'Kalyan nagar',
       'OMBR Layout', 'Horamavu Agara', 'Ambedkar Nagar',
       'Talaghattapura', 'Balagere', 'Jigani', 'Gollarapalya Hosahalli',
       'Old Madras Road', 'Kaggadasapura', '9th Phase JP Nagar', 'Jakkur',
       'TC Palaya', 'Giri Nagar', 'Singasandra', 'AECS Layout',
       'Mallasandra', 'Begur', 'JP Nagar', 'Malleshpalya', 'Munnekollal',
       'Kaggalipura', '6th Phase JP Nagar', 'Ulsoor', 'Thigalarapalya',
       'Somasundara Palya', 'Basaveshwara Nagar', 'Bommasandra',
       'Ardendale', 'Harlur', 'Kodihalli', 'Narayanapura',
       'Bannerghatta Road', 'Hennur', '5th Phase JP Nagar', 'Kodigehaali',
       'Billekahalli', 'Jalahalli', 'Mahadevpura', 'Anekal', 'Sompura',
       'Dodda Nekkundi', 'Hosur Road', 'Battarahalli', 'Sultan Palaya',
       'Ambalipura', 'Hoodi', 'Brookefield', 'Yelenahalli', 'Vittasandra',
       '2nd Stage Nagarbhavi', 'Vidyaranyapura', 'Amruthahalli',
       'Kodigehalli', 'Subramanyapura', 'Basavangudi', 'Kenchenahalli',
       'Banjara Layout', 'Kereguddadahalli', 'Kambipura',
       'Banashankari Stage III', 'Sector 7 HSR Layout', 'Rajiv Nagar',
       'Arekere', 'Mico Layout', 'Kammanahalli', 'Banashankari',
       'Chikkabanavar', 'HRBR Layout', 'Nehru Nagar', 'Kanakapura',
       'Konanakunte', 'Margondanahalli', 'R.T. Nagar', 'Tumkur Road',
       'Vasanthapura', 'GM Palaya', 'Jalahalli East', 'Hosakerehalli',
       'Indira Nagar', 'Kodichikkanahalli', 'Varthur Road', 'Anjanapura',
       'Abbigere', 'Tindlu', 'Gubbalala', 'Parappana Agrahara',
       'Cunningham Road', 'Kudlu', 'Banashankari Stage VI', 'Cox Town',
       'Kathriguppe', 'HBR Layout', 'Yelahanka New Town',
       'Sahakara Nagar', 'Rachenahalli', 'Yelachenahalli',
       'Green Glen Layout', 'Thubarahalli', 'Horamavu Banaswadi',
       '1st Phase JP Nagar', 'NGR Layout', 'Seegehalli', 'BEML Layout',
       'NRI Layout', 'ITPL', 'Babusapalaya', 'Iblur Village',
       'Ananth Nagar', 'Channasandra', 'Choodasandra', 'Kaikondrahalli',
       'Neeladri Nagar', 'Frazer Town', 'Cooke Town', 'Doddakallasandra',
       'Chamrajpet', 'Rayasandra', '5th Block Hbr Layout', 'Pai Layout',
       'Banashankari Stage V', 'Sonnenahalli', 'Benson Town',
       '2nd Phase Judicial Layout', 'Poorna Pragna Layout',
       'Judicial Layout', 'Banashankari Stage II', 'Karuna Nagar',
       'Bannerghatta', 'Marsur', 'Bommenahalli', 'Laggere',
       'Prithvi Layout', 'Banaswadi', 'Sector 2 HSR Layout',
       'Shivaji Nagar', 'Badavala Nagar', 'Nagavarapalya', 'BTM Layout',
       'BTM 2nd Stage', 'Hoskote', 'Doddaballapur', 'Sarakki Nagar',
       'Thyagaraja Nagar', 'Bharathi Nagar', 'HAL 2nd Stage',
       'Kadubeesanahalli'
    )

    location = st.selectbox("Location",location)

    total_sqft = st.slider("Total Sqft", 0,60000,300)

    bath = st.slider("Bathrooms",0,40,1)

    BHK = st.slider("Bedrooms",0,100,1)

    ok = st.button("Calculate Price")
    if ok:
        X = np.array([[location, total_sqft, bath, BHK]])
        X[:, 0] = le_location.transform(X[:,0])
        X = X.astype(float)

        price = lasso.predict(X)
        st.subheader(f"The estimated price is ${price[0]:.2f}")


