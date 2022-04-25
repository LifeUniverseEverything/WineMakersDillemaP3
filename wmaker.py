import streamlit as st

st.title("Decision Making Helper for Harvest Planning")
st.header("Please feel free to move around the sliders to change the assumptions of the model")

prob_mold = st.slider("Probability of Botrytis Mold: ", 0.0, 1.0, 0.1, 0.1)
prob_no = st.slider("Probability  of No Sugar :", 0.0, 1.0, 0.6, 0.1)
prob_sugar =  st.slider("Probability of Typical Sugar Level: ", 0.0, 1.0, 0.3, 0.1)
prob_high = st.slider("Probability of High Sugar Level: ", 0.0, 1.0, 0.1, 0.1)

sensitivity = 0.429
specificity = 0.589
prob_storm = 0.5

payout_harvest = 960000
payout_noharvest_storm_mold = 3300000
payout_noharvest_storm_nomold = 420000
payout_noharvest_storm = payout_noharvest_storm_mold * prob_mold + (1-prob_mold) * payout_noharvest_storm_nomold

payout_noharvest_nostorm = prob_no * 960000 + prob_sugar * 1410000 + prob_high * 1500000


p_dns = specificity * prob_storm + (1 - prob_storm) * (1 - specificity)
p_ns_dns = specificity * prob_storm / p_dns

e_dns_upper = payout_harvest
e_dns_lower = p_ns_dns * payout_noharvest_nostorm + (1 - p_ns_dns) * payout_noharvest_storm

e_dns = max(e_dns_lower, e_dns_upper)
if e_dns == payout_harvest: ns_des = 'harvest NOW'
else: ns_des = 'wait'

p_ds = sensitivity * (1 - prob_storm) + (1 - sensitivity) * prob_storm
p_s_ds = sensitivity * (1 - prob_storm) / p_ds

e_ds_upper = payout_harvest
e_ds_lower = p_s_ds * payout_noharvest_storm + (1 - p_s_ds) * payout_noharvest_nostorm

e_ds = max(e_ds_lower, e_ds_upper)
if e_ds == payout_harvest: s_des = 'harvest NOW'
else: s_des = 'wait'

sum_prob = prob_no + prob_sugar + prob_high

if sum_prob >= 1.10 or sum_prob <= 0.90:

    st.write("Please make sure the three probailities of suger level adds up to 1!")
    
else:
    st.write("If the detectror predicts there is no storm, you are better off to: " + ns_des + \
              " and the expected value of the deicision is $" + str(int(e_dns)))

    st.write("If the detectror predicts there is a storm, you are better off to: " + s_des + \
              " and the expected value of the deicision is $" + str(int(e_ds)))
    
    